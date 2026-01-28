# 📖 Tutorials

> 🏠 [Home](../README.md) > 📖 Tutorials

**Last Updated:** `2026-01-28` | **Version:** 1.1.0

---

## 📑 Table of Contents

- [🎯 Overview](#-overview)
- [🗺️ Learning Path](#️-learning-path)
- [📋 Tutorial Index](#-tutorial-index)
- [⏱️ Time Estimates](#️-time-estimates)
- [📋 Prerequisites](#-prerequisites)

---

## 🎯 Overview

This tutorial series guides you through implementing a complete Microsoft Fabric data platform for casino/gaming analytics. Starting from environment setup through advanced AI/ML, you'll learn industry best practices for medallion architecture, real-time analytics, and data governance.

### What You'll Build

```mermaid
flowchart LR
    subgraph L1["🟢 Foundation"]
        T00[00-Setup]
        T01[01-Bronze]
    end

    subgraph L2["🟡 Core"]
        T02[02-Silver]
        T03[03-Gold]
    end

    subgraph L3["🟠 Advanced"]
        T04[04-Real-Time]
        T05[05-Direct Lake]
    end

    subgraph L4["🔴 Enterprise"]
        T06[06-Pipelines]
        T07[07-Governance]
        T08[08-Mirroring]
        T09[09-AI/ML]
    end

    subgraph L5["🟣 Migration & Integration"]
        T10[10-Teradata]
        T11[11-SAS]
    end

    subgraph L6["🔵 DevOps & Planning"]
        T12[12-CI/CD]
        T13[13-Planning]
    end

    subgraph L7["⚪ Operations & Governance"]
        T14[14-Security]
        T15[15-Cost]
        T16[16-Performance]
        T17[17-Monitoring]
    end

    subgraph L8["🟤 Collaboration & AI"]
        T18[18-Sharing]
        T19[19-Copilot]
    end

    subgraph L9["🟡 Infrastructure & GeoAnalytics"]
        T20[20-Workspace]
        T21[21-GeoAnalytics]
        T22[22-Networking]
        T23[23-Gateways]
    end

    T00 --> T01 --> T02 --> T03 --> T04 --> T05
    T05 --> T06 --> T07 --> T08 --> T09
    T09 --> T10 --> T11
    T11 --> T12 --> T13
    T13 --> T14 --> T15 --> T16 --> T17
    T17 --> T18 --> T19
    T19 --> T20 --> T21 --> T22 --> T23
```

---

## 🗺️ Learning Path

### Recommended Order

Complete tutorials in sequence for the best learning experience:

```
╔════════╦════════╦════════╦════════╦════════╦════════╦════════╦════════╦════════╦════════╗
║   00   ║   01   ║   02   ║   03   ║   04   ║   05   ║   06   ║   07   ║   08   ║   09   ║
║ SETUP  ║ BRONZE ║ SILVER ║  GOLD  ║  RT    ║  PBI   ║ PIPES  ║  GOV   ║ MIRROR ║  AI/ML ║
╠════════╬════════╬════════╬════════╬════════╬════════╬════════╬════════╬════════╬════════╣
║   ⭐   ║   ⭐   ║   ⭐   ║   ⭐   ║  ⭐⭐  ║  ⭐⭐  ║  ⭐⭐  ║  ⭐⭐  ║ ⭐⭐⭐ ║ ⭐⭐⭐ ║
╚════════╩════════╩════════╩════════╩════════╩════════╩════════╩════════╩════════╩════════╝

╔════════╦════════╦════════╦════════╦════════╦════════╦════════╦════════╦════════╦════════╗
║   10   ║   11   ║   12   ║   13   ║   14   ║   15   ║   16   ║   17   ║   18   ║   19   ║
║TERADATA║  SAS   ║ CI/CD  ║PLANNING║SECURITY║  COST  ║  PERF  ║MONITOR ║ SHARE  ║COPILOT ║
╠════════╬════════╬════════╬════════╬════════╬════════╬════════╬════════╬════════╬════════╣
║ ⭐⭐⭐ ║  ⭐⭐  ║  ⭐⭐  ║ ⭐⭐⭐ ║ ⭐⭐⭐ ║  ⭐⭐  ║ ⭐⭐⭐ ║  ⭐⭐  ║  ⭐⭐  ║   ⭐   ║
╚════════╩════════╩════════╩════════╩════════╩════════╩════════╩════════╩════════╩════════╝

╔════════╦════════╦════════╦════════╗
║   20   ║   21   ║   22   ║   23   ║
║WKSPACE ║  GEO   ║NETWORK ║GATEWAY ║
╠════════╬════════╬════════╬════════╣
║  ⭐⭐  ║ ⭐⭐⭐ ║ ⭐⭐⭐ ║ ⭐⭐⭐ ║
╚════════╩════════╩════════╩════════╝
 Beginner ──────────────────────────────────────────────────────────────────────► Advanced
```

---

## 📋 Tutorial Index

| Level | Tutorial | Description | Duration |
|:------|:---------|:------------|:---------|
| 🟢 **Foundation** | | | |
| | [00 - Environment Setup](./00-environment-setup/README.md) | Azure & Fabric workspace provisioning | ~1 hour |
| | [01 - Bronze Layer](./01-bronze-layer/README.md) | Raw data ingestion patterns | ~2 hours |
| 🟡 **Core** | | | |
| | [02 - Silver Layer](./02-silver-layer/README.md) | Data cleansing & validation | ~2 hours |
| | [03 - Gold Layer](./03-gold-layer/README.md) | Business aggregations & KPIs | ~2 hours |
| 🟠 **Advanced** | | | |
| | [04 - Real-Time Analytics](./04-real-time-analytics/README.md) | Eventstreams & Eventhouse | ~3 hours |
| | [05 - Direct Lake & Power BI](./05-direct-lake-powerbi/README.md) | Semantic models & reports | ~2 hours |
| 🔴 **Enterprise** | | | |
| | [06 - Data Pipelines](./06-data-pipelines/README.md) | Orchestration & scheduling | ~2 hours |
| | [07 - Governance & Purview](./07-governance-purview/README.md) | Data catalog & lineage | ~2 hours |
| | [08 - Database Mirroring](./08-database-mirroring/README.md) | SQL Server replication | ~1 hour |
| | [09 - Advanced AI/ML](./09-advanced-ai-ml/README.md) | Machine learning integration | ~3 hours |
| 🟣 **Migration & Integration** | | | |
| | [10 - Teradata Migration](./10-teradata-migration/README.md) | Teradata to Fabric migration & modernization | ~3 hours |
| | [11 - SAS Connectivity](./11-sas-connectivity/README.md) | SAS OLEDB/ODBC connectivity | ~1.5 hours |
| 🔵 **DevOps & Planning** | | | |
| | [12 - CI/CD DevOps](./12-cicd-devops/README.md) | Git integration, pipelines & deployment automation | ~2.5 hours |
| | [13 - Migration Planning](./13-migration-planning/README.md) | 6-month POC to Production enterprise migration | ~4 hours |
| ⚪ **Operations & Governance** | | | |
| | [14 - Security & Networking](./14-security-networking/README.md) | RLS, OLS, Private Link, compliance (PCI-DSS/NIGC) | ~2.5 hours |
| | [15 - Cost Management](./15-cost-optimization/README.md) | Capacity planning, FinOps, pause/resume automation | ~2 hours |
| | [16 - Performance Tuning](./16-performance-tuning/README.md) | V-Order, partitioning, Spark tuning, benchmarking | ~2.5 hours |
| | [17 - Monitoring & Alerting](./17-monitoring-alerting/README.md) | Capacity Metrics, Azure Monitor, KQL diagnostics | ~2 hours |
| 🟤 **Collaboration & AI** | | | |
| | [18 - Data Sharing](./18-data-sharing/README.md) | OneLake shortcuts, cross-workspace, multi-tenant | ~1.5 hours |
| | [19 - Copilot & AI](./19-copilot-ai/README.md) | AI-assisted development across all Fabric workloads | ~1.5 hours |
| 🟡 **Infrastructure & GeoAnalytics** | | | |
| | [20 - Workspace Best Practices](./20-workspace-best-practices/README.md) | Workspace organization, folder structures, environments | ~2.5 hours |
| | [21 - GeoAnalytics & ArcGIS](./21-geoanalytics-arcgis/README.md) | Geospatial analytics, ArcGIS integration, maps | ~3.5 hours |
| | [22 - Networking Connectivity](./22-networking-connectivity/README.md) | Private endpoints, ExpressRoute, VPN, multi-cloud | ~3.5 hours |
| | [23 - SHIR & Data Gateways](./23-shir-data-gateways/README.md) | Self-hosted runtime, on-premises gateways, hybrid | ~2.5 hours |

---

## ⏱️ Time Estimates

### By Level

| Level | Tutorials | Total Time |
|:------|:----------|:-----------|
| 🟢 Foundation | 00-01 | ~3 hours |
| 🟡 Core | 02-03 | ~4 hours |
| 🟠 Advanced | 04-05 | ~5 hours |
| 🔴 Enterprise | 06-09 | ~8 hours |
| 🟣 Migration & Integration | 10-11 | ~4.5 hours |
| 🔵 DevOps & Planning | 12-13 | ~6.5 hours |
| ⚪ Operations & Governance | 14-17 | ~9 hours |
| 🟤 Collaboration & AI | 18-19 | ~3 hours |
| 🟡 Infrastructure & GeoAnalytics | 20-23 | ~12 hours |
| **Total** | All 24 | **~55 hours** |

### By Format

| Format | Duration | Best For |
|:-------|:---------|:---------|
| **3-Day Workshop** | 24 hours | Team training, POC kickoff |
| **Self-Paced** | 2-4 weeks | Individual learning |
| **Quick Start** | 4-6 hours | Foundation only (00-03) |

---

## 📋 Prerequisites

Before starting the tutorials, ensure you have:

- [ ] Azure subscription with Fabric enabled
- [ ] Fabric capacity (F64 recommended, F2 minimum)
- [ ] Completed the [Prerequisites Guide](../docs/PREREQUISITES.md)
- [ ] Generated sample data (optional but recommended)

> 💡 **Tip:** Start with [Tutorial 00](./00-environment-setup/README.md) to set up your environment before proceeding.

---

## 📚 Related Documentation

| Document | Description |
|:---------|:------------|
| [🏗️ Architecture](../docs/ARCHITECTURE.md) | System architecture and design |
| [🚀 Deployment Guide](../docs/DEPLOYMENT.md) | Infrastructure deployment |
| [📋 Prerequisites](../docs/PREREQUISITES.md) | Setup requirements |
| [📅 POC Agenda](../poc-agenda/README.md) | 3-Day workshop schedule |
| [📋 Templates](./templates/README.md) | Progress tracker templates |

---

[⬆️ Back to top](#-tutorials) | [🏠 Home](../README.md)

---

> 📖 **Documentation maintained by:** Microsoft Fabric POC Team
> 🔗 **Repository:** [Supercharge_Microsoft_Fabric](https://github.com/fgarofalo56/Suppercharge_Microsoft_Fabric)
