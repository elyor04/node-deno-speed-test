import asyncio
import aiohttp
import time
from typing import List, Dict
import statistics

URLS = [
    # Node.js
    "http://localhost:3001",
    "http://localhost:3002",
    "http://localhost:3003",
    # Deno
    "http://localhost:3004",
    "http://localhost:3005",
    "http://localhost:3006",
    # Bun
    "http://localhost:3007",
    "http://localhost:3008",
    "http://localhost:3009",
]

SERVER_NAMES = {
    "http://localhost:3001": "Node.js (native)",
    "http://localhost:3002": "Node.js (hono)",
    "http://localhost:3003": "Node.js (express)",
    "http://localhost:3004": "Deno (native)",
    "http://localhost:3005": "Deno (hono)",
    "http://localhost:3006": "Deno (express)",
    "http://localhost:3007": "Bun (native)",
    "http://localhost:3008": "Bun (hono)",
    "http://localhost:3009": "Bun (express)",
}


def calculate_percentile(data: List[float], percentile: float) -> float:
    """Calculate percentile value from a list of numbers"""
    if not data:
        return 0
    sorted_data = sorted(data)
    index = (percentile / 100) * (len(sorted_data) - 1)
    lower = int(index)
    upper = lower + 1
    
    if upper >= len(sorted_data):
        return sorted_data[-1]
    
    weight = index - lower
    return sorted_data[lower] * (1 - weight) + sorted_data[upper] * weight


async def create_user(session: aiohttp.ClientSession, base_url: str, user_id: int) -> Dict:
    """Create a user"""
    start = time.perf_counter()
    try:
        async with session.post(
            f"{base_url}/users",
            json={"name": f"User {user_id}", "email": f"user{user_id}@example.com"}
        ) as response:
            data = await response.json()
            duration = time.perf_counter() - start
            return {"operation": "CREATE", "status": response.status, "duration": duration, "success": True, "data": data}
    except Exception as e:
        duration = time.perf_counter() - start
        return {"operation": "CREATE", "status": 0, "duration": duration, "success": False, "error": str(e)}


async def get_all_users(session: aiohttp.ClientSession, base_url: str) -> Dict:
    """Get all users"""
    start = time.perf_counter()
    try:
        async with session.get(f"{base_url}/users") as response:
            data = await response.json()
            duration = time.perf_counter() - start
            return {"operation": "GET_ALL", "status": response.status, "duration": duration, "success": True, "data": data}
    except Exception as e:
        duration = time.perf_counter() - start
        return {"operation": "GET_ALL", "status": 0, "duration": duration, "success": False, "error": str(e)}


async def get_user(session: aiohttp.ClientSession, base_url: str, user_id: int) -> Dict:
    """Get a single user"""
    start = time.perf_counter()
    try:
        async with session.get(f"{base_url}/users/{user_id}") as response:
            data = await response.json()
            duration = time.perf_counter() - start
            return {"operation": "GET_ONE", "status": response.status, "duration": duration, "success": True, "data": data}
    except Exception as e:
        duration = time.perf_counter() - start
        return {"operation": "GET_ONE", "status": 0, "duration": duration, "success": False, "error": str(e)}


async def update_user(session: aiohttp.ClientSession, base_url: str, user_id: int) -> Dict:
    """Update a user"""
    start = time.perf_counter()
    try:
        async with session.put(
            f"{base_url}/users/{user_id}",
            json={"name": f"Updated User {user_id}"}
        ) as response:
            data = await response.json()
            duration = time.perf_counter() - start
            return {"operation": "UPDATE", "status": response.status, "duration": duration, "success": True, "data": data}
    except Exception as e:
        duration = time.perf_counter() - start
        return {"operation": "UPDATE", "status": 0, "duration": duration, "success": False, "error": str(e)}


async def delete_user(session: aiohttp.ClientSession, base_url: str, user_id: int) -> Dict:
    """Delete a user"""
    start = time.perf_counter()
    try:
        async with session.delete(f"{base_url}/users/{user_id}") as response:
            duration = time.perf_counter() - start
            return {"operation": "DELETE", "status": response.status, "duration": duration, "success": True}
    except Exception as e:
        duration = time.perf_counter() - start
        return {"operation": "DELETE", "status": 0, "duration": duration, "success": False, "error": str(e)}


async def check_server(base_url: str) -> bool:
    """Check if server is running"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{base_url}/users", timeout=aiohttp.ClientTimeout(total=2)) as response:
                return response.status == 200
    except:
        return False


async def run_benchmark(base_url: str, num_requests: int = 100, concurrent: int = 10):
    """Run benchmark tests for a single server"""
    server_name = SERVER_NAMES.get(base_url, base_url)
    
    print(f"\n{'='*70}")
    print(f"API Performance Benchmark - {server_name}")
    print(f"{'='*70}")
    print(f"Target: {base_url}")
    print(f"Total Requests per Operation: {num_requests}")
    print(f"Concurrent Requests: {concurrent}")
    print(f"{'='*70}\n")

    async with aiohttp.ClientSession() as session:
        # Test 1: CREATE users concurrently
        print("Test 1: CREATE operations...")
        operation_start = time.perf_counter()
        tasks = [create_user(session, base_url, i + 1) for i in range(num_requests)]
        create_results = []
        for i in range(0, num_requests, concurrent):
            batch_tasks = tasks[i:i+concurrent]
            batch_results = await asyncio.gather(*batch_tasks)
            create_results.extend(batch_results)
        create_wall_time = time.perf_counter() - operation_start
        
        # Test 2: GET all users
        print("Test 2: GET ALL operations...")
        operation_start = time.perf_counter()
        tasks = [get_all_users(session, base_url) for _ in range(num_requests)]
        get_all_results = []
        for i in range(0, num_requests, concurrent):
            batch_tasks = tasks[i:i+concurrent]
            batch_results = await asyncio.gather(*batch_tasks)
            get_all_results.extend(batch_results)
        get_all_wall_time = time.perf_counter() - operation_start
        
        # Test 3: GET individual users
        print("Test 3: GET ONE operations...")
        operation_start = time.perf_counter()
        tasks = [get_user(session, base_url, result["data"]["id"]) for result in create_results if result["success"]]
        get_one_results = []
        for i in range(0, len(tasks), concurrent):
            batch_tasks = tasks[i:i+concurrent]
            batch_results = await asyncio.gather(*batch_tasks)
            get_one_results.extend(batch_results)
        get_one_wall_time = time.perf_counter() - operation_start
        
        # Test 4: UPDATE users
        print("Test 4: UPDATE operations...")
        operation_start = time.perf_counter()
        tasks = [update_user(session, base_url, result["data"]["id"]) for result in create_results if result["success"]]
        update_results = []
        for i in range(0, len(tasks), concurrent):
            batch_tasks = tasks[i:i+concurrent]
            batch_results = await asyncio.gather(*batch_tasks)
            update_results.extend(batch_results)
        update_wall_time = time.perf_counter() - operation_start
        
        # Test 5: DELETE users
        print("Test 5: DELETE operations...")
        operation_start = time.perf_counter()
        tasks = [delete_user(session, base_url, result["data"]["id"]) for result in create_results if result["success"]]
        delete_results = []
        for i in range(0, len(tasks), concurrent):
            batch_tasks = tasks[i:i+concurrent]
            batch_results = await asyncio.gather(*batch_tasks)
            delete_results.extend(batch_results)
        delete_wall_time = time.perf_counter() - operation_start

    # Combine all results with wall times
    all_results = {
        "CREATE": (create_results, create_wall_time),
        "GET_ALL": (get_all_results, get_all_wall_time),
        "GET_ONE": (get_one_results, get_one_wall_time),
        "UPDATE": (update_results, update_wall_time),
        "DELETE": (delete_results, delete_wall_time),
    }

    # Print statistics
    print(f"\n{'='*70}")
    print(f"Results - {server_name}")
    print(f"{'='*70}\n")

    operation_stats = {}
    total_wall_time = 0
    
    for operation, (results, wall_time) in all_results.items():
        total_wall_time += wall_time
        successful_results = [r for r in results if r["success"]]
        
        if not successful_results:
            print(f"{operation}:")
            print(f"  ❌ All requests failed!")
            print()
            continue
            
        durations = [r["duration"] * 1000 for r in successful_results]  # Convert to ms
        
        # Calculate requests/sec using wall-clock time
        req_per_sec = len(successful_results) / wall_time if wall_time > 0 else 0
        
        # Calculate percentiles
        p95 = calculate_percentile(durations, 95)
        p99 = calculate_percentile(durations, 99)
        
        stats = {
            "total": len(results),
            "successful": len(successful_results),
            "failed": len(results) - len(successful_results),
            "mean": statistics.mean(durations),
            "median": statistics.median(durations),
            "min": min(durations),
            "max": max(durations),
            "p95": p95,
            "p99": p99,
            "stdev": statistics.stdev(durations) if len(durations) > 1 else 0,
            "req_per_sec": req_per_sec,
            "wall_time": wall_time
        }
        
        operation_stats[operation] = stats
        
        print(f"{operation}:")
        print(f"  Total Requests:    {stats['total']}")
        print(f"  Successful:        {stats['successful']}")
        print(f"  Failed:            {stats['failed']}")
        print(f"  Wall Time:         {stats['wall_time']:.3f} s")
        print(f"  Requests/sec:      {stats['req_per_sec']:.2f}")
        print(f"  Mean Duration:     {stats['mean']:.2f} ms")
        print(f"  Median Duration:   {stats['median']:.2f} ms")
        print(f"  Min Duration:      {stats['min']:.2f} ms")
        print(f"  Max Duration:      {stats['max']:.2f} ms")
        print(f"  P95:               {stats['p95']:.2f} ms")
        print(f"  P99:               {stats['p99']:.2f} ms")
        print(f"  Std Deviation:     {stats['stdev']:.2f} ms")
        print()

    # Overall statistics
    total_requests = sum(len(results) for results, _ in all_results.values())
    total_successful = sum(len([r for r in results if r["success"]]) for results, _ in all_results.values())

    if total_successful > 0:
        print(f"{'='*70}")
        print("Overall Summary")
        print(f"{'='*70}")
        print(f"Total Requests:        {total_requests}")
        print(f"Successful Requests:   {total_successful}")
        print(f"Failed Requests:       {total_requests - total_successful}")
        print(f"Total Wall Time:       {total_wall_time:.3f} s")
        print(f"Overall Throughput:    {total_successful / total_wall_time:.2f} req/sec")
        
        # Calculate average duration across all successful requests
        all_durations = []
        for results, _ in all_results.values():
            all_durations.extend([r["duration"] * 1000 for r in results if r["success"]])
        
        if all_durations:
            overall_p95 = calculate_percentile(all_durations, 95)
            overall_p99 = calculate_percentile(all_durations, 99)
            print(f"Average Duration:      {statistics.mean(all_durations):.2f} ms")
            print(f"Overall P95:           {overall_p95:.2f} ms")
            print(f"Overall P99:           {overall_p99:.2f} ms")
        print(f"{'='*70}\n")

    return operation_stats


async def stress_test(base_url: str, duration_seconds: int = 10, concurrent: int = 50):
    """Stress test with continuous requests"""
    server_name = SERVER_NAMES.get(base_url, base_url)
    
    print(f"\n{'='*70}")
    print(f"Stress Test - {server_name}")
    print(f"{'='*70}")
    print(f"Target: {base_url}")
    print(f"Duration: {duration_seconds} seconds")
    print(f"Concurrent Workers: {concurrent}")
    print(f"{'='*70}\n")

    start_time = time.perf_counter()
    id_lock = asyncio.Lock()
    current_id = 0
    results = []

    async def worker(session: aiohttp.ClientSession):
        nonlocal current_id
        while time.perf_counter() - start_time < duration_seconds:
            # Get unique ID
            async with id_lock:
                current_id += 1
                worker_id = current_id
            
            # Perform a mix of operations
            result = await create_user(session, base_url, worker_id)
            results.append(result)

            if result["success"]:
                user_id = result["data"]["id"]
                
                result = await get_user(session, base_url, user_id)
                results.append(result)
                
                result = await update_user(session, base_url, user_id)
                results.append(result)
                
                result = await delete_user(session, base_url, user_id)
                results.append(result)

    async with aiohttp.ClientSession() as session:
        workers = [worker(session) for _ in range(concurrent)]
        await asyncio.gather(*workers)

    # Calculate statistics
    successful_results = [r for r in results if r["success"]]
    
    if not successful_results:
        print("❌ All stress test requests failed!")
        return None
        
    durations = [r["duration"] * 1000 for r in successful_results]
    total_time = time.perf_counter() - start_time
    
    # Calculate percentiles
    p95 = calculate_percentile(durations, 95)
    p99 = calculate_percentile(durations, 99)

    stats = {
        "total": len(results),
        "successful": len(successful_results),
        "failed": len(results) - len(successful_results),
        "total_time": total_time,
        "req_per_sec": len(successful_results) / total_time,
        "mean": statistics.mean(durations),
        "median": statistics.median(durations),
        "min": min(durations),
        "max": max(durations),
        "p95": p95,
        "p99": p99,
        "stdev": statistics.stdev(durations) if len(durations) > 1 else 0
    }

    print(f"Stress Test Results:")
    print(f"  Total Requests:    {stats['total']}")
    print(f"  Successful:        {stats['successful']}")
    print(f"  Failed:            {stats['failed']}")
    print(f"  Total Time:        {stats['total_time']:.2f} seconds")
    print(f"  Requests/sec:      {stats['req_per_sec']:.2f}")
    print(f"  Mean Duration:     {stats['mean']:.2f} ms")
    print(f"  Median Duration:   {stats['median']:.2f} ms")
    print(f"  Min Duration:      {stats['min']:.2f} ms")
    print(f"  Max Duration:      {stats['max']:.2f} ms")
    print(f"  P95:               {stats['p95']:.2f} ms")
    print(f"  P99:               {stats['p99']:.2f} ms")
    print(f"  Std Deviation:     {stats['stdev']:.2f} ms")
    print(f"{'='*70}\n")
    
    return stats


async def compare_servers(benchmark_results: Dict, stress_results: Dict):
    """Compare results from multiple servers"""
    print(f"\n{'='*70}")
    print("COMPARISON SUMMARY")
    print(f"{'='*70}\n")
    
    # Benchmark comparison
    print("Benchmark Results Comparison:")
    print(f"{'='*70}")
    
    operations = ["CREATE", "GET_ALL", "GET_ONE", "UPDATE", "DELETE"]
    
    for operation in operations:
        print(f"\n{operation}:")
        print(f"  {'Server':<25} {'Req/sec':<12} {'Mean':<10} {'Median':<10} {'P95':<10} {'P99':<10}")
        print(f"  {'-'*75}")
        
        best_mean = float('inf')
        best_server = None
        
        for url in URLS:
            if url in benchmark_results and operation in benchmark_results[url]:
                stats = benchmark_results[url][operation]
                server_name = SERVER_NAMES.get(url, url)
                print(f"  {server_name:<25} {stats['req_per_sec']:<12.2f} {stats['mean']:<10.2f} {stats['median']:<10.2f} {stats['p95']:<10.2f} {stats['p99']:<10.2f}")
                
                if stats['mean'] < best_mean:
                    best_mean = stats['mean']
                    best_server = server_name
        
        if best_server:
            print(f"  🏆 Winner (Best Mean): {best_server}")
    
    # Stress test comparison
    if stress_results:
        print(f"\n\nStress Test Comparison:")
        print(f"{'='*70}")
        print(f"  {'Server':<25} {'Req/sec':<12} {'Mean':<10} {'Median':<10} {'P95':<10} {'P99':<10} {'Success':<10}")
        print(f"  {'-'*85}")
        
        best_throughput = 0
        best_server = None
        
        for url in URLS:
            if url in stress_results and stress_results[url]:
                stats = stress_results[url]
                server_name = SERVER_NAMES.get(url, url)
                success_rate = (stats['successful'] / stats['total']) * 100 if stats['total'] > 0 else 0
                print(f"  {server_name:<25} {stats['req_per_sec']:<12.2f} {stats['mean']:<10.2f} {stats['median']:<10.2f} {stats['p95']:<10.2f} {stats['p99']:<10.2f} {success_rate:<10.1f}%")
                
                if stats['req_per_sec'] > best_throughput:
                    best_throughput = stats['req_per_sec']
                    best_server = server_name
        
        if best_server:
            print(f"  🏆 Winner (Best Throughput): {best_server}")
    
    print(f"\n{'='*70}\n")


async def main():
    """Main function to run all tests"""
    print("\n" + "="*70)
    print("SERVER PERFORMANCE TESTING")
    print("="*70)
    
    # Check which servers are running
    print("\nChecking server availability...")
    available_servers = []
    
    for url in URLS:
        server_name = SERVER_NAMES.get(url, url)
        is_running = await check_server(url)
        status = "✅ Running" if is_running else "❌ Not Running"
        print(f"  {server_name}: {status}")
        if is_running:
            available_servers.append(url)
    
    if not available_servers:
        print("\n❌ No servers are running! Please start at least one server.")
        return
    
    print(f"\n{len(available_servers)} server(s) available for testing.\n")
    
    # Run benchmarks
    benchmark_results = {}
    for url in available_servers:
        await asyncio.sleep(1)  # Brief pause between servers
        benchmark_results[url] = await run_benchmark(url, num_requests=1000, concurrent=100)
    
    # Run stress tests
    stress_results = {}
    for url in available_servers:
        await asyncio.sleep(1)  # Brief pause between servers
        stress_results[url] = await stress_test(url, duration_seconds=10, concurrent=200)
    
    # Compare results if multiple servers were tested
    if len(available_servers) > 1:
        await compare_servers(benchmark_results, stress_results)
    
    print("\n✅ All tests completed!\n")


if __name__ == "__main__":
    asyncio.run(main())
