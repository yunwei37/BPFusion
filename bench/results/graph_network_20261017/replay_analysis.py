"""Replay without replacing any canonical analysis or raw trace."""
from pathlib import Path
import gzip,importlib.util,json,os,sys,tempfile,time
def main(a):
    repo=a.parents[2]
    spec=importlib.util.spec_from_file_location("primary",repo/"bench/graph_network_analysis.py")
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    checked=[];start=time.monotonic()
    with tempfile.TemporaryDirectory(prefix="bpfusion-graph-raw-replay-") as tmp:
        tmp=Path(tmp)
        for phase in ["client_dispatch_initial","screen","confirmation"]:
            for original in sorted((a/phase).glob("*.metrics.json")):
                prefix=original.name.removesuffix(".metrics.json");dest=tmp/phase/prefix;dest.mkdir(parents=True)
                for raw in original.parent.glob(prefix+".*"):
                    if raw.name.endswith((".metrics.json",".latency_ecdf.json.gz")) or ".analysis." in raw.name:continue
                    (dest/raw.name).symlink_to(raw)
                expected=json.loads(original.read_text());actual=module.cell(dest/prefix)
                assert actual==expected,original
                ecdf=prefix+".latency_ecdf.json.gz"
                assert (dest/ecdf).read_bytes()==(original.parent/ecdf).read_bytes(),ecdf
                checked.append(str(original.relative_to(a)))
    result=dict(cells=len(checked),metrics_equal=True,ecdf_gzip_byte_equal=True,
        elapsed_s=time.monotonic()-start,checked=checked,
        scope="Original stdlib analyzer replay on OS-temp raw-data symlinks; canonical outputs untouched. Separately see NumPy independent-code owner audit.")
    (a/"analysis_replay.json").write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!="checked"}))
if __name__=="__main__":main(Path(sys.argv[1]))
