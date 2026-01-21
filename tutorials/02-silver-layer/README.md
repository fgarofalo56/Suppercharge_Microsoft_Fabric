# Tutorial 02: Silver Layer

This tutorial covers implementing the Silver layer - data cleansing, validation, and transformation.

## Learning Objectives

By the end of this tutorial, you will:

1. Understand Silver layer principles
2. Implement data quality checks
3. Apply SCD Type 2 for player master
4. Perform deduplication
5. Enforce schemas with Delta Lake

## Silver Layer Principles

The Silver layer transforms raw data into validated, cleansed datasets:

| Principle | Description |
|-----------|-------------|
| Cleansed | Remove/fix invalid data |
| Validated | Apply business rules |
| Deduplicated | Remove duplicate records |
| Conformed | Standardize formats |
| Enriched | Add derived columns |

## Prerequisites

- Completed [Tutorial 01: Bronze Layer](../01-bronze-layer/README.md)
- Bronze tables populated with data
- Access to `lh_silver` Lakehouse

## Step 1: Slot Machine Data Cleansing

### Create Notebook: `01_silver_slot_cleansed`

```python
# Cell 1: Configuration
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from delta.tables import DeltaTable

# Configuration
BRONZE_TABLE = "lh_bronze.bronze_slot_telemetry"
SILVER_TABLE = "silver_slot_cleansed"

print(f"Source: {BRONZE_TABLE}")
print(f"Target: {SILVER_TABLE}")
```

```python
# Cell 2: Read Bronze Data
df_bronze = spark.table(BRONZE_TABLE)

print(f"Bronze records: {df_bronze.count():,}")
df_bronze.printSchema()
```

```python
# Cell 3: Data Quality Checks
# Define quality rules

# Rule 1: event_id not null and unique
null_event_ids = df_bronze.filter(col("event_id").isNull()).count()
print(f"Null event_ids: {null_event_ids}")

# Rule 2: Valid event types
valid_events = [
    "GAME_PLAY", "JACKPOT", "METER_UPDATE", "DOOR_OPEN", "DOOR_CLOSE",
    "BILL_ACCEPTED", "TICKET_PRINTED", "HAND_PAY", "TILT", "POWER_OFF", "POWER_ON"
]
invalid_events = df_bronze.filter(~col("event_type").isin(valid_events)).count()
print(f"Invalid event types: {invalid_events}")

# Rule 3: coin_in >= 0 when present
negative_coin_in = df_bronze.filter(col("coin_in") < 0).count()
print(f"Negative coin_in: {negative_coin_in}")

# Rule 4: event_timestamp within expected range
future_events = df_bronze.filter(col("event_timestamp") > current_timestamp()).count()
print(f"Future timestamps: {future_events}")
```

```python
# Cell 4: Apply Cleansing Transformations
df_cleansed = df_bronze \
    .filter(col("event_id").isNotNull()) \
    .filter(col("event_type").isin(valid_events)) \
    .filter(col("event_timestamp") <= current_timestamp()) \
    .withColumn("coin_in", when(col("coin_in") < 0, 0).otherwise(col("coin_in"))) \
    .withColumn("coin_out", when(col("coin_out") < 0, 0).otherwise(col("coin_out"))) \
    .withColumn("denomination",
        when(col("denomination").isNull(), 0.01).otherwise(col("denomination")))

print(f"After cleansing: {df_cleansed.count():,} records")
```

```python
# Cell 5: Deduplication
# Remove duplicates based on event_id (keep latest ingestion)
from pyspark.sql.window import Window

window_spec = Window.partitionBy("event_id").orderBy(col("_bronze_ingested_at").desc())

df_deduped = df_cleansed \
    .withColumn("row_num", row_number().over(window_spec)) \
    .filter(col("row_num") == 1) \
    .drop("row_num")

removed = df_cleansed.count() - df_deduped.count()
print(f"Duplicates removed: {removed:,}")
```

```python
# Cell 6: Add Silver Metadata & Derived Columns
df_silver = df_deduped \
    .withColumn("_silver_processed_at", current_timestamp()) \
    .withColumn("_silver_batch_id", lit(datetime.now().strftime("%Y%m%d_%H%M%S"))) \
    .withColumn("event_date", to_date(col("event_timestamp"))) \
    .withColumn("event_hour", hour(col("event_timestamp"))) \
    .withColumn("net_win", col("coin_in") - col("coin_out")) \
    .withColumn("hold_percentage",
        when(col("coin_in") > 0, (col("coin_in") - col("coin_out")) / col("coin_in"))
        .otherwise(0))
```

```python
# Cell 7: Write to Silver Table
df_silver.write \
    .format("delta") \
    .mode("overwrite") \
    .partitionBy("event_date") \
    .saveAsTable(SILVER_TABLE)

print(f"Wrote {df_silver.count():,} records to {SILVER_TABLE}")
```

```python
# Cell 8: Verify
df_verify = spark.table(SILVER_TABLE)
print(f"\nSilver Table Statistics:")
print(f"  Records: {df_verify.count():,}")
print(f"  Partitions: {df_verify.select('event_date').distinct().count()}")

# Quality metrics
print(f"\nData Quality Summary:")
print(f"  Null event_ids: {df_verify.filter(col('event_id').isNull()).count()}")
print(f"  Negative coin_in: {df_verify.filter(col('coin_in') < 0).count()}")
```

## Step 2: Player Master with SCD Type 2

### Create Notebook: `02_silver_player_master`

SCD Type 2 maintains history of changes to player records.

```python
# Cell 1: Configuration
BRONZE_TABLE = "lh_bronze.bronze_player_profile"
SILVER_TABLE = "silver_player_master"

# SCD Type 2 columns
BUSINESS_KEY = "player_id"
TRACKED_COLUMNS = [
    "loyalty_tier", "points_balance", "tier_credits",
    "communication_preference", "marketing_opt_in", "account_status"
]
```

```python
# Cell 2: Read Bronze Data
df_bronze = spark.table(BRONZE_TABLE)
print(f"Bronze records: {df_bronze.count():,}")
```

```python
# Cell 3: Prepare Source Data
# Add hash of tracked columns for change detection
df_source = df_bronze \
    .withColumn("_record_hash",
        sha2(concat_ws("|", *[coalesce(col(c).cast("string"), lit("")) for c in TRACKED_COLUMNS]), 256)) \
    .withColumn("_effective_from", current_timestamp()) \
    .withColumn("_effective_to", lit(None).cast("timestamp")) \
    .withColumn("_is_current", lit(True)) \
    .withColumn("_silver_processed_at", current_timestamp())
```

```python
# Cell 4: Check if Silver table exists
table_exists = spark.catalog.tableExists(SILVER_TABLE)
print(f"Silver table exists: {table_exists}")
```

```python
# Cell 5: Initial Load or Merge
if not table_exists:
    # Initial load
    df_source.write \
        .format("delta") \
        .mode("overwrite") \
        .saveAsTable(SILVER_TABLE)
    print(f"Initial load: {df_source.count():,} records")
else:
    # SCD Type 2 Merge
    delta_table = DeltaTable.forName(spark, SILVER_TABLE)

    # Merge logic
    delta_table.alias("target").merge(
        df_source.alias("source"),
        f"target.{BUSINESS_KEY} = source.{BUSINESS_KEY} AND target._is_current = true"
    ).whenMatchedUpdate(
        condition="target._record_hash != source._record_hash",
        set={
            "_effective_to": "source._effective_from",
            "_is_current": "false"
        }
    ).whenNotMatchedInsertAll().execute()

    # Insert new versions for changed records
    # (This is a simplified SCD2 - production would use staging table)
    print("SCD Type 2 merge completed")
```

```python
# Cell 6: Verify SCD History
df_history = spark.table(SILVER_TABLE)

print(f"\nPlayer Master Statistics:")
print(f"  Total records: {df_history.count():,}")
print(f"  Current records: {df_history.filter(col('_is_current')).count():,}")
print(f"  Historical records: {df_history.filter(~col('_is_current')).count():,}")

# Show sample with history
display(
    df_history
    .filter(col("player_id") == df_history.select("player_id").first()[0])
    .select("player_id", "loyalty_tier", "_effective_from", "_effective_to", "_is_current")
)
```

## Step 3: Financial Transaction Reconciliation

### Create Notebook: `03_silver_financial_reconciled`

```python
# Cell 1: Configuration
BRONZE_TABLE = "lh_bronze.bronze_financial_txn"
SILVER_TABLE = "silver_financial_reconciled"
```

```python
# Cell 2: Read and Cleanse
df_bronze = spark.table(BRONZE_TABLE)

df_cleansed = df_bronze \
    .filter(col("transaction_id").isNotNull()) \
    .filter(col("amount") > 0) \
    .filter(col("transaction_timestamp").isNotNull())

print(f"Bronze: {df_bronze.count():,}, After cleansing: {df_cleansed.count():,}")
```

```python
# Cell 3: Validate CTR Threshold
df_validated = df_cleansed \
    .withColumn("ctr_threshold_check",
        when((col("amount") >= 10000) & (~col("ctr_required")), "FAIL")
        .otherwise("PASS")) \
    .withColumn("amount_validated", col("amount") > 0)

# Log validation failures
failures = df_validated.filter(col("ctr_threshold_check") == "FAIL").count()
print(f"CTR validation failures: {failures}")
```

```python
# Cell 4: Add Reconciliation Columns
df_silver = df_validated \
    .withColumn("_silver_processed_at", current_timestamp()) \
    .withColumn("transaction_date", to_date(col("transaction_timestamp"))) \
    .withColumn("is_cash_transaction",
        col("transaction_type").isin(["CASH_IN", "CASH_OUT", "CHIP_PURCHASE", "CHIP_REDEMPTION"])) \
    .withColumn("is_reportable", col("amount") >= 10000) \
    .withColumn("needs_review",
        (col("suspicious_activity_flag")) |
        (col("amount").between(8000, 9999)))
```

```python
# Cell 5: Write Silver Table
df_silver.write \
    .format("delta") \
    .mode("overwrite") \
    .partitionBy("transaction_date") \
    .saveAsTable(SILVER_TABLE)

print(f"Wrote {df_silver.count():,} records to {SILVER_TABLE}")
```

## Step 4: Remaining Silver Tables

Create similar notebooks for:
- `04_silver_table_enriched` - Table games with dealer/game joins
- `05_silver_security_enriched` - Security with event correlation
- `06_silver_compliance_validated` - Compliance with threshold validation

## Step 5: Silver Layer Verification

### Create Notebook: `99_silver_verification`

```python
# Silver Layer Verification
tables = [
    "silver_slot_cleansed",
    "silver_player_master",
    "silver_financial_reconciled",
    "silver_table_enriched",
    "silver_security_enriched",
    "silver_compliance_validated"
]

print("=" * 60)
print("SILVER LAYER VERIFICATION")
print("=" * 60)

for table in tables:
    try:
        df = spark.table(table)
        count = df.count()

        # Check for required columns
        has_processed = "_silver_processed_at" in df.columns
        status = "✓" if has_processed else "⚠"

        print(f"{status} {table:35} {count:>12,} records")
    except Exception as e:
        print(f"✗ {table:35} NOT FOUND")

print("=" * 60)
```

## Data Quality Framework

### Define Quality Rules

```python
# quality_rules.py
QUALITY_RULES = {
    "slot_telemetry": {
        "completeness": ["event_id", "machine_id", "event_type"],
        "validity": {
            "coin_in": "value >= 0",
            "coin_out": "value >= 0",
            "denomination": "value in [0.01, 0.05, 0.25, 0.50, 1.00, 5.00, 25.00, 100.00]"
        },
        "uniqueness": ["event_id"],
        "timeliness": "event_timestamp <= current_timestamp"
    },
    "player_profile": {
        "completeness": ["player_id", "loyalty_number"],
        "validity": {
            "loyalty_tier": "value in ['Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond']",
            "points_balance": "value >= 0"
        },
        "uniqueness": ["player_id"],
    },
    "financial_txn": {
        "completeness": ["transaction_id", "amount", "transaction_type"],
        "validity": {
            "amount": "value > 0",
            "ctr_required": "if amount >= 10000 then ctr_required = true"
        },
        "uniqueness": ["transaction_id"],
    }
}
```

## Validation Checklist

Before proceeding to Gold layer:

- [ ] All 6 Silver tables created
- [ ] Data quality checks passing
- [ ] Deduplication applied
- [ ] SCD Type 2 working for player master
- [ ] Silver metadata columns present

## Best Practices

### Incremental Processing

```python
# Get watermark from last run
last_processed = spark.sql(f"""
    SELECT MAX(_bronze_ingested_at) as watermark
    FROM {SILVER_TABLE}
""").first()["watermark"]

# Process only new records
df_incremental = df_bronze.filter(
    col("_bronze_ingested_at") > last_processed
)
```

### Data Quality Logging

```python
# Log quality metrics to monitoring table
quality_metrics = {
    "table_name": SILVER_TABLE,
    "processed_at": datetime.now(),
    "records_processed": df_silver.count(),
    "records_failed": failures,
    "quality_score": (df_silver.count() - failures) / df_silver.count()
}

spark.createDataFrame([quality_metrics]).write \
    .mode("append") \
    .saveAsTable("data_quality_log")
```

## Troubleshooting

### Schema Mismatch

If schemas don't match between Bronze and Silver:
```python
# Compare schemas
bronze_cols = set(df_bronze.columns)
silver_cols = set(spark.table(SILVER_TABLE).columns)
print(f"New columns: {bronze_cols - silver_cols}")
print(f"Removed columns: {silver_cols - bronze_cols}")
```

### SCD Type 2 Issues

If history not tracking:
- Verify `_record_hash` is changing
- Check merge condition on `_is_current`
- Ensure business key matches correctly

## Next Steps

Continue to [Tutorial 03: Gold Layer](../03-gold-layer/README.md) for aggregations and KPIs.

## Resources

- [Delta Lake Merge](https://docs.delta.io/latest/delta-update.html)
- [SCD Type 2 Patterns](https://learn.microsoft.com/fabric/data-engineering/tutorial-lakehouse-data-engineering)
- [Data Quality in Fabric](https://learn.microsoft.com/fabric/data-engineering/lakehouse-overview)
