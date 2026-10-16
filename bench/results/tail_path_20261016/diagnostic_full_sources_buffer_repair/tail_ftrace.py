from pathlib import Path
import os,json,threading,select,ctypes,time,subprocess
class TailFtrace:
 def __init__(self,prefix,mode,pid,libdir):
  self.prefix=Path(prefix);self.mode=mode;self.pid=pid
  self.root=Path('/sys/kernel/tracing/instances')/('bpfusion-tail-'+str(os.getpid())+'-'+str(pid))
  self.root.mkdir();self.root.joinpath('tracing_on').write_text('0')
  self.root.joinpath('trace_clock').write_text('mono')
  self.root.joinpath('buffer_size_kb').write_text('32768')
  self.events=['io_uring/io_uring_submit_req','io_uring/io_uring_complete','io_uring/io_uring_queue_async_work',
   'io_uring/io_uring_task_add','io_uring/io_uring_task_work_run','io_uring/io_uring_local_work_run',
   'io_uring/io_uring_cqring_wait','sched/sched_switch','sched/sched_wakeup',
   'irq/softirq_entry','irq/softirq_exit','syscalls/sys_enter_sendmsg','syscalls/sys_exit_sendmsg',
   'syscalls/sys_enter_recvfrom','syscalls/sys_exit_recvfrom']
  self.formats={};self.ring=None
  if mode.startswith('uring'):
   class Owner(ctypes.Structure):
    _fields_=[('pid',ctypes.c_uint),('pad',ctypes.c_uint),('ring',ctypes.c_uint64),('nsdev',ctypes.c_uint64),('nsino',ctypes.c_uint64)]
   lib=ctypes.CDLL(str(Path(libdir)/'libbpf.so'));lib.bpf_obj_get.argtypes=[ctypes.c_char_p]
   fd=lib.bpf_obj_get(b'/sys/fs/bpf/bpfusion_uring_owner');assert fd>=0
   try:
    key=ctypes.c_uint(0);owner=Owner()
    assert lib.bpf_map_lookup_elem(fd,ctypes.byref(key),ctypes.byref(owner))==0
    self.ring=owner.ring;assert self.ring
   finally:os.close(fd)
  for event in self.events:
   f=self.root/'events'/event;fmt=f.joinpath('format').read_text();self.formats[event]=fmt
   if self.ring and 'field:void * ctx;' in fmt:
    f.joinpath('filter').write_text('ctx == '+str(self.ring))
   f.joinpath('enable').write_text('1')
  self.gpu_apps=subprocess.run(['nvidia-smi','--query-compute-apps=pid,process_name,used_gpu_memory','--format=csv,noheader'],capture_output=True,text=True)
  self.before=dict(gpu_apps=dict(exit=self.gpu_apps.returncode,stdout=self.gpu_apps.stdout,stderr=self.gpu_apps.stderr),utc=time.time_ns(),monotonic_ns=time.monotonic_ns(),ring=self.ring,pid_namespace_status=Path('/proc/'+str(pid)+'/status').read_text(),
   cpu_stat=Path('/proc/stat').read_text(),softirqs=Path('/proc/softirqs').read_text(),formats=self.formats,
   trace_clock=self.root.joinpath('trace_clock').read_text(),buffer_size_kb=self.root.joinpath('buffer_size_kb').read_text())
  self.marker_fd=os.open(self.root/'trace_marker',os.O_WRONLY)
  self.stop_event=threading.Event();self.reader_error=None;self.byte_count=0
  self.thread=threading.Thread(target=self.read);self.thread.start()
  self.root.joinpath('tracing_on').write_text('1')
 def read(self):
  fd=os.open(self.root/'trace_pipe',os.O_RDONLY|os.O_NONBLOCK)
  try:
   with Path(str(self.prefix)+'.ftrace.txt').open('xb',buffering=0) as out:
    while True:
     try:data=os.read(fd,1024*1024)
     except BlockingIOError:
      if self.stop_event.is_set():break
      select.select([fd],[],[],.02);continue
     if data:out.write(data);self.byte_count+=len(data)
     elif self.stop_event.is_set():break
  except BaseException as e:self.reader_error=repr(e)
  finally:os.close(fd)
 def client_marker(self,marker,fd):
  os.write(self.marker_fd,('BF_CLIENT client_ns='+str(marker)+' tid_ns='+str(threading.get_native_id())+' fd='+str(fd)+'\n').encode())
 def finish(self):
  self.root.joinpath('tracing_on').write_text('0');self.stop_event.set();self.thread.join();os.close(self.marker_fd)
  stats={p.parent.name:p.read_text() for p in self.root.glob('per_cpu/cpu*/stats')}
  result=dict(before=self.before,after_monotonic_ns=time.monotonic_ns(),cpu_stat_after=Path('/proc/stat').read_text(),
   softirqs_after=Path('/proc/softirqs').read_text(),stats=stats,bytes=self.byte_count,reader_error=self.reader_error)
  Path(str(self.prefix)+'.ftrace.json').write_text(json.dumps(result,indent=2))
  self.root.rmdir()
  assert self.reader_error is None,self.reader_error
  for name,text in stats.items():
   values={k.strip():float(v.strip()) for line in text.splitlines() if ':' in line for k,v in [line.split(':',1)]}
   for key in ['overrun','commit overrun','dropped events']:assert values.get(key,0)==0,(name,key,values)
  return result
