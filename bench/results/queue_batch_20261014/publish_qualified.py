import pathlib,json,subprocess,shutil,os,tempfile
r=pathlib.Path('/workspaces/repository');p=pathlib.Path(__file__).parent;a=r/'bench/results/queue_batch_20261014'
assert json.loads((p/'lifecycle.exit.json').read_text())['exit']==0
assert json.loads((p/'qualification.exit.json').read_text())['exit']==0
assert json.loads((p/'preflight1.analysis.exit.json').read_text())['exit']==0
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
a.mkdir(exist_ok=False)
for f in p.iterdir():
 if f.is_file() and f.suffix not in ['.so','.gz']:shutil.copy2(f,a/f.name)
for name in ['lifecycle_amk_smol','lifecycle_vllm_smol','lifecycle_vllm_qwen']:shutil.copytree(p/name,a/name)
for f in a.rglob('*'):
 if f.is_file():
  with f.open('rb') as h:magic=h.read(4)
  assert magic!=b'\x7fELF',str(f)
f=r/'README.md';s=f.read_text();needle='## Repository layout'
text='''The measurements above precede the current experimental queue-publication
batching change. Existing coalesced targets now snapshot ring cursors and
publish prepared SQEs/consumed CQEs once per progression round. Ordinary
noncoalesced targets retain their policy. The
[queue-batching plan](bench/results/queue_batch_20261014/plan.md) passes allnine
real preflight paths, selected protocol qualification and three32-action
lifecycle checks. The full matched performance comparison is pending;
no speedup or latency recovery is established by those checks.

'''
assert needle in s;s=s.replace(needle,text+needle,1);f.write_text(s)
f=r/'docs/architecture.md';s=f.read_text();s+='''\n## Queue publication in coalesced builds

Current BF_IO_COALESCED rounds acquire a finite CQ tail snapshot, consume that
batch and release-publish its head after reads. SQ reservations use a
conservative round-local head/tail snapshot; buffer/SQE writes are system
ordered before one release tail publication, including the early cancel-return
path. Ring-full work can defer to the next round. Timer, FIFO/final ownership,
model quiescence, queue ABI and model arithmetic remain unchanged. Other builds
retain existing per-entry publication. The
[experiment](../bench/results/queue_batch_20261014/plan.md) qualifies the selected
protocol/lifecycle; full performance collection is pending. Finding0050's
numbers describe the earlier coalescing implementation.
''';f.write_text(s)
f=r/'docs/evaluation.md';s=f.read_text();s+='''\n## Coalesced queue-publication batching in progress

The [plan and review](../bench/results/queue_batch_20261014/plan.md) admit a new
source-backed driver intervention after0050: reduce repeated host-mapped
cursor access/publication per network round without changing model arithmetic.
Current main keeps default/noncoalesced policy. Old07ba7e0 coalesced sources are
captured and reconstructed with equal normalized GPU SASS.

Allnine preflight paths/36 cells complete288 measured requests9360 tokens plus
72 checked excluded warmups. Three selected protocol runs each pass622 requests,
22224 tokens/259 rejects plus5000 empty connections. vLLM actual batch/KV
history replay and unchanged whole-output pools pass. Allthree32-action
lifecycle checks pass. The stronger AMK eager-HF failure remains failed.
Full45-executor/180-cell paired latency/throughput comparison is pending;
qualification is dependency evidence, not a performance result. Full generic
serving/performance goal remains active.
''';f.write_text(s)
subprocess.run(['git','diff','--check'],cwd=r,check=True)
paths=['executor/io_uring_tcp.h','README.md','docs/architecture.md','docs/evaluation.md','bench/results/queue_batch_20261014']
subprocess.run(['git','add','--',*paths],cwd=r,check=True)
# Preserve raw compiler/server stdout, including its original whitespace.
code_paths=[str(f.relative_to(r)) for f in a.rglob('*') if f.is_file() and f.suffix in ['.py','.md','.cu','.h']]
subprocess.run(['git','diff','--cached','--check','--','executor/io_uring_tcp.h','README.md','docs/architecture.md','docs/evaluation.md',*code_paths],cwd=r,check=True)
staged=subprocess.check_output(['git','diff','--cached','--name-only'],cwd=r,text=True).splitlines()
assert all(x in paths[:4] or x.startswith(paths[4]+'/') for x in staged)
subprocess.run(['git','commit','-m','Batch coalesced GPU ring publication after protocol qualification'],cwd=r,check=True,stdout=subprocess.DEVNULL)
fd,name=tempfile.mkstemp(prefix='bpfusion-git-askpass-',dir='/tmp');os.write(fd,b'#!/usr/bin/env python3\nimport os,sys\nprint("x-access-token" if "Username" in sys.argv[1] else os.environ["GH_TOKEN"])\n');os.close(fd);os.chmod(name,0o700)
try:
 env=dict(os.environ,GIT_ASKPASS=name,GIT_TERMINAL_PROMPT='0')
 q=subprocess.run(['git','-c','credential.helper=','push','origin','main'],cwd=r,env=env,capture_output=True,text=True);print(q.stderr[-1000:]);q.check_returncode()
 head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip();remote=subprocess.check_output(['git','-c','credential.helper=','ls-remote','origin','refs/heads/main'],cwd=r,env=env,text=True).split()[0];assert head==remote;print('HEAD',head)
finally:os.unlink(name)
print(subprocess.check_output(['git','status','--short'],cwd=r,text=True))
