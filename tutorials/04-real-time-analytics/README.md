# Tutorial 04: Real-Time Analytics

This tutorial covers implementing real-time analytics for casino floor monitoring using Fabric Real-Time Intelligence.

## Learning Objectives

By the end of this tutorial, you will:

1. Create an Eventhouse with KQL database
2. Configure Eventstreams for data ingestion
3. Write KQL queries for real-time monitoring
4. Build real-time dashboards

## Real-Time Intelligence Overview

```
Data Sources → Eventstreams → Eventhouse → KQL Queries → Dashboards
                    │               │
                    │               └── Real-Time Aggregations
                    └── Transformation & Routing
```

## Prerequisites

- Completed Gold layer tutorials
- Access to Fabric workspace with Real-Time Intelligence
- Sample streaming data or Event Hub

## Step 1: Create Eventhouse

### In Fabric Portal

1. Open your workspace (`casino-fabric-poc`)
2. Click **+ New** > **Eventhouse**
3. Configure:
   - Name: `eh_casino_realtime`
   - Enable OneLake availability: Yes
4. Click **Create**

### Create KQL Database

After Eventhouse creation:

1. Click on the Eventhouse
2. Click **+ New database**
3. Name: `casino_floor_monitoring`
4. Click **Create**

## Step 2: Define Tables

### Open KQL Query Editor

1. Click on the database
2. Click **Explore your data**

### Create Slot Events Table

```kql
// Create table for real-time slot events
.create table SlotEvents (
    event_id: string,
    machine_id: string,
    zone: string,
    event_type: string,
    event_timestamp: datetime,
    coin_in: real,
    coin_out: real,
    jackpot_amount: real,
    player_id: string,
    denomination: real,
    ingestion_time: datetime
)

// Create mapping for JSON ingestion
.create table SlotEvents ingestion json mapping 'SlotEventsMapping'
```
[
    {"column": "event_id", "path": "$.event_id"},
    {"column": "machine_id", "path": "$.machine_id"},
    {"column": "zone", "path": "$.zone"},
    {"column": "event_type", "path": "$.event_type"},
    {"column": "event_timestamp", "path": "$.event_timestamp"},
    {"column": "coin_in", "path": "$.coin_in"},
    {"column": "coin_out", "path": "$.coin_out"},
    {"column": "jackpot_amount", "path": "$.jackpot_amount"},
    {"column": "player_id", "path": "$.player_id"},
    {"column": "denomination", "path": "$.denomination"},
    {"column": "ingestion_time", "path": "$.ingestion_time"}
]
```

### Create Security Events Table

```kql
.create table SecurityEvents (
    event_id: string,
    event_type: string,
    event_timestamp: datetime,
    zone: string,
    severity: string,
    description: string,
    responding_officer: string,
    resolution_status: string
)
```

### Create Floor Activity Table

```kql
.create table FloorActivity (
    timestamp: datetime,
    zone: string,
    active_machines: int,
    active_players: int,
    coin_in_rate: real,
    jackpot_count: int
)
```

## Step 3: Configure Eventstream

### Create Eventstream

1. In workspace, click **+ New** > **Eventstream**
2. Name: `es_slot_telemetry`
3. Click **Create**

### Add Source

#### Option A: Event Hub Source

1. Click **Add source** > **External sources** > **Azure Event Hubs**
2. Configure:
   - Connection: Create new or select existing
   - Consumer group: `$Default`
   - Data format: JSON
3. Click **Add**

#### Option B: Custom App Source (for testing)

1. Click **Add source** > **Custom app**
2. Copy the connection string
3. Use Python producer (see Step 6)

### Add Destination

1. Click **Add destination** > **Eventhouse**
2. Select:
   - Eventhouse: `eh_casino_realtime`
   - Database: `casino_floor_monitoring`
   - Table: `SlotEvents`
3. Configure mapping if needed
4. Click **Add**

### Activate Eventstream

1. Review the data flow diagram
2. Click **Publish** to activate

## Step 4: KQL Queries for Monitoring

### Real-Time Slot Activity

```kql
// Last 5 minutes of slot activity by zone
SlotEvents
| where event_timestamp > ago(5m)
| where event_type == "GAME_PLAY"
| summarize
    total_games = count(),
    total_coin_in = sum(coin_in),
    total_coin_out = sum(coin_out),
    unique_players = dcount(player_id),
    active_machines = dcount(machine_id)
by zone
| extend net_win = total_coin_in - total_coin_out
| order by total_coin_in desc
```

### Jackpot Alerts (Real-Time)

```kql
// Recent jackpots (last 15 minutes)
SlotEvents
| where event_timestamp > ago(15m)
| where event_type in ("JACKPOT", "HAND_PAY")
| where jackpot_amount > 0
| project
    event_timestamp,
    machine_id,
    zone,
    jackpot_amount,
    player_id
| order by event_timestamp desc
| take 20
```

### Machine Performance Trends

```kql
// Hourly slot performance trend
SlotEvents
| where event_timestamp > ago(24h)
| where event_type == "GAME_PLAY"
| summarize
    total_coin_in = sum(coin_in),
    total_coin_out = sum(coin_out),
    games = count()
by bin(event_timestamp, 1h), zone
| extend hold_rate = (total_coin_in - total_coin_out) / total_coin_in * 100
| render timechart
```

### Hot/Cold Machine Detection

```kql
// Machines with unusual hold rates (last hour)
SlotEvents
| where event_timestamp > ago(1h)
| where event_type == "GAME_PLAY"
| summarize
    coin_in = sum(coin_in),
    coin_out = sum(coin_out),
    games = count()
by machine_id, zone
| where coin_in > 100  // Minimum threshold
| extend hold_pct = (coin_in - coin_out) / coin_in * 100
| extend machine_status = case(
    hold_pct > 15, "HOT - High Hold",
    hold_pct < -5, "COLD - Paying Out",
    "NORMAL")
| where machine_status != "NORMAL"
| order by hold_pct desc
```

### Floor Heatmap Data

```kql
// Zone activity for heatmap visualization
SlotEvents
| where event_timestamp > ago(30m)
| summarize
    activity_score = count(),
    coin_in = sum(coin_in),
    players = dcount(player_id)
by zone
| extend activity_level = case(
    activity_score > 1000, "Very High",
    activity_score > 500, "High",
    activity_score > 100, "Medium",
    "Low")
```

## Step 5: Create Real-Time Dashboard

### In Fabric Portal

1. Click **+ New** > **Real-Time Dashboard**
2. Name: `Casino Floor Monitor`

### Add Tiles

#### Tile 1: Active Floor Summary

```kql
SlotEvents
| where event_timestamp > ago(5m)
| summarize
    active_machines = dcount(machine_id),
    active_players = dcount(player_id),
    games_per_minute = count() / 5.0,
    coin_in = sum(coin_in)
```

Configure as: **Stat tile** with 4 values

#### Tile 2: Zone Activity Chart

```kql
SlotEvents
| where event_timestamp > ago(1h)
| summarize coin_in = sum(coin_in) by bin(event_timestamp, 5m), zone
| render areachart
```

Configure as: **Area chart**

#### Tile 3: Recent Jackpots

```kql
SlotEvents
| where event_timestamp > ago(1h)
| where jackpot_amount > 0
| project event_timestamp, machine_id, zone, jackpot_amount
| order by event_timestamp desc
| take 10
```

Configure as: **Table**

#### Tile 4: Alert Panel

```kql
// Combine multiple alert conditions
let hot_machines = SlotEvents
| where event_timestamp > ago(30m)
| where event_type == "GAME_PLAY"
| summarize ci = sum(coin_in), co = sum(coin_out) by machine_id
| where ci > 0
| extend hold = (ci - co) / ci * 100
| where hold > 20
| project alert_type = "Hot Machine", detail = machine_id, value = hold;
let big_jackpots = SlotEvents
| where event_timestamp > ago(30m)
| where jackpot_amount > 10000
| project alert_type = "Big Jackpot", detail = machine_id, value = jackpot_amount;
union hot_machines, big_jackpots
| order by value desc
```

Configure as: **Table** with conditional formatting

### Set Auto-Refresh

1. Click **Settings** on dashboard
2. Set **Auto refresh**: 30 seconds
3. Save changes

## Step 6: Streaming Data Producer (Testing)

### Python Event Producer

Create file: `data-generation/generators/streaming/event_producer.py`

```python
"""
Real-Time Event Producer
Sends simulated slot events to Event Hub or Eventstream
"""

import json
import time
import random
from datetime import datetime
from azure.eventhub import EventHubProducerClient, EventData

# Configuration
CONNECTION_STRING = "your_eventstream_connection_string"
EVENTHUB_NAME = "es_slot_telemetry"

# Simulated machines
MACHINES = [f"SM-{i:05d}" for i in range(1, 501)]
ZONES = ["Main Floor", "High Limit", "VIP", "Penny Palace", "Non-Smoking"]
EVENT_TYPES = ["GAME_PLAY", "JACKPOT", "METER_UPDATE"]
EVENT_WEIGHTS = [0.90, 0.02, 0.08]

def generate_event():
    """Generate a single slot event."""
    machine_id = random.choice(MACHINES)
    event_type = random.choices(EVENT_TYPES, EVENT_WEIGHTS)[0]

    event = {
        "event_id": f"EVT-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
        "machine_id": machine_id,
        "zone": random.choice(ZONES),
        "event_type": event_type,
        "event_timestamp": datetime.utcnow().isoformat(),
        "denomination": random.choice([0.01, 0.05, 0.25, 1.00, 5.00]),
        "ingestion_time": datetime.utcnow().isoformat()
    }

    if event_type == "GAME_PLAY":
        coin_in = round(random.uniform(0.25, 50), 2)
        # House edge ~8%
        if random.random() > 0.08:
            coin_out = round(coin_in * random.uniform(0, 2), 2)
        else:
            coin_out = 0
        event["coin_in"] = coin_in
        event["coin_out"] = coin_out
        event["jackpot_amount"] = 0
        if random.random() < 0.6:
            event["player_id"] = f"PLY-{random.randint(1, 10000):06d}"

    elif event_type == "JACKPOT":
        event["coin_in"] = 0
        event["coin_out"] = 0
        event["jackpot_amount"] = round(random.uniform(1200, 50000), 2)
        event["player_id"] = f"PLY-{random.randint(1, 10000):06d}"

    return event

def main():
    """Main producer loop."""
    producer = EventHubProducerClient.from_connection_string(
        conn_str=CONNECTION_STRING,
        eventhub_name=EVENTHUB_NAME
    )

    print("Starting event producer...")
    print(f"Target: {EVENTHUB_NAME}")
    print("Press Ctrl+C to stop")

    events_sent = 0
    try:
        while True:
            # Create batch
            event_batch = producer.create_batch()

            # Generate 10-50 events per batch
            batch_size = random.randint(10, 50)
            for _ in range(batch_size):
                event = generate_event()
                event_batch.add(EventData(json.dumps(event)))

            # Send batch
            producer.send_batch(event_batch)
            events_sent += batch_size

            print(f"Sent {events_sent} events", end="\r")

            # Wait before next batch (simulate ~100 events/second)
            time.sleep(0.1)

    except KeyboardInterrupt:
        print(f"\nStopped. Total events sent: {events_sent}")
    finally:
        producer.close()

if __name__ == "__main__":
    main()
```

### Run Producer

```bash
pip install azure-eventhub
python data-generation/generators/streaming/event_producer.py
```

## Validation Checklist

- [ ] Eventhouse created
- [ ] KQL database with tables
- [ ] Eventstream configured and active
- [ ] Data flowing to KQL tables
- [ ] Queries returning results
- [ ] Real-time dashboard updating

## Troubleshooting

### No Data in Tables

1. Check Eventstream status (should be "Running")
2. Verify source connection
3. Check ingestion mapping matches JSON structure

### Query Performance Issues

1. Add time filters to limit data scanned
2. Use `| take N` for testing
3. Check ingestion latency

### Dashboard Not Updating

1. Verify auto-refresh is enabled
2. Check query returns data
3. Confirm Eventhouse connectivity

## Next Steps

Continue to [Tutorial 05: Direct Lake & Power BI](../05-direct-lake-powerbi/README.md).

## Resources

- [Real-Time Intelligence Overview](https://learn.microsoft.com/fabric/real-time-intelligence/)
- [KQL Quick Reference](https://learn.microsoft.com/azure/data-explorer/kusto/query/)
- [Eventstreams](https://learn.microsoft.com/fabric/real-time-intelligence/event-streams/)
