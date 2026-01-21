# Tutorial 00: Environment Setup

This tutorial guides you through setting up your Microsoft Fabric environment for the Casino/Gaming POC.

## Prerequisites

Before starting, ensure you have:

- [ ] Azure subscription with Fabric enabled
- [ ] Fabric capacity (F64 recommended)
- [ ] Azure CLI installed locally
- [ ] Access to Fabric portal (app.fabric.microsoft.com)

## Learning Objectives

By the end of this tutorial, you will:

1. Understand Microsoft Fabric workspace structure
2. Create and configure a Fabric workspace
3. Create Lakehouses for the medallion architecture
4. Connect to Azure Data Lake Storage
5. Configure workspace settings and access

## Step 1: Access Microsoft Fabric

1. Navigate to [Microsoft Fabric](https://app.fabric.microsoft.com)
2. Sign in with your Azure AD account
3. Verify you see the Fabric home page

### Verify Capacity Access

1. Click on **Settings** (gear icon) in the top right
2. Select **Admin portal** (if you have admin access)
3. Navigate to **Capacity settings**
4. Confirm your F64 capacity is available and running

## Step 2: Create Workspace

### Create a New Workspace

1. In the left navigation, click **Workspaces**
2. Click **+ New workspace**
3. Configure the workspace:

   | Setting | Value |
   |---------|-------|
   | Name | `casino-fabric-poc` |
   | Description | Casino/Gaming Fabric POC - Medallion Architecture |
   | License mode | Fabric capacity |
   | Capacity | Select your F64 capacity |

4. Click **Apply**

### Configure Workspace Settings

1. Open workspace settings (three dots > Settings)
2. Configure the following:

   **General:**
   - Contact list: Add team members
   - Default storage format: Delta

   **Premium:**
   - License mode: Fabric capacity
   - Default storage format: Delta/Parquet

## Step 3: Create Lakehouses

We'll create three Lakehouses for the medallion architecture.

### Bronze Lakehouse (Raw Data)

1. In your workspace, click **+ New** > **Lakehouse**
2. Name: `lh_bronze`
3. Click **Create**

### Silver Lakehouse (Cleansed Data)

1. Click **+ New** > **Lakehouse**
2. Name: `lh_silver`
3. Click **Create**

### Gold Lakehouse (Business Ready)

1. Click **+ New** > **Lakehouse**
2. Name: `lh_gold`
3. Click **Create**

### Verify Lakehouses

Your workspace should now contain:

```
casino-fabric-poc/
├── lh_bronze
├── lh_silver
└── lh_gold
```

## Step 4: Connect to External Storage (Optional)

If you deployed the ADLS Gen2 storage account via Bicep, connect it as a shortcut.

### Create OneLake Shortcut to ADLS

1. Open `lh_bronze`
2. In the **Explorer** pane, right-click on **Files**
3. Select **New shortcut**
4. Choose **Azure Data Lake Storage Gen2**
5. Enter connection details:

   | Setting | Value |
   |---------|-------|
   | URL | Your ADLS DFS endpoint |
   | Connection | Create new |
   | Authentication | Organizational account |

6. Browse to the `landing` container
7. Name the shortcut: `landing_zone`
8. Click **Create**

## Step 5: Configure Workspace Access

### Add Team Members

1. Open workspace settings
2. Navigate to **Access**
3. Add users with appropriate roles:

   | Role | Who | Permissions |
   |------|-----|-------------|
   | Admin | Workspace owners | Full control |
   | Member | Data engineers | Edit all items |
   | Contributor | Developers | Create/edit |
   | Viewer | Business users | Read only |

## Step 6: Verify Setup

### Run Verification Checks

1. **Workspace accessible:** Can see all three Lakehouses
2. **Capacity assigned:** Workspace shows "Premium" badge
3. **Shortcuts working:** Can browse landing zone (if configured)
4. **Permissions correct:** Team members can access

### Create a Test Table

1. Open `lh_bronze`
2. Click **Open notebook** > **New notebook**
3. Run this test code:

```python
# Test Lakehouse connectivity
from pyspark.sql import SparkSession

# Create test data
data = [("test", 1), ("data", 2)]
df = spark.createDataFrame(data, ["name", "value"])

# Write to Bronze Lakehouse
df.write.format("delta").mode("overwrite").save("Tables/test_connection")

print("Success! Lakehouse is configured correctly.")
```

4. Verify the `test_connection` table appears in the Tables folder
5. Delete the test table when done

## Troubleshooting

### Workspace Creation Fails

- Verify Fabric is enabled in your tenant
- Check you have capacity available
- Ensure your account has workspace creation permissions

### Shortcut Connection Fails

- Verify ADLS account exists and is accessible
- Check firewall/private endpoint settings
- Ensure your account has Storage Blob Data Reader role

### Notebook Won't Run

- Verify capacity is running (not paused)
- Check Spark pool is available
- Wait 2-3 minutes for first-time Spark startup

## Next Steps

Continue to [Tutorial 01: Bronze Layer](../01-bronze-layer/README.md) to start ingesting data.

## Resources

- [Microsoft Fabric Documentation](https://learn.microsoft.com/fabric/)
- [Lakehouse Overview](https://learn.microsoft.com/fabric/data-engineering/lakehouse-overview)
- [Workspace Management](https://learn.microsoft.com/fabric/get-started/workspaces)
