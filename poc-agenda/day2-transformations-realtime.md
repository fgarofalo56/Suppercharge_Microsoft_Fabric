# Day 2: Transformations & Real-Time Analytics

## Overview

**Duration:** 8 hours
**Focus:** Complete Silver/Gold layers, implement real-time casino floor monitoring
**Audience:** Data Architects (4 participants)

---

## Morning Session 1: Silver Layer Complete (9:00 - 10:30)

### Objectives

- Complete Silver layer transformations
- Implement SCD Type 2 for player master
- Apply reconciliation patterns for financial data

### 5.1 Player Master with SCD Type 2 (45 min)

SCD Type 2 tracks historical changes to player attributes:

```python
# Notebook: 02_silver_player_master

from delta.tables import DeltaTable
from pyspark.sql.functions import *

# Read new data from Bronze
df_new = spark.table("lh_bronze.bronze_player_profile") \
    .withColumn("effective_date", current_date()) \
    .withColumn("end_date", lit(None).cast("date")) \
    .withColumn("is_current", lit(True))

# Check if Silver table exists
if spark.catalog.tableExists("lh_silver.silver_player_master"):
    # SCD Type 2 merge logic
    silver_table = DeltaTable.forName(spark, "lh_silver.silver_player_master")

    # Get current records
    df_current = silver_table.toDF().filter(col("is_current") == True)

    # Find changes (compare on key attributes)
    df_changes = df_new.alias("new") \
        .join(df_current.alias("current"), "player_id", "left") \
        .filter(
            (col("current.player_id").isNull()) |  # New player
            (col("new.loyalty_tier") != col("current.loyalty_tier")) |  # Tier change
            (col("new.email") != col("current.email")) |  # Email change
            (col("new.address") != col("current.address"))  # Address change
        )

    if df_changes.count() > 0:
        # Close current records
        silver_table.update(
            condition = (col("player_id").isin(df_changes.select("player_id").collect())) &
                       (col("is_current") == True),
            set = {
                "end_date": current_date(),
                "is_current": lit(False)
            }
        )

        # Insert new versions
        df_changes.select(df_new.columns).write \
            .format("delta") \
            .mode("append") \
            .saveAsTable("lh_silver.silver_player_master")
else:
    # Initial load
    df_new.write \
        .format("delta") \
        .mode("overwrite") \
        .saveAsTable("lh_silver.silver_player_master")

# Verification
spark.sql("""
    SELECT player_id, COUNT(*) as versions
    FROM lh_silver.silver_player_master
    GROUP BY player_id
    HAVING COUNT(*) > 1
    ORDER BY versions DESC
    LIMIT 10
""").show()
```

### 5.2 Financial Reconciliation (45 min)

Implement cage reconciliation patterns:

```python
# Notebook: 03_silver_financial_reconciled

# Read Bronze financial data
df_txn = spark.table("lh_bronze.bronze_financial_txn")

# Reconciliation rules
df_reconciled = df_txn \
    .withColumn("reconciliation_status",
        when(col("source_amount") == col("destination_amount"), "MATCHED")
        .when(abs(col("source_amount") - col("destination_amount")) < 0.01, "MATCHED_ROUNDING")
        .otherwise("VARIANCE")) \
    .withColumn("variance_amount",
        col("source_amount") - col("destination_amount")) \
    .withColumn("variance_pct",
        when(col("source_amount") > 0,
             (col("variance_amount") / col("source_amount")) * 100)
        .otherwise(0))

# Flag high-risk transactions
df_silver = df_reconciled \
    .withColumn("risk_flags",
        array_distinct(
            filter(
                array(
                    when(col("amount") >= 10000, lit("CTR_REQUIRED")),
                    when(col("amount").between(8000, 9999), lit("NEAR_CTR")),
                    when(col("variance_pct") > 1, lit("HIGH_VARIANCE")),
                    when(col("transaction_type") == "MARKER", lit("CREDIT_TRANSACTION"))
                ),
                lambda x: x.isNotNull()
            )
        ))

df_silver.write \
    .format("delta") \
    .mode("overwrite") \
    .partitionBy("transaction_date") \
    .saveAsTable("lh_silver.silver_financial_reconciled")

# Reconciliation summary
spark.sql("""
    SELECT
        reconciliation_status,
        COUNT(*) as transactions,
        SUM(amount) as total_amount,
        AVG(variance_pct) as avg_variance_pct
    FROM lh_silver.silver_financial_reconciled
    GROUP BY reconciliation_status
""").show()
```

---

## Morning Session 2: Gold Layer (10:45 - 12:30)

### Objectives

- Create aggregated Gold layer tables
- Implement casino KPI calculations
- Build star schema dimensions

### 6.1 Slot Performance Gold Table (45 min)

```python
# Notebook: 01_gold_slot_performance

# Read Silver slot data
df_silver = spark.table("lh_silver.silver_slot_cleansed")

# Daily aggregations by machine
df_daily = df_silver \
    .withColumn("business_date", to_date("event_timestamp")) \
    .groupBy("machine_id", "zone", "denomination", "business_date") \
    .agg(
        sum("coin_in").alias("total_coin_in"),
        sum("coin_out").alias("total_coin_out"),
        sum("games_played").alias("total_games"),
        sum(when(col("event_type") == "JACKPOT", col("jackpot_amount"))).alias("jackpot_payouts"),
        countDistinct("player_id").alias("unique_players"),
        count("*").alias("total_events"),
        avg("_dq_score").alias("avg_data_quality")
    )

# Calculate KPIs
df_gold = df_daily \
    .withColumn("net_win", col("total_coin_in") - col("total_coin_out")) \
    .withColumn("actual_hold_pct",
        when(col("total_coin_in") > 0,
             (col("net_win") / col("total_coin_in")) * 100)
        .otherwise(0)) \
    .withColumn("avg_bet",
        when(col("total_games") > 0,
             col("total_coin_in") / col("total_games"))
        .otherwise(0)) \
    .withColumn("win_per_unit",
        col("net_win") / 1)  # Per machine per day

# Add theoretical calculations (example: 8% theoretical hold)
df_gold = df_gold \
    .withColumn("theoretical_win", col("total_coin_in") * 0.08) \
    .withColumn("hold_variance", col("net_win") - col("theoretical_win")) \
    .withColumn("hold_variance_pct",
        when(col("theoretical_win") > 0,
             ((col("net_win") - col("theoretical_win")) / col("theoretical_win")) * 100)
        .otherwise(0))

# Write to Gold
df_gold.write \
    .format("delta") \
    .mode("overwrite") \
    .partitionBy("business_date") \
    .saveAsTable("lh_gold.gold_slot_performance")

# OPTIMIZE for Direct Lake
spark.sql("OPTIMIZE lh_gold.gold_slot_performance ZORDER BY (machine_id)")
```

### 6.2 Player 360 Gold Table (45 min)

```python
# Notebook: 02_gold_player_360

# Get current player records
df_players = spark.table("lh_silver.silver_player_master") \
    .filter(col("is_current") == True)

# Aggregate gaming activity
df_slot_activity = spark.table("lh_silver.silver_slot_cleansed") \
    .groupBy("player_id") \
    .agg(
        sum("coin_in").alias("slot_coin_in"),
        sum("coin_out").alias("slot_coin_out"),
        count("*").alias("slot_games_played"),
        max("event_timestamp").alias("last_slot_play")
    )

df_table_activity = spark.table("lh_silver.silver_table_enriched") \
    .groupBy("player_id") \
    .agg(
        sum("buy_in").alias("table_buy_in"),
        sum("cash_out").alias("table_cash_out"),
        sum("hours_played").alias("table_hours_played"),
        max("session_end").alias("last_table_play")
    )

df_financial = spark.table("lh_silver.silver_financial_reconciled") \
    .groupBy("player_id") \
    .agg(
        count("*").alias("total_transactions"),
        sum(when(col("transaction_type") == "CASH_IN", col("amount"))).alias("total_cash_in"),
        sum(when(col("transaction_type") == "MARKER", col("amount"))).alias("total_markers"),
        max("transaction_timestamp").alias("last_transaction")
    )

# Join all activities
df_360 = df_players \
    .join(df_slot_activity, "player_id", "left") \
    .join(df_table_activity, "player_id", "left") \
    .join(df_financial, "player_id", "left")

# Calculate metrics
df_gold = df_360 \
    .withColumn("total_gaming_activity",
        coalesce(col("slot_coin_in"), lit(0)) + coalesce(col("table_buy_in"), lit(0))) \
    .withColumn("total_theo_win",
        (coalesce(col("slot_coin_in"), lit(0)) * 0.08) +
        (coalesce(col("table_hours_played"), lit(0)) * 50)) \
    .withColumn("last_visit",
        greatest(col("last_slot_play"), col("last_table_play"), col("last_transaction"))) \
    .withColumn("days_since_visit",
        datediff(current_date(), col("last_visit"))) \
    .withColumn("churn_risk",
        when(col("days_since_visit") > 90, "High")
        .when(col("days_since_visit") > 30, "Medium")
        .otherwise("Low")) \
    .withColumn("player_value_score",
        (coalesce(col("total_theo_win"), lit(0)) / 1000) +
        (coalesce(col("total_visits"), lit(0)) * 2))

df_gold.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("lh_gold.gold_player_360")
```

### 6.3 Compliance Reporting Gold Table (30 min)

```python
# Notebook: 03_gold_compliance_reporting

df_compliance = spark.table("lh_silver.silver_compliance_validated")
df_financial = spark.table("lh_silver.silver_financial_reconciled")

# Daily compliance summary
df_gold = df_compliance \
    .withColumn("report_date", to_date("filing_timestamp")) \
    .groupBy("report_date") \
    .agg(
        sum(when(col("filing_type") == "CTR", 1).otherwise(0)).alias("ctr_count"),
        sum(when(col("filing_type") == "SAR", 1).otherwise(0)).alias("sar_count"),
        sum(when(col("filing_type") == "W2G", 1).otherwise(0)).alias("w2g_count"),
        sum(when(col("filing_type") == "CTR", col("amount"))).alias("ctr_total_amount"),
        sum(when(col("filing_type") == "W2G", col("amount"))).alias("w2g_total_amount")
    )

# Add potential CTRs from financial (not yet filed)
df_potential_ctr = df_financial \
    .filter(col("amount") >= 10000) \
    .filter(col("ctr_filed") == False) \
    .groupBy(to_date("transaction_timestamp").alias("report_date")) \
    .agg(count("*").alias("pending_ctrs"))

df_gold = df_gold.join(df_potential_ctr, "report_date", "left")

df_gold.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("lh_gold.gold_compliance_reporting")
```

---

## Afternoon Session 3: Real-Time Analytics (13:30 - 15:00)

### Objectives

- Create Eventhouse for real-time data
- Configure Eventstreams for slot telemetry
- Write KQL queries for monitoring

### 7.1 Create Eventhouse (20 min)

1. In workspace, click **+ New** > **Eventhouse**
2. Name: `eh_casino_realtime`
3. Create database: `kdb_floor_monitoring`

### 7.2 Configure Eventstream (40 min)

```
Eventstream: es_slot_telemetry

Source: Custom App (for demo)
  - Later: Event Hub / IoT Hub for production

Transformations:
  1. Parse JSON
  2. Add timestamp
  3. Filter for relevant events

Destination: KQL Database
  - Table: slot_events
```

**Create streaming table in KQL:**

```kql
.create table slot_events (
    machine_id: string,
    event_type: string,
    event_timestamp: datetime,
    coin_in: decimal,
    coin_out: decimal,
    games_played: int,
    jackpot_amount: decimal,
    zone: string,
    denomination: decimal,
    player_id: string
)

.create table slot_events ingestion json mapping 'slot_events_mapping' '[{"column":"machine_id","path":"$.machine_id"},{"column":"event_type","path":"$.event_type"},{"column":"event_timestamp","path":"$.event_timestamp"},{"column":"coin_in","path":"$.coin_in"},{"column":"coin_out","path":"$.coin_out"},{"column":"games_played","path":"$.games_played"},{"column":"jackpot_amount","path":"$.jackpot_amount"},{"column":"zone","path":"$.zone"},{"column":"denomination","path":"$.denomination"},{"column":"player_id","path":"$.player_id"}]'
```

### 7.3 KQL Monitoring Queries (30 min)

**Real-time floor summary:**

```kql
// Current floor activity (last 5 minutes)
slot_events
| where event_timestamp > ago(5m)
| summarize
    active_machines = dcount(machine_id),
    total_coin_in = sum(coin_in),
    total_games = sum(games_played),
    jackpots = countif(event_type == "JACKPOT")
by zone
| order by total_coin_in desc
```

**Machine performance alerts:**

```kql
// Machines with unusual hold (last hour)
slot_events
| where event_timestamp > ago(1h)
| summarize
    coin_in = sum(coin_in),
    coin_out = sum(coin_out)
by machine_id, zone
| extend
    net_win = coin_in - coin_out,
    hold_pct = (coin_in - coin_out) / coin_in * 100
| where hold_pct < 2 or hold_pct > 15
| project machine_id, zone, coin_in, net_win, hold_pct
| order by hold_pct asc
```

**Jackpot tracking:**

```kql
// Recent jackpots
slot_events
| where event_type == "JACKPOT"
| where event_timestamp > ago(24h)
| project
    event_timestamp,
    machine_id,
    zone,
    jackpot_amount,
    player_id
| order by event_timestamp desc
| take 50
```

---

## Afternoon Session 4: Real-Time Dashboards (15:15 - 17:00)

### Objectives

- Create real-time dashboard in Fabric
- Implement auto-refresh
- Build alert rules

### 8.1 Create Real-Time Dashboard (45 min)

1. In Eventhouse, click **New dashboard**
2. Name: `Casino Floor Monitor`

**Tile 1: Active Machines**
```kql
slot_events
| where event_timestamp > ago(5m)
| summarize active = dcount(machine_id)
| project active
```
- Visual: Card

**Tile 2: Coin In by Zone (5 min)**
```kql
slot_events
| where event_timestamp > ago(5m)
| summarize coin_in = sum(coin_in) by zone
| order by coin_in desc
```
- Visual: Bar chart

**Tile 3: Hourly Trend**
```kql
slot_events
| where event_timestamp > ago(24h)
| summarize coin_in = sum(coin_in) by bin(event_timestamp, 1h)
| order by event_timestamp asc
```
- Visual: Line chart

**Tile 4: Jackpot Feed**
```kql
slot_events
| where event_type == "JACKPOT"
| where event_timestamp > ago(1h)
| project event_timestamp, machine_id, zone, jackpot_amount
| order by event_timestamp desc
| take 10
```
- Visual: Table

### 8.2 Configure Alerts (30 min)

**Alert: Large Jackpot**
```kql
slot_events
| where event_type == "JACKPOT"
| where jackpot_amount >= 10000
| where event_timestamp > ago(5m)
```
- Action: Email to floor manager

**Alert: Machine Down (No Events)**
```kql
// Machines that went silent
let active_machines = slot_events
| where event_timestamp > ago(1h) and event_timestamp <= ago(10m)
| distinct machine_id;
let current_machines = slot_events
| where event_timestamp > ago(10m)
| distinct machine_id;
active_machines
| where machine_id !in (current_machines)
```

### 8.3 Streaming Data Producer (30 min)

Create a simple Python producer for testing:

```python
# streaming_producer.py
import json
import time
import random
from datetime import datetime
from azure.eventhub import EventHubProducerClient, EventData

# For demo: using local file stream
# Production: use Event Hub connection string

def generate_event():
    return {
        "machine_id": f"SLOT-{random.randint(1000, 9999)}",
        "event_type": random.choices(
            ["GAME_PLAY", "JACKPOT", "DOOR_OPEN", "METER_UPDATE"],
            weights=[85, 2, 3, 10]
        )[0],
        "event_timestamp": datetime.utcnow().isoformat(),
        "coin_in": round(random.uniform(1, 100), 2),
        "coin_out": round(random.uniform(0, 80), 2),
        "games_played": random.randint(1, 5),
        "jackpot_amount": round(random.uniform(100, 50000), 2) if random.random() < 0.02 else 0,
        "zone": random.choice(["North", "South", "East", "West", "VIP"]),
        "denomination": random.choice([0.01, 0.05, 0.25, 1.00, 5.00]),
        "player_id": f"P{random.randint(10000, 99999)}" if random.random() > 0.3 else None
    }

# Generate events
while True:
    event = generate_event()
    print(json.dumps(event))
    time.sleep(0.1)  # 10 events per second
```

---

## Day 2 Validation Checklist

### Silver Layer
- [ ] `silver_player_master` with SCD Type 2 working
- [ ] `silver_financial_reconciled` with reconciliation status
- [ ] All Silver tables partitioned appropriately

### Gold Layer
- [ ] `gold_slot_performance` with KPIs calculated
- [ ] `gold_player_360` with player metrics
- [ ] `gold_compliance_reporting` summary

### Real-Time
- [ ] Eventhouse `eh_casino_realtime` created
- [ ] KQL database with `slot_events` table
- [ ] Eventstream configured
- [ ] Real-time dashboard with 4+ tiles
- [ ] At least one alert configured

---

## Homework / Preparation for Day 3

1. **Review Direct Lake Tutorial** (Tutorial 05)
2. **Explore KQL:**
   - Write 3 additional monitoring queries
   - Try different visualizations

3. **Prepare for Power BI:**
   - Think about executive dashboard requirements
   - Identify key metrics for compliance reporting

4. **Read About:**
   - Direct Lake mode vs Import mode
   - DAX best practices
   - Purview classifications

---

## Instructor Notes

### Common Issues

1. **SCD Type 2 Not Working**
   - Verify Delta Lake merge syntax
   - Check join conditions

2. **Eventstream Not Flowing**
   - Verify source connection
   - Check KQL mapping

3. **KQL Queries Slow**
   - Add time filters first
   - Use summarize before project

### Key Discussion Points

- When to use SCD Type 1 vs Type 2
- Real-time vs near-real-time trade-offs
- KQL vs Spark SQL for analytics
