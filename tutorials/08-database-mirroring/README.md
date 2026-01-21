# Tutorial 08: Database Mirroring

This tutorial covers implementing Database Mirroring to replicate data from external sources into Fabric.

## Learning Objectives

By the end of this tutorial, you will:

1. Understand Database Mirroring concepts
2. Configure SQL Server mirroring
3. Set up Snowflake mirroring
4. Configure Cosmos DB mirroring
5. Monitor replication status

## Database Mirroring Overview

Database Mirroring provides near real-time replication of data into Fabric OneLake.

```
Source Database → Change Data Capture → OneLake → Delta Tables
      │                    │                │           │
   SQL Server         Continuous         Automatic   Query with
   Snowflake          Replication        Conversion   Spark/SQL
   Cosmos DB
```

### Benefits

- **Near real-time** data availability
- **No ETL code** required
- **Automatic schema** synchronization
- **Delta Lake** format in OneLake
- **Query with Spark** or T-SQL

## Prerequisites

- Fabric workspace with capacity
- Source database with appropriate permissions
- Network connectivity to source

## Step 1: SQL Server Mirroring

### Requirements

- SQL Server 2016+ or Azure SQL Database
- CDC (Change Data Capture) enabled
- Network access from Fabric

### Enable CDC on Source Database

```sql
-- Enable CDC on database
EXEC sys.sp_cdc_enable_db;

-- Enable CDC on tables to mirror
EXEC sys.sp_cdc_enable_table
    @source_schema = N'gaming',
    @source_name = N'slot_transactions',
    @role_name = NULL,
    @supports_net_changes = 1;

EXEC sys.sp_cdc_enable_table
    @source_schema = N'gaming',
    @source_name = N'player_sessions',
    @role_name = NULL,
    @supports_net_changes = 1;
```

### Create Mirrored Database in Fabric

1. Open workspace `casino-fabric-poc`
2. Click **+ New** > **Mirrored database**
3. Select **Azure SQL Database** or **SQL Server**

### Configure Connection

1. **Source connection:**
   - Server: `your-sql-server.database.windows.net`
   - Database: `CasinoOperational`
   - Authentication: SQL or Azure AD
2. **Select tables:**
   - `gaming.slot_transactions`
   - `gaming.player_sessions`
   - `gaming.cage_operations`
3. Click **Mirror database**

### Monitor Replication

1. Open the mirrored database
2. View **Replication status**
3. Check:
   - Initial snapshot progress
   - Ongoing replication lag
   - Table sync status

## Step 2: Snowflake Mirroring

### Requirements

- Snowflake account
- Appropriate permissions
- Network connectivity

### Create Mirrored Database

1. **+ New** > **Mirrored database**
2. Select **Snowflake**

### Configure Connection

```
Account: your-account.snowflakecomputing.com
Warehouse: COMPUTE_WH
Database: CASINO_DW
Schema: ANALYTICS
Authentication: User/Password or OAuth
```

### Select Tables

Choose tables to mirror:
- `ANALYTICS.DAILY_SLOT_SUMMARY`
- `ANALYTICS.PLAYER_METRICS`
- `ANALYTICS.COMPLIANCE_REPORTS`

### Start Mirroring

1. Review configuration
2. Click **Start mirroring**
3. Monitor initial sync

## Step 3: Cosmos DB Mirroring

### Requirements

- Azure Cosmos DB account
- Continuous backup enabled
- Change feed enabled

### Create Mirrored Database

1. **+ New** > **Mirrored database**
2. Select **Azure Cosmos DB**

### Configure Connection

```
Account: your-cosmos-account
Database: casino-realtime
Containers:
  - player-activity
  - security-events
  - jackpot-alerts
```

### Considerations for Cosmos DB

- **Nested documents** are flattened
- **Arrays** become separate rows
- **Schema inference** automatic

## Step 4: Query Mirrored Data

### Access in Lakehouse

Mirrored data appears in the designated Lakehouse:

```
lh_mirrored/
├── Tables/
│   ├── slot_transactions/
│   ├── player_sessions/
│   └── cage_operations/
└── _mirroring/
    └── metadata
```

### Query with Spark

```python
# Read mirrored table
df = spark.table("lh_mirrored.slot_transactions")

# Show recent transactions
df.filter(col("transaction_time") > "2024-01-01") \
  .orderBy(col("transaction_time").desc()) \
  .show(10)
```

### Query with SQL

```sql
-- SQL endpoint access
SELECT
    transaction_date,
    COUNT(*) as transaction_count,
    SUM(amount) as total_amount
FROM lh_mirrored.slot_transactions
WHERE transaction_date >= DATEADD(day, -7, GETDATE())
GROUP BY transaction_date
ORDER BY transaction_date DESC;
```

### Join with Existing Data

```python
# Join mirrored data with Gold layer
df_mirrored = spark.table("lh_mirrored.player_sessions")
df_gold = spark.table("lh_gold.gold_player_360")

df_enriched = df_mirrored.join(
    df_gold,
    df_mirrored.player_id == df_gold.player_id,
    "left"
).select(
    df_mirrored["*"],
    df_gold.loyalty_tier,
    df_gold.player_value_score
)
```

## Step 5: Monitor and Manage

### Replication Dashboard

1. Open mirrored database
2. View **Monitor** tab
3. Check metrics:
   - Replication lag
   - Rows synchronized
   - Errors/warnings

### Common Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Replication Lag | Time behind source | < 5 minutes |
| Throughput | Rows/second | Varies by volume |
| Error Rate | Failed operations | 0% |
| Storage Used | OneLake size | Monitor growth |

### Handle Replication Issues

#### Lag Increasing

1. Check source database load
2. Verify network connectivity
3. Review table sizes
4. Consider partitioning

#### Schema Changes

When source schema changes:
1. Mirroring auto-detects most changes
2. For breaking changes, may need to restart
3. New columns added automatically

## Step 6: Integration Patterns

### Hybrid Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     HYBRID ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Operational Sources              Fabric OneLake               │
│   ─────────────────               ──────────────────            │
│                                                                  │
│   ┌──────────┐                    ┌──────────────┐              │
│   │SQL Server│─── Mirroring ────▶│ lh_mirrored  │              │
│   │(OLTP)    │                    │              │              │
│   └──────────┘                    └──────┬───────┘              │
│                                          │                       │
│   ┌──────────┐                    ┌──────▼───────┐              │
│   │Snowflake │─── Mirroring ────▶│  lh_bronze   │              │
│   │(DW)      │                    │  lh_silver   │              │
│   └──────────┘                    │  lh_gold     │              │
│                                   └──────┬───────┘              │
│   ┌──────────┐                          │                       │
│   │Cosmos DB │─── Mirroring ────▶       │                       │
│   │(NoSQL)   │                          ▼                       │
│   └──────────┘                    ┌──────────────┐              │
│                                   │Semantic Model│              │
│                                   │  Power BI    │              │
│                                   └──────────────┘              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Use Cases for Casino

1. **Real-time player tracking**: Cosmos DB → Fabric
2. **Operational reporting**: SQL Server → Fabric
3. **Historical analytics**: Snowflake → Fabric

## Validation Checklist

- [ ] Source database configured (CDC enabled)
- [ ] Mirrored database created in Fabric
- [ ] Initial sync completed
- [ ] Ongoing replication active
- [ ] Data queryable in Fabric
- [ ] Monitoring configured

## Troubleshooting

### Initial Sync Fails

1. Check network connectivity
2. Verify credentials
3. Review table permissions
4. Check for unsupported data types

### Replication Stops

1. Check source database status
2. Review error logs
3. Verify CDC is still enabled
4. Restart mirroring if needed

### Data Inconsistency

1. Compare row counts
2. Check for deleted records
3. Verify CDC capture window
4. Consider full resync

## Best Practices

1. **Start small** - Mirror critical tables first
2. **Monitor lag** - Set up alerts for high latency
3. **Plan for growth** - Consider storage costs
4. **Test failover** - Know how to restart
5. **Document dependencies** - Track what uses mirrored data

## Next Steps

Continue to [Tutorial 09: Advanced AI/ML](../09-advanced-ai-ml/README.md).

## Resources

- [Database Mirroring Overview](https://learn.microsoft.com/fabric/database/mirrored-database/)
- [SQL Server Mirroring](https://learn.microsoft.com/fabric/database/mirrored-database/azure-sql-database)
- [Snowflake Mirroring](https://learn.microsoft.com/fabric/database/mirrored-database/snowflake)
- [Cosmos DB Mirroring](https://learn.microsoft.com/fabric/database/mirrored-database/cosmos-db)
