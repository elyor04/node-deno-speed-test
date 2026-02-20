# Node.js vs Deno vs Bun: Performance Benchmark

This repository provides a performance comparison between Node.js, Deno, and Bun for a simple in-memory CRUD (Create, Read, Update, Delete) API. The benchmark measures requests per second, latency, and overall throughput of these JavaScript runtimes using their native HTTP servers as well as the Hono and Express frameworks.

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
| Node.js (native) | 5216.25 | 11.88 | 8.96 | 35.75 | 40.97 |
| Deno (native) | 6390.26 | 9.53 | 7.35 | 25.74 | 28.51 |
| Bun (native) | 6444.51 | 9.45 | 7.13 | 25.77 | 28.73 |
| Node.js (hono) | 3124.10 | 14.44 | 9.97 | 51.76 | 65.50 |
| Deno (hono) | 6397.22 | 8.99 | 6.95 | 25.30 | 28.15 |
| Bun (hono) | 5987.58 | 9.99 | 8.59 | 22.75 | 25.68 |
| Node.js (express) | 5956.98 | 9.78 | 7.54 | 27.82 | 31.07 |
| Deno (express) | 3497.99 | 14.21 | 9.81 | 49.71 | 58.30 |
| Bun (express) | 6126.21 | 9.50 | 7.33 | 25.84 | 29.05 |
| **🏆 Winner (Best Mean)** | **Deno (hono)** | | | | |

#### GET ALL
| Server | Req/sec | Mean (ms) | Median (ms) | P95 (ms) | P99 (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Node.js (native) | 4704.90 | 12.06 | 11.20 | 22.47 | 24.75 |
| Deno (native) | 5058.63 | 11.21 | 10.65 | 21.49 | 22.41 |
| Bun (native) | 5685.70 | 9.25 | 8.78 | 11.46 | 21.74 |
| Node.js (hono) | 4344.08 | 11.40 | 10.86 | 18.22 | 25.59 |
| Deno (hono) | 5284.37 | 10.50 | 10.16 | 12.40 | 20.63 |
| Bun (hono) | 5216.85 | 11.29 | 10.25 | 23.02 | 23.53 |
| Node.js (express) | 5034.47 | 10.99 | 10.18 | 21.42 | 21.88 |
| Deno (express) | 4114.65 | 12.48 | 12.69 | 15.77 | 18.16 |
| Bun (express) | 5368.20 | 10.62 | 9.68 | 21.25 | 21.70 |
| **🏆 Winner (Best Mean)** | **Bun (native)** | | | | |

#### GET ONE
| Server | Req/sec | Mean (ms) | Median (ms) | P95 (ms) | P99 (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Node.js (native) | 7056.71 | 8.41 | 8.32 | 10.58 | 13.69 |
| Deno (native) | 8456.73 | 6.46 | 6.35 | 8.60 | 10.71 |
| Bun (native) | 8611.29 | 6.38 | 6.25 | 8.77 | 11.10 |
| Node.js (hono) | 6929.98 | 7.45 | 7.14 | 9.86 | 12.89 |
| Deno (hono) | 8350.93 | 6.66 | 6.56 | 9.10 | 11.79 |
| Bun (hono) | 7573.45 | 8.01 | 7.98 | 10.14 | 12.12 |
| Node.js (express) | 7537.31 | 7.44 | 7.36 | 9.76 | 12.48 |
| Deno (express) | 6054.10 | 8.91 | 8.63 | 11.17 | 13.23 |
| Bun (express) | 6949.01 | 8.72 | 8.60 | 11.64 | 14.36 |
| **🏆 Winner (Best Mean)** | **Bun (native)** | | | | |

#### UPDATE
| Server | Req/sec | Mean (ms) | Median (ms) | P95 (ms) | P99 (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Node.js (native) | 5422.39 | 10.15 | 9.85 | 13.51 | 25.00 |
| Deno (native) | 5607.63 | 9.46 | 9.12 | 13.16 | 24.03 |
| Bun (native) | 6470.43 | 8.10 | 7.33 | 14.32 | 23.01 |
| Node.js (hono) | 4265.21 | 10.92 | 9.66 | 24.02 | 27.59 |
| Deno (hono) | 5658.61 | 10.16 | 9.19 | 22.73 | 25.76 |
| Bun (hono) | 5845.44 | 10.16 | 9.21 | 22.57 | 25.01 |
| Node.js (express) | 5574.49 | 10.01 | 8.93 | 22.84 | 26.04 |
| Deno (express) | 3076.81 | 15.53 | 14.06 | 31.07 | 34.78 |
| Bun (express) | 5262.76 | 11.26 | 10.37 | 23.70 | 26.93 |
| **🏆 Winner (Best Mean)** | **Bun (native)** | | | | |

#### DELETE
| Server | Req/sec | Mean (ms) | Median (ms) | P95 (ms) | P99 (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Node.js (native) | 7599.38 | 7.97 | 7.90 | 10.98 | 13.21 |
| Deno (native) | 9387.87 | 5.90 | 5.79 | 8.42 | 11.16 |
| Bun (native) | 9621.06 | 5.64 | 5.54 | 8.08 | 10.55 |
| Node.js (hono) | 8069.69 | 6.76 | 6.74 | 9.79 | 11.51 |
| Deno (hono) | 9355.29 | 5.77 | 5.65 | 8.24 | 11.39 |
| Bun (hono) | 8265.96 | 7.29 | 7.29 | 9.92 | 11.77 |
| Node.js (express) | 8604.47 | 6.40 | 6.27 | 9.17 | 12.19 |
| Deno (express) | 7723.47 | 7.13 | 7.00 | 11.75 | 13.31 |
| Bun (express) | 7738.72 | 7.70 | 7.68 | 10.33 | 13.07 |
| **🏆 Winner (Best Mean)** | **Bun (native)** | | | | |

### Stress Test Comparison

This test bombards the servers with continuous requests for 10 seconds using 200 concurrent workers.

| Server | Req/sec | Mean (ms) | Median (ms) | P95 (ms) | P99 (ms) | Success |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Node.js (native) | 7283.72 | 27.30 | 13.54 | 15.89 | 16.99 | 100.0 % |
| Deno (native) | 7269.01 | 27.36 | 13.55 | 16.22 | 17.27 | 100.0 % |
| Bun (native) | 8094.92 | 24.55 | 12.21 | 13.94 | 15.16 | 100.0 % |
| Node.js (hono) | 5669.49 | 35.06 | 17.53 | 19.86 | 21.76 | 100.0 % |
| Deno (hono) | 6573.62 | 30.25 | 14.88 | 18.24 | 19.46 | 100.0 % |
| Bun (hono) | 7350.06 | 27.05 | 13.48 | 15.33 | 16.17 | 100.0 % |
| Node.js (express) | 6036.81 | 32.91 | 16.46 | 19.53 | 20.66 | 100.0 % |
| Deno (express) | 4364.33 | 45.46 | 22.78 | 26.99 | 29.72 | 100.0 % |
| Bun (express) | 6341.15 | 31.35 | 15.56 | 18.40 | 19.36 | 100.0 % |
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
You need to open separate terminal windows to run each server concurrently.

- **Node.js Server (native):**
  ```bash
  cd crud-node
  npm run native:server
  ```
- **Deno Server (native):**
  ```bash
  cd crud-deno
  deno task native:server
  ```
- **Bun Server (native):**
  ```bash
  cd crud-bun
  bun run native:server
  ```
- **Node.js Server (hono):**
  ```bash
  cd crud-node-hono
  npm run hono:server
  ```
- **Deno Server (hono):**
  ```bash
  cd crud-deno-hono
  deno task hono:server
  ```
- **Bun Server (hono):**
  ```bash
  cd crud-bun-hono
  bun run hono:server
  ```
- **Node.js Server (express):**
  ```bash
  cd crud-node-express
  npm run express:server
  ```
- **Deno Server (express):**
  ```bash
  cd crud-deno-express
  deno task express:server
  ```
- **Bun Server (express):**
  ```bash
  cd crud-bun-express
  bun run express:server
  ```

Each server will run on a different port:
- Node.js (native): `http://localhost:3001`
- Deno (native): `http://localhost:3004`
- Bun (native): `http://localhost:3007`
- Node.js (hono): `http://localhost:3002`
- Deno (hono): `http://localhost:3005`
- Bun (hono): `http://localhost:3008`
- Node.js (express): `http://localhost:3003`
- Deno (express): `http://localhost:3006`
- Bun (express): `http://localhost:3009`

### 4. Run the Benchmark Script
Open a final terminal window.

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
