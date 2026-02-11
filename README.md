# Node.js vs Deno vs Bun: Performance Benchmark

This repository provides a performance comparison between Node.js, Deno, and Bun for a simple in-memory CRUD (Create, Read, Update, Delete) API. The benchmark measures requests per second, latency, and overall throughput of these JavaScript runtimes using their native HTTP servers.

The tests were conducted using a Python script with `aiohttp` to send asynchronous requests to each server.

## Test Environment
- **OS**: Ubuntu 24.04 (64-bit)
- **Node.js**: 24.13
- **Deno**: 2.6
- **Bun**: 1.3
- **Python**: 3.12 (for the benchmarking script)

## Benchmark Results

The benchmark was run three times to ensure consistency. The results below are from the third and final run. For the complete output of all three runs, please see `result.txt`.

### Individual CRUD Operations

#### CREATE
| Server | Req/sec | Mean (ms) | Median (ms) | P95 (ms) | P99 (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Node.js (native http) | 5818.55 | 10.51 | 8.39 | 26.91 | 30.30 |
| Deno (native) | 6383.47 | 9.57 | 7.29 | 25.26 | 28.04 |
| Bun (native) | 6545.07 | 9.02 | 6.98 | 24.47 | 27.35 |
| **🏆 Winner (Best Mean)** | **Bun (native)** | | | | |

#### GET ALL
| Server | Req/sec | Mean (ms) | Median (ms) | P95 (ms) | P99 (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Node.js (native http) | 5088.28 | 11.54 | 10.58 | 22.34 | 23.51 |
| Deno (native) | 5145.48 | 10.99 | 10.11 | 21.27 | 22.08 |
| Bun (native) | 5743.48 | 9.37 | 8.60 | 12.01 | 21.39 |
| **🏆 Winner (Best Mean)** | **Bun (native)** | | | | |

#### GET ONE
| Server | Req/sec | Mean (ms) | Median (ms) | P95 (ms) | P99 (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Node.js (native http) | 8285.49 | 6.66 | 6.55 | 8.64 | 11.91 |
| Deno (native) | 8588.29 | 6.33 | 6.22 | 8.42 | 10.97 |
| Bun (native) | 8426.79 | 6.45 | 6.27 | 8.45 | 11.93 |
| **🏆 Winner (Best Mean)** | **Deno (native)** | | | | |

#### UPDATE
| Server | Req/sec | Mean (ms) | Median (ms) | P95 (ms) | P99 (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Node.js (native http) | 6135.44 | 8.37 | 8.08 | 11.47 | 23.64 |
| Deno (native) | 5629.95 | 9.50 | 9.20 | 13.15 | 24.43 |
| Bun (native) | 6595.51 | 7.74 | 7.21 | 11.81 | 22.60 |
| **🏆 Winner (Best Mean)** | **Bun (native)** | | | | |

#### DELETE
| Server | Req/sec | Mean (ms) | Median (ms) | P95 (ms) | P99 (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Node.js (native http) | 9262.36 | 6.04 | 5.99 | 8.88 | 10.37 |
| Deno (native) | 9501.76 | 5.80 | 5.73 | 8.37 | 11.08 |
| Bun (native) | 9669.36 | 5.58 | 5.52 | 8.03 | 9.75 |
| **🏆 Winner (Best Mean)** | **Bun (native)** | | | | |

### Stress Test Comparison

This test bombards the servers with continuous requests for 10 seconds using 200 concurrent workers.

| Server | Req/sec | Mean (ms) | Median (ms) | P95 (ms) | P99 (ms) | Success |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Node.js (native http) | 7506.48 | 26.50 | 13.12 | 15.68 | 16.77 | 100.0 % |
| Deno (native) | 7267.91 | 27.36 | 13.51 | 16.18 | 18.59 | 100.0 % |
| Bun (native) | 7970.86 | 24.94 | 12.34 | 14.27 | 15.30 | 100.0 % |
| **🏆 Winner (Best Throughput)** | **Bun (native)** | | | | | |

## How to Run the Benchmark

### 1. Prerequisites
Make sure you have the following installed:
- [Node.js](https://nodejs.org/)
- [Deno](https://deno.land/)
- [Bun](https://bun.sh/)
- [Python 3](https://www.python.org/)

### 2. Clone the Repository
```bash
git clone https://github.com/elyor04/node-deno-speed-test.git
cd node-deno-speed-test
```

### 3. Start the Servers
You need to open three separate terminal windows to run each server concurrently.

- **Node.js Server:**
  ```bash
  cd crud-node
  npm start
  ```
- **Deno Server:**
  ```bash
  cd crud-deno
  deno task start
  ```
- **Bun Server:**
  ```bash
  cd crud-bun
  bun start
  ```

Each server will run on a different port:
- Node.js: `http://localhost:3001`
- Deno: `http://localhost:3002`
- Bun: `http://localhost:3003`

### 4. Run the Benchmark Script
Open a fourth terminal window.

- **Navigate to the test directory and install dependencies:**
  ```bash
  cd test-python
  pip install aiohttp
  ```
- **Run the benchmark:**
  ```bash
  python benchmark.py
  ```

The script will run a series of benchmark and stress tests against all running servers and print a comparative summary at the end.
