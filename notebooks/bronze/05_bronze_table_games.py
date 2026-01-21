# Databricks notebook source
# MAGIC %md
# MAGIC # Bronze Layer: Table Games Ingestion
# MAGIC
# MAGIC This notebook ingests table games data (blackjack, craps, roulette, baccarat, poker).
# MAGIC
# MAGIC ## Key Features:
# MAGIC - RFID chip tracking data
# MAGIC - Game-specific event types
# MAGIC - Dealer and pit information
# MAGIC - Append-only pattern with date partitioning

# COMMAND ----------

from pyspark.sql.functions import *
from pyspark.sql.types import *
from datetime import datetime

# Parameters
batch_id = dbutils.widgets.get("batch_id") if "batch_id" in [w.name for w in dbutils.widgets.getAll()] else datetime.now().strftime("%Y%m%d_%H%M%S")
source_path = "Files/landing/table_games/"
target_table = "lh_bronze.bronze_table_games"

print(f"Processing batch: {batch_id}")
print(f"Source: {source_path}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Define Expected Schema

# COMMAND ----------

# Expected schema for table games data
table_games_schema = StructType([
    StructField("event_id", StringType(), False),
    StructField("table_id", StringType(), False),
    StructField("game_type", StringType(), False),
    StructField("event_type", StringType(), False),
    StructField("event_timestamp", TimestampType(), False),
    StructField("player_id", StringType(), True),
    StructField("dealer_id", StringType(), True),
    StructField("pit_id", StringType(), True),
    StructField("bet_amount", DecimalType(18, 2), True),
    StructField("win_amount", DecimalType(18, 2), True),
    StructField("chip_count", IntegerType(), True),
    StructField("hand_number", IntegerType(), True),
    StructField("cards_dealt", StringType(), True),
    StructField("outcome", StringType(), True),
    StructField("session_id", StringType(), True)
])

# COMMAND ----------

# MAGIC %md
# MAGIC ## Read Raw Table Games Data

# COMMAND ----------

# Read raw data from landing zone
df_raw = spark.read.parquet(f"abfss://{source_path}")

print(f"Records loaded: {df_raw.count():,}")
df_raw.printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Add Bronze Metadata

# COMMAND ----------

# Add ingestion metadata and derived columns
df_bronze = df_raw \
    .withColumn("event_date", to_date("event_timestamp")) \
    .withColumn("event_hour", hour("event_timestamp")) \
    .withColumn("game_category",
        when(col("game_type").isin("BLACKJACK", "BACCARAT", "POKER"), "CARDS")
        .when(col("game_type") == "CRAPS", "DICE")
        .when(col("game_type") == "ROULETTE", "WHEEL")
        .otherwise("OTHER")) \
    .withColumn("is_player_event",
        col("event_type").isin("BET_PLACED", "WIN", "LOSS", "PUSH", "SURRENDER")) \
    .withColumn("net_result",
        coalesce(col("win_amount"), lit(0)) - coalesce(col("bet_amount"), lit(0))) \
    .withColumn("_ingestion_timestamp", current_timestamp()) \
    .withColumn("_batch_id", lit(batch_id)) \
    .withColumn("_source_file", input_file_name())

# COMMAND ----------

# MAGIC %md
# MAGIC ## Write to Bronze Table

# COMMAND ----------

# Write to Bronze with date partitioning
df_bronze.write \
    .format("delta") \
    .mode("append") \
    .partitionBy("event_date", "game_type") \
    .saveAsTable(target_table)

print(f"Written {df_bronze.count():,} records to {target_table}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Validation Summary

# COMMAND ----------

# Summary by game type
spark.sql(f"""
    SELECT
        game_type,
        game_category,
        COUNT(*) as event_count,
        COUNT(DISTINCT table_id) as tables,
        COUNT(DISTINCT player_id) as unique_players,
        SUM(bet_amount) as total_bets,
        SUM(win_amount) as total_wins
    FROM {target_table}
    WHERE _batch_id = '{batch_id}'
    GROUP BY game_type, game_category
    ORDER BY game_type
""").show()

# COMMAND ----------

# Event type distribution
spark.sql(f"""
    SELECT
        event_type,
        COUNT(*) as count,
        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as pct
    FROM {target_table}
    WHERE _batch_id = '{batch_id}'
    GROUP BY event_type
    ORDER BY count DESC
""").show()
