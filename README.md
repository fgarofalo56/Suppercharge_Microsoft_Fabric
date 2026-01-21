# Supercharge Microsoft Fabric - Casino/Gaming Industry POC

A comprehensive, production-ready Microsoft Fabric demonstration environment showcasing enterprise data platform capabilities for the casino and gaming industry.

## Overview

This repository provides a complete, deployable proof-of-concept (POC) environment for Microsoft Fabric, featuring:

- **Medallion Architecture** (Bronze/Silver/Gold) with Lakehouse
- **Real-Time Intelligence** for casino floor monitoring
- **Direct Lake** Power BI integration for sub-second analytics
- **Microsoft Purview** data governance and compliance
- **Infrastructure as Code** (Bicep/ARM) for rapid deployment
- **Step-by-step tutorials** for hands-on learning

## Target Audience

- Data Architects evaluating Microsoft Fabric
- Data Engineers implementing medallion architecture
- BI Developers building Direct Lake solutions
- Solution Architects designing enterprise data platforms
- Organizations in gaming, hospitality, and regulated industries

## Quick Start

### Prerequisites

- Azure subscription with Owner or Contributor access
- Microsoft Fabric capacity (F64 recommended for POC)
- Azure CLI 2.50+ with Bicep extension
- PowerShell 7+ or Bash
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/frgarofa/Suppercharge_Microsoft_Fabric.git
cd Suppercharge_Microsoft_Fabric
```

### 2. Configure Environment

```bash
cp .env.sample .env
# Edit .env with your Azure subscription and tenant details
```

### 3. Deploy Infrastructure

```bash
# Login to Azure
az login

# Deploy to development environment
az deployment sub create \
  --location eastus2 \
  --template-file infra/main.bicep \
  --parameters infra/environments/dev/dev.bicepparam
```

### 4. Follow the Tutorials

Start with [Tutorial 00: Environment Setup](tutorials/00-environment-setup/README.md)

## Architecture

```
                    +------------------+
                    |   Data Sources   |
                    +------------------+
                            |
        +-------------------+-------------------+
        |                   |                   |
   Real-Time            Batch              External
   (Eventstreams)    (Dataflows)         (Mirroring)
        |                   |                   |
        +-------------------+-------------------+
                            |
                    +-------v-------+
                    |  BRONZE LAYER |  Raw data ingestion
                    |   Lakehouse   |  Schema-on-read
                    +-------+-------+
                            |
                    +-------v-------+
                    |  SILVER LAYER |  Cleansed & validated
                    |   Lakehouse   |  Business rules applied
                    +-------+-------+
                            |
                    +-------v-------+
                    |   GOLD LAYER  |  Business-ready
                    |   Lakehouse   |  Aggregations & KPIs
                    +-------+-------+
                            |
            +---------------+---------------+
            |               |               |
    +-------v-------+ +-----v-----+ +-------v-------+
    |  Direct Lake  | | Eventhouse| |    Purview    |
    | Semantic Model| |    KQL    | |  Governance   |
    +-------+-------+ +-----+-----+ +---------------+
            |               |
    +-------v-------+ +-----v-----+
    |   Power BI    | | Real-Time |
    |   Reports     | | Dashboards|
    +---------------+ +-----------+
```

## Casino/Gaming Data Domains

| Domain | Description | Compliance |
|--------|-------------|------------|
| Slot Machines | Telemetry, meters, jackpots | NIGC MICS |
| Table Games | Hand results, chip tracking | NIGC MICS |
| Player/Loyalty | Profiles, rewards, activity | PCI-DSS, PII |
| Financial/Cage | Transactions, fills, credits | FinCEN BSA |
| Security | Surveillance, access logs | State regulations |
| Compliance | CTR, SAR, W-2G filings | Federal/State |

## Repository Structure

```
Suppercharge_Microsoft_Fabric/
├── infra/                     # Infrastructure as Code (Bicep)
│   ├── main.bicep             # Root orchestration
│   ├── modules/               # Reusable modules
│   └── environments/          # Environment-specific parameters
│
├── docs/                      # Documentation
│   ├── ARCHITECTURE.md        # Detailed architecture
│   ├── DEPLOYMENT.md          # Deployment guide
│   └── SECURITY.md            # Security & compliance
│
├── tutorials/                 # Step-by-step tutorials
│   ├── 00-environment-setup/
│   ├── 01-bronze-layer/
│   ├── 02-silver-layer/
│   ├── 03-gold-layer/
│   ├── 04-real-time-analytics/
│   ├── 05-direct-lake-powerbi/
│   └── ...
│
├── poc-agenda/                # 3-Day POC workshop materials
├── data-generation/           # Sample data generators
├── notebooks/                 # Fabric-importable notebooks
└── validation/                # Testing & data quality
```

## 3-Day POC Agenda

This repository supports a structured 3-day POC workshop:

| Day | Focus | Key Activities |
|-----|-------|---------------|
| **Day 1** | Medallion Foundation | Environment setup, Bronze/Silver layers |
| **Day 2** | Transformations | Gold layer, Real-time analytics |
| **Day 3** | BI & Governance | Direct Lake, Power BI, Purview |

See [POC Agenda](poc-agenda/README.md) for detailed schedules.

## Tutorials

### Level 1: Foundation
- [00 - Environment Setup](tutorials/00-environment-setup/README.md)
- [01 - Bronze Layer](tutorials/01-bronze-layer/README.md)

### Level 2: Core Implementation
- [02 - Silver Layer](tutorials/02-silver-layer/README.md)
- [03 - Gold Layer](tutorials/03-gold-layer/README.md)

### Level 3: Advanced Analytics
- [04 - Real-Time Analytics](tutorials/04-real-time-analytics/README.md)
- [05 - Direct Lake & Power BI](tutorials/05-direct-lake-powerbi/README.md)

### Level 4: Enterprise Features
- [06 - Data Pipelines](tutorials/06-data-pipelines/README.md)
- [07 - Governance & Purview](tutorials/07-governance-purview/README.md)
- [08 - Database Mirroring](tutorials/08-database-mirroring/README.md)
- [09 - Advanced AI/ML](tutorials/09-advanced-ai-ml/README.md)

## Compliance Frameworks

This POC addresses compliance requirements for:

- **NIGC MICS** - Minimum Internal Control Standards for gaming
- **FinCEN BSA** - Bank Secrecy Act (CTR, SAR reporting)
- **PCI-DSS** - Payment card data security
- **State Gaming Regulations** - Jurisdiction-specific requirements

## Future Expansions

The architecture supports expansion to:

- **Tribal/Sovereign Nations** - Healthcare (HIPAA), tribal gaming
- **Federal Government** - DOT, FAA, USDA, NOAA datasets
- **Retail/E-commerce** - Customer 360, supply chain

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) before submitting PRs.

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

## Acknowledgments

- Microsoft Fabric Product Team
- Azure Architecture Center
- Gaming industry compliance experts

---

**Built for Microsoft Fabric | Casino/Gaming Industry | Production-Ready POC**
