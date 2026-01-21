# Tutorial 05: Direct Lake & Power BI

This tutorial covers creating Direct Lake semantic models and Power BI reports for casino analytics.

## Learning Objectives

By the end of this tutorial, you will:

1. Understand Direct Lake mode
2. Create a semantic model from Gold tables
3. Define DAX measures for KPIs
4. Build executive and operational reports

## Direct Lake Overview

Direct Lake provides:
- **Sub-second query performance** on Delta tables
- **No data import** - queries go directly to OneLake
- **Automatic refresh** when data changes
- **Full DAX support** for calculations

```
Gold Tables (Delta) → Direct Lake Semantic Model → Power BI Reports
       ↑                        │
  OneLake Storage          Automatic Sync
```

## Prerequisites

- Completed Gold layer tutorials
- Gold tables populated in `lh_gold`
- Power BI license (Pro or Premium)

## Step 1: Create Semantic Model

### From Lakehouse

1. Open `lh_gold` Lakehouse
2. Click **New semantic model**
3. Select tables:
   - `gold_slot_performance`
   - `gold_player_360`
   - `gold_compliance_reporting`
   - `dim_date`
   - `dim_machine`
4. Name: `Casino Analytics Model`
5. Click **Create**

### Verify Direct Lake Mode

1. Open the semantic model
2. Click **Settings**
3. Verify **Storage mode**: Direct Lake
4. Confirm tables show "DirectLake" in diagram

## Step 2: Define Relationships

### Open Model View

1. Click on semantic model
2. Select **Model view**

### Create Relationships

```
dim_date [date_key] → gold_slot_performance [business_date]
dim_machine [machine_id] → gold_slot_performance [machine_id]
dim_date [date_key] → gold_compliance_reporting [report_date]
```

Configure each relationship:
- **Cardinality:** Many-to-One
- **Cross-filter direction:** Single
- **Active:** Yes

## Step 3: Create DAX Measures

### Open DAX Editor

1. In semantic model, click **New measure**
2. Create measures in a "Measures" table

### Slot Performance Measures

```dax
// Total Coin In
Total Coin In =
SUM(gold_slot_performance[total_coin_in])

// Total Coin Out
Total Coin Out =
SUM(gold_slot_performance[total_coin_out])

// Net Win
Net Win =
[Total Coin In] - [Total Coin Out]

// Hold Percentage
Hold % =
DIVIDE([Net Win], [Total Coin In], 0) * 100

// Theoretical Win
Theoretical Win =
SUMX(
    gold_slot_performance,
    gold_slot_performance[total_coin_in] * gold_slot_performance[avg_theoretical_hold]
)

// Hold Variance
Hold Variance =
[Net Win] - [Theoretical Win]

// Games Played
Total Games =
SUM(gold_slot_performance[total_games])

// Unique Players
Unique Players =
SUM(gold_slot_performance[unique_players])

// Average Bet
Avg Bet =
DIVIDE([Total Coin In], [Total Games], 0)

// Win Per Machine
Win Per Machine =
DIVIDE(
    [Net Win],
    DISTINCTCOUNT(gold_slot_performance[machine_id]),
    0
)
```

### Player Measures

```dax
// Total Players
Total Players =
COUNTROWS(gold_player_360)

// VIP Player Count
VIP Players =
CALCULATE(
    COUNTROWS(gold_player_360),
    gold_player_360[vip_flag] = TRUE
)

// High Churn Risk Players
High Churn Risk Players =
CALCULATE(
    COUNTROWS(gold_player_360),
    gold_player_360[churn_risk] = "High"
)

// Average Player Value Score
Avg Player Value =
AVERAGE(gold_player_360[player_value_score])

// Total Player Theo
Total Player Theo =
SUM(gold_player_360[total_theo_win])

// Active Players (30 days)
Active Players 30D =
CALCULATE(
    COUNTROWS(gold_player_360),
    gold_player_360[days_since_visit] <= 30
)
```

### Compliance Measures

```dax
// Total CTR Filings
CTR Count =
SUM(gold_compliance_reporting[ctr_count])

// Total SAR Filings
SAR Count =
SUM(gold_compliance_reporting[sar_count])

// Total W2G Filings
W2G Count =
SUM(gold_compliance_reporting[w2g_count])

// CTR Amount
CTR Total Amount =
SUM(gold_compliance_reporting[ctr_total_amount])

// Compliance Filing Rate
Daily Filing Rate =
DIVIDE(
    [CTR Count] + [SAR Count] + [W2G Count],
    DISTINCTCOUNT(gold_compliance_reporting[report_date]),
    0
)
```

### Time Intelligence Measures

```dax
// Coin In MTD
Coin In MTD =
TOTALMTD([Total Coin In], dim_date[date_key])

// Coin In YTD
Coin In YTD =
TOTALYTD([Total Coin In], dim_date[date_key])

// Net Win Previous Period
Net Win PP =
CALCULATE(
    [Net Win],
    DATEADD(dim_date[date_key], -1, MONTH)
)

// Net Win Growth %
Net Win Growth % =
DIVIDE(
    [Net Win] - [Net Win PP],
    [Net Win PP],
    0
) * 100

// 7-Day Rolling Avg Coin In
Coin In 7D Avg =
AVERAGEX(
    DATESINPERIOD(dim_date[date_key], MAX(dim_date[date_key]), -7, DAY),
    [Total Coin In]
)
```

## Step 4: Create Report - Executive Dashboard

### Create New Report

1. From semantic model, click **Create report**
2. Or in Power BI service, **+ New** > **Report** > Select model

### Page 1: Executive Summary

#### Layout

```
┌────────────────────────────────────────────────────────────┐
│  CASINO EXECUTIVE DASHBOARD              Date: [Slicer]    │
├──────────┬──────────┬──────────┬──────────┬───────────────┤
│  Net Win │ Hold %   │ Players  │ Games    │   Zone Filter │
│  $2.5M   │  8.2%    │  12,450  │ 1.2M     │   [Slicer]    │
├──────────┴──────────┴──────────┴──────────┴───────────────┤
│                    NET WIN TREND                           │
│  [Line Chart - Daily Net Win over time]                   │
├───────────────────────────┬────────────────────────────────┤
│   ZONE PERFORMANCE        │   TOP 10 MACHINES              │
│   [Bar Chart]             │   [Table]                      │
├───────────────────────────┴────────────────────────────────┤
│   COMPLIANCE SUMMARY       │   PLAYER TIER DISTRIBUTION    │
│   CTR: 45  SAR: 12  W2G:   │   [Donut Chart]               │
│   234                      │                                │
└────────────────────────────────────────────────────────────┘
```

#### Create Visuals

**Card Visuals (KPIs):**
1. Net Win - Format: Currency
2. Hold % - Format: Percentage
3. Unique Players - Format: Number
4. Total Games - Format: Number

**Line Chart (Trend):**
- X-axis: `dim_date[date_key]`
- Y-axis: `[Net Win]`
- Legend: (optional) Zone

**Bar Chart (Zone Performance):**
- Y-axis: `gold_slot_performance[zone]`
- X-axis: `[Net Win]`
- Sort: Descending by Net Win

**Table (Top Machines):**
- Columns: machine_id, zone, [Net Win], [Hold %], [Total Games]
- Top N filter: Top 10 by Net Win

**Donut Chart (Player Tiers):**
- Legend: `gold_player_360[loyalty_tier]`
- Values: Count of player_id

### Page 2: Slot Operations

#### Layout

```
┌────────────────────────────────────────────────────────────┐
│  SLOT OPERATIONS                    Filters: [Date] [Zone]│
├──────────────────────────────────────────────────────────┤
│                  MACHINE PERFORMANCE MATRIX               │
│  [Matrix: Zone x Denomination with Coin In, Hold %, Games]│
├───────────────────────────┬────────────────────────────────┤
│   HOURLY ACTIVITY         │   HOLD VARIANCE ANALYSIS      │
│   [Area Chart]            │   [Scatter Plot]              │
├───────────────────────────┼────────────────────────────────┤
│   MANUFACTURER PERF       │   JACKPOT SUMMARY             │
│   [Clustered Bar]         │   [Table with totals]         │
└───────────────────────────┴────────────────────────────────┘
```

### Page 3: Player Analytics

#### Layout

```
┌────────────────────────────────────────────────────────────┐
│  PLAYER ANALYTICS                              [Tier Slicer]│
├──────────┬──────────┬──────────┬──────────────────────────┤
│  Total   │  VIP     │  At Risk │  Avg Value              │
│ Players  │ Players  │ (Churn)  │  Score                  │
├──────────┴──────────┴──────────┴──────────────────────────┤
│           PLAYER VALUE DISTRIBUTION                        │
│  [Histogram of player_value_score]                        │
├───────────────────────────┬────────────────────────────────┤
│   TIER BREAKDOWN          │   CHURN RISK ANALYSIS         │
│   [Stacked Bar]           │   [Pie Chart]                 │
├───────────────────────────┴────────────────────────────────┤
│             TOP PLAYERS BY THEO                            │
│  [Table: player_id, tier, theo, visits, churn_risk]       │
└────────────────────────────────────────────────────────────┘
```

## Step 5: Configure Report Settings

### Publish Report

1. Save report: `Casino Executive Dashboard`
2. Click **Publish**
3. Select workspace: `casino-fabric-poc`

### Set Refresh Schedule

For Direct Lake, data updates automatically. But you can configure:

1. Open report in service
2. Click **Settings**
3. Under **Refresh**, verify "DirectLake - no refresh needed"

### Configure RLS (Row-Level Security)

```dax
// Example: Restrict by zone
[Zone Security] =
VAR CurrentUserZone = LOOKUPVALUE(
    UserZones[Zone],
    UserZones[UserEmail], USERPRINCIPALNAME()
)
RETURN
    gold_slot_performance[zone] = CurrentUserZone
    || CurrentUserZone = "All"
```

## Step 6: Create Paginated Report (Optional)

For compliance reporting that requires exact formatting:

### In Power BI Report Builder

1. Connect to semantic model
2. Create dataset with compliance measures
3. Design tabular layout for CTR/SAR/W2G reports
4. Add parameters for date range
5. Export format: PDF for regulators

## Validation Checklist

- [ ] Semantic model created with Direct Lake
- [ ] Relationships configured correctly
- [ ] All DAX measures calculating
- [ ] Executive dashboard complete
- [ ] Report published to workspace
- [ ] Data refreshing automatically

## Performance Optimization

### For Direct Lake

1. **Pre-aggregate in Gold layer** where possible
2. **Avoid complex calculated columns** - use measures
3. **Limit table columns** - only include needed fields
4. **Use numeric keys** for relationships

### For Reports

1. **Limit visuals per page** - 6-8 maximum
2. **Use slicers efficiently** - dropdown for many values
3. **Avoid ALL function** on large tables
4. **Test with realistic data volumes**

## Troubleshooting

### Fallback to Import Mode

If queries fall back to DirectQuery:
1. Check table doesn't exceed limits
2. Verify no unsupported DAX functions
3. Review complex calculated columns

### Slow Query Performance

1. Check Gold table partitioning
2. Review measure complexity
3. Add filters to reduce data scanned

## Next Steps

Continue to [Tutorial 06: Data Pipelines](../06-data-pipelines/README.md).

## Resources

- [Direct Lake Overview](https://learn.microsoft.com/fabric/data-warehouse/direct-lake-mode)
- [DAX Reference](https://learn.microsoft.com/dax/)
- [Power BI Best Practices](https://learn.microsoft.com/power-bi/guidance/)
