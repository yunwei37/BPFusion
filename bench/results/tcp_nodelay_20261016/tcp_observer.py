"""Bounded own-port packet and own-server socket telemetry, diagnostic only."""
import ctypes,json,os,socket,struct,threading,time
from pathlib import Path
libc=ctypes.CDLL(None,use_errno=True)
class Filter(ctypes.Structure):
    _fields_=[("code",ctypes.c_ushort),("jt",ctypes.c_ubyte),("jf",ctypes.c_ubyte),("k",ctypes.c_uint)]
class Program(ctypes.Structure):
    _fields_=[("length",ctypes.c_ushort),("filters",ctypes.POINTER(Filter))]
class Observer:
 def __init__(self,pid,path,port=39403):
    self.pid=pid;self.port=port;self.path=Path(path);self.raw=self.path.open("x",buffering=1)
    self.lock=threading.Lock();self.done=threading.Event();self.sockets={};self.thread=None;self.packet_thread=None
    self.packet=None;self.pidfd=None;self.count=0;self.info_count=0
 def emit(self,event,**kw):
    with self.lock:self.raw.write(json.dumps(dict(event=event,mono_ns=time.monotonic_ns(),**kw))+"\n")
 def start(self):
    self.emit("observer_start",pid=self.pid,port=self.port,boot=Path("/proc/sys/kernel/random/boot_id").read_text().strip(),cpu_ns=time.process_time_ns())
    try:self.pidfd=os.pidfd_open(self.pid)
    except OSError as e:self.emit("pidfd_error",error=repr(e))
    try:
     s=socket.socket(socket.AF_PACKET,socket.SOCK_RAW,socket.htons(0x0800));self.packet=s
     filters=(Filter*11)(*[Filter(*i) for i in [(0x28,0,0,12),(0x15,0,8,0x0800),(0x30,0,0,23),(0x15,0,6,6),(0xb1,0,0,14),(0x48,0,0,14),(0x15,2,0,self.port),(0x48,0,0,16),(0x15,0,1,self.port),(0x06,0,0,65535),(0x06,0,0,0)]])
     prog=Program(11,filters)
     assert libc.setsockopt(s.fileno(),socket.SOL_SOCKET,26,ctypes.byref(prog),ctypes.sizeof(prog))==0,ctypes.get_errno()
     s.setsockopt(socket.SOL_SOCKET,35,1);s.bind(("lo",0));s.settimeout(.1)
     self.emit("packet_setup",filter="IPv4 TCP own port only; retain pkttype for duplicate handling",clock="kernel SCM_TIMESTAMPNS realtime plus userspace monotonic",realtime_ns=time.time_ns())
     self.packet_thread=threading.Thread(target=self.capture);self.packet_thread.start()
    except BaseException as e:self.emit("packet_error",error=repr(e))
    self.thread=threading.Thread(target=self.poll);self.thread.start()
 def discover(self):
    if self.pidfd is None:return
    try:fds=list(Path("/proc/%d/fd"%self.pid).iterdir())
    except OSError:return
    for f in fds:
     try:
      if not f.readlink().as_posix().startswith("socket:"):continue
      fd=int(f.name)
      if fd in self.sockets:continue
      dup=libc.syscall(438,self.pidfd,fd,0)
      if dup<0:
       self.emit("duplicate_error",fd=fd,errno=ctypes.get_errno());continue
      c=socket.socket(fileno=dup)
      try:
       local=c.getsockname()
       if not isinstance(local,tuple) or local[1]!=self.port:c.close();continue
       try:peer=c.getpeername()
       except OSError:peer=None
       self.sockets[fd]=c
       self.emit("socket",fd=fd,local=local,peer=peer,nodelay=c.getsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY),cork=c.getsockopt(socket.IPPROTO_TCP,socket.TCP_CORK))
      except BaseException:c.close()
     except (OSError,ValueError):continue
 def poll(self):
    next_discover=0
    while not self.done.is_set():
     now=time.monotonic_ns()
     if now>=next_discover:self.discover();next_discover=now+10000000
     for fd,c in list(self.sockets.items()):
      try:
       raw=c.getsockopt(socket.IPPROTO_TCP,socket.TCP_INFO,256)
       if raw[0]==10:continue
       def u32(n):return struct.unpack_from("=I",raw,n)[0] if len(raw)>=n+4 else None
       def u64(n):return struct.unpack_from("=Q",raw,n)[0] if len(raw)>=n+8 else None
       self.emit("tcp_info",fd=fd,length=len(raw),state=raw[0],unacked=u32(24),rto=u32(8),ato=u32(12),snd_mss=u32(16),snd_cwnd=u32(80),retrans=u32(36),total_retrans=u32(100),notsent=u32(144),bytes_acked=u64(120),bytes_sent=u64(200),snd_wnd=u32(228),raw=raw.hex())
       self.info_count+=1
      except OSError as e:self.emit("info_error",fd=fd,error=repr(e))
     self.done.wait(.001)
 def capture(self):
    while not self.done.is_set():
     try:data,anc,flags,addr=self.packet.recvmsg(65535,128)
     except socket.timeout:continue
     except OSError as e:self.emit("capture_error",error=repr(e));break
     seen=time.monotonic_ns()
     if len(data)<54 or data[12:14]!=b"\x08\x00" or data[23]!=6:continue
     ihl=(data[14]&15)*4;off=14+ihl
     sport,dport,seq,ack=struct.unpack_from("!HHII",data,off)
     if self.port not in (sport,dport):continue
     total=struct.unpack_from("!H",data,16)[0];thl=(data[off+12]>>4)*4
     stamp=None
     for level,kind,payload in anc:
      if level==socket.SOL_SOCKET and kind==35:
       sec,nsec=struct.unpack("=qq",payload[:16]);stamp=sec*1000000000+nsec
     self.emit("packet",seen_ns=seen,kernel_realtime_ns=stamp,pkttype=addr[2],sport=sport,dport=dport,seq=seq,ack=ack,flags=data[off+13],window=struct.unpack_from("!H",data,off+14)[0],payload_len=total-ihl-thl,ip_id=struct.unpack_from("!H",data,18)[0],tcp_header=data[off:off+thl].hex())
     self.count+=1
 def stop(self):
    self.done.set()
    if self.thread:self.thread.join()
    if self.packet_thread:self.packet_thread.join()
    stats=None
    if self.packet:
     try:stats=struct.unpack("=II",self.packet.getsockopt(263,6,8))
     except OSError:pass
     self.packet.close()
    for c in self.sockets.values():c.close()
    if self.pidfd is not None:os.close(self.pidfd)
    self.emit("observer_terminal",packets=self.count,info_samples=self.info_count,packet_stats=stats,realtime_ns=time.time_ns(),cpu_ns=time.process_time_ns())
    self.raw.close()
