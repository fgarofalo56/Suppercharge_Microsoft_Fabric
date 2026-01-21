# Tutorial 03: Gold Layer

This tutorial covers implementing the Gold layer - business-ready aggregations and KPIs.

## Learning Objectives

By the end of this tutorial, you will:

1. Understand Gold layer principles
2. Create slot machine performance metrics
3. Build Player 360 view
4. Implement compliance reporting tables
5. Design for Direct Lake optimization

## Gold Layer Principles

The Gold layer provides business-ready, aggregated data:

| Principle | Description |
|-----------|-------------|
| Business-Aligned | Organized by business domain |
| Aggregated | Pre-computed KPIs and metrics |
| Optimized | Designed for query performance |
| Star Schema | Fact and dimension tables |
| Direct Lake Ready | Optimized for Power BI |

## Prerequisites

- Completed [Tutorial 02: Silver Layer](../02-silver-layer/README.md)
- Silver tables populated
- Access to `lh_gold` Lakehouse

## Step 1: Slot Performance Metrics

### Create Notebook: `01_gold_slot_performance`

```python
# Cell 1: Configuration
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from datetime import datetime

SILVER_TABLE = "lh_silver.silver_slot_cleansed"
GOLD_TABLE = "gold_slot_performance"

print(f"Source: {SILVER_TABLE}")
print(f"Target: {GOLD_TABLE}")
```

```python
# Cell 2: Read Silver Data
df_silver = spark.table(SILVER_TABLE)
print(f"Silver records: {df_silver.count():,}")
```

```python
# Cell 3: Calculate Daily Machine Performance
df_daily = df_silver \
    .filter(col("event_type") == "GAME_PLAY") \
    .groupBy(
        col("machine_id"),
        col("event_date").alias("business_date"),
        col("zone"),
        col("machine_type"),
        col("denomination"),
        col("manufacturer"),
        col("game_theme")
    ) \
    .agg(
        # Volume Metrics
        count("*").alias("total_games"),
        countDistinct("player_id").alias("unique_players"),
        countDistinct("session_id").alias("total_sessions"),

        # Financial Metrics
        sum("coin_in").alias("total_coin_in"),
        sum("coin_out").alias("total_coin_out"),
        sum("jackpot_amount").alias("total_jackpots"),

        # Performance Metrics
        avg("coin_in").alias("avg_bet"),
        max("coin_in").alias("max_bet"),
        avg("theoretical_hold").alias("avg_theoretical_hold"),

        # Time Metrics
        min("event_timestamp").alias("first_play"),
        max("event_timestamp").alias("last_play")
    )

print(f"Daily aggregations: {df_daily.count():,} rows")
```

```python
# Cell 4: Calculate KPIs
df_kpis = df_daily \
    .withColumn("net_win", col("total_coin_in") - col("total_coin_out")) \
    .withColumn("actual_hold_pct",
        when(col("total_coin_in") > 0,
             (col("total_coin_in") - col("total_coin_out")) / col("total_coin_in") * 100)
        .otherwise(0)) \
    .withColumn("theo_win", col("total_coin_in") * col("avg_theoretical_hold")) \
    .withColumn("hold_variance", col("actual_hold_pct") - (col("avg_theoretical_hold") * 100)) \
    .withColumn("avg_session_length_games",
        when(col("total_sessions") > 0, col("total_games") / col("total_sessions"))
        .otherwise(0)) \
    .withColumn("games_per_player",
        when(col("unique_players") > 0, col("total_games") / col("unique_players"))
        .otherwise(0)) \
    .withColumn("jackpot_hit_rate",
        when(col("total_games") > 0, col("total_jackpots") / col("total_games"))
        .otherwise(0))
```

```python
# Cell 5: Add Gold Metadata
df_gold = df_kpis \
    .withColumn("_gold_processed_at", current_timestamp()) \
    .withColumn("_gold_batch_id", lit(datetime.now().strftime("%Y%m%d")))

# Reorder columns for clarity
column_order = [
    # Keys
    "business_date", "machine_id", "zone", "machine_type", "denomination",
    "manufacturer", "game_theme",
    # Volume
    "total_games", "unique_players", "total_sessions",
    # Financial
    "total_coin_in", "total_coin_out", "net_win", "total_jackpots",
    # Performance KPIs
    "actual_hold_pct", "avg_theoretical_hold", "theo_win", "hold_variance",
    # Averages
    "avg_bet", "max_bet", "avg_session_length_games", "games_per_player",
    "jackpot_hit_rate",
    # Time
    "first_play", "last_play",
    # Metadata
    "_gold_processed_at", "_gold_batch_id"
]

df_gold = df_gold.select(column_order)
```

```python
# Cell 6: Write to Gold Table
df_gold.write \
    .format("delta") \
    .mode("overwrite") \
    .partitionBy("business_date") \
    .saveAsTable(GOLD_TABLE)

print(f"Wrote {df_gold.count():,} records to {GOLD_TABLE}")
```

```python
# Cell 7: Verify and Sample
df_verify = spark.table(GOLD_TABLE)

print("\nGold Table Statistics:")
print(f"  Records: {df_verify.count():,}")
print(f"  Date range: {df_verify.agg(min('business_date'), max('business_date')).first()}")

print("\nTop 10 Machines by Net Win:")
display(
    df_verify
    .groupBy("machine_id", "machine_type", "zone")
    .agg(sum("net_win").alias("total_net_win"))
    .orderBy(col("total_net_win").desc())
    .limit(10)
)
```

## Step 2: Player 360 View

### Create Notebook: `02_gold_player_360`

```python
# Cell 1: Configuration
SILVER_PLAYER = "lh_silver.silver_player_master"
SILVER_SLOTS = "lh_silver.silver_slot_cleansed"
SILVER_TABLES = "lh_silver.silver_table_enriched"
SILVER_FINANCIAL = "lh_silver.silver_financial_reconciled"
GOLD_TABLE = "gold_player_360"
```

```python
# Cell 2: Get Current Player Data
df_player = spark.table(SILVER_PLAYER) \
    .filter(col("_is_current") == True) \
    .select(
        "player_id", "loyalty_number", "loyalty_tier",
        "enrollment_date", "total_visits", "total_theo",
        "preferred_game", "vip_flag", "self_excluded", "account_status"
    )

print(f"Active players: {df_player.count():,}")
```

```python
# Cell 3: Calculate Slot Activity
df_slot_activity = spark.table(SILVER_SLOTS) \
    .filter(col("player_id").isNotNull()) \
    .groupBy("player_id") \
    .agg(
        count("*").alias("slot_games_played"),
        sum("coin_in").alias("slot_coin_in"),
        sum("coin_out").alias("slot_coin_out"),
        countDistinct("machine_id").alias("unique_machines"),
        countDistinct("event_date").alias("slot_visit_days"),
        max("event_timestamp").alias("last_slot_play")
    )
```

```python
# Cell 4: Calculate Table Activity
df_table_activity = spark.table(SILVER_TABLES) \
    .filter(col("player_id").isNotNull()) \
    .groupBy("player_id") \
    .agg(
        sum("average_bet").alias("table_total_wagered"),
        sum("theoretical_win").alias("table_theo_win"),
        sum("actual_win_loss").alias("table_actual_wl"),
        sum("hours_played").alias("table_hours_played"),
        countDistinct("event_date").alias("table_visit_days"),
        max("event_timestamp").alias("last_table_play")
    )
```

```python
# Cell 5: Calculate Financial Activity
df_financial = spark.table(SILVER_FINANCIAL) \
    .filter(col("player_id").isNotNull()) \
    .groupBy("player_id") \
    .agg(
        sum(when(col("transaction_type") == "CASH_IN", col("amount"))).alias("total_cash_in"),
        sum(when(col("transaction_type") == "CASH_OUT", col("amount"))).alias("total_cash_out"),
        sum(when(col("transaction_type") == "MARKER_ISSUE", col("amount"))).alias("total_markers"),
        count("*").alias("total_transactions")
    )
```

```python
# Cell 6: Join All Sources
df_360 = df_player \
    .join(df_slot_activity, "player_id", "left") \
    .join(df_table_activity, "player_id", "left") \
    .join(df_financial, "player_id", "left")

# Fill nulls
df_360 = df_360.fillna(0, subset=[
    "slot_games_played", "slot_coin_in", "slot_coin_out",
    "table_total_wagered", "table_theo_win", "table_actual_wl",
    "total_cash_in", "total_cash_out", "total_markers"
])
```

```python
# Cell 7: Calculate Player KPIs
df_gold = df_360 \
    .withColumn("total_gaming_activity",
        col("slot_coin_in") + col("table_total_wagered")) \
    .withColumn("total_theo_win",
        col("slot_coin_in") * 0.08 + col("table_theo_win")) \
    .withColumn("net_cash_position",
        col("total_cash_in") - col("total_cash_out")) \
    .withColumn("last_activity_date",
        greatest(col("last_slot_play"), col("last_table_play"))) \
    .withColumn("days_since_visit",
        datediff(current_date(), col("last_activity_date"))) \
    .withColumn("churn_risk",
        when(col("days_since_visit") > 90, "High")
        .when(col("days_since_visit") > 30, "Medium")
        .otherwise("Low")) \
    .withColumn("player_value_score",
        (col("total_theo_win") / 1000) +
        (col("total_visits") * 10) +
        when(col("loyalty_tier") == "Diamond", 500)
        .when(col("loyalty_tier") == "Platinum", 200)
        .when(col("loyalty_tier") == "Gold", 100)
        .when(col("loyalty_tier") == "Silver", 50)
        .otherwise(10)) \
    .withColumn("_gold_processed_at", current_timestamp())
```

```python
# Cell 8: Write Gold Table
df_gold.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable(GOLD_TABLE)

print(f"Wrote {df_gold.count():,} player 360 records")
```

```python
# Cell 9: Verify
display(
    spark.table(GOLD_TABLE)
    .select(
        "player_id", "loyalty_tier", "total_gaming_activity",
        "total_theo_win", "churn_risk", "player_value_score"
    )
    .orderBy(col("player_value_score").desc())
    .limit(20)
)
```

## Step 3: Compliance Reporting

### Create Notebook: `03_gold_compliance_reporting`

```python
# Cell 1: Configuration
SILVER_TABLE = "lh_silver.silver_compliance_validated"
GOLD_TABLE = "gold_compliance_reporting"
```

```python
# Cell 2: Read and Aggregate
df_silver = spark.table(SILVER_TABLE)

# Daily compliance summary
df_daily = df_silver \
    .withColumn("filing_date_parsed", to_date(col("filing_date"))) \
    .groupBy(
        col("filing_date_parsed").alias("report_date"),
        "report_type",
        "status"
    ) \
    .agg(
        count("*").alias("report_count"),
        sum("transaction_amount").alias("total_amount"),
        avg("transaction_amount").alias("avg_amount"),
        countDistinct("player_id").alias("unique_patrons")
    )
```

```python
# Cell 3: Pivot by Report Type
df_pivot = df_silver \
    .withColumn("report_date", to_date(col("filing_date"))) \
    .groupBy("report_date") \
    .pivot("report_type", ["CTR", "SAR", "W2G", "MTLAP", "CTRC"]) \
    .agg(
        count("*").alias("count"),
        sum("transaction_amount").alias("amount")
    )

# Flatten column names
for col_name in df_pivot.columns:
    if "_count" in col_name or "_amount" in col_name:
        new_name = col_name.lower().replace("_count", "_count").replace("_amount", "_total_amount")
        df_pivot = df_pivot.withColumnRenamed(col_name, new_name)
```

```python
# Cell 4: Add Compliance KPIs
df_gold = df_pivot \
    .withColumn("total_filings",
        coalesce(col("ctr_count"), lit(0)) +
        coalesce(col("sar_count"), lit(0)) +
        coalesce(col("w2g_count"), lit(0))) \
    .withColumn("ctr_compliance_indicator",
        when(col("ctr_count") > 0, "Filings Present").otherwise("No CTR")) \
    .withColumn("sar_alert_level",
        when(col("sar_count") > 10, "High")
        .when(col("sar_count") > 5, "Medium")
        .otherwise("Normal")) \
    .withColumn("w2g_jackpot_activity",
        when(col("w2g_total_amount") > 100000, "High")
        .when(col("w2g_total_amount") > 50000, "Medium")
        .otherwise("Normal")) \
    .withColumn("_gold_processed_at", current_timestamp())
```

```python
# Cell 5: Write Gold Table
df_gold.write \
    .format("delta") \
    .mode("overwrite") \
    .partitionBy("report_date") \
    .saveAsTable(GOLD_TABLE)

print(f"Wrote {df_gold.count():,} compliance summary records")
```

## Step 4: Create Dimension Tables

### Date Dimension

```python
# Create Date Dimension
from pyspark.sql.functions import explode, sequence, to_date

# Generate date range
start_date = "2024-01-01"
end_date = "2025-12-31"

df_dates = spark.sql(f"""
    SELECT explode(sequence(to_date('{start_date}'), to_date('{end_date}'))) as date_key
""")

df_dim_date = df_dates \
    .withColumn("year", year("date_key")) \
    .withColumn("quarter", quarter("date_key")) \
    .withColumn("month", month("date_key")) \
    .withColumn("month_name", date_format("date_key", "MMMM")) \
    .withColumn("week", weekofyear("date_key")) \
    .withColumn("day_of_week", dayofweek("date_key")) \
    .withColumn("day_name", date_format("date_key", "EEEE")) \
    .withColumn("is_weekend", dayofweek("date_key").isin([1, 7])) \
    .withColumn("fiscal_year",
        when(month("date_key") >= 10, year("date_key") + 1)
        .otherwise(year("date_key"))) \
    .withColumn("fiscal_quarter",
        when(quarter("date_key") >= 4, quarter("date_key") - 3)
        .otherwise(quarter("date_key") + 1))

df_dim_date.write.format("delta").mode("overwrite").saveAsTable("dim_date")
```

### Machine Dimension

```python
# Create Machine Dimension from Slot data
df_dim_machine = spark.table("lh_silver.silver_slot_cleansed") \
    .select(
        "machine_id", "asset_number", "location_id", "zone",
        "machine_type", "manufacturer", "game_theme", "denomination"
    ) \
    .distinct() \
    .withColumn("machine_key", monotonically_increasing_id())

df_dim_machine.write.format("delta").mode("overwrite").saveAsTable("dim_machine")
```

## Step 5: Gold Layer Verification

```python
# Gold Layer Verification
tables = [
    "gold_slot_performance",
    "gold_player_360",
    "gold_compliance_reporting",
    "gold_table_analytics",
    "gold_financial_summary",
    "dim_date",
    "dim_machine"
]

print("=" * 60)
print("GOLD LAYER VERIFICATION")
print("=" * 60)

for table in tables:
    try:
        df = spark.table(table)
        count = df.count()
        print(f"✓ {table:35} {count:>12,} records")
    except:
        print(f"✗ {table:35} NOT FOUND")

print("=" * 60)
```

## Direct Lake Optimization

For optimal Power BI Direct Lake performance:

### 1. Column Ordering
Place frequently filtered columns first:
```python
# Good: date and key columns first
df.select("business_date", "machine_id", "zone", ...)
```

### 2. Data Types
Use appropriate types for Direct Lake:
```python
df = df \
    .withColumn("metric", col("metric").cast("decimal(18,2)")) \
    .withColumn("flag", col("flag").cast("boolean"))
```

### 3. Partitioning
Partition by date for time-series data:
```python
df.write.partitionBy("business_date").saveAsTable(table)
```

### 4. Optimize Tables
Run optimization after writes:
```python
spark.sql(f"OPTIMIZE {table} ZORDER BY (machine_id)")
```

## Validation Checklist

- [ ] All Gold tables created
- [ ] KPIs calculating correctly
- [ ] Dimension tables populated
- [ ] Partitioning applied
- [ ] Direct Lake optimization done

## Next Steps

Continue to [Tutorial 04: Real-Time Analytics](../04-real-time-analytics/README.md).

## Resources

- [Gold Layer Best Practices](https://learn.microsoft.com/fabric/data-engineering/lakehouse-overview)
- [Direct Lake Mode](https://learn.microsoft.com/fabric/data-warehouse/direct-lake-mode)
- [Star Schema Design](https://learn.microsoft.com/power-bi/guidance/star-schema)
