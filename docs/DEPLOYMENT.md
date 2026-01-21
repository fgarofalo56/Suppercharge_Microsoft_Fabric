# Deployment Guide

This guide covers deploying the Microsoft Fabric Casino/Gaming POC environment using Infrastructure as Code (Bicep) and GitHub Actions.

## Prerequisites

### Azure Requirements

- **Azure Subscription:** Owner or Contributor access
- **Microsoft Fabric:** Enabled in your tenant
- **Resource Providers:** Register the following:
  - `Microsoft.Fabric`
  - `Microsoft.Purview`
  - `Microsoft.Storage`
  - `Microsoft.KeyVault`
  - `Microsoft.Network`
  - `Microsoft.OperationalInsights`

### Local Tools

```bash
# Azure CLI (2.50+)
az --version

# Bicep (0.22+)
az bicep version

# Git
git --version

# PowerShell 7+ (optional, for scripts)
pwsh --version
```

### Install Required Tools

```bash
# Install/Update Azure CLI
winget install -e --id Microsoft.AzureCLI

# Install Bicep
az bicep install
az bicep upgrade

# Install PowerShell 7+
winget install -e --id Microsoft.PowerShell
```

## Quick Deployment

### Step 1: Clone and Configure

```bash
# Clone repository
git clone https://github.com/frgarofa/Suppercharge_Microsoft_Fabric.git
cd Suppercharge_Microsoft_Fabric

# Copy environment template
cp .env.sample .env

# Edit .env with your values
code .env  # or your preferred editor
```

### Step 2: Login to Azure

```bash
# Interactive login
az login

# Set subscription
az account set --subscription "<subscription-id>"

# Verify
az account show
```

### Step 3: Validate Deployment

```bash
# Build and validate Bicep
az bicep build --file infra/main.bicep

# What-if analysis (preview changes)
az deployment sub what-if \
  --location eastus2 \
  --template-file infra/main.bicep \
  --parameters infra/environments/dev/dev.bicepparam
```

### Step 4: Deploy

```bash
# Deploy infrastructure
az deployment sub create \
  --name "fabric-poc-$(date +%Y%m%d-%H%M%S)" \
  --location eastus2 \
  --template-file infra/main.bicep \
  --parameters infra/environments/dev/dev.bicepparam
```

## Environment-Specific Deployment

### Development

```bash
az deployment sub create \
  --location eastus2 \
  --template-file infra/main.bicep \
  --parameters infra/environments/dev/dev.bicepparam
```

### Staging

```bash
az deployment sub create \
  --location eastus2 \
  --template-file infra/main.bicep \
  --parameters infra/environments/staging/staging.bicepparam
```

### Production

```bash
az deployment sub create \
  --location eastus2 \
  --template-file infra/main.bicep \
  --parameters infra/environments/prod/prod.bicepparam
```

## GitHub Actions Deployment

### Setting Up OIDC Authentication

1. **Create Azure AD Application:**

```bash
# Create app registration
az ad app create --display-name "github-fabric-poc"

# Get app ID
APP_ID=$(az ad app list --display-name "github-fabric-poc" --query "[0].appId" -o tsv)

# Create service principal
az ad sp create --id $APP_ID

# Get subscription and tenant IDs
SUBSCRIPTION_ID=$(az account show --query id -o tsv)
TENANT_ID=$(az account show --query tenantId -o tsv)

# Assign Contributor role
az role assignment create \
  --assignee $APP_ID \
  --role "Contributor" \
  --scope "/subscriptions/$SUBSCRIPTION_ID"
```

2. **Configure Federated Credentials:**

```bash
# Create federated credential for main branch
az ad app federated-credential create \
  --id $APP_ID \
  --parameters '{
    "name": "github-main",
    "issuer": "https://token.actions.githubusercontent.com",
    "subject": "repo:<your-org>/Suppercharge_Microsoft_Fabric:ref:refs/heads/main",
    "audiences": ["api://AzureADTokenExchange"]
  }'

# Create federated credential for pull requests
az ad app federated-credential create \
  --id $APP_ID \
  --parameters '{
    "name": "github-pr",
    "issuer": "https://token.actions.githubusercontent.com",
    "subject": "repo:<your-org>/Suppercharge_Microsoft_Fabric:pull_request",
    "audiences": ["api://AzureADTokenExchange"]
  }'
```

3. **Add GitHub Secrets:**

Go to your repository Settings > Secrets and variables > Actions:

| Secret | Value |
|--------|-------|
| `AZURE_CLIENT_ID` | Application (client) ID |
| `AZURE_TENANT_ID` | Directory (tenant) ID |
| `AZURE_SUBSCRIPTION_ID` | Subscription ID |

### Manual Workflow Trigger

```bash
# Trigger deployment via GitHub CLI
gh workflow run deploy-infra.yml \
  --ref main \
  -f environment=dev
```

## Post-Deployment Configuration

### 1. Verify Fabric Capacity

```bash
# List Fabric capacities
az resource list \
  --resource-type "Microsoft.Fabric/capacities" \
  --query "[].{Name:name, Location:location, SKU:sku.name}"
```

### 2. Configure Fabric Workspace

After Bicep deployment, manually configure in Fabric Portal:

1. Navigate to [Microsoft Fabric](https://app.fabric.microsoft.com)
2. Create workspace linked to deployed capacity
3. Create Lakehouse for each medallion layer
4. Import notebooks from `notebooks/` directory

### 3. Connect Purview

```bash
# Get Purview account endpoint
az purview account show \
  --name "<purview-account-name>" \
  --resource-group "<resource-group>" \
  --query "endpoints"
```

### 4. Configure Key Vault Access

```bash
# Grant current user access
az keyvault set-policy \
  --name "<keyvault-name>" \
  --upn "$(az ad signed-in-user show --query userPrincipalName -o tsv)" \
  --secret-permissions get list set delete
```

## Deployment Verification

### Automated Verification Script

```bash
# Run verification
./scripts/verify-deployment.sh

# Expected output:
# ✓ Fabric capacity deployed
# ✓ Purview account accessible
# ✓ Storage account created
# ✓ Key Vault configured
# ✓ Network connectivity verified
```

### Manual Verification Checklist

- [ ] Fabric capacity shows in Azure portal
- [ ] Fabric capacity shows in Fabric admin portal
- [ ] Purview account accessible
- [ ] Storage account ADLS Gen2 enabled
- [ ] Key Vault secrets accessible
- [ ] Log Analytics receiving logs
- [ ] Private endpoints connected (if enabled)

## Troubleshooting

### Common Issues

#### Fabric Capacity Deployment Fails

```
Error: Microsoft.Fabric/capacities resource provider not registered
```

**Solution:**
```bash
az provider register --namespace Microsoft.Fabric
az provider show --namespace Microsoft.Fabric --query "registrationState"
```

#### Insufficient Permissions

```
Error: AuthorizationFailed
```

**Solution:** Ensure you have Owner or Contributor role at subscription level.

#### Capacity SKU Not Available

```
Error: SKU F64 not available in region
```

**Solution:** Check [Fabric capacity availability](https://learn.microsoft.com/fabric/enterprise/region-availability) and choose supported region.

#### Purview Name Already Exists

```
Error: Purview account name already exists
```

**Solution:** Purview names are globally unique. Use a different name in `.env`.

### Deployment Logs

```bash
# Get deployment details
az deployment sub show \
  --name "<deployment-name>" \
  --query "properties.outputs"

# Get deployment operations (for debugging)
az deployment sub operation list \
  --name "<deployment-name>" \
  --query "[?properties.provisioningState=='Failed']"
```

## Cleanup

### Remove All Resources

```bash
# Delete resource group (removes all resources)
az group delete --name "rg-fabric-poc-dev" --yes --no-wait

# Or delete specific deployment
az deployment sub delete --name "<deployment-name>"
```

### Preserve Specific Resources

```bash
# Remove lock before deletion (if locked)
az lock delete --name "CanNotDelete" --resource-group "rg-fabric-poc-dev"
```

## Cost Optimization

### Development Environment

- Use F2 or F4 SKU for development
- Enable auto-pause (suspend when idle)
- Schedule capacity pause overnight

### Production Environment

- Use reserved capacity for predictable costs
- Monitor CU consumption via Log Analytics
- Set up cost alerts

```bash
# Create cost alert
az monitor metrics alert create \
  --name "fabric-cost-alert" \
  --resource-group "rg-fabric-poc-prod" \
  --scopes "<capacity-resource-id>" \
  --condition "total Cost > 1000" \
  --window-size 1d \
  --action "<action-group-id>"
```

## Next Steps

After successful deployment:

1. [Tutorial 00: Environment Setup](../tutorials/00-environment-setup/README.md)
2. [Tutorial 01: Bronze Layer](../tutorials/01-bronze-layer/README.md)
3. [Generate Sample Data](../data-generation/README.md)
