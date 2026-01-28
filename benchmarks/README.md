# Performance Benchmarks

> **Home > Benchmarks**

---

## Overview

This directory contains performance benchmarks, baseline metrics, and load testing scripts for the Casino Analytics platform. Use these benchmarks to validate performance, plan capacity, and identify optimization opportunities.

---

## Benchmark Categories

| Category | Description | Target |
|----------|-------------|--------|
| **Query Performance** | Lakehouse query latency | < 5 seconds (P95) |
| **Ingestion Throughput** | Bronze layer ingestion rate | > 100K records/min |
| **Real-Time Latency** | End-to-end streaming | < 30 seconds |
| **Report Load Time** | Power BI report rendering | < 3 seconds |
| **Refresh Duration** | Semantic model refresh | < 15 minutes |

---

## Baseline Metrics (F64 Capacity)

### Query Performance Baselines

| Query Type | Data Volume | P50 | P95 | P99 |
|------------|-------------|-----|-----|-----|
| Simple aggregation | 1M rows | 0.5s | 1.2s | 2.0s |
| Complex join | 10M rows | 2.1s | 4.5s | 6.8s |
| Window function | 50M rows | 5.2s | 12.0s | 18.5s |
| Full table scan | 100M rows | 8.5s | 15.0s | 22.0s |

### Ingestion Throughput Baselines

| Source | Format | Records/Min | MB/Min |
|--------|--------|-------------|--------|
| Event Hub | JSON | 500K | 250 |
| ADLS Files | Parquet | 2M | 500 |
| ADLS Files | CSV | 800K | 400 |
| SQL Server | JDBC | 300K | 150 |

### Real-Time Pipeline Latency

| Stage | Latency |
|-------|---------|
| Event Hub → Eventstream | 2-5s |
| Eventstream → Eventhouse | 5-10s |
| Eventhouse → KQL Query | 1-3s |
| KQL Query → Dashboard | 2-5s |
| **Total End-to-End** | **10-23s** |

---

## Benchmark Scripts

### Query Performance Benchmark

```python
# benchmarks/query_benchmark.py

from pyspark.sql import SparkSession
from datetime import datetime
import time
import statistics

def benchmark_query(spark, query_name: str, query: str, iterations: int = 10):
    """
    Benchmark a query and collect timing statistics.
    """
    times = []

    # Warm-up run
    spark.sql(query).collect()

    # Benchmark runs
    for i in range(iterations):
        start = time.time()
        spark.sql(query).collect()
        elapsed = time.time() - start
        times.append(elapsed)
        print(f"  Run {i+1}: {elapsed:.3f}s")

    # Calculate statistics
    return {
        "query": query_name,
        "iterations": iterations,
        "min": min(times),
        "max": max(times),
        "mean": statistics.mean(times),
        "median": statistics.median(times),
        "p95": sorted(times)[int(iterations * 0.95)],
        "stdev": statistics.stdev(times) if iterations > 1 else 0
    }


def run_benchmark_suite():
    """Run complete benchmark suite."""

    spark = SparkSession.builder.getOrCreate()

    benchmarks = [
        ("Simple Count", """
            SELECT COUNT(*) FROM silver_slot_telemetry
        """),
        ("Daily Aggregation", """
            SELECT
                DATE(event_timestamp) as play_date,
                SUM(bet_amount) as total_coin_in,
                SUM(win_amount) as total_coin_out,
                COUNT(*) as spin_count
            FROM silver_slot_telemetry
            WHERE event_type = 'SPIN'
            GROUP BY DATE(event_timestamp)
        """),
        ("Machine Performance", """
            SELECT
                machine_id,
                casino_id,
                SUM(bet_amount) as coin_in,
                SUM(win_amount) as coin_out,
                (SUM(bet_amount) - SUM(win_amount)) / SUM(bet_amount) * 100 as hold_pct
            FROM silver_slot_telemetry
            WHERE event_type = 'SPIN'
            GROUP BY machine_id, casino_id
            ORDER BY coin_in DESC
            LIMIT 100
        """),
        ("Player Join", """
            SELECT
                p.loyalty_tier,
                COUNT(DISTINCT s.player_id) as player_count,
                SUM(s.bet_amount) as total_wagered
            FROM silver_slot_telemetry s
            JOIN dim_player p ON s.player_id = p.player_id
            WHERE p.is_current = TRUE
            GROUP BY p.loyalty_tier
        """),
        ("Time Window Analysis", """
            SELECT
                machine_id,
                DATE(event_timestamp) as play_date,
                SUM(bet_amount) as daily_coin_in,
                SUM(SUM(bet_amount)) OVER (
                    PARTITION BY machine_id
                    ORDER BY DATE(event_timestamp)
                    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
                ) as rolling_7day
            FROM silver_slot_telemetry
            WHERE event_type = 'SPIN'
            GROUP BY machine_id, DATE(event_timestamp)
        """)
    ]

    results = []
    print("=" * 60)
    print("QUERY BENCHMARK SUITE")
    print("=" * 60)

    for name, query in benchmarks:
        print(f"\nBenchmarking: {name}")
        result = benchmark_query(spark, name, query)
        results.append(result)
        print(f"  Mean: {result['mean']:.3f}s | P95: {result['p95']:.3f}s")

    # Save results
    results_df = spark.createDataFrame(results)
    results_df.write.format("delta").mode("overwrite").saveAsTable("benchmark_results")

    print("\n" + "=" * 60)
    print("BENCHMARK COMPLETE")
    print("=" * 60)

    return results
```

### Ingestion Throughput Benchmark

```python
# benchmarks/ingestion_benchmark.py

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from datetime import datetime
import time

def benchmark_ingestion(
    spark,
    source_path: str,
    target_table: str,
    batch_sizes: list = [10000, 50000, 100000, 500000]
):
    """
    Benchmark ingestion throughput at different batch sizes.
    """
    results = []

    for batch_size in batch_sizes:
        print(f"\nTesting batch size: {batch_size:,}")

        # Read source data
        df = spark.read.parquet(source_path).limit(batch_size)
        record_count = df.count()
        df.cache()
        df.count()  # Materialize cache

        # Time the write
        start = time.time()
        df.write \
            .format("delta") \
            .mode("append") \
            .saveAsTable(f"{target_table}_benchmark")
        elapsed = time.time() - start

        # Calculate throughput
        records_per_second = record_count / elapsed
        records_per_minute = records_per_second * 60

        result = {
            "batch_size": batch_size,
            "actual_records": record_count,
            "elapsed_seconds": elapsed,
            "records_per_second": records_per_second,
            "records_per_minute": records_per_minute
        }
        results.append(result)

        print(f"  Records: {record_count:,}")
        print(f"  Time: {elapsed:.2f}s")
        print(f"  Throughput: {records_per_minute:,.0f} records/min")

        # Cleanup
        df.unpersist()
        spark.sql(f"DROP TABLE IF EXISTS {target_table}_benchmark")

    return results
```

### Load Testing Script

```python
# benchmarks/load_test.py

import concurrent.futures
from datetime import datetime
import time

def simulate_user_query(spark, user_id: int, query: str):
    """Simulate a user running a query."""
    start = time.time()
    result = spark.sql(query).collect()
    elapsed = time.time() - start
    return {
        "user_id": user_id,
        "elapsed": elapsed,
        "row_count": len(result),
        "timestamp": datetime.now().isoformat()
    }


def run_load_test(
    spark,
    concurrent_users: int = 10,
    queries_per_user: int = 5,
    query: str = None
):
    """
    Run concurrent load test.

    Args:
        concurrent_users: Number of simultaneous users
        queries_per_user: Queries each user runs
        query: Query to execute
    """
    if query is None:
        query = """
            SELECT
                machine_id,
                SUM(bet_amount) as coin_in,
                COUNT(*) as spins
            FROM silver_slot_telemetry
            WHERE event_type = 'SPIN'
            GROUP BY machine_id
            LIMIT 100
        """

    print(f"Starting load test:")
    print(f"  Concurrent users: {concurrent_users}")
    print(f"  Queries per user: {queries_per_user}")

    results = []
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_users) as executor:
        futures = []
        for user_id in range(concurrent_users):
            for query_num in range(queries_per_user):
                future = executor.submit(simulate_user_query, spark, user_id, query)
                futures.append(future)

        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    total_time = time.time() - start_time
    total_queries = len(results)

    # Calculate metrics
    latencies = [r["elapsed"] for r in results]

    print(f"\nLoad Test Results:")
    print(f"  Total queries: {total_queries}")
    print(f"  Total time: {total_time:.2f}s")
    print(f"  Queries/second: {total_queries/total_time:.2f}")
    print(f"  Avg latency: {statistics.mean(latencies):.3f}s")
    print(f"  P95 latency: {sorted(latencies)[int(len(latencies)*0.95)]:.3f}s")
    print(f"  Max latency: {max(latencies):.3f}s")

    return {
        "concurrent_users": concurrent_users,
        "total_queries": total_queries,
        "total_time": total_time,
        "qps": total_queries / total_time,
        "avg_latency": statistics.mean(latencies),
        "p95_latency": sorted(latencies)[int(len(latencies)*0.95)],
        "max_latency": max(latencies)
    }
```

---

## Capacity Planning Calculator

### Estimating Required Capacity

| Workload Profile | F2 | F4 | F8 | F16 | F32 | F64 | F128 |
|-----------------|----|----|----|----|-----|-----|------|
| Small (< 10 users) | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Medium (10-50 users) | No | Yes | Yes | Yes | Yes | Yes | Yes |
| Large (50-200 users) | No | No | No | Yes | Yes | Yes | Yes |
| Enterprise (200+ users) | No | No | No | No | Yes | Yes | Yes |

### Daily Data Volume Guidelines

| Daily Volume | Minimum SKU | Recommended SKU |
|--------------|-------------|-----------------|
| < 1 GB | F2 | F4 |
| 1-10 GB | F4 | F8 |
| 10-50 GB | F8 | F16 |
| 50-200 GB | F16 | F32 |
| 200-500 GB | F32 | F64 |
| > 500 GB | F64 | F128 |

---

## Performance Optimization Checklist

### Query Optimization
- [ ] Use partitioning on frequently filtered columns
- [ ] Apply Z-ordering on join columns
- [ ] Limit SELECT columns (avoid SELECT *)
- [ ] Use predicate pushdown where possible
- [ ] Cache frequently accessed data
- [ ] Optimize join order (small table first)

### Table Optimization
- [ ] Run OPTIMIZE regularly (weekly)
- [ ] Configure appropriate file sizes (128MB-256MB)
- [ ] Use V-Order for analytical queries
- [ ] Set appropriate retention policies
- [ ] Partition by date for time-series data

### Semantic Model Optimization
- [ ] Use Direct Lake mode
- [ ] Minimize calculated columns
- [ ] Use incremental refresh
- [ ] Aggregate tables for large datasets
- [ ] Optimize DAX measures

---

## Running Benchmarks

```bash
# From Fabric Notebook

# 1. Query Performance
%run "./query_benchmark.py"
results = run_benchmark_suite()

# 2. Ingestion Throughput
%run "./ingestion_benchmark.py"
ingestion_results = benchmark_ingestion(
    spark,
    source_path="/lakehouse/default/Files/raw/slot_telemetry/",
    target_table="bronze_benchmark"
)

# 3. Load Test
%run "./load_test.py"
load_results = run_load_test(
    spark,
    concurrent_users=20,
    queries_per_user=10
)
```

---

[Back to Documentation](../docs/README.md)
