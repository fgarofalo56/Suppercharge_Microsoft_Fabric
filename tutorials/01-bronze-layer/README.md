# Tutorial 01: Bronze Layer

This tutorial covers implementing the Bronze layer of the medallion architecture - raw data ingestion with minimal transformation.

## Learning Objectives

By the end of this tutorial, you will:

1. Understand Bronze layer principles
2. Ingest slot machine telemetry data
3. Ingest player profile data
4. Ingest financial transaction data
5. Implement metadata tracking columns
6. Configure Delta Lake tables

## Bronze Layer Principles

The Bronze layer is the foundation of the medallion architecture:

| Principle | Description |
|-----------|-------------|
| Raw Data | Store data as-is from source systems |
| Append-Only | Never update or delete; always append |
| Full Fidelity | Preserve all source fields |
| Metadata | Track ingestion time, source, batch |
| Schema-on-Read | Minimal schema enforcement |

## Prerequisites

- Completed [Tutorial 00: Environment Setup](../00-environment-setup/README.md)
- Generated sample data (see [Data Generation](../../data-generation/README.md))
- Access to `lh_bronze` Lakehouse

## Step 1: Upload Sample Data

### Option A: Upload via Fabric UI

1. Generate sample data locally:
   ```bash
   cd data-generation
   python generate.py --all --days 30 --output ./output
   ```

2. In Fabric, open `lh_bronze`
3. In **Files** section, click **Upload** > **Upload folder**
4. Upload the `output` folder

### Option B: Use Shortcut to ADLS

If you configured ADLS shortcut in Tutorial 00:
1. Copy generated files to your ADLS landing zone
2. Files will be accessible via the shortcut

## Step 2: Slot Machine Telemetry Ingestion

### Create the Notebook

1. In `lh_bronze`, click **Open notebook** > **New notebook**
2. Name it: `01_bronze_slot_telemetry`

### Notebook Code

```python
# Cell 1: Configuration
# =====================
# Bronze Layer - Slot Machine Telemetry Ingestion

from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, lit, input_file_name
from pyspark.sql.types import *
from datetime import datetime

# Configuration
SOURCE_PATH = "Files/output/bronze_slot_telemetry.parquet"
TARGET_TABLE = "bronze_slot_telemetry"
BATCH_ID = datetime.now().strftime("%Y%m%d_%H%M%S")
```

```python
# Cell 2: Read Source Data
# ========================

# Read parquet file
df_raw = spark.read.parquet(SOURCE_PATH)

print(f"Source records: {df_raw.count():,}")
print(f"Source columns: {len(df_raw.columns)}")
df_raw.printSchema()
```

```python
# Cell 3: Add Metadata Columns
# ============================

# Add Bronze layer metadata
df_bronze = df_raw \
    .withColumn("_bronze_ingested_at", current_timestamp()) \
    .withColumn("_bronze_source_file", input_file_name()) \
    .withColumn("_bronze_batch_id", lit(BATCH_ID))

print("Added metadata columns:")
print(f"  - _bronze_ingested_at")
print(f"  - _bronze_source_file")
print(f"  - _bronze_batch_id: {BATCH_ID}")
```

```python
# Cell 4: Write to Delta Table
# ============================

# Write to Bronze Delta table
df_bronze.write \
    .format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .saveAsTable(TARGET_TABLE)

print(f"Successfully wrote {df_bronze.count():,} records to {TARGET_TABLE}")
```

```python
# Cell 5: Verify Ingestion
# ========================

# Read back and verify
df_verify = spark.table(TARGET_TABLE)

print(f"\nTable Statistics:")
print(f"  Total records: {df_verify.count():,}")
print(f"  Columns: {len(df_verify.columns)}")

# Show sample
print(f"\nSample records:")
df_verify.select(
    "event_id", "machine_id", "event_type",
    "event_timestamp", "_bronze_ingested_at"
).show(5, truncate=False)
```

```python
# Cell 6: Table Metadata
# ======================

# Display Delta table history
from delta.tables import DeltaTable

delta_table = DeltaTable.forName(spark, TARGET_TABLE)
print("Table History:")
delta_table.history(5).select("version", "timestamp", "operation", "operationMetrics").show(truncate=False)
```

### Run the Notebook

1. Click **Run all** to execute all cells
2. Verify the table appears in the **Tables** section of `lh_bronze`
3. Check the row count matches expected

## Step 3: Player Profile Ingestion

### Create Notebook

Create notebook: `02_bronze_player_profile`

```python
# Cell 1: Configuration
SOURCE_PATH = "Files/output/bronze_player_profile.parquet"
TARGET_TABLE = "bronze_player_profile"
BATCH_ID = datetime.now().strftime("%Y%m%d_%H%M%S")

# Cell 2: Read and transform
df_raw = spark.read.parquet(SOURCE_PATH)

# Add metadata
df_bronze = df_raw \
    .withColumn("_bronze_ingested_at", current_timestamp()) \
    .withColumn("_bronze_source_file", input_file_name()) \
    .withColumn("_bronze_batch_id", lit(BATCH_ID))

# Cell 3: Write
df_bronze.write \
    .format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .saveAsTable(TARGET_TABLE)

print(f"Wrote {df_bronze.count():,} player records")
```

## Step 4: Financial Transaction Ingestion

### Create Notebook

Create notebook: `03_bronze_financial_txn`

```python
# Configuration
SOURCE_PATH = "Files/output/bronze_financial_txn.parquet"
TARGET_TABLE = "bronze_financial_txn"

# Read source
df_raw = spark.read.parquet(SOURCE_PATH)

# Add metadata
df_bronze = df_raw \
    .withColumn("_bronze_ingested_at", current_timestamp()) \
    .withColumn("_bronze_source_file", input_file_name()) \
    .withColumn("_bronze_batch_id", lit(BATCH_ID))

# Write to table
df_bronze.write \
    .format("delta") \
    .mode("append") \
    .saveAsTable(TARGET_TABLE)
```

## Step 5: Ingest Remaining Data

Repeat the pattern for:
- `04_bronze_table_games`
- `05_bronze_security_events`
- `06_bronze_compliance`

Each notebook follows the same pattern:
1. Read source file
2. Add metadata columns
3. Write to Delta table
4. Verify counts

## Step 6: Create Bronze Layer Verification

### Create Verification Notebook

Create notebook: `99_bronze_verification`

```python
# Bronze Layer Verification
# =========================

tables = [
    "bronze_slot_telemetry",
    "bronze_player_profile",
    "bronze_financial_txn",
    "bronze_table_games",
    "bronze_security_events",
    "bronze_compliance"
]

print("=" * 60)
print("BRONZE LAYER VERIFICATION")
print("=" * 60)

total_records = 0
for table in tables:
    try:
        count = spark.table(table).count()
        total_records += count
        status = "✓"
    except Exception as e:
        count = 0
        status = "✗"

    print(f"{status} {table:30} {count:>12,} records")

print("-" * 60)
print(f"  {'TOTAL':30} {total_records:>12,} records")
print("=" * 60)
```

## Validation Checklist

Before proceeding to Silver layer:

- [ ] All 6 Bronze tables created
- [ ] Row counts match source data
- [ ] Metadata columns present (`_bronze_*`)
- [ ] Delta format confirmed
- [ ] No schema errors

## Best Practices

### Schema Evolution

Enable schema evolution for changing source schemas:

```python
df.write \
    .option("mergeSchema", "true") \
    .saveAsTable(table_name)
```

### Partitioning

For large tables, consider partitioning:

```python
df.write \
    .partitionBy("event_date") \
    .saveAsTable(table_name)
```

### Optimization

After ingestion, optimize tables:

```python
spark.sql(f"OPTIMIZE {table_name}")
spark.sql(f"VACUUM {table_name}")
```

## Troubleshooting

### File Not Found

- Verify file path in SOURCE_PATH
- Check Files section in Lakehouse
- Ensure upload completed successfully

### Schema Mismatch

- Use `mergeSchema` option
- Check source file schema
- Verify column names match

### Performance Issues

- Reduce data volume for testing
- Check capacity CU utilization
- Consider partitioning strategy

## Next Steps

Continue to [Tutorial 02: Silver Layer](../02-silver-layer/README.md) for data cleansing and transformation.

## Resources

- [Delta Lake in Fabric](https://learn.microsoft.com/fabric/data-engineering/delta-lake)
- [Lakehouse Tables](https://learn.microsoft.com/fabric/data-engineering/lakehouse-overview)
- [PySpark Reference](https://spark.apache.org/docs/latest/api/python/)
