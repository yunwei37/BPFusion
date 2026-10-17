#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Offline raw-data replay and paper-number comparison. No GPU or network."""
import argparse
import contextlib
import gzip
import types
import io
import json
import math
from pathlib import Path
import re
import runpy
import statistics as st
import sys
import tempfile
import time

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "bench/results"
INPUTS = set()
T95 = 2.776445105


def audit(event, args):
    if event in {"socket.connect", "socket.getaddrinfo", "socket.bind"}:
        raise RuntimeError("This replay is offline: network access forbidden")
    if event == "open" and isinstance(args[0], (str, bytes)):
        try:
            p = Path(args[0]).resolve()
            if p.is_file() and p.is_relative_to(ROOT):
                INPUTS.add(p.relative_to(ROOT).as_posix())
        except (OSError, ValueError):
            pass


def load_module(name, file):
    module = types.ModuleType(name)
    module.__file__ = str(file)
    exec(compile(file.read_text(), str(file), "exec"), module.__dict__)
    return module


def replay(script, *args):
    old = sys.argv
    sys.argv = [str(script), *map(str, args)]
    output = io.StringIO()
    try:
        with contextlib.redirect_stdout(output):
            runpy.run_path(str(script), run_name="__main__")
    finally:
        sys.argv = old
    return [json.loads(s) for s in output.getvalue().splitlines() if s.startswith("{")]


def raw_rows(path):
    path = Path(path)
    if not path.exists():
        path = Path(str(path) + ".gz")
    with gzip.open(path, "rt") if path.suffix == ".gz" else path.open() as stream:
        return [json.loads(line) for line in stream]


def cells(rows):
    return [r for r in rows if r.get("event") == "cell_metrics"]


def mean(rows, field, **where):
    selected = [r[field] for r in rows if all(r.get(k) == v for k, v in where.items())]
    assert len(selected) == 5, (field, where, len(selected))
    return st.mean(selected)


def ratio(values):
    logs = [math.log(a / b) for a, b in values]
    center = st.mean(logs)
    half = T95 * st.stdev(logs) / math.sqrt(5)
    return [math.exp(center), math.exp(center - half), math.exp(center + half)]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", type=Path, required=True, help="New output directory outside the source tree")
    args = ap.parse_args()
    out = args.output.resolve()
    if out.is_relative_to(ROOT):
        ap.error("--output must be outside the source tree")
    out.mkdir(parents=True, exist_ok=False)
    sys.addaudithook(audit)
    start = time.monotonic()
    paper = (ROOT / "paper/bpfusion.tex").read_text()
    checks = []

    def compare(label, actual, printed, tolerance=None):
        printed = str(printed).replace(",", "")
        expected = float(printed)
        places = len(printed.partition(".")[2])
        tolerance = .5 * 10 ** -places + 1e-10 if tolerance is None else tolerance
        passed = math.isfinite(actual) and abs(actual - expected) <= tolerance
        checks.append(dict(item=label, paper=expected, recomputed=actual,
                           tolerance=tolerance, status="PASS" if passed else "MISMATCH"))

    def inline(label, pattern, actuals, tolerance=None):
        m = re.search(pattern, paper, re.S)
        if m is None:
            checks.append(dict(item=label, status="PAPER_CHANGED", pattern=pattern))
            return
        for i, (printed, actual) in enumerate(zip(m.groups(), actuals)):
            compare(label + (" [%d]" % i if len(actuals) > 1 else ""), actual, printed, tolerance[i] if isinstance(tolerance, list) else tolerance)

    def stage(name, script, *argv):
        print("Replaying " + name, flush=True)
        rows = replay(script, *argv)
        (out / (name + ".jsonl")).write_text("".join(json.dumps(r) + "\n" for r in rows))
        return rows

    o = RESULTS / "official_sustained_20261016"
    official_rows = stage("official_transport", o / "official_remote_analysis.py", o / "official_remote_full_retry2")
    official = cells(official_rows)
    q = RESULTS / "resident_queue_relief_20261017"
    capacity = cells(stage("capacity", q / "queue_relief_analysis.py", q / "queue_relief_full"))
    a = RESULTS / "active_admission_wait_20261016"
    wait = cells(stage("active_wait", a / "active_wait_analysis.py", a / "active_wait_full"))
    e = RESULTS / "connection_reclamation_20261016"
    eof = cells(stage("reclamation", e / "reclaim_analysis.py", e / "verified_reclaim_full"))
    t = RESULTS / "tcp_nodelay_20261016"
    tcp = cells(stage("nodelay", t / "tcp_analysis.py", t / "tcp_full/full.jsonl"))
    m = RESULTS / "mixed_batching_20261015"
    mixed = cells(stage("mixed", m / "analyze.py", m / "full_qwen.jsonl"))
    tcp_diagnostic = stage("tcp_diagnostic", t / "tcp_diagnostic_analysis.py", t / "tcp_preflight")
    p = RESULTS / "kernel_cpu_profile_20261016"
    profiles = stage("perf", p / "profile_summary.py", p / "cpu_profile_full")
    perf = {("kernel" if "_kernel_" in x["file"] else "native"): x for x in profiles}
    graph = load_module("graph_primary", ROOT / "bench/graph_network_analysis.py")
    g = RESULTS / "graph_network_20261017"
    graph_cells = {}
    splits = {}
    observer = []
    print("Replaying graph screen and confirmation (90 cells)", flush=True)
    with tempfile.TemporaryDirectory(prefix="paper-graph-replay-") as tmp:
        tmp = Path(tmp)
        for phase in ["screen", "confirmation"]:
            selected = []
            for original in sorted((g / phase).glob("*.metrics.json")):
                tag = original.name.removesuffix(".metrics.json")
                dest = tmp / tag
                dest.mkdir()
                for raw in original.parent.glob(tag + ".*"):
                    if raw.name.endswith((".metrics.json", ".latency_ecdf.json.gz")) or ".analysis." in raw.name:
                        continue
                    (dest / raw.name).symlink_to(raw.resolve())
                metric = graph.cell(dest / tag)
                expected = json.loads(original.read_text())
                assert metric == expected, ("raw replay differs from archive", tag)
                # Recompute tick-based splits directly from original /proc counters.
                rows = graph.read(dest / (tag + ".resources.jsonl.gz"))
                samples = [x for x in rows if x["event"] == "sample"]
                aa, bb = samples[0], samples[-1]
                tick = rows[0]["clock_tick"]
                split = {}
                for field, index in [("user", 11), ("system", 12)]:
                    def ticks(sample):
                        return sum(int(v["stat"].rsplit(") ", 1)[1].split()[index])
                                   for v in sample["process_group"].values())
                    split[field] = (ticks(bb) - ticks(aa)) / tick * 1e6 / metric["attempts"]
                splits[tag] = split
                observer.append((bb["observer_cpu_ns"] - aa["observer_cpu_ns"]) / 1000 / metric["attempts"])
                selected.append(metric)
            graph_cells[phase] = selected
            (out / (phase + ".jsonl")).write_text("".join(json.dumps(x) + "\n" for x in selected))
    assert len(graph_cells["screen"]) == 60 and len(graph_cells["confirmation"]) == 30

    tables = re.findall(r"\\begin\{tabular\}.*?\n(.*?)\\end\{tabular\}", paper, re.S)
    assert len(tables) == 3
    table1 = [line.split("&")[1:] for line in tables[0].splitlines() if "&" in line and not line.startswith("Path ") and re.search(r"\d", line)]
    actual_table1 = []
    for data, conditions in [(official, ["candidate", "native", "official"]),
                             (capacity, ["before", "native", "official"])]:
        for condition in conditions:
            actual_table1.append([mean(data, key, condition=condition) for key in
                                  ["output_tokens_per_s", "connect_completion_ms_p99", "owned_group_cpu_ms_per_attempt"]])
    assert len(table1) == len(actual_table1) == 6
    for i, (printed, actual) in enumerate(zip(table1, actual_table1), 1):
        for metric, value, text in zip(["tokens/s", "P99 ms", "CPU ms"], actual, printed):
            compare("Table 1 row %d %s" % (i, metric), value, re.search(r"[\d,]+(?:\.\d+)?", text)[0])

    confirmation = graph_cells["confirmation"]
    effects = []
    figure_cpu = []
    for index in range(3):
        by = {(x["tag"].split("_")[-1], int(re.search(r"_p(\d)_", x["tag"])[1])): x
              for x in confirmation if x["tag"].startswith("confirm_s%d_" % index)}
        assert len(by) == 10
        effect = {}
        for key in ["group_cpu", "p99", "host_cpu", "throughput"]:
            def get(x):
                return {"group_cpu": x["owned_group_cpu_ms_per_attempt"],
                        "p99": x["latency"]["scheduled_response_ms"]["p99"],
                        "host_cpu": x["host_active_cpu_ms_per_attempt"], "throughput": x["throughput"]}[key]
            effect[key] = ratio([(get(by["kernel", pair]), get(by["native", pair])) for pair in range(5)])
        effect["failures"] = sum(x["failures"] for x in by.values())
        cpu, tail, rate = effect["group_cpu"], effect["p99"], effect["throughput"]
        effect["advantage"] = (not effect["failures"] and rate[1] >= .98 and
                               ((cpu[2] < .90 and tail[2] <= 1.05) or (tail[2] < .90 and cpu[2] <= 1.05)))
        effects.append(effect)
        if index < 2:
            for mode in ["native", "kernel"]:
                values = [by[mode, pair] for pair in range(5)]
                figure_cpu.append(dict(label=("FFT" if index == 0 else "GEMM") + (" N" if mode == "native" else " K"),
                    user=st.mean(splits[x["tag"]]["user"] for x in values),
                    system=st.mean(splits[x["tag"]]["system"] for x in values),
                    total=st.mean(x["owned_group_cpu_ms_per_attempt"] * 1000 for x in values)))
    table2 = [line.split("&")[1:] for line in tables[1].splitlines() if "&" in line and not line.startswith("Point ") and "[" in line]
    assert len(table2) == 3
    for i, (printed, effect) in enumerate(zip(table2, effects), 1):
        for metric, text in zip(["group_cpu", "p99"], printed):
            nums = re.findall(r"\d+\.\d+", text)
            assert len(nums) == 3
            for j, value in enumerate(effect[metric]):
                compare("Table 2 row %d %s %s" % (i, metric, ["ratio", "low", "high"][j]), value, nums[j])

    tcp_before = mean(tcp, "client_token_gap_ms_p99", mode="kernel_before", regime="closed16")
    tcp_after = mean(tcp, "client_token_gap_ms_p99", mode="kernel_after", regime="closed16")
    tpot_before = mean(mixed, "tpot_ms_mean", mode="uring_loop_16_original", rate=96)
    tpot_after = mean(mixed, "tpot_ms_mean", mode="uring_loop_16_mixed", rate=96)
    fixes = [
        [tcp_before, tcp_after, mean(tcp, "output_tokens_per_s", mode="kernel_before", regime="closed16"),
         mean(tcp, "output_tokens_per_s", mode="kernel_after", regime="closed16")],
        [sum(x["failures"] for x in eof if x["condition"] == "global"),
         sum(x["failures"] for x in eof if x["condition"] == "local"), 57600,
         mean(eof, "output_tokens_per_s", condition="global"), mean(eof, "output_tokens_per_s", condition="local")],
        [mean(wait, "owned_group_cpu_ms_per_attempt", condition="before"),
         mean(wait, "owned_group_cpu_ms_per_attempt", condition="candidate")],
        [tpot_before, tpot_after, (tpot_after / tpot_before - 1) * 100],
        [mean(capacity, "connect_completion_ms_p99", condition="before"),
         mean(capacity, "connect_completion_ms_p99", condition="native")]]
    table3 = [line.split("&")[-1] for line in tables[2].splitlines() if "&" in line and
              any(s in line for s in ["NODELAY", "reclamation", "polling", "prefill", "slots"])]
    assert len(table3) == 5
    for i, (text, actual) in enumerate(zip(table3, fixes), 1):
        printed = re.findall(r"-?\d[\d,]*(?:\.\d+)?", text.replace("P99", ""))
        assert len(printed) == len(actual), (text, printed, actual)
        for j, (v, s) in enumerate(zip(actual, printed)):
            compare("Table 3 row %d value %d" % (i, j), v, s)

    figure2 = paper.split(r"\label{tab:small}", 1)[1].split(r"\label{fig:cpu}", 1)[0]
    plots = re.findall(r"\\addplot.*?coordinates \{(.*?)\};", figure2, re.S)
    assert len(plots) == 2
    for field, text in zip(["user", "system"], plots):
        entries = re.findall(r"\((FFT [NK]|GEMM [NK]),([\d.]+)\)", text)
        assert len(entries) == 4
        for item, (label, printed) in zip(figure_cpu, entries):
            assert item["label"] == label
            compare("Figure 2 " + label + " " + field, item[field], printed)
    totals = re.findall(r"axis cs:(FFT [NK]|GEMM [NK]),40.5\) \{([\d.]+)\}", figure2)
    assert len(totals) == 4
    for item, (label, printed) in zip(figure_cpu, totals):
        assert item["label"] == label
        compare("Figure 2 " + label + " high-resolution total", item["total"], printed)

    figure3 = paper.split(r"\label{sec:why}", 1)[1].split(r"\label{fig:profile}", 1)[0]
    plots = re.findall(r"\\addplot.*?coordinates \{(.*?)\};", figure3, re.S)
    assert len(plots) == 4
    figure_perf = {}
    for mode, profile in perf.items():
        cats = profile["categories"]
        def share(cat):
            return cats.get(cat, {}).get("fraction", 0) * 100
        values = [share("socket_network_or_softirq"), share("loop_coordination_other"),
                  share("bpf_map_without_socket_ancestor")]
        values.append(100 - sum(values))
        figure_perf[mode] = values
    for category, text in enumerate(plots):
        for printed, label in re.findall(r"\(([\d.]+),(Kernel-owned|Native epoll)\)", text):
            mode = "kernel" if label == "Kernel-owned" else "native"
            compare("Figure 3 " + mode + " category %d" % category, figure_perf[mode][category], printed)

    # Important numerical prose: capture current TeX values rather than a duplicated expected-results file.
    inline("transport P99 difference and interval", r"\(\$(-?\d+)\$\\,ms, interval \$\[(-?\d+), (\d+)\]\$",
           [mean(official, "connect_completion_ms_p99", condition="candidate") - mean(official, "connect_completion_ms_p99", condition="native"),
            *next(x["signed_t95"] for x in official_rows
                  if x.get("event") == "paired" and x["contrast"] == "candidate minus native" and x["metric"] == "connect_completion_ms_p99")])
    inline("earlier group CPU reduction percent", r"measured ([\d.]+)\\% lower process-group",
           [(1 - mean(wait, "owned_group_cpu_ms_per_attempt", condition="candidate") / mean(wait, "owned_group_cpu_ms_per_attempt", condition="native")) * 100])
    delta_tpot = mean(capacity, "tpot_ms_mean", condition="native") - mean(capacity, "tpot_ms_mean", condition="before")
    delta_energy = mean(capacity, "device_energy_J_per_attempt", condition="native") - mean(capacity, "device_energy_J_per_attempt", condition="official")
    inline("capacity mean token time cost", r"cost ([\d.]+)\\,ms of mean", [delta_tpot])
    inline("capacity device energy cost", r"and\s+([\d.]+)\\,J more device", [delta_energy])
    inline("host ratios", r"Whole-host CPU ratios \(([\d.]+), ([\d.]+) and ([\d.]+)\)", [x["host_cpu"][0] for x in effects])
    inline("one CPU adverse tail", r"one logical CPU.*?P99 was\s+([\d.]+)\$\\times\$", [effects[2]["p99"][0]])
    inline("kernel/native sample counts", r"\(([\d,]+) versus ([\d,]+)\)", [perf["kernel"]["samples"], perf["native"]["samples"]])
    inline("sample count ratio", r"had ([\d.]+)\$\\times\$ more on-CPU", [perf["kernel"]["samples"] / perf["native"]["samples"]])
    inline("combined coordination percent", r"where (\d+)\\%\s+of the loop thread", [sum(figure_perf["kernel"][1:3])])
    inline("native networking percent", r"thread spends (\d+)\\% of its kernel", [figure_perf["native"][0]])
    # Rebuild native TTFT/generation arrival buckets from original timestamps.
    bucket_means, gen = [], []
    for pth in sorted((o / "official_remote_full_retry2").glob("*_native_r192.client.jsonl.gz")):
        raw = raw_rows(pth)
        cell = next(x for x in raw if x["event"] == "cell")
        for bucket in [0, 5]:
            requests = [x for x in raw if x["event"] == "request" and x["outcome"] == "success"
                        and int((x["scheduled_ns"] - cell["epoch_ns"]) / 1e10) == bucket]
            bucket_means.append((bucket, st.mean((x["arrival_ns"][0] - x["connect_begin_ns"]) / 1e6 for x in requests)))
        requests = [x for x in raw if x["event"] == "request" and x["outcome"] == "success"]
        gen.append(st.mean((x["arrival_ns"][-1] - x["arrival_ns"][0]) / 1e6 for x in requests))
    inline("first/last ten-second TTFT", r"about (\d+)\\,ms in the first.*?to ([\d,]+)\\,ms in the last",
           [st.mean(v for b, v in bucket_means if b == 0), st.mean(v for b, v in bucket_means if b == 5)])
    inline("generation span", r"generation stayed near (\d+)\\,ms", [st.mean(gen)])
    screen = graph_cells["screen"]
    screen_by = {(x["operation"], x["repeat"], x["cores"], x["offered_rate"], x["mode"]): x for x in screen}
    reduction = max((1 - x["owned_group_cpu_ms_per_attempt"] /
                     screen_by[x["operation"], x["repeat"], x["cores"], x["offered_rate"], "native"]["owned_group_cpu_ms_per_attempt"]) * 100
                    for x in screen if x["mode"] == "kernel")
    inline("largest screen CPU reduction", r"screen was about ([\d.]+)\\%", [reduction])
    inline("screen request count million", r"covered ([\d.]+) million requests", [sum(x["attempts"] for x in screen) / 1e6])
    inline("confirmation request count", r"new seeds \(([\d,]+) requests\)", [sum(x["attempts"] for x in confirmation)])
    inline("main graph requests million", r"All ([\d.]+) million requests", [sum(x["attempts"] for x in screen + confirmation) / 1e6])
    inline("observer range us", r"cost (\d+) to (\d+)\\us", [min(observer), max(observer)])
    inline("abstract CPU split", r"\(([\d.]+)\+([\d.]+)\\us\{\} versus\s+([\d.]+)\+([\d.]+)\\us\)",
           [figure_cpu[0]["user"], figure_cpu[0]["system"], figure_cpu[1]["user"], figure_cpu[1]["system"]])
    # Approximate order-of-magnitude prose, explicitly looser than rounded table values.
    inline("approximate slot tail factor", r"a (\d+)\$\\times\$ lower completion", [fixes[4][0] / fixes[4][1]], tolerance=1)
    inline("approximate NODELAY tail factor", r"a (\d+)\$\\times\$ lower token-gap", [tcp_before / tcp_after], tolerance=1)
    inline("LLM top request count", r"over ([\d,]+)\s+requests with no failures", [sum(x["attempts"] for x in official)])
    count = sum(x["attempts"] for x in official + capacity + screen + confirmation)
    minimum = float(re.search(r"more than ([\d.]+) million", paper)[1]) * 1e6
    checks.append(dict(item="abstract final-experiment request lower bound", paper=minimum, recomputed=count,
                       status="PASS" if count > minimum else "MISMATCH"))
    checks.append(dict(item="prespecified useful graph advantage", recomputed=any(x["advantage"] for x in effects),
                       status="PASS" if not any(x["advantage"] for x in effects) else "MISMATCH"))
    checks.append(dict(item="main final-experiment failures", recomputed=sum(x["failures"] for x in official + capacity + screen + confirmation),
                       status="PASS" if not any(x["failures"] for x in official + capacity + screen + confirmation) else "MISMATCH"))
    # Mechanism prose uses the recorded diagnostic episodes, not benchmark P99.
    episode = next(x["longest_queued_example"] for x in tcp_diagnostic if "kernel_before" in x["file"])
    packets = episode["packets"]
    first = next(i for i, x in enumerate(packets) if x["sport"] == 39403 and x["payload_len"] == 4)
    sent = packets[first]
    ack = next(x for x in packets[first + 1:] if x["dport"] == 39403 and x["payload_len"] == 0)
    released = next(x for x in packets[first + 1:] if x["sport"] == 39403 and x["payload_len"] > 0)
    inline("small-send diagnostic bytes and ACK wait", r"a (\d+)-byte write left (\d+) queued bytes waiting about (\d+)\\,ms",
           [sent["payload_len"], released["payload_len"], (ack["kernel_realtime_ns"] - sent["kernel_realtime_ns"]) / 1e6],
           tolerance=[.5, .5, 1])
    snapshot = json.loads((e / "errno/kernel_snapshot_now.json").read_text())
    owned = set(snapshot["owned_fd"].values())
    close_wait = sum(line.split()[3] == "08" and "socket:[" + line.split()[9] + "]" in owned for line in snapshot["tcp"])
    inline("owned CLOSE_WAIT sockets", r"([\d,]+) sockets sat in CLOSE", [close_wait])
    inline("reclamation removed timeouts", r"removed all ([\d,]+)\s+timeouts", [fixes[1][0]])
    inline("screen cell count", r"A (\d+)-cell screen", [len(screen)])
    # Model/shape/load numbers and statistical design are independently checked from raw metadata.
    raw_meta = raw_rows(next((g / "confirmation").glob("*.client.jsonl.gz")))[0]
    inline("graph request/reply bytes and connections", r"with (\d+)-byte requests,\s+(\d+)-byte replies and (\d+) persistent connections",
           [24 + 64 * 4, 64 * 4, raw_meta["workers"] * raw_meta["connections_per_worker"]])
    inline("LLM tokens/rate/duration/offered tokens", r"output tokens, (\d+) requests/s for (\d+)\\,s \(([\d,]+) offered tokens/s\)",
           [official[0]["rate"], 60, official[0]["rate"] * 64])
    inline("LLM output tokens", r"short prompts, (\d+)\s+output tokens", [official[0]["output_tokens"] / official[0]["successes"]])
    host = json.loads((g / "preflight_environment.json").read_text())
    inline("logical CPUs", r"285K \((\d+) logical\s+CPUs\)", [len(host["server_allowed_cpus"])])
    ratios = [actual_table1[2][2] / actual_table1[1][2], actual_table1[5][2] / actual_table1[4][2]]
    inline("resident/official CPU factor range", r"used (\d+)--(\d+)\$\\times\$ less process CPU",
           [ratios[0], ratios[1]], tolerance=1)
    header = (p / "cpu_profile_full/cpu_profile_full_p0_kernel_r192.perf_header.txt").read_text()
    frequency = int(re.search(r"-F (\d+) ", header)[1])
    inline("perf sample frequency Hz", r"perf at (\d+)\\,Hz", [frequency])
    inline("graph repetitions", r"repeated (\d+), (\d+) or (\d+) times",
           sorted({x["repeat"] for x in screen}))
    inline("service affinity counts", r"affinity \((\d+), (\d+) or all", sorted({x["cores"] for x in screen if x["cores"]}))
    inline("frame header and word bits", r"a (\d+)-byte header followed by\s+(\d+)-bit words", [24, 32])
    timer_source = (ROOT / "bpf/kernel_tcp.bpf.c").read_text()
    active_ns = int(re.search(r"__u64 ns = idle \? deadline-now : (\d+);", timer_source)[1])
    inline("active BPF timer us", r"io\\_uring, (\d+)\\us", [active_ns / 1000])
    warnings = [
        "Numerical agreement does not validate the paper's causal explanations.",
        "'Throughput was identical' and 'whole-host totals were unchanged' are stronger than intervals crossing zero/one; neither equivalence nor exclusive total-CPU attribution was established.",
        "The 32-slot full arm is native only. Capacity is shared architecturally, but an equal measured gain on kernel-owned 32 slots is not established.",
        "Perf Figure 3 is one ordered pair, not five counterbalanced process blocks; networking ancestry may include unrelated packets and most kernel stacks contain unknown frames.",
        "Final ordinary LLM performance trajectories retain finite-reference disagreements; exact replay qualifies finite traced cases, not every performance output.",
        "Linux 7.3-rc3 with the tested io_uring BPF interfaces is required; stable-release/fresh-OS/general compatibility is not demonstrated."
    ]
    (out / "interpretation_limits.json").write_text(json.dumps(warnings, indent=2))
    (out / "figure_data.json").write_text(json.dumps(dict(cpu=figure_cpu, perf=figure_perf, effects=effects), indent=2))
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 10, "pdf.fonttype": 42})
    fig, ax = plt.subplots(figsize=(6.0, 3.2), layout="constrained")
    labels = [x["label"] for x in figure_cpu]
    user, system = [[x[k] for x in figure_cpu] for k in ["user", "system"]]
    ax.bar(labels, user, label="user", color="#eda64a")
    ax.bar(labels, system, bottom=user, label="system", color="#91bad5")
    for i, x in enumerate(figure_cpu):
        ax.text(i, 40.5, "%.2f" % x["total"], ha="center", fontsize=9)
    ax.set(ylim=(0, 46), ylabel="CPU per request (microseconds)")
    ax.legend(ncols=2, loc="upper center")
    for ext in ["png", "pdf"]:
        fig.savefig(out / ("figure2_cpu." + ext), dpi=180)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(6.8, 2.6), layout="constrained")
    left = [0, 0]
    for i, (label, color) in enumerate(zip(["network and softirq", "loop coordination", "BPF map operations", "other"],
                                         ["#91bad5", "#da8c8c", "#eda64a", "#cccccc"])):
        values = [figure_perf[mode][i] for mode in ["native", "kernel"]]
        ax.barh(["Native epoll", "Kernel-owned"], values, left=left, label=label, color=color)
        left = [a + b for a, b in zip(left, values)]
    ax.set(xlim=(0, 100), xlabel="Share of on-CPU kernel sampled periods (%)")
    ax.legend(ncols=2, loc="upper center", bbox_to_anchor=(.5, 1.65), fontsize=8)
    for ext in ["png", "pdf"]:
        fig.savefig(out / ("figure3_perf." + ext), dpi=180)
    plt.close(fig)
    report = dict(paper="paper/bpfusion.tex", checks=checks, counts={status: sum(x["status"] == status for x in checks)
                  for status in ["PASS", "MISMATCH", "PAPER_CHANGED"]}, elapsed_s=time.monotonic() - start,
                  python=sys.version, matplotlib=matplotlib.__version__,
                  method="Archived primary analyzers replay raw logs, native binary records and counters; current TeX tables, plots and prose provide expected values. Linear quantiles and five process-block t(df4), not pooled quantiles. Figures use recomputed unrounded data.")
    (out / "comparison.json").write_text(json.dumps(report, indent=2))
    (out / "inputs.txt").write_text("".join(p + "\n" for p in sorted(INPUTS)))
    lines = ["# Paper raw-data comparison", "", "| Check | Status | Paper | Recomputed |", "|---|---|---:|---:|"]
    for x in checks:
        lines.append("| %s | %s | %s | %s |" % (x["item"], x["status"], x.get("paper", ""), x.get("recomputed", "")))
    (out / "comparison.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(dict(output=str(out), counts=report["counts"], elapsed_s=report["elapsed_s"]), indent=2))
    return 1 if report["counts"]["MISMATCH"] or report["counts"]["PAPER_CHANGED"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
