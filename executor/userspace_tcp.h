// SPDX-License-Identifier: Apache-2.0
// Matched userspace network control: same page ABI and resident GPU dispatcher.
#include <sys/epoll.h>
#include <sys/uio.h>
#include <cerrno>
#include <cstring>
#include <map>
#include <memory>
#include <string>
#include <chrono>

static int user_network(bf_page *page,int listener,unsigned seconds,
                        volatile sig_atomic_t *stopped) {
    struct Peer {
        int fd;
        bool eof=false;
        int slot=-1;
        std::string input;
    };
    struct Reply {
        std::shared_ptr<Peer> peer;
        std::string header;
        size_t header_sent=0,bytes=0;
    } replies[BF_LLM_SLOTS];
    std::map<int,std::shared_ptr<Peer>> peers;
    unsigned head=0,completed=0,rejected_count=0,accepted=0;
    int ep=epoll_create1(EPOLL_CLOEXEC);
    if(ep<0) { perror("epoll_create1");return 1; }
    fcntl(listener,F_SETFL,fcntl(listener,F_GETFL)|O_NONBLOCK);
    epoll_event watch={};watch.events=EPOLLIN;watch.data.fd=listener;
    if(epoll_ctl(ep,EPOLL_CTL_ADD,listener,&watch)) { close(ep);return 1; }
    auto disconnect=[&](Peer &peer) {
        if(peer.fd>=0) {
            epoll_ctl(ep,EPOLL_CTL_DEL,peer.fd,nullptr);
            close(peer.fd);peer.fd=-1;
        }
        peer.eof=true;
    };
    auto send_reply=[&](Peer &peer,Reply &reply,bf_llm_slot *slot,unsigned produced) {
        iovec vec[2];unsigned count=0;
        size_t header_bytes=reply.header.size()-reply.header_sent;
        if(header_bytes) vec[count++]={reply.header.data()+reply.header_sent,header_bytes};
        if(produced*4>reply.bytes)
            vec[count++]={(char *)slot->tok_out+reply.bytes,produced*4-reply.bytes};
        if(!count) return;
        msghdr msg={};msg.msg_iov=vec;msg.msg_iovlen=count;
        ssize_t n=sendmsg(peer.fd,&msg,MSG_DONTWAIT|MSG_NOSIGNAL);
        if(n<0 && errno!=EAGAIN && errno!=EWOULDBLOCK && errno!=EINTR)
            disconnect(peer);
        if(n>0) {
            size_t sent_header=(size_t)n<header_bytes ? (size_t)n : header_bytes;
            reply.header_sent+=sent_header;reply.bytes+=(size_t)n-sent_header;
        }
    };
    auto deadline=std::chrono::steady_clock::now()+std::chrono::seconds(seconds);
    while(!*stopped && std::chrono::steady_clock::now()<deadline) {
        // Busy completion polling is a low-latency control; report its CPU cost.
        epoll_event events[BF_LLM_SLOTS*2];
        int n=epoll_wait(ep,events,BF_LLM_SLOTS*2,0);
        if(n<0 && errno!=EINTR) { perror("epoll_wait");break; }
        for(int e=0;e<n;e++) {
            int fd=events[e].data.fd;
            if(fd==listener) {
                while(true) {
                    int child=accept4(listener,nullptr,nullptr,SOCK_NONBLOCK|SOCK_CLOEXEC);
                    if(child<0) break;
                    auto peer=std::make_shared<Peer>();peer->fd=child;
                    peers[child]=peer;accepted++;
                    watch.events=EPOLLIN|EPOLLRDHUP;watch.data.fd=child;
                    if(epoll_ctl(ep,EPOLL_CTL_ADD,child,&watch)) disconnect(*peer);
                }
            } else {
                auto it=peers.find(fd);if(it==peers.end()) continue;
                Peer &peer=*it->second;
                char buffer[4096];
                while(peer.fd>=0) {
                    ssize_t got=recv(peer.fd,buffer,sizeof(buffer),MSG_DONTWAIT);
                    if(got>0) peer.input.append(buffer,got);
                    else {
                        if(got==0) {
                            peer.eof=true;epoll_ctl(ep,EPOLL_CTL_DEL,peer.fd,nullptr);
                        } else if(errno!=EAGAIN && errno!=EWOULDBLOCK && errno!=EINTR)
                            disconnect(peer);
                        break;
                    }
                }
            }
        }
        for(unsigned i=0;i<BF_LLM_SLOTS;i++) {
            Reply &reply=replies[i];if(!reply.peer) continue;
            Peer &peer=*reply.peer;bf_llm_slot *slot=&page->llm[i];
            unsigned state=__atomic_load_n(&slot->state,__ATOMIC_ACQUIRE);
            unsigned short flags=__atomic_load_n(&slot->pad,__ATOMIC_ACQUIRE);
            bool rejected=flags&BF_LLM_REJECTED;
            if((flags&BF_LLM_VALIDATING) || (rejected && state!=BF_DONE)) continue;
            unsigned produced=__atomic_load_n(&slot->produced,__ATOMIC_ACQUIRE);
            if(state!=BF_DONE && produced==slot->n_gen && produced) produced--;
            if(rejected && (flags&BF_LLM_TRANSPORT_MASK)==1) disconnect(peer);
            if((flags&BF_LLM_TRANSPORT_MASK)==2 && reply.header.empty()) {
                reply.header="HTTP/1.1 "+std::string(rejected ? "400 Bad Request" : "200 OK")
                    +"\r\nContent-Type: application/octet-stream\r\nContent-Length: "
                    +std::to_string(rejected ? 0 : slot->n_gen*4)+"\r\n\r\n";
            }
            // Keep default TCP buffering; submit header and first tokens together.
            if(peer.fd>=0 && (produced || rejected))
                send_reply(peer,reply,slot,produced);
            if(state==BF_DONE && (peer.fd<0 ||
                (reply.header_sent==reply.header.size() && reply.bytes==produced*4))) {
                peer.slot=-1;reply={};
                __atomic_store_n(&slot->state,(unsigned)BF_FREE,__ATOMIC_RELEASE);
                completed++;if(rejected) rejected_count++;
            }
        }
        for(auto it=peers.begin();it!=peers.end();) {
            auto peer=it->second;
            if(peer->fd>=0 && peer->slot<0 && !peer->input.empty()) {
                size_t offset=0;
                bool http=peer->input.compare(0,4,"POST")==0;
                if(http) {
                    size_t end=peer->input.find("\r\n\r\n");
                    if(end==std::string::npos) { ++it;continue; }
                    offset=end+4;
                }
                if(peer->input.size()<offset+24) { ++it;continue; }
                unsigned fields[4];unsigned long long client_ns;
                memcpy(fields,peer->input.data()+offset,16);
                memcpy(&client_ns,peer->input.data()+offset+16,8);
                unsigned prompt=fields[1],gen=fields[2];
                if(fields[0]!=BF_LLM_MAGIC || !prompt || prompt>BF_LLM_MAX_TOK ||
                   !gen || gen>BF_LLM_MAX_TOK) {
                    disconnect(*peer);
                } else {
                    size_t bytes=24+prompt*4;
                    if(http) {
                        size_t key=peer->input.find("\r\nContent-Length: ");
                        if(key==std::string::npos || key>=offset ||
                           strtoul(peer->input.c_str()+key+18,nullptr,10)!=bytes) {
                            disconnect(*peer);++it;continue;
                        }
                    }
                    if(peer->input.size()<offset+bytes) { ++it;continue; }
                    unsigned i=head%BF_LLM_SLOTS;bf_llm_slot *slot=&page->llm[i];
                    if(__atomic_load_n(&slot->state,__ATOMIC_ACQUIRE)==BF_FREE) {
                        __atomic_store_n(&slot->state,(unsigned)BF_WRITING,__ATOMIC_RELEASE);
                        slot->n_prompt=prompt;slot->n_gen=gen;slot->produced=0;
                        slot->client_ns=client_ns;
                        slot->pad=(http ? 2 : 1)|BF_LLM_VALIDATING;
                        memcpy(slot->tok_in,peer->input.data()+offset+24,prompt*4);
                        peer->input.erase(0,offset+bytes);
                        replies[i].peer=peer;peer->slot=i;
                        __atomic_store_n(&slot->state,(unsigned)BF_PENDING,__ATOMIC_RELEASE);
                        __atomic_store_n(&page->llm_head,++head,__ATOMIC_RELEASE);
                    }
                }
            }
            if(peer->slot<0 && (peer->fd<0 || (peer->eof && peer->input.empty()))) {
                disconnect(*peer);it=peers.erase(it);
            } else ++it;
        }
    }
    for(auto &item:peers) disconnect(*item.second);
    close(ep);
    printf("userspace TCP stopped: accepted=%u published=%u completed=%u rejected=%u\n",
           accepted,head,completed,rejected_count);fflush(stdout);
    return 0;
}
