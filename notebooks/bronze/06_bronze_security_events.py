# Databricks notebook source
# MAGIC %md
# MAGIC # Bronze Layer: Security Events Ingestion
# MAGIC
# MAGIC This notebook ingests security and surveillance events.
# MAGIC
# MAGIC ## Event Categories:
# MAGIC - Access control (door entries, badge swipes)
# MAGIC - Surveillance alerts (camera triggers, motion detection)
# MAGIC - Incident reports
# MAGIC - Player exclusion events

# COMMAND ----------

from pyspark.sql.functions import *
from pyspark.sql.types import *
from datetime import datetime

# Parameters
batch_id = dbutils.widgets.get("batch_id") if "batch_id" in [w.name for w in dbutils.widgets.getAll()] else datetime.now().strftime("%Y%m%d_%H%M%S")
source_path = "Files/landing/security/"
target_table = "lh_bronze.bronze_security_events"

print(f"Processing batch: {batch_id}")
print(f"Source: {source_path}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Read Raw Security Events

# COMMAND ----------

# Read raw security event data
df_raw = spark.read.parquet(f"abfss://{source_path}")

print(f"Records loaded: {df_raw.count():,}")
df_raw.printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Add Bronze Metadata and Categorization

# COMMAND ----------

# Security event severity mapping
df_bronze = df_raw \
    .withColumn("event_date", to_date("event_timestamp")) \
    .withColumn("event_hour", hour("event_timestamp")) \
    .withColumn("severity_level",
        when(col("event_type").isin("THREAT_DETECTED", "EXCLUSION_VIOLATION", "TRESPASS"), "CRITICAL")
        .when(col("event_type").isin("SUSPICIOUS_ACTIVITY", "UNAUTHORIZED_ACCESS", "ALTERCATION"), "HIGH")
        .when(col("event_type").isin("ACCESS_DENIED", "CAMERA_OBSTRUCTION", "PATRON_COMPLAINT"), "MEDIUM")
        .otherwise("LOW")) \
    .withColumn("requires_response",
        col("event_type").isin(
            "THREAT_DETECTED", "EXCLUSION_VIOLATION", "TRESPASS",
            "UNAUTHORIZED_ACCESS", "ALTERCATION", "MEDICAL_EMERGENCY"
        )) \
    .withColumn("event_category",
        when(col("event_type").isin("BADGE_SWIPE", "DOOR_ENTRY", "ACCESS_GRANTED", "ACCESS_DENIED"), "ACCESS_CONTROL")
        .when(col("event_type").isin("CAMERA_ALERT", "MOTION_DETECTED", "CAMERA_OBSTRUCTION"), "SURVEILLANCE")
        .when(col("event_type").isin("EXCLUSION_CHECK", "EXCLUSION_VIOLATION"), "EXCLUSION")
        .when(col("event_type").isin("INCIDENT_REPORT", "ALTERCATION", "MEDICAL_EMERGENCY"), "INCIDENT")
        .otherwise("OTHER")) \
    .withColumn("_ingestion_timestamp", current_timestamp()) \
    .withColumn("_batch_id", lit(batch_id)) \
    .withColumn("_source_file", input_file_name())

# COMMAND ----------

# MAGIC %md
# MAGIC ## Write to Bronze Table

# COMMAND ----------

# Write to Bronze with date and severity partitioning
df_bronze.write \
    .format("delta") \
    .mode("append") \
    .partitionBy("event_date", "severity_level") \
    .saveAsTable(target_table)

print(f"Written {df_bronze.count():,} records to {target_table}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Validation Summary

# COMMAND ----------

# Summary by severity
spark.sql(f"""
    SELECT
        severity_level,
        COUNT(*) as event_count,
        COUNT(DISTINCT location_id) as locations,
        SUM(CASE WHEN requires_response THEN 1 ELSE 0 END) as requires_response_count
    FROM {target_table}
    WHERE _batch_id = '{batch_id}'
    GROUP BY severity_level
    ORDER BY
        CASE severity_level
            WHEN 'CRITICAL' THEN 1
            WHEN 'HIGH' THEN 2
            WHEN 'MEDIUM' THEN 3
            ELSE 4
        END
""").show()

# COMMAND ----------

# Event category distribution
spark.sql(f"""
    SELECT
        event_category,
        event_type,
        COUNT(*) as count
    FROM {target_table}
    WHERE _batch_id = '{batch_id}'
    GROUP BY event_category, event_type
    ORDER BY event_category, count DESC
""").show(50)

# COMMAND ----------

# Critical/High events requiring attention
critical_events = spark.sql(f"""
    SELECT
        event_timestamp,
        event_type,
        severity_level,
        location_id,
        description
    FROM {target_table}
    WHERE _batch_id = '{batch_id}'
      AND severity_level IN ('CRITICAL', 'HIGH')
    ORDER BY event_timestamp DESC
    LIMIT 20
""")

if critical_events.count() > 0:
    print("CRITICAL/HIGH SEVERITY EVENTS:")
    critical_events.show(truncate=False)
else:
    print("No critical or high severity events in this batch.")
