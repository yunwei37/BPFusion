// SPDX-License-Identifier: Apache-2.0
// BPFusion: resident daemon = GPU executor + packet gateway.
//
// One process, two threads, one shared page:
//
//   main thread (GPU, pinned)     consumes PENDING slots from the mmap'able
//                                 control page written by the socket filter,
//                                 runs one kernel per batch, publishes the
//                                 completions back into the same page and
//                                 bumps the futex word (done_seq).
//   responder thread (pinned)     sleeps on done_seq with FUTEX_WAIT, and for
//                                 every published completion sends the
//                                 response datagram to the peer address the
//                                 kernel recorded. It also drains the ingress
//                                 socket, so datagrams do not pile up in the
//                                 kernel after the filter returns -1.
//
// There is no control plane: no per-request syscall on the ingress side, no
// thread per connection, no lock. The page is the queue.
#include <arpa/inet.h>
#include <errno.h>
#include <linux/futex.h>
#include <netinet/in.h>
#include <pthread.h>
#include <sched.h>
#include <sys/epoll.h>
#include <sys/mman.h>
#include <sys/socket.h>
#include <sys/syscall.h>
#include <unistd.h>

#include <bpf/bpf.h>
#include <bpf/libbpf.h>

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <ctime>

#include "cuda_timer.h"
#include "bpfusion_queue.h"

// One request: `work` passes of a 16x16x16 triple with a leaky-ReLU, so the
// measured latency is arithmetic rather than pure launch overhead.
__global__ void bf_exec_kernel(struct bf_ctl_slot *in, struct bf_done_slot *out,
			       unsigned int n, unsigned int work)
{
	__shared__ float w1[16][16], w2[16][16], w3[16][16];
	unsigned long long t_start = 0, t_done = 0;
	int t = threadIdx.x;

	for (int i = t; i < 256; i += blockDim.x) {
		w1[i / 16][i % 16] = 0.01f * (float)((i * 7 + 1) % 13) - 0.05f;
		w2[i / 16][i % 16] = 0.01f * (float)((i * 5 + 3) % 11) - 0.05f;
		w3[i / 16][i % 16] = 0.01f * (float)((i * 3 + 5) % 17) - 0.08f;
	}
	__syncthreads();

	if (t >= 16)
		return;
	for (unsigned int k = 0; k < n; k++) {
		if (in[k].state != BF_PENDING)
			continue;
		if (t == 0)
			asm volatile("mov.u64 %0, %%globaltimer;" : "=l"(t_start));
		float a[16], b[16];

		for (int i = 0; i < 16; i++)
			a[i] = in[k].x[i];
		for (unsigned int w = 0; w < work; w++) {
			for (int o = 0; o < 16; o++) {
				float s = 0;

				for (int i = 0; i < 16; i++)
					s += w1[o][i] * a[i];
				b[o] = s > 0 ? s : 0.01f * s;
			}
			for (int o = 0; o < 16; o++) {
				float s = 0;

				for (int i = 0; i < 16; i++)
					s += w2[o][i] * b[i];
				a[o] = s > 0 ? s : 0.01f * s;
			}
			for (int o = 0; o < 16; o++) {
				float s = 0;

				for (int i = 0; i < 16; i++)
					s += w3[o][i] * a[i];
				b[o] = s;
			}
			for (int i = 0; i < 16; i++)
				a[i] = b[i];
		}
		if (t == 0) {
			asm volatile("mov.u64 %0, %%globaltimer;" : "=l"(t_done));
			out[k].id = in[k].id;
			out[k].client_ns = in[k].client_ns;
			out[k].ingress_ns = in[k].ingress_ns;
			for (int i = 0; i < 16; i++)
				out[k].y[i] = a[i];
			out[k].gpu_start_ns = t_start;
			out[k].gpu_done_ns = t_done;
			__threadfence_system();
			out[k].state = BF_DONE;
			in[k].state = BF_FREE;
		}
	}
}

struct daemon {
	struct bf_page *page;
	int sock;
	long pg;
	int run_seconds;
	int work;
	int batch;
	int cpu_gpu;
	int cpu_responder;
	int idle_mode; /* 0 futex, 1 spin, 2 stop after settle */

	unsigned long n_busy;  /* GPU passes that had a batch ready */
	unsigned long n_idle;  /* passes that had to wait for the doorbell */
	/* Honest bubble accounting:
	 *   busy_ns - host wall time the GPU loop was staging or executing a
	 *             batch (i.e. at least one request was queued);
	 *   gpu_ns  - kernel execution time summed from the GPU clock;
	 *   wait_ns - time the loop spent waiting for the doorbell.
	 * The exposed bubble is busy_ns - gpu_ns. */
	uint64_t busy_ns;
	uint64_t gpu_ns;
	uint64_t wait_ns;


	uint64_t deadline;

	/* responder results */
	unsigned long drained, served;
	uint64_t *lat_egress;
	int ne;
	int ne_max;
	int r_futex_timeouts;
	int r_errors;
};

static int futex_wait_ns(volatile uint32_t *w, uint32_t val, int ms)
{
	struct timespec ts = {.tv_sec = ms / 1000,
			      .tv_nsec = (long)(ms % 1000) * 1000000};

	return syscall(SYS_futex, (void *)w, FUTEX_WAIT, val, &ts, NULL, 0);
}

static int futex_wake(volatile uint32_t *w)
{
	return syscall(SYS_futex, (void *)w, FUTEX_WAKE, 1, NULL, NULL, 0);
}

static void pin_cpu(int cpu)
{
	cpu_set_t set;

	if (cpu < 0)
		return;
	CPU_ZERO(&set);
	CPU_SET(cpu, &set);
	sched_setaffinity(0, sizeof(set), &set);
}

static void *responder(void *arg)
{
	struct daemon *d = (struct daemon *)arg;
	uint32_t published, seen;

	pin_cpu(d->cpu_responder);
	while (bf_host_mono_ns() < d->deadline) {
		char buf[2048];
		ssize_t r = recv(d->sock, buf, sizeof(buf), MSG_DONTWAIT);

		if (r > 0) {
			d->drained++;
			continue;
		}
		published = __atomic_load_n(&d->page->published,
					    __ATOMIC_ACQUIRE);
		if (d->page->acked == published) {
			if (d->idle_mode == 1)
				continue; /* busy-poll: re-read published */
			/* Classic futex: read the word, re-check the predicate,
			 * then wait for the value that was seen. The executor
			 * increments the word before waking, so no wake is
			 * lost. */
			seen = __atomic_load_n(&d->page->done_seq,
					       __ATOMIC_ACQUIRE);
			if (d->page->acked !=
			    __atomic_load_n(&d->page->published,
					    __ATOMIC_ACQUIRE))
				continue;
			if (futex_wait_ns(&d->page->done_seq, seen, 20) == -1 &&
			    errno == ETIMEDOUT && d->idle_mode == 2)
				d->r_futex_timeouts++;
			continue;
		}
		while (d->page->acked <
		       __atomic_load_n(&d->page->published, __ATOMIC_ACQUIRE)) {
			uint32_t idx = d->page->acked % BF_SLOTS;
			struct bf_done_slot *ds = &d->page->done[idx];
			struct bf_resp_hdr resp;
			struct sockaddr_in to;
			uint64_t t0;

			if (__atomic_load_n(&ds->state, __ATOMIC_ACQUIRE) !=
				    BF_DONE ||
			    ds->id != d->page->acked)
				break;
			memset(&resp, 0, sizeof(resp));
			resp.magic = BF_MAGIC;
			resp.id = ds->id;
			resp.client_ns = ds->client_ns;
			resp.ingress_ns = ds->ingress_ns;
			resp.gpu_start_ns = ds->gpu_start_ns;
			resp.gpu_done_ns = ds->gpu_done_ns;
			memcpy(resp.y, ds->y, sizeof(resp.y));
			memset(&to, 0, sizeof(to));
			to.sin_family = AF_INET;
			to.sin_addr.s_addr = d->page->peers[idx].addr_be;
			to.sin_port = d->page->peers[idx].port_be;
			t0 = bf_host_mono_ns();
			if (sendto(d->sock, &resp, sizeof(resp), 0,
				   (struct sockaddr *)&to, sizeof(to)) < 0)
				d->r_errors++;
			if (d->ne < d->ne_max)
				d->lat_egress[d->ne++] = bf_host_mono_ns() - t0;
			/* Recycle: only now may the producer reuse the slot.
			 * The ctl slot must be freed here too, since the GPU
			 * only frees its staged copy, not the mmap'ed page. */
			__atomic_store_n(&d->page->slots[idx].state, BF_FREE,
					 __ATOMIC_RELEASE);
			__atomic_store_n(&ds->state, BF_FREE, __ATOMIC_RELEASE);
			d->page->acked++;
			d->served++;
		}
	}
	return NULL;
}

static int cmp_u64(const void *a, const void *b)
{
	uint64_t x = *(const uint64_t *)a, y = *(const uint64_t *)b;

	return (x > y) - (x < y);
}

static int rb_sample(void *ctx, void *data, size_t size)
{
	(void)ctx;
	(void)data;
	(void)size;
	return 0;
}

static void report(const char *name, uint64_t *v, int n)
{
	double s = 0;

	if (n <= 0) {
		printf("%-34s (no samples)\n", name);
		return;
	}
	qsort(v, n, sizeof(uint64_t), cmp_u64);
	for (int i = 0; i < n; i++)
		s += v[i];
	printf("%-34s n=%7d  p50=%8lu  p90=%8lu  p99=%8lu  max=%10lu  mean=%9.0f ns\n",
	       name, n, v[n / 2], v[n * 90 / 100], v[n * 99 / 100], v[n - 1],
	       s / n);
}

int main(int argc, char **argv)
{
	struct daemon d;
	int port = 39400;
	int cpu_gpu = 2, cpu_responder = 3;
	int idle_mode = 0;
	int ctl_fd, ep;
	struct sockaddr_in addr;
	pthread_t th;
	unsigned long served = 0, drained = 0;

	d.run_seconds = argc > 1 ? atoi(argv[1]) : 5;
	d.work = argc > 2 ? atoi(argv[2]) : 4;
	d.batch = argc > 3 ? atoi(argv[3]) : BF_MAX_BATCH;
	if (argc > 4)
		cpu_gpu = atoi(argv[4]);
	if (argc > 5)
		cpu_responder = atoi(argv[5]);
	if (argc > 6)
		idle_mode = atoi(argv[6]);
	d.cpu_gpu = cpu_gpu;
	d.cpu_responder = cpu_responder;
	d.idle_mode = idle_mode;
	d.ne = 0;
	d.ne_max = 4000000;
	d.drained = 0;
	d.served = 0;
	d.r_futex_timeouts = 0;
	d.r_errors = 0;
	d.n_busy = 0;
	d.n_idle = 0;
	d.busy_ns = 0;
	d.gpu_ns = 0;
	d.wait_ns = 0;

	d.lat_egress = (uint64_t *)malloc(sizeof(uint64_t) * d.ne_max);

	d.pg = sysconf(_SC_PAGESIZE);

	/* The loader owns the object lifetime and pins the maps; the daemon
	 * only opens them, so both processes share one page and one program. */
	if ((ctl_fd = bpf_obj_get("/sys/fs/bpf/bpfusion_ctl")) < 0) {
		fprintf(stderr, "bpf_obj_get ctl: %s\n", strerror(errno));
		return 1;
	}
	d.page = (struct bf_page *)mmap(NULL, BF_PAGE_MMAP_BYTES,
					PROT_READ | PROT_WRITE, MAP_SHARED,
					ctl_fd, 0);
	if (d.page == MAP_FAILED) {
		perror("mmap ctl");
		return 1;
	}
	{
		int db_fd = bpf_obj_get("/sys/fs/bpf/bpfusion_db");

		if (db_fd < 0) {
			fprintf(stderr, "bpf_obj_get doorbell: %s\n",
				strerror(errno));
			return 1;
		}
		ep = epoll_create1(0);
		{
			struct epoll_event ev = {.events = EPOLLIN};

			epoll_ctl(ep, EPOLL_CTL_ADD, db_fd, &ev);
		}
	}

	d.sock = socket(AF_INET, SOCK_DGRAM, 0);
	memset(&addr, 0, sizeof(addr));
	addr.sin_family = AF_INET;
	addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
	addr.sin_port = htons((uint16_t)port);
	if (bind(d.sock, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
		perror("bind");
		return 1;
	}
	{
		int sz = 8 << 20;

		setsockopt(d.sock, SOL_SOCKET, SO_RCVBUF, &sz, sizeof(sz));
	}

	/* --- GPU side ------------------------------------------------------ */
	{
		cudaStream_t stream;
		struct bf_ctl_slot *d_in;
		struct bf_done_slot *d_out;
		struct bf_ctl_slot *h_in;
		struct bf_done_slot *h_out;
		volatile uint64_t *ts_slot;
		void *d_ts;
		bf_timer_sync tinfo;
		__u32 consumed = 0;
		uint64_t *lat_dev, *lat_kernel;
		int nb = 0, nk = 0;
		struct ring_buffer *rb;

		lat_dev = (uint64_t *)malloc(sizeof(uint64_t) * 4000000);
		lat_kernel = (uint64_t *)malloc(sizeof(uint64_t) * 4000000);

		cudaSetDevice(0);
		cudaStreamCreateWithFlags(&stream, cudaStreamNonBlocking);
		cudaMalloc((void **)&d_in, sizeof(struct bf_ctl_slot) * BF_SLOTS);
		cudaMalloc((void **)&d_out, sizeof(struct bf_done_slot) * BF_SLOTS);
		cudaMemset(d_in, 0, sizeof(struct bf_ctl_slot) * BF_SLOTS);
		cudaMemset(d_out, 0, sizeof(struct bf_done_slot) * BF_SLOTS);
		cudaHostAlloc(&h_in, sizeof(struct bf_ctl_slot) * BF_SLOTS,
			      cudaHostAllocDefault);
		cudaHostAlloc(&h_out, sizeof(struct bf_done_slot) * BF_SLOTS,
			      cudaHostAllocDefault);
		cudaHostAlloc((void **)&ts_slot, 8, cudaHostAllocMapped);
		cudaHostGetDevicePointer(&d_ts, (void *)ts_slot, 0);
		tinfo = bf_timer_sync_sample(ts_slot, d_ts, stream, 64);
		memset(h_in, 0, sizeof(struct bf_ctl_slot) * BF_SLOTS);
		memset(h_out, 0, sizeof(struct bf_done_slot) * BF_SLOTS);
		rb = ring_buffer__new(bpf_obj_get("/sys/fs/bpf/bpfusion_db"),
				      rb_sample, NULL, NULL);
		if (!rb) {
			fprintf(stderr, "ring_buffer__new failed\n");
			return 1;
		}

		printf("daemon: slots=%d batch=%d work=%d gpu_cpu=%d "
		       "resp_cpu=%d idle=%d\n",
		       BF_SLOTS, d.batch, d.work, cpu_gpu, cpu_responder,
		       idle_mode);
		printf("daemon: globaltimer offset=%lld ns (spread %lld ns)\n",
		       (long long)tinfo.offset, (long long)tinfo.spread);

		d.deadline = bf_host_mono_ns() +
			     (uint64_t)d.run_seconds * 1000000000ull;
		__atomic_store_n(&d.page->ready, 1, __ATOMIC_RELEASE);
		pthread_create(&th, NULL, responder, &d);
		pin_cpu(cpu_gpu);

		uint64_t t_run0 = bf_host_mono_ns();

		while (bf_host_mono_ns() < d.deadline) {
			uint64_t t_wait0 = bf_host_mono_ns();
			__u32 head = __atomic_load_n(&d.page->head,
						     __ATOMIC_ACQUIRE);
			__u32 pending = head - consumed;
			uint64_t t_pass;
			int n, i;

			if (pending == 0) {
				struct epoll_event ev;
				int r = epoll_wait(ep, &ev, 1, 20);

				d.n_idle++;
				d.wait_ns += bf_host_mono_ns() - t_wait0;
				if (r <= 0)
					continue;
				ring_buffer__consume(rb);
				continue;
			}
			d.n_busy++;
			t_pass = bf_host_mono_ns();

			n = pending > (__u32)d.batch ? d.batch : (int)pending;
			if (n > BF_SLOTS - (int)(consumed % BF_SLOTS))
				n = BF_SLOTS - (int)(consumed % BF_SLOTS);

			/* The producer's slots live in the mmap'ed page, which
			 * is not a pinned DMA region, so a batch is staged
			 * through pinned memory. */
			for (i = 0; i < n; i++) {
				__u32 idx = (consumed + i) % BF_SLOTS;

				h_in[i] = d.page->slots[idx];
			}
			cudaMemcpyAsync(d_in, h_in,
					sizeof(struct bf_ctl_slot) * n,
					cudaMemcpyHostToDevice, stream);
			bf_exec_kernel<<<1, 32, 0, stream>>>(d_in, d_out, n,
							     d.work);
			cudaMemcpyAsync(h_out, d_out,
					sizeof(struct bf_done_slot) * n,
					cudaMemcpyDeviceToHost, stream);
			cudaStreamSynchronize(stream);

			for (i = 0; i < n; i++) {
				struct bf_done_slot *ds = &h_out[i];
				__u32 idx = (consumed + i) % BF_SLOTS;

				/* Slot may already have been handled (and freed)
				 * by a previous pass; skipping keeps `published`
				 * monotonic and the responder in lockstep. */
				if (ds->state != BF_DONE ||
				    d.page->done[idx].state == BF_DONE)
					continue;
				/* Store on the host clock: `offset` converts
				 * the GPU's %globaltimer into CLOCK_MONOTONIC,
				 * so client RTT and parse→GPU-start share one
				 * time base. */
				ds->gpu_start_ns =
					(uint64_t)((int64_t)ds->gpu_start_ns +
						   (int64_t)tinfo.offset);
				ds->gpu_done_ns =
					(uint64_t)((int64_t)ds->gpu_done_ns +
						   (int64_t)tinfo.offset);
				d.page->done[idx] = *ds;
				if (ds->gpu_done_ns > ds->gpu_start_ns &&
				    nb < 4000000)
					lat_dev[nb++] = ds->gpu_done_ns -
							ds->gpu_start_ns;
				if (nk < 4000000)
					lat_kernel[nk++] =
						ds->gpu_done_ns - ds->ingress_ns;
				if (ds->gpu_done_ns > ds->gpu_start_ns)
					d.gpu_ns += ds->gpu_done_ns -
						   ds->gpu_start_ns;
			}
			/* Charge the whole pass to busy_ns; the kernel time
			 * added above is then the part of busy_ns the GPU was
			 * actually executing, so busy_ns - gpu_ns is the
			 * staging/memcpy/launch bubble. */
			d.busy_ns += bf_host_mono_ns() - t_pass;
			consumed += n;
			__atomic_store_n(&d.page->published, consumed,
					 __ATOMIC_RELEASE);
			if (idle_mode != 1)
				futex_wake(&d.page->done_seq);
		}
		d.deadline = 0; /* let the responder exit immediately */
		__atomic_store_n(&d.page->published, consumed, __ATOMIC_RELEASE);
		futex_wake(&d.page->done_seq);
		pthread_join(th, NULL);
		drained = d.drained;
		served = d.served;

		{
			double run_ns = (double)(bf_host_mono_ns() - t_run0);

			printf("daemon: consumed=%u published=%u head=%u "
			       "drops=%u acked=%u\n",
			       consumed, d.page->published, d.page->head,
			       d.page->drops, d.page->acked);
			printf("daemon: drained=%lu served=%lu errors=%d "
			       "futex_timeouts=%d\n",
			       drained, served, d.r_errors,
			       d.r_futex_timeouts);
			printf("daemon: gpu passes busy=%lu idle=%lu "
			       "(idle %.1f%% of %.2f s; wall %.0f req/s)\n",
			       d.n_busy, d.n_idle,
			       run_ns > 0 ? 100.0 * (double)d.n_idle /
						    (double)(d.n_busy + d.n_idle)
					  : 0.0,
			       run_ns / 1e9,
			       run_ns > 0 ? (double)served * 1e9 / run_ns : 0.0);
			/* Occupancy: kernel_exec / wall while requests were
			 * queued. Anything below 100% is the staging bubble
			 * that this design cannot hide yet. */
			printf("daemon: gpu kernel %.2f s busy_wall %.2f s "
			       "wait %.2f s -> occupancy %.1f%% "
			       "(bubble %.2f s)\n",
			       (double)d.gpu_ns / 1e9,
			       (double)d.busy_ns / 1e9,
			       (double)d.wait_ns / 1e9,
			       d.busy_ns > 0 ? 100.0 * (double)d.gpu_ns /
						       (double)d.busy_ns
					     : 0.0,
			       (double)(d.busy_ns - d.gpu_ns) / 1e9);
		}
		report("GPU start -> GPU done", lat_dev, nb);
		report("kernel parse -> GPU done", lat_kernel, nk);
		report("responder sendto()", d.lat_egress, d.ne);
	}
	return 0;
}
