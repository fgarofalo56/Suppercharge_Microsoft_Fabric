# Architecture Documentation

## Overview

This document describes the architecture of the Microsoft Fabric Casino/Gaming POC environment. The solution implements a modern data lakehouse architecture using the medallion pattern (Bronze/Silver/Gold) with real-time analytics capabilities.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DATA SOURCES                                    │
├──────────┬──────────┬──────────┬──────────┬──────────┬─────────────────────┤
│   Slot   │  Table   │  Player  │ Financial│ Security │    Compliance       │
│ Machines │  Games   │ Loyalty  │   Cage   │Surveillance│   Systems         │
└────┬─────┴────┬─────┴────┬─────┴────┬─────┴────┬─────┴─────────┬───────────┘
     │          │          │          │          │               │
     └──────────┴──────────┴──────────┴──────────┴───────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
              ┌─────▼─────┐  ┌──────▼──────┐  ┌────▼────┐
              │Eventstreams│  │Dataflows G2 │  │Pipelines│
              │ Real-Time  │  │   Batch     │  │  ETL    │
              └─────┬─────┘  └──────┬──────┘  └────┬────┘
                    │               │              │
                    └───────────────┴──────────────┘
                                    │
┌───────────────────────────────────┼───────────────────────────────────────┐
│                         FABRIC LAKEHOUSE                                   │
│                                   │                                        │
│  ┌────────────────────────────────▼────────────────────────────────────┐  │
│  │                         BRONZE LAYER                                 │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │  │
│  │  │  Slot    │ │  Table   │ │  Player  │ │Financial │ │ Security │  │  │
│  │  │Telemetry │ │  Games   │ │ Profile  │ │   Txn    │ │  Events  │  │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘  │  │
│  └─────────────────────────────────┬───────────────────────────────────┘  │
│                                    │                                       │
│  ┌─────────────────────────────────▼───────────────────────────────────┐  │
│  │                         SILVER LAYER                                 │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │  │
│  │  │  Slot    │ │  Table   │ │  Player  │ │Financial │ │ Security │  │  │
│  │  │ Cleansed │ │ Enriched │ │  Master  │ │Reconciled│ │ Enriched │  │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘  │  │
│  └─────────────────────────────────┬───────────────────────────────────┘  │
│                                    │                                       │
│  ┌─────────────────────────────────▼───────────────────────────────────┐  │
│  │                          GOLD LAYER                                  │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │  │
│  │  │  Slot    │ │  Table   │ │  Player  │ │Financial │ │Compliance│  │  │
│  │  │Performance│ │Analytics │ │   360    │ │ Summary  │ │Reporting │  │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘  │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
└───────────────────────────────────┬────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
┌───────▼───────┐          ┌────────▼────────┐         ┌───────▼───────┐
│  Direct Lake  │          │   Eventhouse    │         │   Purview     │
│Semantic Model │          │  KQL Database   │         │  Governance   │
└───────┬───────┘          └────────┬────────┘         └───────────────┘
        │                           │
┌───────▼───────┐          ┌────────▼────────┐
│   Power BI    │          │   Real-Time     │
│   Reports     │          │   Dashboards    │
└───────────────┘          └─────────────────┘
```

## Medallion Architecture

### Bronze Layer (Raw Data)

**Purpose:** Land raw data with minimal transformation for auditability and reprocessing.

| Table | Source | Update Pattern | Retention |
|-------|--------|----------------|-----------|
| `bronze_slot_telemetry` | SAS Protocol / IoT | Streaming | 90 days |
| `bronze_table_games` | Gaming terminals | Micro-batch | 90 days |
| `bronze_player_profile` | Loyalty system | CDC | 90 days |
| `bronze_financial_txn` | Cage system | Batch | 7 years |
| `bronze_security_events` | Surveillance | Streaming | 30 days |
| `bronze_compliance` | Compliance systems | Batch | 7 years |

**Key Characteristics:**
- Schema-on-read approach
- Append-only inserts
- Full source fidelity preserved
- Metadata columns: `_ingested_at`, `_source_file`, `_batch_id`

### Silver Layer (Cleansed Data)

**Purpose:** Validated, cleansed, and enriched data with enforced schema.

| Table | Transformations | SCD Type |
|-------|-----------------|----------|
| `silver_slot_cleansed` | Dedup, null handling, meter validation | Type 1 |
| `silver_table_enriched` | Join game rules, dealer info | Type 1 |
| `silver_player_master` | PII handling, SCD history | Type 2 |
| `silver_financial_reconciled` | Reconciliation, validation | Type 1 |
| `silver_security_enriched` | Event correlation, alert tagging | Type 1 |
| `silver_compliance_validated` | Threshold checks, rule validation | Type 1 |

**Key Characteristics:**
- Schema enforcement (Delta Lake)
- Data quality rules applied
- Referential integrity checked
- Business keys established

### Gold Layer (Business Ready)

**Purpose:** Aggregated, business-oriented views optimized for analytics.

| Table | Grain | Key Metrics |
|-------|-------|-------------|
| `gold_slot_performance` | Machine/Day | Coin-in, Theo, Hold %, Jackpots |
| `gold_table_analytics` | Table/Shift | Drop, Win, Hold %, Hands played |
| `gold_player_360` | Player | LTV, Tier, Churn score, Preferences |
| `gold_financial_summary` | Day/Cage | Deposits, Withdrawals, Fills, Credits |
| `gold_security_dashboard` | Hour/Zone | Incidents, Alerts, Response time |
| `gold_compliance_reporting` | Day/Type | CTR count, SAR count, W-2G count |

**Key Characteristics:**
- Star schema design
- Pre-aggregated metrics
- Direct Lake optimized
- Incremental refresh enabled

## Real-Time Intelligence Architecture

```
┌─────────────────┐
│ Slot Machines   │──┐
│  (SAS Stream)   │  │
└─────────────────┘  │     ┌─────────────┐     ┌─────────────┐
                     ├────▶│ Eventstream │────▶│ Eventhouse  │
┌─────────────────┐  │     │ (Ingestion) │     │(KQL Database)│
│ Table Games     │──┤     └─────────────┘     └──────┬──────┘
│  (RFID/POS)     │  │                                │
└─────────────────┘  │                                │
                     │                         ┌──────▼──────┐
┌─────────────────┐  │                         │ Real-Time   │
│ Security        │──┘                         │ Dashboards  │
│  (Cameras/Access)                            └─────────────┘
└─────────────────┘
```

### Eventhouse Configuration

| Database | Purpose | Retention |
|----------|---------|-----------|
| `casino_realtime` | Live floor monitoring | 7 days |
| `casino_analytics` | Historical analysis | 90 days |

### Key KQL Tables

- `SlotEvents` - Real-time slot machine events
- `TableGameEvents` - Table game transactions
- `SecurityAlerts` - Security incident stream
- `FloorHeatmap` - Aggregated activity by zone

## Data Governance

### Purview Integration

```
┌─────────────────────────────────────────────────────────────────┐
│                     MICROSOFT PURVIEW                            │
├──────────────────┬──────────────────┬───────────────────────────┤
│   Data Catalog   │  Data Lineage    │  Access Policies          │
├──────────────────┼──────────────────┼───────────────────────────┤
│ - Glossary terms │ - End-to-end     │ - Data access policies    │
│ - Classifications│ - Transformation │ - Sensitivity labels      │
│ - Ownership      │ - Impact analysis│ - Row-level security      │
└──────────────────┴──────────────────┴───────────────────────────┘
```

### Data Classification

| Classification | Examples | Handling |
|----------------|----------|----------|
| `Highly Confidential` | SSN, Full card numbers | Encrypted, masked |
| `Confidential` | Player balances, Win/Loss | RBAC restricted |
| `Internal` | Operational metrics | Staff access |
| `Public` | Aggregated reports | Open access |

## Security Architecture

### Network Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      VIRTUAL NETWORK                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  Fabric Subnet  │  │ Private Endpoint │  │  Management     │ │
│  │   10.0.1.0/24   │  │    Subnet        │  │    Subnet       │ │
│  │                 │  │   10.0.2.0/24    │  │   10.0.3.0/24   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │  Private Endpoints │
                    ├───────────────────┤
                    │ - Storage Account │
                    │ - Key Vault       │
                    │ - Purview         │
                    └───────────────────┘
```

### Identity & Access

- **Managed Identity:** System-assigned for Fabric workspace
- **RBAC:** Principle of least privilege
- **Key Vault:** All secrets and certificates
- **Conditional Access:** MFA required for admin operations

## Capacity Planning

### F64 SKU Specifications

| Resource | Allocation |
|----------|------------|
| Compute CUs | 64 |
| Parallel jobs | 16 |
| Max memory per query | 400 GB |
| OneLake storage | Unlimited (pay-per-use) |

### Estimated Resource Usage (POC)

| Workload | CU Consumption |
|----------|----------------|
| Bronze ingestion | 4-8 CUs |
| Silver transformation | 8-16 CUs |
| Gold aggregation | 4-8 CUs |
| Real-time analytics | 8-12 CUs |
| Power BI Direct Lake | 4-8 CUs |

## Disaster Recovery

### RPO/RTO Targets

| Tier | RPO | RTO | Strategy |
|------|-----|-----|----------|
| Bronze | 1 hour | 4 hours | Geo-redundant storage |
| Silver/Gold | 1 hour | 2 hours | Delta Lake time travel |
| Real-time | 5 minutes | 15 minutes | Eventhouse replication |
| Reports | 1 day | 1 hour | Git version control |

## Monitoring & Alerting

### Key Metrics

- **Pipeline Health:** Success rate, latency, data volume
- **Data Quality:** Completeness, validity, freshness
- **Capacity:** CU utilization, throttling events
- **Security:** Access anomalies, failed authentications

### Alert Thresholds

| Metric | Warning | Critical |
|--------|---------|----------|
| Pipeline failure rate | > 5% | > 20% |
| CU utilization | > 80% | > 95% |
| Data freshness (Bronze) | > 15 min | > 1 hour |
| Query latency (P95) | > 5 sec | > 30 sec |

## Technology Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Storage Format | Delta Lake | ACID, time travel, schema evolution |
| Processing | PySpark | Industry standard, Fabric native |
| Real-time | Eventstreams + KQL | Low latency, powerful queries |
| BI Connectivity | Direct Lake | Sub-second queries, no import |
| Governance | Purview | Unified catalog, native integration |
| IaC | Bicep | Azure native, type-safe |
