<#
.SYNOPSIS
    Retrieves metadata for Azure Verified Modules (AVM) from the Bicep Public Registry.

.DESCRIPTION
    Fetches and displays information about available Azure Verified Modules,
    including module names, descriptions, versions, and documentation links.

.PARAMETER Search
    Search term to filter modules

.PARAMETER Type
    Module type filter: res (resource), ptn (pattern), utl (utility), or all

.PARAMETER OutputFormat
    Output format: Table, Json, or List

.PARAMETER ShowLatest
    Show only the latest 20 modules (faster)

.EXAMPLE
    .\get-avm-modules.ps1

.EXAMPLE
    .\get-avm-modules.ps1 -Search "storage"

.EXAMPLE
    .\get-avm-modules.ps1 -Type res -Search "network"
#>

param(
    [string]$Search = "",

    [ValidateSet("all", "res", "ptn", "utl")]
    [string]$Type = "all",

    [ValidateSet("Table", "Json", "List")]
    [string]$OutputFormat = "Table",

    [switch]$ShowLatest
)

Write-Host "Azure Verified Modules (AVM) Catalog" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# AVM module index URL
$indexUrl = "https://azure.github.io/Azure-Verified-Modules/indexes/bicep/"

# Define commonly used AVM modules with their details
# This is a curated list - for full catalog, visit the AVM website
$avmModules = @(
    # Resource Modules (res)
    @{
        Name = "avm/res/storage/storage-account"
        Description = "Storage Account with blob, file, queue, and table services"
        Type = "res"
        LatestVersion = "0.9.0"
        DocsUrl = "https://github.com/Azure/bicep-registry-modules/tree/main/avm/res/storage/storage-account"
        RegistryRef = "br/public:avm/res/storage/storage-account:0.9.0"
    },
    @{
        Name = "avm/res/network/virtual-network"
        Description = "Virtual Network with subnets, peering, and DNS configuration"
        Type = "res"
        LatestVersion = "0.4.0"
        DocsUrl = "https://github.com/Azure/bicep-registry-modules/tree/main/avm/res/network/virtual-network"
        RegistryRef = "br/public:avm/res/network/virtual-network:0.4.0"
    },
    @{
        Name = "avm/res/network/network-security-group"
        Description = "Network Security Group with security rules"
        Type = "res"
        LatestVersion = "0.3.0"
        DocsUrl = "https://github.com/Azure/bicep-registry-modules/tree/main/avm/res/network/network-security-group"
        RegistryRef = "br/public:avm/res/network/network-security-group:0.3.0"
    },
    @{
        Name = "avm/res/compute/virtual-machine"
        Description = "Virtual Machine with extensions and diagnostics"
        Type = "res"
        LatestVersion = "0.5.0"
        DocsUrl = "https://github.com/Azure/bicep-registry-modules/tree/main/avm/res/compute/virtual-machine"
        RegistryRef = "br/public:avm/res/compute/virtual-machine:0.5.0"
    },
    @{
        Name = "avm/res/key-vault/vault"
        Description = "Key Vault with secrets, keys, and certificates management"
        Type = "res"
        LatestVersion = "0.6.0"
        DocsUrl = "https://github.com/Azure/bicep-registry-modules/tree/main/avm/res/key-vault/vault"
        RegistryRef = "br/public:avm/res/key-vault/vault:0.6.0"
    },
    @{
        Name = "avm/res/web/site"
        Description = "Web App / App Service with configuration and deployment slots"
        Type = "res"
        LatestVersion = "0.3.0"
        DocsUrl = "https://github.com/Azure/bicep-registry-modules/tree/main/avm/res/web/site"
        RegistryRef = "br/public:avm/res/web/site:0.3.0"
    },
    @{
        Name = "avm/res/web/serverfarm"
        Description = "App Service Plan for hosting web apps"
        Type = "res"
        LatestVersion = "0.2.0"
        DocsUrl = "https://github.com/Azure/bicep-registry-modules/tree/main/avm/res/web/serverfarm"
        RegistryRef = "br/public:avm/res/web/serverfarm:0.2.0"
    },
    @{
        Name = "avm/res/sql/server"
        Description = "Azure SQL Server with databases and firewall rules"
        Type = "res"
        LatestVersion = "0.4.0"
        DocsUrl = "https://github.com/Azure/bicep-registry-modules/tree/main/avm/res/sql/server"
        RegistryRef = "br/public:avm/res/sql/server:0.4.0"
    },
    @{
        Name = "avm/res/container-service/managed-cluster"
        Description = "Azure Kubernetes Service (AKS) cluster"
        Type = "res"
        LatestVersion = "0.3.0"
        DocsUrl = "https://github.com/Azure/bicep-registry-modules/tree/main/avm/res/container-service/managed-cluster"
        RegistryRef = "br/public:avm/res/container-service/managed-cluster:0.3.0"
    },
    @{
        Name = "avm/res/container-registry/registry"
        Description = "Azure Container Registry (ACR)"
        Type = "res"
        LatestVersion = "0.4.0"
        DocsUrl = "https://github.com/Azure/bicep-registry-modules/tree/main/avm/res/container-registry/registry"
        RegistryRef = "br/public:avm/res/container-registry/registry:0.4.0"
    },
    @{
        Name = "avm/res/operational-insights/workspace"
        Description = "Log Analytics Workspace"
        Type = "res"
        LatestVersion = "0.4.0"
        DocsUrl = "https://github.com/Azure/bicep-registry-modules/tree/main/avm/res/operational-insights/workspace"
        RegistryRef = "br/public:avm/res/operational-insights/workspace:0.4.0"
    },
    @{
        Name = "avm/res/network/private-endpoint"
        Description = "Private Endpoint for Azure services"
        Type = "res"
        LatestVersion = "0.4.0"
        DocsUrl = "https://github.com/Azure/bicep-registry-modules/tree/main/avm/res/network/private-endpoint"
        RegistryRef = "br/public:avm/res/network/private-endpoint:0.4.0"
    },
    @{
        Name = "avm/res/network/application-gateway"
        Description = "Application Gateway with WAF"
        Type = "res"
        LatestVersion = "0.3.0"
        DocsUrl = "https://github.com/Azure/bicep-registry-modules/tree/main/avm/res/network/application-gateway"
        RegistryRef = "br/public:avm/res/network/application-gateway:0.3.0"
    },
    @{
        Name = "avm/res/network/load-balancer"
        Description = "Azure Load Balancer"
        Type = "res"
        LatestVersion = "0.2.0"
        DocsUrl = "https://github.com/Azure/bicep-registry-modules/tree/main/avm/res/network/load-balancer"
        RegistryRef = "br/public:avm/res/network/load-balancer:0.2.0"
    },
    @{
        Name = "avm/res/insights/component"
        Description = "Application Insights"
        Type = "res"
        LatestVersion = "0.3.0"
        DocsUrl = "https://github.com/Azure/bicep-registry-modules/tree/main/avm/res/insights/component"
        RegistryRef = "br/public:avm/res/insights/component:0.3.0"
    },
    # Pattern Modules (ptn)
    @{
        Name = "avm/ptn/authorization/resource-role-assignment"
        Description = "Role assignment pattern for RBAC"
        Type = "ptn"
        LatestVersion = "0.1.0"
        DocsUrl = "https://github.com/Azure/bicep-registry-modules/tree/main/avm/ptn/authorization/resource-role-assignment"
        RegistryRef = "br/public:avm/ptn/authorization/resource-role-assignment:0.1.0"
    },
    @{
        Name = "avm/ptn/network/private-link-private-dns-zones"
        Description = "Private Link DNS zone configuration"
        Type = "ptn"
        LatestVersion = "0.2.0"
        DocsUrl = "https://github.com/Azure/bicep-registry-modules/tree/main/avm/ptn/network/private-link-private-dns-zones"
        RegistryRef = "br/public:avm/ptn/network/private-link-private-dns-zones:0.2.0"
    },
    @{
        Name = "avm/ptn/lz/sub-vending"
        Description = "Landing zone subscription vending"
        Type = "ptn"
        LatestVersion = "0.1.0"
        DocsUrl = "https://github.com/Azure/bicep-registry-modules/tree/main/avm/ptn/lz/sub-vending"
        RegistryRef = "br/public:avm/ptn/lz/sub-vending:0.1.0"
    },
    # Utility Modules (utl)
    @{
        Name = "avm/utl/types/avm-common-types"
        Description = "Common type definitions for AVM modules"
        Type = "utl"
        LatestVersion = "0.1.0"
        DocsUrl = "https://github.com/Azure/bicep-registry-modules/tree/main/avm/utl/types/avm-common-types"
        RegistryRef = "br/public:avm/utl/types/avm-common-types:0.1.0"
    }
)

# Filter by type
if ($Type -ne "all") {
    $avmModules = $avmModules | Where-Object { $_.Type -eq $Type }
}

# Filter by search term
if ($Search) {
    $avmModules = $avmModules | Where-Object {
        $_.Name -like "*$Search*" -or $_.Description -like "*$Search*"
    }
}

# Display results
$count = $avmModules.Count

if ($count -eq 0) {
    Write-Host "No modules found matching your criteria." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "For the complete catalog, visit:" -ForegroundColor Cyan
    Write-Host "  https://azure.github.io/Azure-Verified-Modules/indexes/bicep/" -ForegroundColor Blue
    exit 0
}

switch ($OutputFormat) {
    "Table" {
        Write-Host "Module Type Legend: res=Resource, ptn=Pattern, utl=Utility" -ForegroundColor Gray
        Write-Host ""

        foreach ($module in $avmModules) {
            $typeColor = switch ($module.Type) {
                "res" { "Green" }
                "ptn" { "Magenta" }
                "utl" { "Yellow" }
            }

            Write-Host "[$($module.Type)]" -ForegroundColor $typeColor -NoNewline
            Write-Host " $($module.Name)" -ForegroundColor Cyan
            Write-Host "  $($module.Description)" -ForegroundColor Gray
            Write-Host "  Version: $($module.LatestVersion) | " -ForegroundColor DarkGray -NoNewline
            Write-Host "Ref: $($module.RegistryRef)" -ForegroundColor DarkGray
            Write-Host ""
        }
    }
    "List" {
        foreach ($module in $avmModules) {
            Write-Host "$($module.RegistryRef)"
        }
    }
    "Json" {
        $avmModules | ConvertTo-Json -Depth 3
    }
}

Write-Host "Total modules: $count" -ForegroundColor Cyan
Write-Host ""
Write-Host "Usage Example:" -ForegroundColor Yellow
Write-Host "==============" -ForegroundColor Yellow
Write-Host ""

$example = @"
// Use in your Bicep file
module storage 'br/public:avm/res/storage/storage-account:0.9.0' = {
  name: 'storageDeployment'
  params: {
    name: 'mystorageaccount'
    location: location
  }
}
"@

Write-Host $example -ForegroundColor Gray

Write-Host ""
Write-Host "Full AVM Catalog: https://azure.github.io/Azure-Verified-Modules/indexes/bicep/" -ForegroundColor Blue
Write-Host "GitHub: https://github.com/Azure/bicep-registry-modules" -ForegroundColor Blue
