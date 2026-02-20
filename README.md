# Node.js vs Deno vs Bun — HTTP Performance Benchmark

> A rigorous, three-run comparison of Node.js, Deno, and Bun across native HTTP, Hono, and Express — measuring throughput, latency, and stability under real load.

---

## Contents

- [Overview](#overview)
- [Test Environment](#test-environment)
- [TL;DR — Key Takeaways](#tldr--key-takeaways)
- [Benchmark Results](#benchmark-results)
  - [CREATE](#create)
  - [GET ALL](#get-all)
  - [GET ONE](#get-one)
  - [UPDATE](#update)
  - [DELETE](#delete)
  - [Stress Test](#stress-test)
- [Analysis](#analysis)
  - [Runtime Performance](#runtime-performance)
  - [Framework Impact](#framework-impact)
  - [Latency Stability](#latency-stability)
  - [Notable Patterns](#notable-patterns)
- [Final Verdict](#final-verdict)
- [Recommendations](#recommendations)
- [How to Run](#how-to-run)

---

## Overview

This benchmark measures the raw HTTP performance of three modern JavaScript runtimes — **Node.js**, **Deno**, and **Bun** — each tested with three server implementations:

- **Native** HTTP server (no framework)
- **Hono** (lightweight, edge-optimized framework)
- **Express** (the Node.js ecosystem standard)

Each CRUD operation (Create, Read, Update, Delete) was benchmarked individually, followed by a 10-second stress test under 200 concurrent workers. The entire suite was run **three times** to validate consistency. Results below are from the **third and final run**.

---

## Test Environment

| Component | Version |
| :--- | :--- |
| OS | Ubuntu 24.04 (64-bit) |
| Node.js | 24.13 |
| Deno | 2.6 |
| Bun | 1.3 |
| Python (test runner) | 3.12 |

---

## TL;DR — Key Takeaways

| Category | Winner | Notes |
| :--- | :--- | :--- |
| Best raw throughput | **Bun (native)** | Wins stress test in all 3 runs |
| Best latency stability | **Deno** | Cleanest P95/P99 across the board |
| Best framework pairing | **Deno + Hono** | Near-native performance, excellent consistency |
| Worst combination | **Deno + Express** | Express is built for Node internals — not Deno |
| Most ecosystem-friendly | **Node + Express** | Mature, predictable, widest library support |

---

## Benchmark Results

All tables show results from **Run 3**. Full output for all three runs is available in `result.txt`.

### CREATE

| Server | Req/sec | Mean (ms) | Median (ms) | P95 (ms) | P99 (ms) |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Node.js (native) | 5,216 | 11.88 | 8.96 | 35.75 | 40.97 |
| Deno (native) | 6,390 | 9.53 | 7.35 | 25.74 | 28.51 |
| Bun (native) | 6,445 | 9.45 | 7.13 | 25.77 | 28.73 |
| Node.js (hono) | 3,124 | 14.44 | 9.97 | 51.76 | 65.50 |
| Deno (hono) | 6,397 | **8.99** | **6.95** | 25.30 | 28.15 |
| Bun (hono) | 5,988 | 9.99 | 8.59 | 22.75 | 25.68 |
| Node.js (express) | 5,957 | 9.78 | 7.54 | 27.82 | 31.07 |
| Deno (express) | 3,498 | 14.21 | 9.81 | 49.71 | 58.30 |
| Bun (express) | 6,126 | 9.50 | 7.33 | 25.84 | 29.05 |
| 🏆 **Winner** | | **Deno (hono)** | | | |

---

### GET ALL

| Server | Req/sec | Mean (ms) | Median (ms) | P95 (ms) | P99 (ms) |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Node.js (native) | 4,705 | 12.06 | 11.20 | 22.47 | 24.75 |
| Deno (native) | 5,059 | 11.21 | 10.65 | 21.49 | 22.41 |
| Bun (native) | 5,686 | **9.25** | **8.78** | **11.46** | 21.74 |
| Node.js (hono) | 4,344 | 11.40 | 10.86 | 18.22 | 25.59 |
| Deno (hono) | 5,284 | 10.50 | 10.16 | 12.40 | **20.63** |
| Bun (hono) | 5,217 | 11.29 | 10.25 | 23.02 | 23.53 |
| Node.js (express) | 5,034 | 10.99 | 10.18 | 21.42 | 21.88 |
| Deno (express) | 4,115 | 12.48 | 12.69 | 15.77 | 18.16 |
| Bun (express) | 5,368 | 10.62 | 9.68 | 21.25 | 21.70 |
| 🏆 **Winner** | | **Bun (native)** | | | |

---

### GET ONE

| Server | Req/sec | Mean (ms) | Median (ms) | P95 (ms) | P99 (ms) |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Node.js (native) | 7,057 | 8.41 | 8.32 | 10.58 | 13.69 |
| Deno (native) | 8,457 | 6.46 | 6.35 | 8.60 | 10.71 |
| Bun (native) | 8,611 | **6.38** | **6.25** | 8.77 | 11.10 |
| Node.js (hono) | 6,930 | 7.45 | 7.14 | 9.86 | 12.89 |
| Deno (hono) | 8,351 | 6.66 | 6.56 | 9.10 | 11.79 |
| Bun (hono) | 7,573 | 8.01 | 7.98 | 10.14 | 12.12 |
| Node.js (express) | 7,537 | 7.44 | 7.36 | **9.76** | 12.48 |
| Deno (express) | 6,054 | 8.91 | 8.63 | 11.17 | 13.23 |
| Bun (express) | 6,949 | 8.72 | 8.60 | 11.64 | 14.36 |
| 🏆 **Winner** | | **Bun (native)** | | | |

---

### UPDATE

| Server | Req/sec | Mean (ms) | Median (ms) | P95 (ms) | P99 (ms) |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Node.js (native) | 5,422 | 10.15 | 9.85 | 13.51 | 25.00 |
| Deno (native) | 5,608 | 9.46 | 9.12 | 13.16 | 24.03 |
| Bun (native) | 6,470 | **8.10** | **7.33** | 14.32 | **23.01** |
| Node.js (hono) | 4,265 | 10.92 | 9.66 | 24.02 | 27.59 |
| Deno (hono) | 5,659 | 10.16 | 9.19 | 22.73 | 25.76 |
| Bun (hono) | 5,845 | 10.16 | 9.21 | 22.57 | 25.01 |
| Node.js (express) | 5,574 | 10.01 | 8.93 | 22.84 | 26.04 |
| Deno (express) | 3,077 | 15.53 | 14.06 | 31.07 | 34.78 |
| Bun (express) | 5,263 | 11.26 | 10.37 | 23.70 | 26.93 |
| 🏆 **Winner** | | **Bun (native)** | | | |

---

### DELETE

| Server | Req/sec | Mean (ms) | Median (ms) | P95 (ms) | P99 (ms) |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Node.js (native) | 7,599 | 7.97 | 7.90 | 10.98 | 13.21 |
| Deno (native) | 9,388 | 5.90 | 5.79 | 8.42 | 11.16 |
| Bun (native) | 9,621 | **5.64** | **5.54** | **8.08** | **10.55** |
| Node.js (hono) | 8,070 | 6.76 | 6.74 | 9.79 | 11.51 |
| Deno (hono) | 9,355 | 5.77 | 5.65 | 8.24 | 11.39 |
| Bun (hono) | 8,266 | 7.29 | 7.29 | 9.92 | 11.77 |
| Node.js (express) | 8,604 | 6.40 | 6.27 | 9.17 | 12.19 |
| Deno (express) | 7,723 | 7.13 | 7.00 | 11.75 | 13.31 |
| Bun (express) | 7,739 | 7.70 | 7.68 | 10.33 | 13.07 |
| 🏆 **Winner** | | **Bun (native)** | | | |

---

### Stress Test

Continuous requests for **10 seconds** with **200 concurrent workers**.

| Server | Req/sec | Mean (ms) | Median (ms) | P95 (ms) | P99 (ms) | Success |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| Node.js (native) | 7,284 | 27.30 | 13.54 | 15.89 | 16.99 | 100% |
| Deno (native) | 7,269 | 27.36 | 13.55 | 16.22 | 17.27 | 100% |
| **Bun (native)** | **8,095** | **24.55** | **12.21** | **13.94** | **15.16** | 100% |
| Node.js (hono) | 5,669 | 35.06 | 17.53 | 19.86 | 21.76 | 100% |
| Deno (hono) | 6,574 | 30.25 | 14.88 | 18.24 | 19.46 | 100% |
| Bun (hono) | 7,350 | 27.05 | 13.48 | 15.33 | 16.17 | 100% |
| Node.js (express) | 6,037 | 32.91 | 16.46 | 19.53 | 20.66 | 100% |
| Deno (express) | 4,364 | 45.46 | 22.78 | 26.99 | 29.72 | 100% |
| Bun (express) | 6,341 | 31.35 | 15.56 | 18.40 | 19.36 | 100% |
| 🏆 **Winner** | **Bun (native)** | | | | | |

---

## Analysis

### Runtime Performance

Across all three runs and all five CRUD operations, a clear hierarchy emerged for native HTTP performance.

**Bun** is the most consistent all-around performer. It wins the majority of CREATE, UPDATE, and DELETE operations and dominates the stress test in every single run — often by a meaningful margin. Its Zig-based core and aggressively optimized event loop are the likely drivers of this advantage under high concurrency.

**Deno** excels in read-heavy workloads. It competes closely with Bun on GET operations and frequently leads on DELETE, where minimal application logic makes it a near-pure HTTP stack speed test. Deno also shows the most stable latency curves of any runtime.

**Node.js** is reliable but rarely the fastest. It never wins a category outright and shows the widest P95/P99 spreads under load. That said, its behavior is entirely predictable — which has real value in production environments where consistency matters more than peak numbers.

### Framework Impact

**Hono** performance varies significantly by runtime. On Deno, it runs at almost identical speed to native — occasionally even faster — suggesting the framework was designed with Deno's HTTP internals in mind. On Bun, overhead is minimal. On Node.js, however, results are inconsistent and sometimes 30–40% slower than native, indicating a fundamental mismatch with Node's HTTP architecture.

**Express** is at home on Node, where it delivers stable and competitive numbers across all three runs. On Bun it performs decently. On Deno it falls apart — Express is tightly coupled to Node's `http` module and runs on Deno only via a compatibility layer, introducing substantial overhead the numbers confirm decisively.

### Latency Stability

Raw throughput is only part of the picture. Tail latency (P95/P99) determines the experience for the slowest users and is often the more important number in real production systems.

Deno's P95 and P99 values are consistently the tightest of any runtime. Its medians sit close to its means, indicating low jitter and predictable behavior even under sustained load. For latency-sensitive applications that cannot tolerate spikes, Deno is the safest choice.

Bun's P99 occasionally spikes in write-heavy operations (CREATE, UPDATE) despite having the lowest mean latency overall. This is a known characteristic of aggressive throughput optimization — average speed increases, but worst-case requests can suffer.

Node's tail latency is the least predictable, frequently showing P95 values 2–3× the median during write operations.

### Notable Patterns

**DELETE is the clearest runtime speed test.** Because it involves minimal application logic — no JSON parsing, no request body, just a map lookup and a response — it isolates raw HTTP stack performance. Bun and Deno consistently beat Node here, confirming both runtimes have materially faster HTTP implementations than Node 24.

**Hono on Node is unreliable.** In two of three runs, Node + Hono was among the slowest configurations for CREATE. The large variance between runs (3,124 vs. 5,713 req/sec) points to framework-runtime incompatibility rather than measurement noise.

**Express on Deno is a trap.** It consistently underperforms every other Deno configuration by 30–50%. Anyone running Express on Deno expecting to benefit from the runtime's speed will find the compatibility shim erases the advantage entirely.

---

## Final Verdict

| Category | Winner |
| :--- | :--- |
| Raw throughput | 🏆 Bun (native) |
| Read workloads | 🏆 Deno (native) |
| Latency stability | 🏆 Deno |
| Framework efficiency | 🏆 Deno + Hono |
| Stress test | 🏆 Bun (native) |
| Ecosystem maturity | 🏆 Node + Express |
| Worst pairing | ❌ Deno + Express |

---

## Recommendations

**For maximum throughput** — use **Bun (native)**. It leads the stress test in every run, posts the lowest mean latency overall, and requires zero framework overhead. The right choice when raw speed is the primary concern.

**For production APIs where architecture matters** — use **Deno + Hono**. Hono runs at near-native speed on Deno, latency curves are clean and consistent, and the combination is excellent for building well-structured services without sacrificing performance.

**For ecosystem compatibility and team familiarity** — use **Node + Express**. It is the slowest of the three runtimes but by far the most stable in terms of library support, tooling, and community knowledge. The performance gap is real but unlikely to be the bottleneck in most real-world applications.

**Avoid Deno + Express** unless you have a specific reason to need Express on Deno. The performance cost is substantial and entirely consistent across runs.

---

## How to Run

### Prerequisites

- [Node.js](https://nodejs.org/)
- [Deno](https://deno.land/)
- [Bun](https://bun.sh/)
- [Python 3](https://www.python.org/)

### 1. Clone the Repository

```bash
git clone https://github.com/elyor04/node-deno-speed-test.git
cd node-deno-speed-test
```

### 2. Start All Servers

Open a separate terminal for each server.

| Runtime | Framework | Command | Port |
| :--- | :--- | :--- | :--- |
| Node.js | native | `cd crud-node && npm run native:server` | 3001 |
| Deno | native | `cd crud-deno && deno task native:server` | 3004 |
| Bun | native | `cd crud-bun && bun run native:server` | 3007 |
| Node.js | hono | `cd crud-node && npm run hono:server` | 3002 |
| Deno | hono | `cd crud-deno && deno task hono:server` | 3005 |
| Bun | hono | `cd crud-bun && bun run hono:server` | 3008 |
| Node.js | express | `cd crud-node && npm run express:server` | 3003 |
| Deno | express | `cd crud-deno && deno task express:server` | 3006 |
| Bun | express | `cd crud-bun && bun run express:server` | 3009 |

### 3. Run the Benchmark

```bash
cd test-python
pip install aiohttp
python benchmark.py
```

The script will benchmark all nine servers across all CRUD operations and the stress test, then print a full comparative summary.
