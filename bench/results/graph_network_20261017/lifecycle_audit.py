"""Check actual per-request GPU launches, reply bytes and normal termination."""
from pathlib import Path
import json,re,sys
def main(a):
    checked=[]
    for phase in ["client_dispatch_initial","screen","confirmation"]:
        for path in sorted((a/phase).glob("*.metrics.json")):
            m=json.loads(path.read_text());prefix=path.with_name(path.name.removesuffix(".metrics.json"))
            text=Path(str(prefix)+".server.stdout").read_text()
            match=re.search(r"graph backend stopped: admitted=(\d+) retired=(\d+) graph_launches=(\d+) graph_error=(\d+)",text)
            assert match,prefix
            counts=list(map(int,match.groups()));expected=m["attempts"]+32
            assert counts==[expected,expected,expected,0],(prefix,counts,expected)
            terminal=json.loads(Path(str(prefix)+".server_terminal.json").read_text())
            assert terminal["exit"]==0 and not terminal["remaining_pins"]
            network=None
            if m["mode"]=="kernel":
                network=json.loads(next(line[7:] for line in text.splitlines() if line.startswith("RESULT ")))
                assert network["received"]==network["completed"]==expected
                assert network["bytes"]==expected*256 and network["aborted"]==0
                assert network["accepted"]==network["closed"]
                assert not any(network[k] for k in ["error","pending","reserved","dropped","overflow"])
                assert network["sqhead"]==network["sqtail"] and network["cqhead"]==network["cqtail"]
            checked.append(dict(phase=phase,tag=m["tag"],measured=m["attempts"],warmups=32,
                graph_launches=expected,reply_bytes=network["bytes"] if network else None,
                network_sends=network["sends"] if network else None,server_exit=0))
    d=a/"control_connection_interruption";text=(d/"confirm_s2_p1_native.server.stdout").read_text()
    match=re.search(r"graph backend stopped: admitted=(\d+) retired=(\d+) graph_launches=(\d+) graph_error=(\d+)",text)
    assert match and list(map(int,match.groups()))==[32,32,32,0]
    out=dict(cells=len(checked),measured=sum(x["measured"] for x in checked),
        measured_cell_warmups=sum(x["warmups"] for x in checked),
        extra_unmeasured_interruption_warmups=32,checked=checked,
        scope="Actual graph calls/counts/normal stop and kernel reply byte accounting. No GPU-interval timing or universal numerical claim.")
    (a/"lifecycle_audit.json").write_text(json.dumps(out,indent=2))
    print(json.dumps({k:v for k,v in out.items() if k!="checked"}))
if __name__=="__main__":main(Path(sys.argv[1]))
