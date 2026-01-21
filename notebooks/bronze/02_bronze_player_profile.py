# Databricks notebook source
# MAGIC %md
# MAGIC # Bronze Layer: Player Profile Ingestion
# MAGIC
# MAGIC This notebook ingests player profile data into the Bronze layer with PII handling.
# MAGIC
# MAGIC ## Key Features:
# MAGIC - SSN hashing at ingestion (never store raw SSN)
# MAGIC - Metadata enrichment
# MAGIC - Full load pattern for dimension data

# COMMAND ----------

from pyspark.sql.functions import *
from pyspark.sql.types import *
from datetime import datetime

# Parameters
batch_id = dbutils.widgets.get("batch_id") if "batch_id" in [w.name for w in dbutils.widgets.getAll()] else datetime.now().strftime("%Y%m%d_%H%M%S")
source_path = "Files/landing/player_profiles/"
target_table = "lh_bronze.bronze_player_profile"

print(f"Processing batch: {batch_id}")
print(f"Source: {source_path}")

# COMMAND ----------

# Read raw player data
df_raw = spark.read.parquet(f"abfss://{source_path}")

print(f"Records loaded: {df_raw.count():,}")
df_raw.printSchema()

# COMMAND ----------

# CRITICAL: Hash SSN immediately - never store raw SSN
# This is a compliance requirement for gaming industry

df_bronze = df_raw \
    .withColumn("ssn_hash",
        when(col("ssn").isNotNull(), sha2(col("ssn"), 256))
        .otherwise(None)) \
    .drop("ssn") \
    .withColumn("_ingestion_timestamp", current_timestamp()) \
    .withColumn("_batch_id", lit(batch_id)) \
    .withColumn("_source_file", input_file_name())

# COMMAND ----------

# Write to Bronze (overwrite for dimension tables)
df_bronze.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(target_table)

print(f"Written {df_bronze.count():,} records to {target_table}")

# COMMAND ----------

# Validation
spark.sql(f"""
    SELECT
        COUNT(*) as total,
        COUNT(ssn_hash) as has_ssn_hash,
        COUNT(DISTINCT loyalty_tier) as tiers
    FROM {target_table}
""").show()
