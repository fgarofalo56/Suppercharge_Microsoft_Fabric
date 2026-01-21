# Fabric Notebooks

This directory contains notebooks designed for Microsoft Fabric. They can be imported directly into a Fabric workspace.

## Directory Structure

```
notebooks/
├── bronze/          # Bronze layer ingestion notebooks
├── silver/          # Silver layer transformation notebooks
├── gold/            # Gold layer aggregation notebooks
├── real-time/       # Real-time analytics notebooks
└── ml/              # Machine learning notebooks
```

## Bronze Layer Notebooks

Raw data ingestion from landing zone to Bronze tables.

| Notebook | Description | Source Data |
|----------|-------------|-------------|
| `01_bronze_slot_telemetry.py` | Slot machine events ingestion | Parquet files |
| `02_bronze_player_profile.py` | Player demographics with SSN hashing | Parquet files |
| `03_bronze_financial_txn.py` | Cage transactions with CTR flagging | Parquet files |
| `04_bronze_compliance.py` | Regulatory filings (CTR, SAR, W2G) | Parquet files |
| `05_bronze_table_games.py` | Table game transactions | Parquet files |
| `06_bronze_security_events.py` | Security/surveillance logs | Parquet files |

## Silver Layer Notebooks

Data cleansing, validation, and enrichment.

| Notebook | Description | Transformations |
|----------|-------------|-----------------|
| `01_silver_slot_cleansed.py` | Cleansed slot data | Deduplication, DQ scoring |
| `02_silver_player_master.py` | Player master with SCD Type 2 | Slowly changing dimensions |
| `03_silver_table_enriched.py` | Enriched table games | Session aggregations, patterns |
| `04_silver_financial_reconciled.py` | Reconciled transactions | CTR validation, structuring detection |
| `05_silver_security_enriched.py` | Enriched security events | Threat scoring, correlation |
| `06_silver_compliance_validated.py` | Validated compliance filings | Threshold validation, deadlines |

## Gold Layer Notebooks

Business-ready aggregations and KPIs.

| Notebook | Description | Key Metrics |
|----------|-------------|-------------|
| `01_gold_slot_performance.py` | Slot machine KPIs | Coin-in, Theo, Hold%, variance |
| `02_gold_player_360.py` | Player 360 view | LTV, churn risk, tier |
| `03_gold_compliance_reporting.py` | Compliance reports | CTR, SAR, W2G counts |
| `04_gold_table_analytics.py` | Table games analytics | Drop, Win, Hold% |
| `05_gold_financial_summary.py` | Financial summary | Daily P&L, cash flow |
| `06_gold_security_dashboard.py` | Security dashboard | Incidents, threats, response |

## Real-Time Notebooks

Streaming and real-time analytics.

| Notebook | Description |
|----------|-------------|
| `01_realtime_slot_streaming.py` | Eventstream to Lakehouse streaming |
| `02_kql_casino_floor.kql` | KQL queries for Eventhouse monitoring |

## Machine Learning Notebooks

Predictive models and AI/ML pipelines.

| Notebook | Description | Model Type |
|----------|-------------|------------|
| `01_ml_player_churn_prediction.py` | Player churn prediction | GBT Classifier |
| `02_ml_fraud_detection.py` | Fraud/anomaly detection | Isolation Forest |

## Importing Notebooks

### Via Fabric UI

1. Open your Fabric workspace
2. Click **+ New** > **Import notebook**
3. Select the `.py` or `.ipynb` file
4. Click **Upload**

### Via Fabric API

```python
import requests

# Upload notebook via API
url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/notebooks"
headers = {"Authorization": f"Bearer {token}"}
files = {"file": open("notebook.py", "rb")}

response = requests.post(url, headers=headers, files=files)
```

## Notebook Format

Notebooks use the **Databricks notebook format** with `# COMMAND ----------` separators:

```python
# Databricks notebook source
# MAGIC %md
# MAGIC # Notebook Title

# COMMAND ----------

# Python code cell
df = spark.read.parquet("path")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Section Header

# COMMAND ----------

# More code
df.show()
```

## Environment Configuration

Notebooks expect the following:
- Default Lakehouse attached
- Spark session available as `spark`
- Delta Lake support enabled

### Setting Default Lakehouse

1. Open notebook in Fabric
2. Click **Lakehouse** in left panel
3. Select your Lakehouse (e.g., `lh_bronze`)
4. Click **Pin** to set as default

### Lakehouse References

The notebooks use the following Lakehouse naming convention:

| Lakehouse | Purpose |
|-----------|---------|
| `lh_bronze` | Raw ingested data |
| `lh_silver` | Cleansed/enriched data |
| `lh_gold` | Business-ready aggregations |

## Best Practices

### Parameterization

Use widgets for configurable values:

```python
# Configuration cell
dbutils.widgets.text("source_path", "Files/data/")
dbutils.widgets.text("batch_date", "2024-01-01")

source_path = dbutils.widgets.get("source_path")
batch_date = dbutils.widgets.get("batch_date")
```

### Error Handling

Wrap operations in try-except:

```python
try:
    df.write.saveAsTable(table_name)
    print(f"Success: Wrote {df.count()} records")
except Exception as e:
    print(f"Error: {e}")
    raise
```

### Logging

Include progress logging:

```python
from datetime import datetime

print(f"[{datetime.now()}] Starting ingestion...")
print(f"[{datetime.now()}] Read {df.count()} records")
print(f"[{datetime.now()}] Wrote to {table_name}")
```

## Dependencies

Notebooks use standard Fabric libraries:
- PySpark
- Delta Lake
- pandas (for small datasets)
- matplotlib/seaborn (for visualization)
- MLflow (for ML notebooks)

No additional packages required for core functionality.

## Execution Order

### Initial Load (One-Time)

1. Bronze notebooks (parallel execution possible)
2. Silver notebooks (in order, after Bronze)
3. Gold notebooks (after Silver)

### Incremental Processing

1. Bronze: Append new data
2. Silver: Process incremental batches
3. Gold: Refresh aggregations

### Real-Time

- `01_realtime_slot_streaming.py` runs continuously
- KQL queries are on-demand via Eventhouse

## Testing

Before running in production:

1. Verify source paths exist
2. Check Lakehouse connections
3. Run with small data subset
4. Validate row counts and schemas
5. Check data quality scores

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Table not found | Ensure Lakehouse is pinned and previous layer completed |
| Permission denied | Check workspace role assignments |
| Timeout | Increase cluster size or reduce data volume |
| Schema mismatch | Use `overwriteSchema` option or fix source data |
