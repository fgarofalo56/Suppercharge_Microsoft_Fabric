# Tutorial 07: Governance & Purview

This tutorial covers implementing data governance using Microsoft Purview integration with Fabric.

## Learning Objectives

By the end of this tutorial, you will:

1. Connect Purview to Fabric workspace
2. Scan and catalog data assets
3. Apply classifications and sensitivity labels
4. Create glossary terms
5. View data lineage

## Governance Overview

Microsoft Purview provides:
- **Data Catalog**: Discover and understand data assets
- **Data Map**: Unified view of data estate
- **Classifications**: Identify sensitive data
- **Lineage**: Track data flow and transformations
- **Access Policies**: Govern data access

## Prerequisites

- Completed Power BI tutorials
- Microsoft Purview account deployed
- Purview Data Curator or higher role

## Step 1: Connect Purview to Fabric

### Register Fabric as a Source

1. Open [Microsoft Purview Portal](https://purview.microsoft.com)
2. Navigate to **Data Map** > **Sources**
3. Click **Register** > **Microsoft Fabric**
4. Configure:
   - Name: `Fabric-Casino-POC`
   - Tenant: Select your tenant
   - Workspace: `casino-fabric-poc`
5. Click **Register**

### Create Scan

1. On the registered source, click **New Scan**
2. Configure:
   - Name: `fabric-full-scan`
   - Integration runtime: Azure integration runtime
   - Credential: Use existing or create new
3. **Scope**: Select all Lakehouses
4. **Scan rule set**: System default
5. Click **Continue**

### Set Scan Trigger

1. **Scan trigger**: Recurring
2. **Frequency**: Weekly
3. **Start time**: Off-peak hours
4. Click **Save and Run**

## Step 2: Review Scanned Assets

### View Data Catalog

1. Go to **Data Catalog** > **Browse**
2. Filter by Source: `Fabric-Casino-POC`
3. You should see:
   - Lakehouses (lh_bronze, lh_silver, lh_gold)
   - Delta tables
   - Semantic models

### Explore Table Details

Click on a table (e.g., `gold_slot_performance`):

**Overview Tab:**
- Description
- Schema
- Classifications
- Glossary terms

**Schema Tab:**
- Column names and types
- Column classifications
- Column descriptions

**Lineage Tab:**
- Upstream sources
- Downstream consumers

## Step 3: Apply Classifications

### Built-in Classifications

Purview includes classifications for:
- Personal information (PII)
- Financial data
- Healthcare data
- Government identifiers

### Review Auto-Classifications

1. Navigate to table: `silver_player_master`
2. Check **Schema** tab
3. Verify columns classified:
   - `ssn_hash`: Government ID
   - `email`: Email Address
   - `phone`: Phone Number
   - `date_of_birth`: Date of Birth

### Apply Custom Classifications

1. Click **Edit** on the asset
2. Under **Classifications**, add:
   - `Casino - Player PII`
   - `Regulatory - BSA/AML`
3. Click **Save**

### Create Custom Classification

1. Go to **Data Map** > **Classifications**
2. Click **+ New**
3. Configure:
   - Name: `Casino - Gaming Data`
   - Description: `Casino gaming metrics and transaction data`
   - Pattern (optional): `coin_in|coin_out|jackpot`
4. Click **Create**

## Step 4: Create Glossary Terms

### Navigate to Glossary

1. Go to **Data Catalog** > **Glossary**
2. Create a hierarchy for casino terms

### Create Business Terms

#### Term: Coin In

```
Name: Coin In
Definition: Total amount wagered by players on a gaming device.
            Represents the handle or total bets placed.

Acronym: CI
Status: Approved

Related Terms:
- Coin Out
- Net Win
- Hold Percentage

Experts: [Casino Analytics Team]

Resources:
- NIGC MICS Section 543.24
```

#### Term: Theoretical Win (Theo)

```
Name: Theoretical Win
Definition: The statistical expected win from a player or device based on
            the mathematical house advantage and total wagers.

Formula: Theo = Coin In × House Edge

Synonyms: Theoretical, Expected Win
Status: Approved

Related Terms:
- Hold Percentage
- Actual Win
- Player Theo
```

#### Term: Hold Percentage

```
Name: Hold Percentage
Definition: The percentage of total wagers retained by the casino.
            Calculated as (Coin In - Coin Out) / Coin In × 100.

Formula: Hold % = Net Win / Coin In × 100
Synonyms: Hold, Win Percentage
Status: Approved
```

#### Term: CTR (Currency Transaction Report)

```
Name: Currency Transaction Report
Definition: Federal filing required for cash transactions of $10,000 or more
            in a single gaming day.

Acronym: CTR
Status: Approved
Regulatory Reference: 31 CFR 1021.311

Related Terms:
- SAR
- BSA
- Gaming Day
```

### Assign Terms to Assets

1. Open table `gold_slot_performance`
2. Click **Edit**
3. In **Glossary terms**, add:
   - Coin In → `total_coin_in` column
   - Net Win → `net_win` column
   - Hold Percentage → `actual_hold_pct` column
4. Click **Save**

## Step 5: View Data Lineage

### Navigate to Lineage

1. Open any Gold table
2. Click **Lineage** tab

### Understand Lineage View

```
Bronze Tables → Silver Tables → Gold Tables → Semantic Model → Reports
     │              │              │              │              │
     ↓              ↓              ↓              ↓              ↓
 Raw Data      Cleansed       Aggregated      DAX           Visuals
               Validated       KPIs         Measures
```

### Lineage for Slot Performance

```
bronze_slot_telemetry
        ↓
silver_slot_cleansed
        ↓
gold_slot_performance
        ↓
Casino Analytics Model (semantic model)
        ↓
Casino Executive Dashboard (report)
```

### Impact Analysis

1. On `silver_slot_cleansed`, click **View Lineage**
2. Click on a downstream asset
3. Click **Impact Analysis**
4. See all downstream dependencies

This shows what will be affected if you change the Silver table.

## Step 6: Create Data Policies

### Access Policies (Preview)

1. Go to **Data Policy** > **Data access policies**
2. Click **New policy**
3. Configure:
   - Name: `Casino Data Access - Analysts`
   - Data resources: `lh_gold/*`
   - Principals: `Casino Analysts` group
   - Permissions: Read
4. Click **Save**

### Sensitivity Labels

1. In Purview, go to **Information Protection**
2. Apply labels to sensitive tables:
   - `silver_player_master`: Confidential
   - `silver_compliance_validated`: Highly Confidential
3. Configure label policies for automatic application

## Step 7: Monitoring and Reporting

### Data Health

1. Go to **Data Estate Insights**
2. View dashboards:
   - Asset distribution
   - Classification coverage
   - Glossary usage
   - Scan history

### Create Custom Reports

Export data from Purview for custom analysis:

```python
# Using Purview REST API
import requests

endpoint = "https://your-purview.purview.azure.com"
headers = {"Authorization": f"Bearer {token}"}

# Get all classified assets
response = requests.get(
    f"{endpoint}/catalog/api/atlas/v2/search/advanced",
    headers=headers,
    json={
        "keywords": "*",
        "filter": {
            "classification": "MICROSOFT.PERSONAL.EMAIL"
        }
    }
)
```

## Compliance Reporting

### Generate Compliance Report

1. Go to **Data Catalog** > **Browse**
2. Filter: Classification = "Regulatory - BSA/AML"
3. Export list of regulated data assets
4. Include in compliance documentation

### Audit Trail

1. Go to **Monitoring** > **Diagnostics**
2. Review:
   - Scan history
   - Classification changes
   - Access requests
3. Export for audit purposes

## Validation Checklist

- [ ] Purview connected to Fabric workspace
- [ ] Scan completed successfully
- [ ] All tables cataloged
- [ ] Classifications applied (auto + manual)
- [ ] Glossary terms created
- [ ] Terms assigned to columns
- [ ] Lineage visible for Gold tables
- [ ] Access policies configured

## Best Practices

### Governance Framework

1. **Define data domains** before cataloging
2. **Establish glossary** with business input
3. **Automate classification** with rules
4. **Review lineage** regularly
5. **Monitor data quality** metrics

### For Casino/Gaming

1. **Classify compliance data** (CTR, SAR, W-2G)
2. **Tag PII columns** in player data
3. **Document regulatory requirements** in glossary
4. **Track financial data lineage** for audits

## Troubleshooting

### Scan Failures

1. Check integration runtime connectivity
2. Verify credentials have correct permissions
3. Review scan logs for specific errors

### Missing Classifications

1. Verify classification rules match data patterns
2. Check column data types
3. Run classification scan manually

### Lineage Not Showing

1. Ensure scan includes all sources
2. Check transformation tracking is enabled
3. Verify naming consistency across layers

## Next Steps

Continue to [Tutorial 08: Database Mirroring](../08-database-mirroring/README.md).

## Resources

- [Microsoft Purview Documentation](https://learn.microsoft.com/purview/)
- [Fabric + Purview Integration](https://learn.microsoft.com/fabric/governance/)
- [Data Governance Best Practices](https://learn.microsoft.com/purview/concept-best-practices)
