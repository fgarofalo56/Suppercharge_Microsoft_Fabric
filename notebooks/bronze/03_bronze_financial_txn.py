# Databricks notebook source
# MAGIC %md
# MAGIC # Bronze Layer: Financial Transaction Ingestion
# MAGIC
# MAGIC This notebook ingests cage financial transactions with compliance flagging.
# MAGIC
# MAGIC ## Key Features:
# MAGIC - CTR threshold detection ($10,000+)
# MAGIC - Partitioned by transaction date
# MAGIC - Append-only pattern

# COMMAND ----------

from pyspark.sql.functions import *
from pyspark.sql.types import *
from datetime import datetime

# Parameters
batch_id = dbutils.widgets.get("batch_id") if "batch_id" in [w.name for w in dbutils.widgets.getAll()] else datetime.now().strftime("%Y%m%d_%H%M%S")
source_path = "Files/landing/financial/"
target_table = "lh_bronze.bronze_financial_txn"

# Compliance thresholds
CTR_THRESHOLD = 10000

print(f"Processing batch: {batch_id}")
print(f"CTR Threshold: ${CTR_THRESHOLD:,}")

# COMMAND ----------

# Read raw financial data
df_raw = spark.read.parquet(f"abfss://{source_path}")

print(f"Records loaded: {df_raw.count():,}")

# COMMAND ----------

# Add Bronze metadata and compliance flags
df_bronze = df_raw \
    .withColumn("transaction_date", to_date("transaction_timestamp")) \
    .withColumn("ctr_required", col("amount") >= CTR_THRESHOLD) \
    .withColumn("near_ctr",
        col("amount").between(CTR_THRESHOLD * 0.8, CTR_THRESHOLD - 0.01)) \
    .withColumn("_ingestion_timestamp", current_timestamp()) \
    .withColumn("_batch_id", lit(batch_id)) \
    .withColumn("_source_file", input_file_name())

# COMMAND ----------

# Write to Bronze with date partitioning
df_bronze.write \
    .format("delta") \
    .mode("append") \
    .partitionBy("transaction_date") \
    .saveAsTable(target_table)

print(f"Written {df_bronze.count():,} records to {target_table}")

# COMMAND ----------

# Compliance summary
spark.sql(f"""
    SELECT
        transaction_date,
        COUNT(*) as total_txns,
        SUM(CASE WHEN ctr_required THEN 1 ELSE 0 END) as ctr_required,
        SUM(CASE WHEN near_ctr THEN 1 ELSE 0 END) as near_ctr,
        SUM(amount) as total_amount
    FROM {target_table}
    WHERE _batch_id = '{batch_id}'
    GROUP BY transaction_date
    ORDER BY transaction_date DESC
""").show()
