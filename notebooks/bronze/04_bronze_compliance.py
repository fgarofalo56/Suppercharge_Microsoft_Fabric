# Databricks notebook source
# MAGIC %md
# MAGIC # Bronze Layer: Compliance Filings Ingestion
# MAGIC
# MAGIC This notebook ingests regulatory compliance filings (CTR, SAR, W-2G).
# MAGIC
# MAGIC ## Regulatory Context:
# MAGIC - **CTR**: Currency Transaction Report (FinCEN) - $10,000+ cash
# MAGIC - **SAR**: Suspicious Activity Report (FinCEN) - Structuring, etc.
# MAGIC - **W-2G**: IRS Form for gambling winnings >= $1,200 (slots)

# COMMAND ----------

from pyspark.sql.functions import *
from pyspark.sql.types import *
from datetime import datetime

# Parameters
batch_id = dbutils.widgets.get("batch_id") if "batch_id" in [w.name for w in dbutils.widgets.getAll()] else datetime.now().strftime("%Y%m%d_%H%M%S")
source_path = "Files/landing/compliance/"
target_table = "lh_bronze.bronze_compliance_filings"

print(f"Processing batch: {batch_id}")

# COMMAND ----------

# Read raw compliance data
df_raw = spark.read.parquet(f"abfss://{source_path}")

print(f"Records loaded: {df_raw.count():,}")
df_raw.printSchema()

# COMMAND ----------

# Add metadata and categorization
df_bronze = df_raw \
    .withColumn("_ingestion_timestamp", current_timestamp()) \
    .withColumn("_batch_id", lit(batch_id)) \
    .withColumn("_source_file", input_file_name()) \
    .withColumn("_regulatory_agency",
        when(col("filing_type").isin("CTR", "SAR"), "FinCEN")
        .when(col("filing_type") == "W2G", "IRS")
        .otherwise("Other")) \
    .withColumn("filing_date", to_date("filing_timestamp"))

# COMMAND ----------

# Write to Bronze
df_bronze.write \
    .format("delta") \
    .mode("append") \
    .partitionBy("filing_date") \
    .saveAsTable(target_table)

print(f"Written {df_bronze.count():,} records to {target_table}")

# COMMAND ----------

# Filing summary
spark.sql(f"""
    SELECT
        filing_type,
        _regulatory_agency,
        COUNT(*) as count,
        SUM(amount) as total_amount,
        AVG(amount) as avg_amount
    FROM {target_table}
    WHERE _batch_id = '{batch_id}'
    GROUP BY filing_type, _regulatory_agency
    ORDER BY filing_type
""").show()
