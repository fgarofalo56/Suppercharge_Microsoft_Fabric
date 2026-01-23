<#
.SYNOPSIS
    Lists Azure resource types for a specific provider with their API versions.

.DESCRIPTION
    Queries the Azure Resource Manager to retrieve all resource types available
    for a given provider namespace, along with their available API versions.

.PARAMETER Provider
    The Azure provider namespace (e.g., Microsoft.Storage, Microsoft.Compute)

.PARAMETER ShowAllVersions
    If specified, shows all available API versions instead of just the latest

.PARAMETER OutputFormat
    Output format: Table, Json, or Csv

.EXAMPLE
    .\get-resource-types.ps1 -Provider "Microsoft.Storage"

.EXAMPLE
    .\get-resource-types.ps1 -Provider "Microsoft.Compute" -ShowAllVersions -OutputFormat Json
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$Provider,

    [switch]$ShowAllVersions,

    [ValidateSet("Table", "Json", "Csv")]
    [string]$OutputFormat = "Table"
)

# Check if Azure CLI is installed
if (-not (Get-Command az -ErrorAction SilentlyContinue)) {
    Write-Error "Azure CLI is not installed. Please install it from https://docs.microsoft.com/cli/azure/install-azure-cli"
    exit 1
}

# Check if logged in
$account = az account show 2>$null | ConvertFrom-Json
if (-not $account) {
    Write-Error "Not logged in to Azure. Please run 'az login' first."
    exit 1
}

Write-Host "Fetching resource types for provider: $Provider" -ForegroundColor Cyan
Write-Host "Subscription: $($account.name)" -ForegroundColor Gray
Write-Host ""

try {
    if ($ShowAllVersions) {
        $query = "resourceTypes[].{ResourceType:resourceType, ApiVersions:apiVersions}"
    } else {
        $query = "resourceTypes[].{ResourceType:resourceType, LatestApiVersion:apiVersions[0]}"
    }

    $result = az provider show --namespace $Provider --query $query 2>&1

    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to fetch resource types: $result"
        exit 1
    }

    $resourceTypes = $result | ConvertFrom-Json

    if (-not $resourceTypes -or $resourceTypes.Count -eq 0) {
        Write-Warning "No resource types found for provider: $Provider"
        Write-Host "Make sure the provider is registered in your subscription."
        Write-Host "Run: az provider register --namespace $Provider"
        exit 0
    }

    switch ($OutputFormat) {
        "Table" {
            if ($ShowAllVersions) {
                foreach ($rt in $resourceTypes) {
                    Write-Host "`n$Provider/$($rt.ResourceType)" -ForegroundColor Green
                    Write-Host "API Versions:" -ForegroundColor Yellow
                    $rt.ApiVersions | ForEach-Object { Write-Host "  $_" }
                }
            } else {
                Write-Host "Resource Type".PadRight(60) "Latest API Version" -ForegroundColor Yellow
                Write-Host ("-" * 80)
                foreach ($rt in $resourceTypes | Sort-Object ResourceType) {
                    $fullType = "$Provider/$($rt.ResourceType)"
                    Write-Host "$($fullType.PadRight(60)) $($rt.LatestApiVersion)"
                }
            }
            Write-Host ""
            Write-Host "Total resource types: $($resourceTypes.Count)" -ForegroundColor Cyan
        }
        "Json" {
            $output = $resourceTypes | ForEach-Object {
                @{
                    FullResourceType = "$Provider/$($_.ResourceType)"
                    ResourceType = $_.ResourceType
                    ApiVersions = if ($ShowAllVersions) { $_.ApiVersions } else { @($_.LatestApiVersion) }
                }
            }
            $output | ConvertTo-Json -Depth 3
        }
        "Csv" {
            if ($ShowAllVersions) {
                $resourceTypes | ForEach-Object {
                    [PSCustomObject]@{
                        FullResourceType = "$Provider/$($_.ResourceType)"
                        ResourceType = $_.ResourceType
                        ApiVersions = $_.ApiVersions -join ";"
                    }
                } | ConvertTo-Csv -NoTypeInformation
            } else {
                $resourceTypes | ForEach-Object {
                    [PSCustomObject]@{
                        FullResourceType = "$Provider/$($_.ResourceType)"
                        ResourceType = $_.ResourceType
                        LatestApiVersion = $_.LatestApiVersion
                    }
                } | ConvertTo-Csv -NoTypeInformation
            }
        }
    }

} catch {
    Write-Error "An error occurred: $_"
    exit 1
}

# Output Bicep usage example
Write-Host ""
Write-Host "Example Bicep usage:" -ForegroundColor Cyan
Write-Host "resource myResource '$Provider/<resourceType>@<apiVersion>' = {" -ForegroundColor Gray
Write-Host "  name: 'resourceName'" -ForegroundColor Gray
Write-Host "  location: location" -ForegroundColor Gray
Write-Host "  properties: {}" -ForegroundColor Gray
Write-Host "}" -ForegroundColor Gray
