# 3-Day POC Agenda

## Casino/Gaming Microsoft Fabric POC Workshop

This 3-day hands-on workshop guides participants through building a complete data platform using Microsoft Fabric with a casino/gaming industry focus.

## Overview

| Day | Focus | Key Deliverables |
|-----|-------|------------------|
| **Day 1** | Foundation | Workspace, Bronze/Silver layers |
| **Day 2** | Transformation | Gold layer, Real-time analytics |
| **Day 3** | Analytics & Governance | Power BI, Purview, Mirroring |

## Audience

| Day | Participants | Count |
|-----|--------------|-------|
| Day 1-2 | Data Architects & Engineers | 4 |
| Day 3 (AM) | + BI Developers | 6 |
| Day 3 (PM) | + All Stakeholders | 10+ |

## Prerequisites

All participants should have:
- [ ] Azure account with Fabric access
- [ ] Completed pre-work modules (online)
- [ ] Laptop with Azure CLI installed
- [ ] Access to workshop workspace

---

## Day 1: Medallion Foundation

**Focus:** Establish the core data architecture

### Schedule

| Time | Duration | Session | Facilitator |
|------|----------|---------|-------------|
| 9:00-9:30 | 30 min | Welcome & Overview | Lead Architect |
| 9:30-10:30 | 1 hr | Environment Setup | Hands-on |
| 10:30-10:45 | 15 min | Break | - |
| 10:45-12:30 | 1 hr 45 min | Bronze Layer Part 1 | Hands-on |
| 12:30-13:30 | 1 hr | Lunch | - |
| 13:30-15:00 | 1 hr 30 min | Bronze Layer Part 2 | Hands-on |
| 15:00-15:15 | 15 min | Break | - |
| 15:15-16:45 | 1 hr 30 min | Silver Layer Start | Hands-on |
| 16:45-17:00 | 15 min | Day 1 Wrap-up | Discussion |

### Day 1 Objectives

By end of Day 1, participants will have:

1. **Workspace Configuration**
   - Created Fabric workspace
   - Configured capacity settings
   - Created three Lakehouses (Bronze/Silver/Gold)

2. **Bronze Layer Complete**
   - Ingested slot machine telemetry
   - Ingested player profiles
   - Ingested financial transactions
   - Ingested table games data
   - Ingested security events
   - Ingested compliance records

3. **Silver Layer Started**
   - Understood data quality requirements
   - Implemented basic cleansing patterns

### Day 1 Materials

- [Tutorial 00: Environment Setup](../tutorials/00-environment-setup/README.md)
- [Tutorial 01: Bronze Layer](../tutorials/01-bronze-layer/README.md)
- [Day 1 Detailed Guide](./day1-medallion-foundation.md)

---

## Day 2: Transformations & Real-Time

**Focus:** Data quality, aggregations, and streaming

### Schedule

| Time | Duration | Session | Facilitator |
|------|----------|---------|-------------|
| 9:00-9:15 | 15 min | Day 1 Review | Lead Architect |
| 9:15-10:30 | 1 hr 15 min | Silver Layer Complete | Hands-on |
| 10:30-10:45 | 15 min | Break | - |
| 10:45-12:30 | 1 hr 45 min | Gold Layer | Hands-on |
| 12:30-13:30 | 1 hr | Lunch | - |
| 13:30-15:00 | 1 hr 30 min | Real-Time Analytics Setup | Hands-on |
| 15:00-15:15 | 15 min | Break | - |
| 15:15-16:45 | 1 hr 30 min | Real-Time Dashboards | Hands-on |
| 16:45-17:00 | 15 min | Day 2 Wrap-up | Discussion |

### Day 2 Objectives

By end of Day 2, participants will have:

1. **Silver Layer Complete**
   - Data cleansing and validation
   - SCD Type 2 for player master
   - Deduplication patterns
   - Schema enforcement

2. **Gold Layer Complete**
   - Slot performance aggregations
   - Player 360 view
   - Compliance reporting tables
   - KPI calculations

3. **Real-Time Intelligence**
   - Eventhouse configured
   - Eventstream ingestion
   - KQL queries for monitoring
   - Real-time dashboard

### Day 2 Materials

- [Tutorial 02: Silver Layer](../tutorials/02-silver-layer/README.md)
- [Tutorial 03: Gold Layer](../tutorials/03-gold-layer/README.md)
- [Tutorial 04: Real-Time Analytics](../tutorials/04-real-time-analytics/README.md)
- [Day 2 Detailed Guide](./day2-transformations-realtime.md)

---

## Day 3: BI, Governance & Advanced

**Focus:** Analytics, compliance, and enterprise features

### Schedule

| Time | Duration | Session | Facilitator |
|------|----------|---------|-------------|
| 9:00-9:15 | 15 min | Day 2 Review | Lead Architect |
| 9:15-10:30 | 1 hr 15 min | Direct Lake Setup | Hands-on |
| 10:30-10:45 | 15 min | Break | - |
| 10:45-12:30 | 1 hr 45 min | Power BI Reports | Hands-on |
| 12:30-13:30 | 1 hr | Lunch | - |
| 13:30-15:00 | 1 hr 30 min | Purview Governance | Demo + Hands-on |
| 15:00-15:15 | 15 min | Break | - |
| 15:15-16:30 | 1 hr 15 min | Database Mirroring | Demo |
| 16:30-17:00 | 30 min | POC Summary & Next Steps | All |

### Day 3 Objectives

By end of Day 3, participants will have:

1. **Direct Lake & Power BI**
   - Semantic model created
   - DAX measures implemented
   - Executive dashboard
   - Operational reports

2. **Purview Governance**
   - Data catalog populated
   - Lineage visualization
   - Classification applied
   - Glossary terms defined

3. **Database Mirroring** (Demo)
   - SQL Server mirroring concept
   - Snowflake integration overview
   - Near real-time sync patterns

### Day 3 Materials

- [Tutorial 05: Direct Lake & Power BI](../tutorials/05-direct-lake-powerbi/README.md)
- [Tutorial 07: Governance & Purview](../tutorials/07-governance-purview/README.md)
- [Tutorial 08: Database Mirroring](../tutorials/08-database-mirroring/README.md)
- [Day 3 Detailed Guide](./day3-bi-governance-mirroring.md)

---

## Workshop Deliverables

Upon completion, the team will have:

### Technical Assets
- [ ] Fully configured Fabric workspace
- [ ] Complete medallion architecture (Bronze/Silver/Gold)
- [ ] Real-time analytics pipeline
- [ ] Power BI semantic model and reports
- [ ] Purview data catalog integration

### Documentation
- [ ] Architecture diagram
- [ ] Data dictionary
- [ ] Deployment runbook
- [ ] Operational procedures

### Knowledge Transfer
- [ ] Recorded sessions (if applicable)
- [ ] Q&A documentation
- [ ] Best practices guide

---

## Success Criteria

| Metric | Target |
|--------|--------|
| Bronze tables populated | 6 tables, 500K+ records |
| Silver transformations | All data cleansed |
| Gold aggregations | KPIs calculated |
| Real-time latency | < 1 minute |
| Report load time | < 3 seconds |
| Governance coverage | 100% tables cataloged |

---

## Logistics

### Room Setup
- Projector/large display
- Whiteboard
- Power outlets for all laptops
- Stable internet connection

### Accounts Required
- Azure AD accounts for all participants
- Fabric workspace access
- Purview access (Day 3)

### Support
- Technical support contact available
- Backup facilitator identified
- Escalation path documented

---

## Post-Workshop

### Follow-up Actions
1. **Week 1:** Review recordings, practice exercises
2. **Week 2:** Implement with real data (subset)
3. **Week 3:** Production planning meeting
4. **Week 4:** Go/No-Go decision

### Resources
- This repository (ongoing reference)
- Microsoft Fabric documentation
- Support channels
