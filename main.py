import redis
import time
import random
import matplotlib.pyplot as plt
from tabulate import tabulate
import sys


class DatabaseSimulator:
    def __init__(self, delay_range=(0.5, 2.0)):
        self.delay_range = delay_range
        self.query_count = 0
        
        self.fake_database = {
            "user:1": {"id": 1, "name": "Ali Ahmadi", "email": "ali@example.com", "age": 28},
            "user:2": {"id": 2, "name": "Sara Mohammadi", "email": "sara@example.com", "age": 24},
            "user:3": {"id": 3, "name": "Reza Karimi", "email": "reza@example.com", "age": 31},
            "user:4": {"id": 4, "name": "Mina Hosseini", "email": "mina@example.com", "age": 26},
            "user:5": {"id": 5, "name": "Hossein Rezaei", "email": "hossein@example.com", "age": 35},
            "product:1": {"id": 1, "name": "Laptop", "price": 25000000, "stock": 15},
            "product:2": {"id": 2, "name": "Mouse", "price": 500000, "stock": 120},
            "product:3": {"id": 3, "name": "Keyboard", "price": 1200000, "stock": 80},
            "product:4": {"id": 4, "name": "Monitor", "price": 8000000, "stock": 25},
            "product:5": {"id": 5, "name": "Headphone", "price": 1500000, "stock": 60},
        }
    
    def query(self, key):
        self.query_count += 1
        delay = random.uniform(*self.delay_range)
        time.sleep(delay)
        
        return self.fake_database.get(key, None)


class CacheManager:
    def __init__(self, redis_host='localhost', redis_port=6379, ttl=60):
        try:
            self.redis_client = redis.Redis(
                host=redis_host,
                port=redis_port,
                decode_responses=True,
                socket_connect_timeout=5
            )
            self.redis_client.ping()
            self.enabled = True
            self.ttl = ttl
            self.hit_count = 0
            self.miss_count = 0
        except (redis.ConnectionError, redis.TimeoutError):
            print("Warning: Redis is not available. Running without cache.")
            self.enabled = False
    
    def get(self, key):
        if not self.enabled:
            return None
        
        try:
            value = self.redis_client.get(key)
            if value:
                self.hit_count += 1
                return eval(value)
            else:
                self.miss_count += 1
                return None
        except Exception as e:
            print(f"Cache get error: {e}")
            return None
    
    def set(self, key, value, ttl=None):
        if not self.enabled:
            return False
        
        try:
            ttl = ttl or self.ttl
            self.redis_client.setex(key, ttl, str(value))
            return True
        except Exception as e:
            print(f"Cache set error: {e}")
            return False
    
    def clear(self):
        if self.enabled:
            try:
                self.redis_client.flushdb()
            except Exception as e:
                print(f"Cache clear error: {e}")
    
    def get_stats(self):
        total = self.hit_count + self.miss_count
        hit_rate = (self.hit_count / total * 100) if total > 0 else 0
        return {
            "hits": self.hit_count,
            "misses": self.miss_count,
            "hit_rate": hit_rate
        }


class DistributedCacheDemo:
    def __init__(self):
        self.db = DatabaseSimulator(delay_range=(0.8, 1.5))
        self.cache = CacheManager()
    
    def fetch_without_cache(self, key):
        start = time.time()
        data = self.db.query(key)
        elapsed = time.time() - start
        return data, elapsed
    
    def fetch_with_cache(self, key):
        start = time.time()
        
        cached_data = self.cache.get(key)
        if cached_data:
            elapsed = time.time() - start
            return cached_data, elapsed, True
        
        data = self.db.query(key)
        self.cache.set(key, data)
        elapsed = time.time() - start
        return data, elapsed, False
    
    def run_benchmark(self, keys, iterations=3):
        print("\n" + "="*70)
        print("BENCHMARK: WITHOUT CACHE")
        print("="*70)
        
        results_no_cache = []
        for iteration in range(iterations):
            print(f"\nIteration {iteration + 1}/{iterations}")
            for key in keys:
                data, elapsed = self.fetch_without_cache(key)
                results_no_cache.append(elapsed)
                print(f"  {key}: {elapsed:.4f}s")
        
        self.cache.clear()
        
        print("\n" + "="*70)
        print("BENCHMARK: WITH REDIS CACHE")
        print("="*70)
        
        results_with_cache = []
        cache_hits = 0
        for iteration in range(iterations):
            print(f"\nIteration {iteration + 1}/{iterations}")
            for key in keys:
                data, elapsed, from_cache = self.fetch_with_cache(key)
                results_with_cache.append(elapsed)
                status = "(CACHE HIT)" if from_cache else "(DB QUERY)"
                print(f"  {key}: {elapsed:.4f}s {status}")
                if from_cache:
                    cache_hits += 1
        
        return results_no_cache, results_with_cache, cache_hits
    
    def visualize_results(self, results_no_cache, results_with_cache, keys, iterations):
        avg_no_cache = sum(results_no_cache) / len(results_no_cache)
        avg_with_cache = sum(results_with_cache) / len(results_with_cache)
        
        improvement = ((avg_no_cache - avg_with_cache) / avg_no_cache) * 100
        
        print("\n" + "="*70)
        print("RESULTS SUMMARY")
        print("="*70)
        
        table_data = [
            ["Without Cache", f"{avg_no_cache:.4f}s", "-"],
            ["With Redis Cache", f"{avg_with_cache:.4f}s", f"{improvement:.2f}%"]
        ]
        print(tabulate(table_data, headers=["Mode", "Avg Response Time", "Improvement"], tablefmt="grid"))
        
        if self.cache.enabled:
            stats = self.cache.get_stats()
            print(f"\nCache Statistics:")
            print(f"  - Hits: {stats['hits']}")
            print(f"  - Misses: {stats['misses']}")
            print(f"  - Hit Rate: {stats['hit_rate']:.2f}%")
        
        print(f"\nDatabase Queries: {self.db.query_count}")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        iterations_list = list(range(1, len(results_no_cache) + 1))
        ax1.plot(iterations_list, results_no_cache, 'o-', color='red', label='Without Cache', linewidth=2)
        ax1.plot(iterations_list, results_with_cache, 's-', color='green', label='With Redis Cache', linewidth=2)
        ax1.set_xlabel('Request Number')
        ax1.set_ylabel('Response Time (seconds)')
        ax1.set_title('Response Time Comparison: Request by Request')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        categories = ['Without Cache', 'With Redis Cache']
        averages = [avg_no_cache, avg_with_cache]
        colors = ['#FF6B6B', '#51CF66']
        bars = ax2.bar(categories, averages, color=colors, alpha=0.8)
        ax2.set_ylabel('Average Response Time (seconds)')
        ax2.set_title('Average Response Time Comparison')
        ax2.grid(True, alpha=0.3, axis='y')
        
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.4f}s',
                    ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('benchmark_results.png', dpi=300)
        print("\n✓ Chart saved as 'benchmark_results.png'")
        plt.show()


def main():
    print("\n" + "="*70)
    print("DISTRIBUTED CACHING WITH REDIS - DEMONSTRATION")
    print("="*70)
    print("\nMake sure Redis server is running on localhost:6379")
    print("Start Redis with: redis-server")
    
    input("\nPress Enter to start the benchmark...")
    
    demo = DistributedCacheDemo()
    
    if not demo.cache.enabled:
        print("\n⚠ WARNING: Redis is not available!")
        print("This demo will run WITHOUT cache to show the difference.")
        print("To see the full benefit, please start Redis and run again.\n")
    
    test_keys = ["user:1", "user:2", "product:1", "product:2", "user:3"]
    iterations = 3
    
    results_no_cache, results_with_cache, cache_hits = demo.run_benchmark(test_keys, iterations)
    
    demo.visualize_results(results_no_cache, results_with_cache, test_keys, iterations)
    
    print("\n" + "="*70)
    print("BENCHMARK COMPLETED")
    print("="*70)


if __name__ == "__main__":
    main()
