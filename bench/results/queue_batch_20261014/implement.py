import pathlib,subprocess
r=pathlib.Path('/workspaces/repository');p=pathlib.Path(__file__).parent
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
f=r/'executor/io_uring_tcp.h';s=f.read_text()
assert f.read_bytes()==(p/'original_io_uring_tcp.h').read_bytes()
s=s.replace('io_uring_sqe *sqes;io_uring_cqe *cqes;unsigned mask,cqmask;','io_uring_sqe *sqes;io_uring_cqe *cqes;unsigned mask,cqmask;\n#ifdef BF_IO_COALESCED\n    unsigned sq_head,sq_tail,sq_published;\n#endif',1)
start=s.index('__device__ bool io_submit(');end=s.index('__device__ unsigned long long io_id',start)
old=s[start:end]
new='''#ifdef BF_IO_COALESCED
__device__ bool io_submit(IoRing &ring,io_uring_sqe entry,IoStats *stats) {
    if(ring.sq_tail-ring.sq_head>ring.mask)return false;
    ring.sqes[ring.sq_tail++&ring.mask]=entry;stats->pending++;return true;
}
__device__ void io_publish(IoRing &ring) {
    if(ring.sq_tail==ring.sq_published)return;
    __threadfence_system();io_store(ring.tail,ring.sq_tail);
    ring.sq_published=ring.sq_tail;
}
#else
'''+old+'#endif\n'
s=s[:start]+new+s[end:]
s=s.replace('auto ring=s->ring;auto *page=s->page;', 'auto ring=s->ring;\n#ifdef BF_IO_COALESCED\n    ring.sq_head=io_load(ring.head);ring.sq_tail=ring.sq_published=io_load(ring.tail);\n#endif\n    auto *page=s->page;',1)
old='''unsigned ch=io_load(ring.cqhead);
        while(ch!=io_load(ring.cqtail)) {
            auto e=ring.cqes[ch&ring.cqmask];io_store(ring.cqhead,++ch);'''
new='''unsigned ch=io_load(ring.cqhead);
#ifdef BF_IO_COALESCED
        unsigned begin=ch,end=io_load(ring.cqtail);
        while(ch!=end) {
            auto e=ring.cqes[ch++&ring.cqmask];
#else
        while(ch!=io_load(ring.cqtail)) {
            auto e=ring.cqes[ch&ring.cqmask];io_store(ring.cqhead,++ch);
#endif'''
assert old in s;s=s.replace(old,new,1)
s=s.replace('''        if(stopping&&!cancelled) {''','''#ifdef BF_IO_COALESCED
        if(ch!=begin)io_store(ring.cqhead,ch);
#endif
        if(stopping&&!cancelled) {''',1)
s=s.replace('''        if(stopping&&!cancel_done){__nanosleep(1000);return true;}''','''        if(stopping&&!cancel_done) {
#ifdef BF_IO_COALESCED
            io_publish(ring);
#endif
            __nanosleep(1000);return true;
        }''',1)
s=s.replace('''        if(stopping&&cancelled&&!out->pending&&active<0&&!active_requests) {''','''#ifdef BF_IO_COALESCED
        io_publish(ring);
#endif
        if(stopping&&cancelled&&!out->pending&&active<0&&!active_requests) {''',1)
f.write_text(s);(p/'candidate_io_uring_tcp.h').write_text(s)
print(subprocess.check_output(['git','diff','--stat'],cwd=r,text=True))
subprocess.run(['git','diff','--check'],cwd=r,check=True)
