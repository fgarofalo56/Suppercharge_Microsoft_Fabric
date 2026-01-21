# Prerequisites Guide

Complete this checklist before deploying the Microsoft Fabric Casino/Gaming POC environment.

## Azure Requirements

### Subscription Access

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Role | Contributor | Owner |
| Scope | Resource Group | Subscription |
| Quota | Sufficient for F64 | 2x capacity |

### Resource Provider Registration

Register these providers before deployment:

```bash
# Register required providers
az provider register --namespace Microsoft.Fabric
az provider register --namespace Microsoft.Purview
az provider register --namespace Microsoft.Storage
az provider register --namespace Microsoft.KeyVault
az provider register --namespace Microsoft.Network
az provider register --namespace Microsoft.OperationalInsights
az provider register --namespace Microsoft.ManagedIdentity

# Verify registration (should show "Registered")
az provider list --query "[?namespace=='Microsoft.Fabric'].registrationState" -o tsv
```

### Microsoft Fabric Requirements

| Requirement | Details |
|-------------|---------|
| Fabric enabled | Must be enabled in Azure AD tenant |
| Capacity available | F64 SKU recommended for POC |
| Region support | Check [region availability](https://learn.microsoft.com/fabric/enterprise/region-availability) |

#### Enable Fabric in Tenant

1. Go to [Azure Portal](https://portal.azure.com) > Microsoft Fabric
2. Or [Fabric Admin Portal](https://app.fabric.microsoft.com/admin-portal)
3. Ensure Fabric is enabled for your organization

### Quota Verification

```bash
# Check current quota for Fabric capacities
az quota show \
  --scope "/subscriptions/{subscription-id}/providers/Microsoft.Fabric/locations/eastus2" \
  --resource-name "F64"
```

## Local Development Environment

### Required Tools

| Tool | Version | Installation |
|------|---------|--------------|
| Azure CLI | 2.50+ | `winget install -e --id Microsoft.AzureCLI` |
| Bicep | 0.22+ | `az bicep install && az bicep upgrade` |
| Git | 2.40+ | `winget install -e --id Git.Git` |
| PowerShell | 7.0+ | `winget install -e --id Microsoft.PowerShell` |
| Python | 3.10+ | `winget install -e --id Python.Python.3.11` |
| VS Code | Latest | `winget install -e --id Microsoft.VisualStudioCode` |

### VS Code Extensions

```bash
# Install recommended extensions
code --install-extension ms-azuretools.vscode-bicep
code --install-extension ms-vscode.azure-account
code --install-extension ms-python.python
code --install-extension ms-toolsai.jupyter
code --install-extension GitHub.copilot
```

### Python Environment Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.\.venv\Scripts\Activate

# Activate (Linux/Mac)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Verify Installation

```bash
# Verify all tools
echo "Azure CLI: $(az --version | head -1)"
echo "Bicep: $(az bicep version)"
echo "Git: $(git --version)"
echo "PowerShell: $(pwsh --version)"
echo "Python: $(python --version)"
```

## Azure AD Configuration

### Required Permissions

| Permission | Scope | Purpose |
|------------|-------|---------|
| User.Read | Delegated | Read user profile |
| Directory.Read.All | Application | Read directory data |
| Fabric.Read.All | Delegated | Read Fabric resources |

### Service Principal Setup (for CI/CD)

```bash
# Create service principal
az ad sp create-for-rbac \
  --name "sp-fabric-poc-deploy" \
  --role "Contributor" \
  --scopes "/subscriptions/{subscription-id}" \
  --sdk-auth

# Save output for GitHub secrets
```

### Configure OIDC for GitHub Actions

```bash
# Get app registration object ID
APP_ID=$(az ad app list --display-name "sp-fabric-poc-deploy" --query "[0].appId" -o tsv)

# Create federated credential
az ad app federated-credential create \
  --id $APP_ID \
  --parameters '{
    "name": "github-actions-main",
    "issuer": "https://token.actions.githubusercontent.com",
    "subject": "repo:YOUR_ORG/Suppercharge_Microsoft_Fabric:ref:refs/heads/main",
    "audiences": ["api://AzureADTokenExchange"]
  }'
```

## Network Requirements

### Outbound Connectivity

Ensure these endpoints are accessible:

| Service | Endpoints |
|---------|-----------|
| Azure Management | `management.azure.com` |
| Azure AD | `login.microsoftonline.com` |
| Fabric | `*.fabric.microsoft.com` |
| Power BI | `*.powerbi.com` |
| Storage | `*.blob.core.windows.net` |
| Key Vault | `*.vault.azure.net` |

### Firewall Rules (if applicable)

```
# Azure services (add to allowlist)
AzureCloud.EastUS2
AzureCloud.WestUS2
```

## Pre-Deployment Checklist

### Azure Subscription

- [ ] Subscription with sufficient quota
- [ ] Owner or Contributor access
- [ ] Resource providers registered
- [ ] Fabric enabled in tenant

### Local Environment

- [ ] Azure CLI installed and logged in
- [ ] Bicep extension installed
- [ ] Git configured
- [ ] Python environment ready

### Configuration Files

- [ ] `.env` file created from `.env.sample`
- [ ] All required values populated
- [ ] Unique names for globally unique resources

### Security

- [ ] Service principal created (for CI/CD)
- [ ] GitHub secrets configured
- [ ] Key Vault access policies planned

## Environment Variables Reference

```bash
# Required variables in .env
AZURE_SUBSCRIPTION_ID=        # Your Azure subscription ID
AZURE_TENANT_ID=              # Your Azure AD tenant ID
AZURE_LOCATION=eastus2        # Deployment region
ENVIRONMENT=dev               # dev, staging, or prod
PROJECT_PREFIX=fabricpoc      # 3-10 char prefix for naming

# Fabric settings
FABRIC_CAPACITY_SKU=F64       # Capacity SKU
FABRIC_ADMIN_EMAIL=           # Admin notification email

# Resource names (must be globally unique)
PURVIEW_ACCOUNT_NAME=         # Purview account
STORAGE_ACCOUNT_NAME=         # ADLS Gen2 storage
KEY_VAULT_NAME=               # Key Vault
```

## Validation Script

Save and run this script to verify prerequisites:

```bash
#!/bin/bash
# verify-prerequisites.sh

echo "=== Verifying Prerequisites ==="

# Check Azure CLI
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI not installed"
    exit 1
else
    echo "✅ Azure CLI: $(az --version | head -1)"
fi

# Check login status
if ! az account show &> /dev/null; then
    echo "❌ Not logged into Azure"
    exit 1
else
    echo "✅ Logged into Azure: $(az account show --query name -o tsv)"
fi

# Check Bicep
if ! az bicep version &> /dev/null; then
    echo "❌ Bicep not installed"
    exit 1
else
    echo "✅ Bicep: $(az bicep version)"
fi

# Check Fabric provider
FABRIC_STATE=$(az provider show --namespace Microsoft.Fabric --query registrationState -o tsv 2>/dev/null)
if [ "$FABRIC_STATE" != "Registered" ]; then
    echo "❌ Microsoft.Fabric provider not registered"
else
    echo "✅ Microsoft.Fabric provider registered"
fi

# Check .env file
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found (copy from .env.sample)"
else
    echo "✅ .env file exists"
fi

echo "=== Verification Complete ==="
```

## Troubleshooting

### Azure CLI Login Issues

```bash
# Clear cached credentials
az account clear
az cache purge
az login
```

### Bicep Build Errors

```bash
# Update Bicep to latest
az bicep upgrade

# Clear Bicep cache
rm -rf ~/.bicep
```

### Provider Registration Stuck

```bash
# Force re-registration
az provider unregister --namespace Microsoft.Fabric
az provider register --namespace Microsoft.Fabric
```

## Next Steps

After completing prerequisites:

1. Review [ARCHITECTURE.md](ARCHITECTURE.md) for system design
2. Follow [DEPLOYMENT.md](DEPLOYMENT.md) for deployment steps
3. Start [Tutorial 00](../tutorials/00-environment-setup/README.md) for hands-on setup
