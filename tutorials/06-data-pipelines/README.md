# Tutorial 06: Data Pipelines

This tutorial covers creating orchestrated data pipelines in Microsoft Fabric.

## Learning Objectives

By the end of this tutorial, you will:

1. Create Data Factory pipelines
2. Orchestrate notebook execution
3. Implement incremental loading patterns
4. Handle errors and retries
5. Schedule pipeline runs

## Prerequisites

- Completed Bronze, Silver, Gold tutorials
- Notebooks created for each layer
- Access to Fabric workspace

## Step 1: Create Master Pipeline

### In Fabric Portal

1. Open workspace `casino-fabric-poc`
2. Click **+ New** > **Data pipeline**
3. Name: `pl_medallion_full_load`

### Pipeline Design

```
┌─────────────────────────────────────────────────────────────────┐
│                    pl_medallion_full_load                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌──────────┐     ┌──────────┐     ┌──────────┐               │
│   │  Bronze  │────▶│  Silver  │────▶│   Gold   │               │
│   │ Pipeline │     │ Pipeline │     │ Pipeline │               │
│   └──────────┘     └──────────┘     └──────────┘               │
│        │                │                │                      │
│        ▼                ▼                ▼                      │
│   ┌──────────────────────────────────────────────────┐         │
│   │              On Failure: Send Alert              │         │
│   └──────────────────────────────────────────────────┘         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Step 2: Create Bronze Pipeline

### Create Pipeline

1. **+ New** > **Data pipeline**
2. Name: `pl_bronze_ingestion`

### Add Activities

#### Activity 1: Set Variables

1. Add **Set variable** activity
2. Name: `Set Batch ID`
3. Variable name: `batch_id`
4. Value: `@concat(formatDateTime(utcnow(), 'yyyyMMdd_HHmmss'))`

#### Activity 2: Execute Slot Notebook

1. Add **Notebook** activity
2. Name: `Bronze - Slot Telemetry`
3. Settings:
   - Notebook: `01_bronze_slot_telemetry`
   - Lakehouse: `lh_bronze`
   - Base parameters:
     ```json
     {
       "batch_id": "@variables('batch_id')",
       "source_path": "Files/landing/slot_telemetry/"
     }
     ```

#### Activity 3-6: Additional Notebooks

Add parallel notebooks for:
- `Bronze - Player Profile`
- `Bronze - Financial Txn`
- `Bronze - Table Games`
- `Bronze - Security Events`
- `Bronze - Compliance`

### Configure Parallel Execution

1. Select all Bronze notebooks
2. Connect from `Set Batch ID` with **On success**
3. All notebooks will run in parallel

### Complete Pipeline

```
Set Batch ID
     │
     └─┬─────┬─────┬─────┬─────┬─────┐
       │     │     │     │     │     │
       ▼     ▼     ▼     ▼     ▼     ▼
    Slot  Player Finance Table Security Compliance
       │     │     │     │     │     │
       └─────┴─────┴─────┴─────┴─────┘
                     │
                     ▼
              Verify Bronze
```

## Step 3: Create Silver Pipeline

### Create Pipeline

Name: `pl_silver_transformation`

### Activities

```
┌─────────────────────────────────────────────────────────────────┐
│                    pl_silver_transformation                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌──────────────┐                                              │
│   │ Get Watermark│                                              │
│   └──────┬───────┘                                              │
│          │                                                       │
│          ▼                                                       │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │
│   │ Silver Slot  │───▶│Silver Player │───▶│Silver Finance│     │
│   │  (Parallel)  │    │  (SCD Type2) │    │ (Sequential) │     │
│   └──────────────┘    └──────────────┘    └──────────────┘     │
│          │                                       │               │
│          └───────────────────┬───────────────────┘               │
│                              ▼                                   │
│                    ┌─────────────────┐                          │
│                    │ Update Watermark │                          │
│                    └─────────────────┘                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Watermark Pattern

#### Get Watermark Activity

1. Add **Lookup** activity
2. Name: `Get Last Watermark`
3. Settings:
   - Source: `watermark_table`
   - Query: `SELECT MAX(last_processed) as watermark FROM watermarks WHERE table_name = 'silver_slot'`

#### Pass Watermark to Notebook

```json
{
  "watermark": "@activity('Get Last Watermark').output.firstRow.watermark"
}
```

#### Update Watermark Activity

1. Add **Stored procedure** or **Script** activity
2. Update watermark after successful processing

## Step 4: Create Gold Pipeline

### Create Pipeline

Name: `pl_gold_aggregation`

### Activities

```
┌─────────────────────────────────────────────────────────────────┐
│                      pl_gold_aggregation                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌──────────────┐                                              │
│   │Slot Performance│                                            │
│   └──────┬───────┘                                              │
│          │                                                       │
│          ▼                                                       │
│   ┌──────────────┐                                              │
│   │ Player 360   │                                              │
│   └──────┬───────┘                                              │
│          │                                                       │
│          ▼                                                       │
│   ┌──────────────┐    ┌──────────────┐                         │
│   │ Compliance   │───▶│  Optimize    │                         │
│   │  Reporting   │    │   Tables     │                         │
│   └──────────────┘    └──────────────┘                         │
│                              │                                   │
│                              ▼                                   │
│                    ┌─────────────────┐                          │
│                    │ Refresh Semantic│                          │
│                    │     Model       │                          │
│                    └─────────────────┘                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Optimize Tables Activity

```sql
-- Run after Gold aggregations
OPTIMIZE gold_slot_performance ZORDER BY (machine_id);
OPTIMIZE gold_player_360 ZORDER BY (player_id);
VACUUM gold_slot_performance RETAIN 168 HOURS;
```

## Step 5: Error Handling

### Add Error Handler

1. Add **If Condition** activity after each notebook
2. Condition: `@equals(activity('Notebook').Status, 'Failed')`
3. On True: Execute error handling

### Error Logging

Create a logging notebook that captures:

```python
# Error logging
error_log = {
    "pipeline_name": pipeline_name,
    "activity_name": activity_name,
    "error_message": error_message,
    "timestamp": datetime.utcnow(),
    "run_id": run_id
}

spark.createDataFrame([error_log]).write \
    .mode("append") \
    .saveAsTable("pipeline_error_log")
```

### Retry Configuration

1. Click on notebook activity
2. Go to **Settings** > **Retry**
3. Configure:
   - Retry count: 3
   - Retry interval: 30 seconds

## Step 6: Master Orchestration

### Create Master Pipeline

Name: `pl_casino_daily_refresh`

```
┌─────────────────────────────────────────────────────────────────┐
│                    pl_casino_daily_refresh                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌──────────────┐                                              │
│   │    Start     │                                              │
│   │  (Schedule)  │                                              │
│   └──────┬───────┘                                              │
│          │                                                       │
│          ▼                                                       │
│   ┌──────────────┐                                              │
│   │    Bronze    │                                              │
│   │   Pipeline   │─────────────┐                                │
│   └──────┬───────┘             │                                │
│          │ On Success          │ On Failure                     │
│          ▼                     ▼                                 │
│   ┌──────────────┐      ┌─────────────┐                        │
│   │    Silver    │      │ Send Alert  │                        │
│   │   Pipeline   │─────▶│   (Email)   │                        │
│   └──────┬───────┘      └─────────────┘                        │
│          │ On Success                                           │
│          ▼                                                       │
│   ┌──────────────┐                                              │
│   │     Gold     │                                              │
│   │   Pipeline   │                                              │
│   └──────┬───────┘                                              │
│          │ On Success                                           │
│          ▼                                                       │
│   ┌──────────────┐                                              │
│   │   Complete   │                                              │
│   │  (Success)   │                                              │
│   └──────────────┘                                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Add Execute Pipeline Activities

1. **Execute pipeline** activity for each sub-pipeline
2. Configure **Wait on completion**: Yes
3. Set **On success** and **On failure** paths

## Step 7: Schedule Pipeline

### Create Trigger

1. Open `pl_casino_daily_refresh`
2. Click **Schedule**
3. Configure:
   - Recurrence: Daily
   - Time: 6:00 AM UTC (after gaming day ends)
   - Time zone: Select appropriate
4. Click **Apply**

### Monitor Runs

1. Go to **Monitor** in Fabric workspace
2. View pipeline runs
3. Check activity status
4. Review error logs

## Pipeline Parameters

### Parameterize Pipelines

```json
// Pipeline parameters
{
  "environment": "dev",
  "date_override": "",
  "full_refresh": false
}
```

### Use in Activities

```json
// Notebook base parameters
{
  "environment": "@pipeline().parameters.environment",
  "process_date": "@if(empty(pipeline().parameters.date_override), formatDateTime(utcnow(), 'yyyy-MM-dd'), pipeline().parameters.date_override)",
  "is_full_refresh": "@pipeline().parameters.full_refresh"
}
```

## Validation Checklist

- [ ] Bronze pipeline runs successfully
- [ ] Silver pipeline with incremental load
- [ ] Gold pipeline with optimizations
- [ ] Error handling configured
- [ ] Master pipeline orchestration
- [ ] Schedule trigger created
- [ ] Monitoring working

## Best Practices

1. **Fail fast** - Stop early on critical errors
2. **Idempotent operations** - Safe to re-run
3. **Logging** - Capture all pipeline metadata
4. **Alerts** - Notify on failures immediately
5. **Documentation** - Comment complex logic

## Next Steps

Continue to [Tutorial 07: Governance & Purview](../07-governance-purview/README.md).

## Resources

- [Data Factory in Fabric](https://learn.microsoft.com/fabric/data-factory/)
- [Pipeline Activities](https://learn.microsoft.com/fabric/data-factory/activity-overview)
- [Orchestration Patterns](https://learn.microsoft.com/fabric/data-factory/pipeline-runs)
