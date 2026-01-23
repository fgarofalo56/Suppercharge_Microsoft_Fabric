# Bicep Reference Documentation

Comprehensive reference for Azure Bicep infrastructure-as-code development.

## Table of Contents

1. [Resource Type Discovery](#resource-type-discovery)
2. [Schema Retrieval](#schema-retrieval)
3. [Common Azure Providers](#common-azure-providers)
4. [Azure Verified Modules Catalog](#azure-verified-modules-catalog)
5. [Deployment Commands](#deployment-commands)
6. [Advanced Best Practices](#advanced-best-practices)
7. [Troubleshooting](#troubleshooting)

---

## Resource Type Discovery

### Listing Resource Types for a Provider

Use Azure CLI to list all resource types available for a specific provider:

```bash
# List all resource types for a provider with latest API versions
az provider show --namespace Microsoft.Storage \
  --query "resourceTypes[].{Type:resourceType,ApiVersions:apiVersions[0]}" \
  -o table

# Get all providers
az provider list --query "[].namespace" -o tsv

# Show all resource types in JSON format
az provider show --namespace Microsoft.Compute --expand resourceTypes
```

### Common Provider Namespaces

| Provider | Description |
|----------|-------------|
| `Microsoft.Compute` | VMs, VM Scale Sets, Disks |
| `Microsoft.Storage` | Storage Accounts, Blob, File, Queue, Table |
| `Microsoft.Network` | VNets, NSGs, Load Balancers, Application Gateway |
| `Microsoft.Web` | App Services, Function Apps |
| `Microsoft.Sql` | Azure SQL Database |
| `Microsoft.KeyVault` | Key Vault |
| `Microsoft.ContainerService` | AKS |
| `Microsoft.ContainerRegistry` | ACR |
| `Microsoft.Insights` | Application Insights, Metrics, Alerts |
| `Microsoft.OperationalInsights` | Log Analytics |
| `Microsoft.Authorization` | RBAC, Policy |
| `Microsoft.Resources` | Resource Groups, Deployments |

---

## Schema Retrieval

### Using Bicep CLI

```bash
# Decompile ARM template to see Bicep types
bicep decompile template.json

# Build and see schema structure
bicep build main.bicep --stdout
```

### Using Azure REST API

```bash
# Get resource provider schema
az rest --method get \
  --uri "https://management.azure.com/subscriptions/{subscription-id}/providers/Microsoft.Storage?api-version=2021-04-01"
```

### Resource Schema Structure

All Azure resources follow this structure:

```bicep
resource <symbolic-name> '<provider>/<type>@<api-version>' = {
  name: '<resource-name>'
  location: '<location>'
  tags: {}
  sku: {}
  kind: '<kind>'
  properties: {}
  dependsOn: []
}
```

---

## Common Azure Providers

### Microsoft.Storage

```bicep
// Storage Account
resource storage 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageAccountName
  location: location
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
    supportsHttpsTrafficOnly: true
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    networkAcls: {
      defaultAction: 'Deny'
      bypass: 'AzureServices'
    }
  }
}

// Blob Service
resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2023-05-01' = {
  parent: storage
  name: 'default'
  properties: {
    deleteRetentionPolicy: {
      enabled: true
      days: 7
    }
  }
}

// Blob Container
resource container 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = {
  parent: blobService
  name: 'mycontainer'
  properties: {
    publicAccess: 'None'
  }
}
```

### Microsoft.Network

```bicep
// Virtual Network
resource vnet 'Microsoft.Network/virtualNetworks@2023-09-01' = {
  name: vnetName
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: ['10.0.0.0/16']
    }
    subnets: [
      {
        name: 'default'
        properties: {
          addressPrefix: '10.0.1.0/24'
          networkSecurityGroup: { id: nsg.id }
        }
      }
    ]
  }
}

// Network Security Group
resource nsg 'Microsoft.Network/networkSecurityGroups@2023-09-01' = {
  name: nsgName
  location: location
  properties: {
    securityRules: [
      {
        name: 'AllowHTTPS'
        properties: {
          priority: 100
          direction: 'Inbound'
          access: 'Allow'
          protocol: 'Tcp'
          sourceAddressPrefix: '*'
          sourcePortRange: '*'
          destinationAddressPrefix: '*'
          destinationPortRange: '443'
        }
      }
    ]
  }
}

// Public IP
resource pip 'Microsoft.Network/publicIPAddresses@2023-09-01' = {
  name: pipName
  location: location
  sku: { name: 'Standard' }
  properties: {
    publicIPAllocationMethod: 'Static'
    dnsSettings: {
      domainNameLabel: dnsLabel
    }
  }
}
```

### Microsoft.Compute

```bicep
// Virtual Machine
resource vm 'Microsoft.Compute/virtualMachines@2023-09-01' = {
  name: vmName
  location: location
  properties: {
    hardwareProfile: {
      vmSize: 'Standard_D2s_v3'
    }
    osProfile: {
      computerName: vmName
      adminUsername: adminUsername
      adminPassword: adminPassword
    }
    storageProfile: {
      imageReference: {
        publisher: 'Canonical'
        offer: '0001-com-ubuntu-server-jammy'
        sku: '22_04-lts-gen2'
        version: 'latest'
      }
      osDisk: {
        createOption: 'FromImage'
        managedDisk: {
          storageAccountType: 'Premium_LRS'
        }
      }
    }
    networkProfile: {
      networkInterfaces: [
        { id: nic.id }
      ]
    }
  }
}
```

### Microsoft.KeyVault

```bicep
// Key Vault
resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: keyVaultName
  location: location
  properties: {
    tenantId: subscription().tenantId
    sku: {
      family: 'A'
      name: 'standard'
    }
    enableRbacAuthorization: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 90
    enablePurgeProtection: true
    networkAcls: {
      defaultAction: 'Deny'
      bypass: 'AzureServices'
    }
  }
}

// Secret
resource secret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'mySecret'
  properties: {
    value: secretValue
  }
}
```

### Microsoft.Web

```bicep
// App Service Plan
resource appServicePlan 'Microsoft.Web/serverfarms@2023-01-01' = {
  name: appServicePlanName
  location: location
  sku: {
    name: 'P1v3'
    tier: 'PremiumV3'
  }
  kind: 'linux'
  properties: {
    reserved: true
  }
}

// Web App
resource webApp 'Microsoft.Web/sites@2023-01-01' = {
  name: webAppName
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'DOTNETCORE|8.0'
      minTlsVersion: '1.2'
      ftpsState: 'Disabled'
    }
  }
  identity: {
    type: 'SystemAssigned'
  }
}
```

### Microsoft.ContainerService (AKS)

```bicep
// AKS Cluster
resource aks 'Microsoft.ContainerService/managedClusters@2024-01-01' = {
  name: aksName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    dnsPrefix: dnsPrefix
    kubernetesVersion: '1.28'
    agentPoolProfiles: [
      {
        name: 'systempool'
        count: 3
        vmSize: 'Standard_D4s_v3'
        mode: 'System'
        osType: 'Linux'
        enableAutoScaling: true
        minCount: 1
        maxCount: 5
      }
    ]
    networkProfile: {
      networkPlugin: 'azure'
      networkPolicy: 'azure'
    }
  }
}
```

---

## Azure Verified Modules Catalog

### Resource Modules (avm/res/)

Popular resource modules available in the Bicep Public Registry:

| Module | Description | Example |
|--------|-------------|---------|
| `avm/res/storage/storage-account` | Storage Account | `br/public:avm/res/storage/storage-account:0.9.0` |
| `avm/res/network/virtual-network` | Virtual Network | `br/public:avm/res/network/virtual-network:0.4.0` |
| `avm/res/compute/virtual-machine` | Virtual Machine | `br/public:avm/res/compute/virtual-machine:0.5.0` |
| `avm/res/key-vault/vault` | Key Vault | `br/public:avm/res/key-vault/vault:0.6.0` |
| `avm/res/web/site` | Web App | `br/public:avm/res/web/site:0.3.0` |
| `avm/res/container-service/managed-cluster` | AKS | `br/public:avm/res/container-service/managed-cluster:0.3.0` |
| `avm/res/sql/server` | SQL Server | `br/public:avm/res/sql/server:0.4.0` |

### Pattern Modules (avm/ptn/)

| Module | Description |
|--------|-------------|
| `avm/ptn/authorization/resource-role-assignment` | Role assignment pattern |
| `avm/ptn/network/private-link-private-dns-zones` | Private Link DNS zones |
| `avm/ptn/lz/sub-vending` | Landing zone subscription vending |

### Using AVM Modules

```bicep
// Configure the Bicep registry alias
// bicepconfig.json:
// {
//   "moduleAliases": {
//     "br": {
//       "public": { "registry": "mcr.microsoft.com/bicep" }
//     }
//   }
// }

// Use in your template
module storage 'br/public:avm/res/storage/storage-account:0.9.0' = {
  name: 'storageDeployment'
  params: {
    name: 'mystorageaccount${uniqueString(resourceGroup().id)}'
    location: location
    skuName: 'Standard_LRS'
    kind: 'StorageV2'
  }
}
```

### Finding AVM Modules

1. **Official Catalog**: https://azure.github.io/Azure-Verified-Modules/indexes/bicep/
2. **GitHub Repository**: https://github.com/Azure/bicep-registry-modules
3. **Bicep Registry**: Available at `mcr.microsoft.com/bicep`

---

## Deployment Commands

### Azure CLI

```bash
# Deploy to resource group
az deployment group create \
  --resource-group myRG \
  --template-file main.bicep \
  --parameters @main.bicepparam

# Deploy to subscription
az deployment sub create \
  --location eastus \
  --template-file main.bicep

# Deploy to management group
az deployment mg create \
  --management-group-id myMG \
  --location eastus \
  --template-file main.bicep

# What-if deployment (preview changes)
az deployment group what-if \
  --resource-group myRG \
  --template-file main.bicep

# Validate without deploying
az deployment group validate \
  --resource-group myRG \
  --template-file main.bicep
```

### PowerShell

```powershell
# Deploy to resource group
New-AzResourceGroupDeployment `
  -ResourceGroupName myRG `
  -TemplateFile main.bicep `
  -TemplateParameterFile main.bicepparam

# Deploy to subscription
New-AzSubscriptionDeployment `
  -Location eastus `
  -TemplateFile main.bicep

# What-if deployment
New-AzResourceGroupDeployment `
  -ResourceGroupName myRG `
  -TemplateFile main.bicep `
  -WhatIf
```

### Deployment Stacks

```bash
# Create deployment stack at resource group scope
az stack group create \
  --name myStack \
  --resource-group myRG \
  --template-file main.bicep \
  --action-on-unmanage detachAll \
  --deny-settings-mode none

# Update deployment stack
az stack group create \
  --name myStack \
  --resource-group myRG \
  --template-file main.bicep \
  --action-on-unmanage deleteAll

# Delete deployment stack
az stack group delete \
  --name myStack \
  --resource-group myRG \
  --action-on-unmanage deleteAll
```

---

## Advanced Best Practices

### Conditional Deployments

```bicep
// Conditional resource deployment
resource diagSettings 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = if (enableDiagnostics) {
  name: 'diag'
  scope: storageAccount
  properties: {
    workspaceId: logAnalyticsWorkspaceId
    logs: [
      {
        category: 'StorageRead'
        enabled: true
      }
    ]
  }
}
```

### Loops

```bicep
// Array iteration
param storageAccounts array = ['sa1', 'sa2', 'sa3']

resource storages 'Microsoft.Storage/storageAccounts@2023-05-01' = [for name in storageAccounts: {
  name: '${name}${uniqueString(resourceGroup().id)}'
  location: location
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
}]

// Index-based loop
resource subnets 'Microsoft.Network/virtualNetworks/subnets@2023-09-01' = [for (subnet, i) in subnetsConfig: {
  name: '${vnet.name}/${subnet.name}'
  properties: {
    addressPrefix: subnet.prefix
  }
}]
```

### User-Defined Types

```bicep
// Define custom type
type storageAccountConfig = {
  name: string
  sku: 'Standard_LRS' | 'Standard_GRS' | 'Premium_LRS'
  @description('Enable blob public access')
  allowBlobPublicAccess: bool?
}

// Use the type
param storageConfig storageAccountConfig
```

### User-Defined Functions (Preview)

```bicep
// Define function
func buildResourceName(prefix string, suffix string) string => '${prefix}-${uniqueString(resourceGroup().id)}-${suffix}'

// Use function
var vmName = buildResourceName('vm', 'prod')
```

### Using `loadTextContent` and `loadJsonContent`

```bicep
// Load external content
var script = loadTextContent('scripts/configure.sh')
var config = loadJsonContent('config/settings.json')
```

---

## Troubleshooting

### Common Errors

**Error: Resource type not found**
- Check the provider namespace spelling
- Verify the API version exists
- Ensure the provider is registered in the subscription

**Error: Invalid resource name**
- Check naming constraints (length, allowed characters)
- Ensure uniqueness where required

**Error: Deployment failed - resource exists**
- Use `existing` keyword for pre-existing resources
- Check if resource is in a different resource group

### Debugging Tips

```bash
# Verbose deployment output
az deployment group create \
  --resource-group myRG \
  --template-file main.bicep \
  --debug

# View deployment operations
az deployment group show \
  --resource-group myRG \
  --name deploymentName \
  --query properties.outputs

# Check deployment errors
az deployment operation group list \
  --resource-group myRG \
  --name deploymentName \
  --query "[?properties.statusMessage.error != null]"
```

### VS Code Bicep Extension

Install the official Bicep extension for:
- IntelliSense and auto-completion
- Syntax highlighting
- Real-time validation
- Quick fixes
- Hover documentation

---

## Additional Resources

- [Bicep Documentation](https://learn.microsoft.com/azure/azure-resource-manager/bicep/)
- [Bicep Playground](https://aka.ms/bicepdemo)
- [Azure Verified Modules](https://azure.github.io/Azure-Verified-Modules/)
- [Bicep GitHub Repository](https://github.com/Azure/bicep)
- [ARM Template Reference](https://learn.microsoft.com/azure/templates/)
