import asyncio
import aiohttp
import time
from typing import List, Dict
import statistics

URLS = [
    "http://localhost:3001",  # Node.js
    "http://localhost:3002",  # Deno
    "http://localhost:3003",  # Bun
]

SERVER_NAMES = {
    "http://localhost:3001": "Node.js (native http)",
    "http://localhost:3002": "Deno (native)",
    "http://localhost:3003": "Bun (native)",
}


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
        tasks = [create_user(session, base_url, i + 1) for i in range(num_requests)]
        create_results = []
        for i in range(0, num_requests, concurrent):
            batch_tasks = tasks[i:i+concurrent]
            batch_results = await asyncio.gather(*batch_tasks)
            create_results.extend(batch_results)
        
        # Test 2: GET all users
        print("Test 2: GET ALL operations...")
        tasks = [get_all_users(session, base_url) for _ in range(num_requests)]
        get_all_results = []
        for i in range(0, num_requests, concurrent):
            batch_tasks = tasks[i:i+concurrent]
            batch_results = await asyncio.gather(*batch_tasks)
            get_all_results.extend(batch_results)
        
        # Test 3: GET individual users
        print("Test 3: GET ONE operations...")
        tasks = [get_user(session, base_url, result["data"]["id"]) for result in create_results]
        get_one_results = []
        for i in range(0, num_requests, concurrent):
            batch_tasks = tasks[i:i+concurrent]
            batch_results = await asyncio.gather(*batch_tasks)
            get_one_results.extend(batch_results)
        
        # Test 4: UPDATE users
        print("Test 4: UPDATE operations...")
        tasks = [update_user(session, base_url, result["data"]["id"]) for result in create_results]
        update_results = []
        for i in range(0, num_requests, concurrent):
            batch_tasks = tasks[i:i+concurrent]
            batch_results = await asyncio.gather(*batch_tasks)
            update_results.extend(batch_results)
        
        # Test 5: DELETE users
        print("Test 5: DELETE operations...")
        tasks = [delete_user(session, base_url, result["data"]["id"]) for result in create_results]
        delete_results = []
        for i in range(0, num_requests, concurrent):
            batch_tasks = tasks[i:i+concurrent]
            batch_results = await asyncio.gather(*batch_tasks)
            delete_results.extend(batch_results)

    # Combine all results
    all_results = {
        "CREATE": create_results,
        "GET_ALL": get_all_results,
        "GET_ONE": get_one_results,
        "UPDATE": update_results,
        "DELETE": delete_results,
    }

    # Print statistics
    print(f"\n{'='*70}")
    print(f"Results - {server_name}")
    print(f"{'='*70}\n")

    operation_stats = {}
    
    for operation, results in all_results.items():
        successful_results = [r for r in results if r["success"]]
        
        if not successful_results:
            print(f"{operation}:")
            print(f"  ❌ All requests failed!")
            print()
            continue
            
        durations = [r["duration"] * 1000 for r in successful_results]  # Convert to ms
        
        stats = {
            "total": len(results),
            "successful": len(successful_results),
            "failed": len(results) - len(successful_results),
            "mean": statistics.mean(durations),
            "median": statistics.median(durations),
            "min": min(durations),
            "max": max(durations),
            "stdev": statistics.stdev(durations) if len(durations) > 1 else 0,
            "req_per_sec": len(successful_results) / sum(durations) * 1000
        }
        
        operation_stats[operation] = stats
        
        print(f"{operation}:")
        print(f"  Total Requests:    {stats['total']}")
        print(f"  Successful:        {stats['successful']}")
        print(f"  Failed:            {stats['failed']}")
        print(f"  Mean Duration:     {stats['mean']:.2f} ms")
        print(f"  Median Duration:   {stats['median']:.2f} ms")
        print(f"  Min Duration:      {stats['min']:.2f} ms")
        print(f"  Max Duration:      {stats['max']:.2f} ms")
        print(f"  Std Deviation:     {stats['stdev']:.2f} ms")
        print(f"  Requests/sec:      {stats['req_per_sec']:.2f}")
        print()

    # Overall statistics
    all_durations = []
    for results in all_results.values():
        all_durations.extend([r["duration"] * 1000 for r in results if r["success"]])

    if all_durations:
        total_requests = sum(len(results) for results in all_results.values())
        total_successful = len(all_durations)
        total_time = sum(all_durations) / 1000  # Convert back to seconds

        print(f"{'='*70}")
        print("Overall Summary")
        print(f"{'='*70}")
        print(f"Total Requests:        {total_requests}")
        print(f"Successful Requests:   {total_successful}")
        print(f"Failed Requests:       {total_requests - total_successful}")
        print(f"Total Duration:        {sum(all_durations):.2f} ms")
        print(f"Average Duration:      {statistics.mean(all_durations):.2f} ms")
        print(f"Overall Throughput:    {total_successful / total_time:.2f} req/sec")
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
    current_id = 1
    results = []

    async def worker(session: aiohttp.ClientSession):
        nonlocal current_id
        while time.perf_counter() - start_time < duration_seconds:
            # Perform a mix of operations
            result = await create_user(session, base_url, current_id)
            results.append(result)

            user_id = result["data"]["id"]
            current_id += 1
            
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
        print(f"  {'Server':<25} {'Mean (ms)':<12} {'Median (ms)':<12} {'Req/sec':<12}")
        print(f"  {'-'*60}")
        
        best_mean = float('inf')
        best_server = None
        
        for url in URLS:
            if url in benchmark_results and operation in benchmark_results[url]:
                stats = benchmark_results[url][operation]
                server_name = SERVER_NAMES.get(url, url)
                print(f"  {server_name:<25} {stats['mean']:<12.2f} {stats['median']:<12.2f} {stats['req_per_sec']:<12.2f}")
                
                if stats['mean'] < best_mean:
                    best_mean = stats['mean']
                    best_server = server_name
        
        if best_server:
            print(f"  🏆 Winner: {best_server}")
    
    # Stress test comparison
    if stress_results:
        print(f"\n\nStress Test Comparison:")
        print(f"{'='*70}")
        print(f"  {'Server':<25} {'Req/sec':<12} {'Mean (ms)':<12} {'Success Rate':<15}")
        print(f"  {'-'*65}")
        
        best_throughput = 0
        best_server = None
        
        for url in URLS:
            if url in stress_results and stress_results[url]:
                stats = stress_results[url]
                server_name = SERVER_NAMES.get(url, url)
                success_rate = (stats['successful'] / stats['total']) * 100 if stats['total'] > 0 else 0
                print(f"  {server_name:<25} {stats['req_per_sec']:<12.2f} {stats['mean']:<12.2f} {success_rate:<15.1f}%")
                
                if stats['req_per_sec'] > best_throughput:
                    best_throughput = stats['req_per_sec']
                    best_server = server_name
        
        if best_server:
            print(f"  🏆 Winner: {best_server}")
    
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
