from pathlib import Path
import subprocess,json,os,datetime
t=Path(__file__).resolve().parent
cmd=json.loads((t/"graph_build.command.json").read_text())
env=dict(os.environ,**json.loads((t/"environment.json").read_text()))
with (t/"graph_build_repaired.stdout").open("x") as out,(t/"graph_build_repaired.stderr").open("x") as err:
 z=subprocess.run(cmd,cwd="/workspaces/repository",env=env,stdout=out,stderr=err)
(t/"graph_build.exit.json").write_text(json.dumps(dict(exit=z.returncode,command=cmd,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())))
