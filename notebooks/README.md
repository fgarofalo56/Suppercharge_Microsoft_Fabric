# :notebook: Fabric Notebooks

> **[Home](../README.md)** | **[Data Generation](../data-generation/)** | **[Validation](../validation/)** | **[Tutorials](../tutorials/)**

Production-ready notebooks designed for Microsoft Fabric, implementing the medallion architecture for casino/gaming data.

---

## Overview

```
+------------------+     +------------------+     +------------------+
|   BRONZE LAYER   |     |   SILVER LAYER   |     |    GOLD LAYER    |
+------------------+     +------------------+     +------------------+
| 01_slot_telemetry| --> | 01_slot_cleansed | --> | 01_slot_perf     |
| 02_player_profile| --> | 02_player_master | --> | 02_player_360    |
| 03_financial_txn | --> | 03_table_enriched| --> | 03_compliance    |
| 04_compliance    | --> | 04_financial_rec | --> | 04_table_analytics|
| 05_table_games   | --> | 05_security_enr  | --> | 05_financial_sum |
| 06_security_events| --> | 06_compliance_val| --> | 06_security_dash |
+------------------+     +------------------+     +------------------+
                                                          |
                              +----------------------------+
                              |
        +---------------------+---------------------+
        |                                           |
+-------v--------+                          +-------v--------+
|   REAL-TIME    |                          |   MACHINE      |
|   ANALYTICS    |                          |   LEARNING     |
+----------------+                          +----------------+
| Eventstream    |                          | Churn Model    |
| KQL Queries    |                          | Fraud Detection|
+----------------+                          +----------------+
```

---

## Notebook Inventory

### Bronze Layer Notebooks

Raw data ingestion from landing zone to Bronze tables.

| # | Notebook | Description | Source | Output Table |
|---|----------|-------------|--------|--------------|
| 01 | `bronze_slot_telemetry.py` | Slot machine events ingestion | Parquet | `bronze_slot_telemetry` |
| 02 | `bronze_player_profile.py` | Player demographics with SSN hashing | Parquet | `bronze_player_profile` |
| 03 | `bronze_financial_txn.py` | Cage transactions with CTR flagging | Parquet | `bronze_financial_txn` |
| 04 | `bronze_compliance.py` | Regulatory filings (CTR, SAR, W2G) | Parquet | `bronze_compliance` |
| 05 | `bronze_table_games.py` | Table game transactions | Parquet | `bronze_table_games` |
| 06 | `bronze_security_events.py` | Security/surveillance logs | Parquet | `bronze_security_events` |

### Silver Layer Notebooks

Data cleansing, validation, and enrichment.

| # | Notebook | Description | Key Transformations |
|---|----------|-------------|---------------------|
| 01 | `silver_slot_cleansed.py` | Cleansed slot data | Deduplication, DQ scoring |
| 02 | `silver_player_master.py` | Player master with SCD Type 2 | Slowly changing dimensions |
| 03 | `silver_table_enriched.py` | Enriched table games | Session aggregations, patterns |
| 04 | `silver_financial_reconciled.py` | Reconciled transactions | CTR validation, structuring detection |
| 05 | `silver_security_enriched.py` | Enriched security events | Threat scoring, correlation |
| 06 | `silver_compliance_validated.py` | Validated compliance filings | Threshold validation, deadlines |

### Gold Layer Notebooks

Business-ready aggregations and KPIs.

| # | Notebook | Description | Key Metrics |
|---|----------|-------------|-------------|
| 01 | `gold_slot_performance.py` | Slot machine KPIs | Coin-in, Theo, Hold%, variance |
| 02 | `gold_player_360.py` | Player 360 view | LTV, churn risk, tier |
| 03 | `gold_compliance_reporting.py` | Compliance reports | CTR, SAR, W2G counts |
| 04 | `gold_table_analytics.py` | Table games analytics | Drop, Win, Hold% |
| 05 | `gold_financial_summary.py` | Financial summary | Daily P&L, cash flow |
| 06 | `gold_security_dashboard.py` | Security dashboard | Incidents, threats, response |

### Real-Time Notebooks

Streaming and real-time analytics.

| Notebook | Description | Technology |
|----------|-------------|------------|
| `realtime_slot_streaming.py` | Eventstream to Lakehouse streaming | Spark Structured Streaming |
| `kql_casino_floor.kql` | KQL queries for Eventhouse monitoring | KQL |

### Machine Learning Notebooks

Predictive models and AI/ML pipelines.

| Notebook | Description | Model Type | Use Case |
|----------|-------------|------------|----------|
| `ml_player_churn_prediction.py` | Player churn prediction | GBT Classifier | Retention |
| `ml_fraud_detection.py` | Fraud/anomaly detection | Isolation Forest | Security |

---

## Importing Notebooks

### Via Fabric UI

1. Open your Fabric workspace
2. Click **+ New** > **Import notebook**
3. Select the `.py` or `.ipynb` file
4. Click **Upload**

> **Tip:** Import notebooks in layer order: Bronze first, then Silver, then Gold.

### Via Fabric API

```python
import requests

# Upload notebook via API
workspace_id = "your-workspace-id"
token = "your-access-token"

url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/notebooks"
headers = {"Authorization": f"Bearer {token}"}
files = {"file": open("notebook.py", "rb")}

response = requests.post(url, headers=headers, files=files)
print(response.json())
```

---

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

---

## Environment Configuration

### Prerequisites

Notebooks expect the following:

| Requirement | Description |
|-------------|-------------|
| Default Lakehouse | Must be attached to notebook |
| Spark Session | Available as `spark` variable |
| Delta Lake | Support enabled (default in Fabric) |

### Setting Default Lakehouse

1. Open notebook in Fabric
2. Click **Lakehouse** in left panel
3. Select your Lakehouse (e.g., `lh_bronze`)
4. Click **Pin** to set as default

### Lakehouse References

| Lakehouse | Purpose | Layer |
|-----------|---------|-------|
| `lh_bronze` | Raw ingested data | Bronze |
| `lh_silver` | Cleansed/enriched data | Silver |
| `lh_gold` | Business-ready aggregations | Gold |

---

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

---

## Dependencies

Notebooks use standard Fabric libraries (no additional packages required):

| Library | Version | Purpose |
|---------|---------|---------|
| PySpark | 3.4+ | Data processing |
| Delta Lake | 2.4+ | Table format |
| pandas | 2.0+ | Small dataset operations |
| matplotlib | 3.7+ | Visualization |
| seaborn | 0.12+ | Statistical visualization |
| MLflow | 2.0+ | ML experiment tracking |

---

## Execution Order

### Initial Load (One-Time)

```
1. Bronze Notebooks (can run in parallel)
   |-- 01_bronze_slot_telemetry.py
   |-- 02_bronze_player_profile.py
   |-- 03_bronze_financial_txn.py
   |-- 04_bronze_compliance.py
   |-- 05_bronze_table_games.py
   +-- 06_bronze_security_events.py

2. Silver Notebooks (run after Bronze, in order)
   |-- 01_silver_slot_cleansed.py
   |-- 02_silver_player_master.py
   |-- 03_silver_table_enriched.py
   |-- 04_silver_financial_reconciled.py
   |-- 05_silver_security_enriched.py
   +-- 06_silver_compliance_validated.py

3. Gold Notebooks (run after Silver)
   |-- 01_gold_slot_performance.py
   |-- 02_gold_player_360.py
   |-- 03_gold_compliance_reporting.py
   |-- 04_gold_table_analytics.py
   |-- 05_gold_financial_summary.py
   +-- 06_gold_security_dashboard.py
```

### Incremental Processing

| Layer | Strategy | Frequency |
|-------|----------|-----------|
| Bronze | Append new data | Hourly |
| Silver | Process incremental batches | Hourly |
| Gold | Refresh aggregations | Daily |

### Real-Time

- `realtime_slot_streaming.py` - Runs continuously
- KQL queries - On-demand via Eventhouse

---

## Testing Notebooks

Before running in production:

- [ ] Verify source paths exist
- [ ] Check Lakehouse connections
- [ ] Run with small data subset
- [ ] Validate row counts and schemas
- [ ] Check data quality scores
- [ ] Review execution logs

---

## Troubleshooting

| Issue | Possible Cause | Solution |
|-------|----------------|----------|
| Table not found | Lakehouse not pinned | Ensure Lakehouse is pinned and previous layer completed |
| Permission denied | Role assignment | Check workspace role assignments |
| Timeout | Large data volume | Increase cluster size or reduce data volume |
| Schema mismatch | Column changes | Use `overwriteSchema` option or fix source data |
| Memory error | Large dataset | Use partitioning or process in batches |
| Job failed | Various | Check Spark UI for detailed error logs |

---

## Directory Structure

```
notebooks/
|-- bronze/                   # Bronze layer ingestion notebooks
|   |-- 01_bronze_slot_telemetry.py
|   |-- 02_bronze_player_profile.py
|   |-- 03_bronze_financial_txn.py
|   |-- 04_bronze_compliance.py
|   |-- 05_bronze_table_games.py
|   +-- 06_bronze_security_events.py
|-- silver/                   # Silver layer transformation notebooks
|   |-- 01_silver_slot_cleansed.py
|   |-- 02_silver_player_master.py
|   +-- ...
|-- gold/                     # Gold layer aggregation notebooks
|   |-- 01_gold_slot_performance.py
|   |-- 02_gold_player_360.py
|   +-- ...
|-- real-time/                # Real-time analytics notebooks
|   |-- 01_realtime_slot_streaming.py
|   +-- 02_kql_casino_floor.kql
|-- ml/                       # Machine learning notebooks
|   |-- 01_ml_player_churn_prediction.py
|   +-- 02_ml_fraud_detection.py
+-- README.md
```

---

## Related Resources

| Resource | Description |
|----------|-------------|
| [Tutorials](../tutorials/README.md) | Step-by-step implementation guides |
| [Data Generation](../data-generation/README.md) | Generate test data for notebooks |
| [Validation](../validation/README.md) | Test notebook outputs |
| [Fabric Documentation](https://learn.microsoft.com/fabric/) | Official Microsoft Fabric docs |

---

<div align="center">

**[Back to Top](#notebook-fabric-notebooks)** | **[Main README](../README.md)**

</div>
