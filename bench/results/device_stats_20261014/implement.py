import pathlib,subprocess
r=pathlib.Path('/workspaces/repository');p=pathlib.Path(__file__).parent
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
f=r/'executor/io_uring_tcp.h'
s=f.read_text();assert s==(p/'original_io_uring_tcp.h').read_text()
def change(old,new):
 global s
 assert s.count(old)==1,old
 s=s.replace(old,new)
change('#include <utility>\n','#include <utility>\n#include <cstddef>\n')
change('    IoRequest requests[BF_LLM_SLOTS]={};','''#ifdef BF_IO_COALESCED
    bf_uring_loop_control *control=nullptr;
#endif
    IoRequest requests[BF_LLM_SLOTS]={};''')
change('    auto *buffer=s->buffer;auto host_buffer=s->host_buffer;auto *out=s->out;int listener=s->listener;','''    auto *buffer=s->buffer;auto host_buffer=s->host_buffer;auto *out=s->out;int listener=s->listener;
#ifdef BF_IO_COALESCED
    auto *control=s->control;
#else
    auto *control=&out->loop;
#endif''')
change('io_load(&out->loop.model_quiesced)','io_load(&control->model_quiesced)')
change('io_store(&out->loop.finished,1)','io_store(&control->finished,1)')
change('    size_t sq_bytes,ring_bytes,buffer_bytes;cudaStream_t stream;','''    size_t sq_bytes,ring_bytes,buffer_bytes;cudaStream_t stream;
#ifdef BF_IO_COALESCED
    IoStats *stats;
#endif''')
change('    initial.buffer=dbuffer;initial.host_buffer=(uint64_t)net->buffer;initial.out=dreport;initial.listener=listener;','''    initial.buffer=dbuffer;initial.host_buffer=(uint64_t)net->buffer;initial.out=dreport;initial.listener=listener;
#ifdef BF_IO_COALESCED
    // Only loop control is shared during service; bookkeeping stays GPU-local.
    io_check(cudaMalloc(&net->stats,sizeof(IoStats)),"io stats allocation");
    io_check(cudaMemcpy(net->stats,net->report,sizeof(IoStats),cudaMemcpyHostToDevice),"io stats upload");
    initial.out=net->stats;initial.control=&dreport->loop;
#endif''')
change('    io_check(cudaStreamSynchronize(net->stream),"io finish");','''    io_check(cudaStreamSynchronize(net->stream),"io finish");
#ifdef BF_IO_COALESCED
    // Preserve live host/BPF control flags; download only the finished report.
    constexpr size_t offset=offsetof(IoStats,accepted);
    io_check(cudaMemcpy((char*)net->report+offset,(char*)net->stats+offset,
                        sizeof(IoStats)-offset,cudaMemcpyDeviceToHost),"io stats download");
#endif''')
change('    io_check(cudaFree(net->state),"io state free");','''    io_check(cudaFree(net->state),"io state free");
#ifdef BF_IO_COALESCED
    io_check(cudaFree(net->stats),"io stats free");
#endif''')
f.write_text(s);(p/'candidate_io_uring_tcp.h').write_text(s)
assert (r/'executor/vllm_graph.cu').read_bytes()==(p/'original_vllm_graph.cu').read_bytes()
assert (r/'executor/qwen_graph.cu').read_bytes()==(p/'original_qwen_graph.cu').read_bytes()
subprocess.run(['git','diff','--check','--','executor/io_uring_tcp.h'],cwd=r,check=True)
(p/'candidate.diff').write_bytes(subprocess.check_output(['git','diff','--','executor/io_uring_tcp.h'],cwd=r))
