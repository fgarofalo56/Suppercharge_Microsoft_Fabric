# Instructor Guide - Casino Fabric POC

## Overview

This guide provides instructors with everything needed to deliver the 3-day Microsoft Fabric POC for casino/gaming analytics.

---

## Pre-POC Preparation

### 2 Weeks Before

- [ ] Verify Azure subscription has sufficient credits/budget
- [ ] Confirm F64 capacity is available
- [ ] Test data generator scripts work correctly
- [ ] Validate all notebooks execute without errors
- [ ] Prepare participant list and roles
- [ ] Send pre-reading materials to participants

### 1 Week Before

- [ ] Generate sample data (run all generators)
- [ ] Upload sample data to OneLake
- [ ] Create backup of working notebooks
- [ ] Test Purview connectivity
- [ ] Prepare SQL Server source for mirroring demo (if available)
- [ ] Set up communication channels (Teams, email)

### Day Before

- [ ] Verify workspace is accessible
- [ ] Test all Power BI reports render
- [ ] Prepare demo environment
- [ ] Print handouts (if needed)
- [ ] Test projector/screen sharing

---

## Environment Setup Checklist

### Azure Resources Required

| Resource | SKU | Purpose |
|----------|-----|---------|
| Fabric Capacity | F64 | POC workload |
| Purview Account | Standard | Data governance |
| SQL Server (optional) | Standard | Mirroring demo |
| Storage Account | Standard LRS | Landing zone |

### Fabric Workspace Configuration

```yaml
Workspace Name: casino-fabric-poc
Capacity: F64
Workloads:
  - Data Engineering: Enabled
  - Data Science: Enabled
  - Data Warehouse: Enabled
  - Real-Time Intelligence: Enabled
  - Power BI: Enabled
```

### Lakehouses

| Lakehouse | Purpose | Tables |
|-----------|---------|--------|
| lh_bronze | Raw data | 6 tables |
| lh_silver | Cleansed | 6 tables |
| lh_gold | Business-ready | 3+ tables |
| lh_mirrored | Mirrored data | Varies |

---

## Data Generation Instructions

### Generate All Data

```bash
cd data-generation

# Install dependencies
pip install -r requirements.txt

# Generate slot machine data (500K records, 30 days)
python generate.py slot_machine \
    --records 500000 \
    --days 30 \
    --output ../sample-data/slot_telemetry/

# Generate player profiles (10K records)
python generate.py player \
    --records 10000 \
    --output ../sample-data/player_profiles/

# Generate table games (100K records, 30 days)
python generate.py table_games \
    --records 100000 \
    --days 30 \
    --output ../sample-data/table_games/

# Generate financial transactions (50K records, 30 days)
python generate.py financial \
    --records 50000 \
    --days 30 \
    --output ../sample-data/financial/

# Generate security events (10K records, 30 days)
python generate.py security \
    --records 10000 \
    --days 30 \
    --output ../sample-data/security/

# Generate compliance data (5K records, 30 days)
python generate.py compliance \
    --records 5000 \
    --days 30 \
    --output ../sample-data/compliance/
```

### Verify Data Quality

```python
import pandas as pd
import os

# Check all files generated
data_dirs = ['slot_telemetry', 'player_profiles', 'table_games',
             'financial', 'security', 'compliance']

for dir_name in data_dirs:
    path = f'../sample-data/{dir_name}'
    if os.path.exists(path):
        files = os.listdir(path)
        print(f"{dir_name}: {len(files)} files")
        if files:
            df = pd.read_parquet(os.path.join(path, files[0]))
            print(f"  Sample rows: {len(df)}, columns: {df.columns.tolist()}")
    else:
        print(f"{dir_name}: MISSING")
```

---

## Session Facilitation Guide

### Day 1: Medallion Foundation

#### Morning Sessions (9:00 - 12:30)

**Key Teaching Points:**
1. Why medallion architecture?
   - Separation of concerns
   - Data quality progression
   - Auditability

2. Bronze layer principles:
   - Immutable storage
   - Append-only pattern
   - Source fidelity

**Common Participant Questions:**

Q: "Why not transform data immediately at ingestion?"
A: Bronze preserves the original data for auditing, debugging, and reprocessing. You can always rebuild Silver/Gold from Bronze.

Q: "How do we handle schema changes in source systems?"
A: Bronze uses schema-on-read with `mergeSchema` option. Discuss evolution strategies.

Q: "What about real-time data?"
A: Preview Day 2's Eventhouse content. Bronze can receive streaming data too.

**Hands-On Exercises:**
- Exercise 1: Create Bronze table for slot telemetry (guided)
- Exercise 2: Create Bronze table for table games (independent)
- Exercise 3: Add custom metadata columns

#### Afternoon Sessions (13:30 - 17:00)

**Key Teaching Points:**
1. Player profile PII handling
   - Hash SSN at Bronze layer
   - Never store clear-text sensitive data

2. Financial data patterns
   - CTR threshold ($10,000)
   - Near-CTR flagging ($8,000-$9,999)

3. Silver layer introduction
   - Schema enforcement
   - Data quality rules

**Hands-On Exercises:**
- Exercise 4: Implement PII hashing
- Exercise 5: Add CTR flags to financial data
- Exercise 6: Write first Silver transformation

---

### Day 2: Transformations & Real-Time

#### Morning Sessions (9:00 - 12:30)

**Key Teaching Points:**
1. SCD Type 2 pattern
   - Why track history?
   - Effective dating
   - Current record flag

2. Financial reconciliation
   - Variance detection
   - Risk flagging

3. Gold layer KPIs
   - Theo calculation
   - Hold percentage
   - Player value score

**Common Participant Questions:**

Q: "When should we use SCD Type 1 vs Type 2?"
A: Type 1 for attributes that don't need history (e.g., email preference). Type 2 for business-critical attributes (e.g., loyalty tier, address for compliance).

Q: "How often should Gold tables refresh?"
A: Depends on use case. Daily for reports, more frequently for operational dashboards. Direct Lake enables near-real-time.

**Hands-On Exercises:**
- Exercise 7: Implement SCD Type 2 merge
- Exercise 8: Create reconciliation status
- Exercise 9: Calculate slot KPIs

#### Afternoon Sessions (13:30 - 17:00)

**Key Teaching Points:**
1. Eventhouse vs Lakehouse
   - When to use each
   - Query performance trade-offs

2. KQL basics
   - Time-series analysis
   - Aggregations
   - Alerts

3. Real-time dashboards
   - Auto-refresh
   - Tile configuration

**Demo Script - Streaming Producer:**

```python
# Run this in a separate terminal to simulate real-time data
# Show participants how data flows through Eventstream to KQL

import json
import time
import random
from datetime import datetime

while True:
    event = {
        "machine_id": f"SLOT-{random.randint(1000, 9999)}",
        "event_type": "GAME_PLAY",
        "event_timestamp": datetime.utcnow().isoformat(),
        "coin_in": round(random.uniform(1, 100), 2),
        "coin_out": round(random.uniform(0, 80), 2),
        "zone": random.choice(["North", "South", "East", "West"])
    }
    print(json.dumps(event))
    time.sleep(0.5)
```

**Hands-On Exercises:**
- Exercise 10: Create Eventhouse and database
- Exercise 11: Write KQL monitoring query
- Exercise 12: Build real-time dashboard tile

---

### Day 3: BI, Governance & Mirroring

#### Morning Sessions (9:00 - 12:30)

**Key Teaching Points:**
1. Direct Lake benefits
   - No data import
   - Sub-second queries
   - Automatic refresh

2. DAX best practices
   - Measures vs calculated columns
   - Time intelligence

3. Report design
   - Executive vs operational views
   - Drill-through patterns

**Expanded Audience:**
Day 3 morning adds BI developers (2) to the architects (4).

**Common Participant Questions:**

Q: "What happens if Direct Lake falls back to DirectQuery?"
A: Discuss fallback triggers and how to avoid them (table size, unsupported DAX).

Q: "Can we use Import mode instead?"
A: Yes, but you lose automatic refresh. Discuss trade-offs.

**Hands-On Exercises:**
- Exercise 13: Create semantic model
- Exercise 14: Write DAX measures
- Exercise 15: Build executive dashboard

#### Afternoon Sessions (13:30 - 17:00)

**Key Teaching Points:**
1. Purview value proposition
   - Data discovery
   - Compliance
   - Lineage

2. Classifications
   - Automatic vs manual
   - Gaming-specific patterns

3. Database Mirroring
   - Use cases
   - Limitations
   - Hybrid patterns

**Expanded Audience:**
Day 3 afternoon includes all teams (10+).

**Demo Script - Mirroring:**
If SQL Server source is available:
1. Show CDC configuration
2. Create mirrored database
3. Query mirrored data
4. Show replication lag

If no source available:
1. Walk through UI steps
2. Discuss architecture patterns
3. Show documentation

**Hands-On Exercises:**
- Exercise 16: Connect Purview to Fabric
- Exercise 17: Create glossary terms
- Exercise 18: View lineage

---

## Troubleshooting Guide

### Common Issues

#### Workspace Access
**Symptom:** Participants can't access workspace
**Solution:**
1. Check workspace permissions
2. Verify capacity assignment
3. Clear browser cache

#### Notebook Failures
**Symptom:** Notebook times out or fails
**Solution:**
1. Check Spark session state
2. Reduce data volume for testing
3. Verify Lakehouse attachment

#### Eventstream Not Flowing
**Symptom:** No data appearing in KQL
**Solution:**
1. Check source connection
2. Verify JSON mapping
3. Review ingestion errors

#### Direct Lake Fallback
**Symptom:** Reports show DirectQuery instead of Direct Lake
**Solution:**
1. Check table size limits
2. Review measure complexity
3. Verify relationships

#### Purview Scan Fails
**Symptom:** Scan shows errors
**Solution:**
1. Verify integration runtime
2. Check credentials
3. Review firewall rules

---

## Assessment Checkpoints

### Day 1 End

| Checkpoint | Criteria | Pass/Fail |
|------------|----------|-----------|
| Environment | 3 Lakehouses created | |
| Bronze Slot | 500K+ records | |
| Bronze Player | 10K records, SSN hashed | |
| Bronze Financial | CTR flags added | |
| Silver Started | At least 1 Silver table | |

### Day 2 End

| Checkpoint | Criteria | Pass/Fail |
|------------|----------|-----------|
| SCD Type 2 | Player history tracking | |
| Gold KPIs | Hold %, Net Win calculating | |
| Eventhouse | Database created | |
| KQL Queries | 3+ monitoring queries | |
| Real-Time Dashboard | 4+ tiles | |

### Day 3 End

| Checkpoint | Criteria | Pass/Fail |
|------------|----------|-----------|
| Semantic Model | Direct Lake mode | |
| DAX Measures | 10+ measures | |
| Reports | 3 reports complete | |
| Purview | Scan complete, terms added | |
| Lineage | Visible for Gold tables | |

---

## Participant Materials

### Pre-Reading

1. [Microsoft Fabric Overview](https://learn.microsoft.com/fabric/get-started/microsoft-fabric-overview)
2. [Medallion Architecture](https://learn.microsoft.com/fabric/data-engineering/lakehouse-medallion-architecture)
3. [Direct Lake Mode](https://learn.microsoft.com/fabric/data-warehouse/direct-lake-mode)

### Reference Cards

Provide printed/PDF reference cards for:
- Delta Lake commands
- Common KQL queries
- DAX formula patterns
- Keyboard shortcuts

### Post-POC Resources

- Full tutorial documentation (this repo)
- Microsoft Learn paths
- Community forums
- Support contacts

---

## Feedback Collection

### Daily Feedback

At end of each day, collect:
1. What worked well?
2. What could be improved?
3. Pace rating (1-5)
4. Content clarity (1-5)

### Post-POC Survey

Send within 1 week:
1. Overall satisfaction
2. Most valuable content
3. Least valuable content
4. Recommendations for future
5. Production readiness assessment

---

## Contact Information

**POC Lead:** [Name] - [Email]
**Microsoft Contact:** [Name] - [Email]
**Technical Support:** [Email/Teams channel]

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-21 | Initial release |
