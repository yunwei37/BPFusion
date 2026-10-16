from pathlib import Path
import subprocess,json,datetime
t=Path('/tmp/bpfusion-mixed-batching-pa97uj6t')
cmd=['/usr/bin/python3', '-m', 'pip', '--python', '/tmp/bpfusion-mixed-batching-pa97uj6t/runtime/bin/python', 'install', 'numpy==2.3.5', 'matplotlib']
with (t/'plot_install.stdout').open('x') as out,(t/'plot_install.stderr').open('x') as err:z=subprocess.run(cmd,stdout=out,stderr=err)
(t/'plot_install.exit.json').write_text(json.dumps(dict(exit=z.returncode,command=cmd,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
raise SystemExit(z.returncode)
