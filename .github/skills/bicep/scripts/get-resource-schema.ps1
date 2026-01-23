<#
.SYNOPSIS
    Retrieves the schema for a specific Azure resource type.

.DESCRIPTION
    Uses the Bicep CLI and Azure provider data to retrieve detailed schema
    information for a specific Azure resource type and API version.

.PARAMETER ResourceType
    The full resource type string (e.g., Microsoft.Storage/storageAccounts@2023-05-01)

.PARAMETER Provider
    The provider namespace (e.g., Microsoft.Storage)

.PARAMETER Type
    The resource type within the provider (e.g., storageAccounts)

.PARAMETER ApiVersion
    The API version to use (e.g., 2023-05-01)

.EXAMPLE
    .\get-resource-schema.ps1 -ResourceType "Microsoft.Storage/storageAccounts@2023-05-01"

.EXAMPLE
    .\get-resource-schema.ps1 -Provider "Microsoft.Storage" -Type "storageAccounts" -ApiVersion "2023-05-01"
#>

param(
    [Parameter(ParameterSetName = "FullType")]
    [string]$ResourceType,

    [Parameter(ParameterSetName = "Components", Mandatory = $true)]
    [string]$Provider,

    [Parameter(ParameterSetName = "Components", Mandatory = $true)]
    [string]$Type,

    [Parameter(ParameterSetName = "Components", Mandatory = $true)]
    [string]$ApiVersion,

    [switch]$ShowExample
)

# Build resource type string if components provided
if ($Provider -and $Type -and $ApiVersion) {
    $ResourceType = "$Provider/$Type@$ApiVersion"
}

# Validate ResourceType
if (-not $ResourceType) {
    Write-Error "ResourceType is required. Provide either -ResourceType or -Provider, -Type, and -ApiVersion"
    Write-Host ""
    Write-Host "Usage examples:" -ForegroundColor Cyan
    Write-Host "  .\get-resource-schema.ps1 -ResourceType 'Microsoft.Storage/storageAccounts@2023-05-01'"
    Write-Host "  .\get-resource-schema.ps1 -Provider Microsoft.Storage -Type storageAccounts -ApiVersion 2023-05-01"
    exit 1
}

# Parse the resource type
if ($ResourceType -match "^(.+)/(.+)@(.+)$") {
    $parsedProvider = $Matches[1]
    $parsedType = $Matches[2]
    $parsedApiVersion = $Matches[3]
} else {
    Write-Error "Invalid resource type format. Expected: Provider/Type@ApiVersion"
    Write-Host "Example: Microsoft.Storage/storageAccounts@2023-05-01"
    exit 1
}

Write-Host "Fetching schema for: $ResourceType" -ForegroundColor Cyan
Write-Host ""

# Check for Bicep CLI
$hasBicep = Get-Command bicep -ErrorAction SilentlyContinue

if ($hasBicep) {
    Write-Host "Using Bicep CLI to generate schema information..." -ForegroundColor Gray

    # Create a temporary Bicep file to extract type information
    $tempDir = [System.IO.Path]::GetTempPath()
    $tempFile = Join-Path $tempDir "schema_$([guid]::NewGuid().ToString('N').Substring(0,8)).bicep"

    @"
// Auto-generated for schema extraction
resource example '$ResourceType' = {
  name: 'example'
  location: 'eastus'
  properties: {}
}

output resourceId string = example.id
"@ | Set-Content $tempFile

    try {
        # Try to build and capture any warnings/errors that reveal schema
        $buildResult = bicep build $tempFile --stdout 2>&1

        Write-Host "Resource Type Information:" -ForegroundColor Yellow
        Write-Host "=========================" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Provider:     $parsedProvider" -ForegroundColor Green
        Write-Host "Type:         $parsedType" -ForegroundColor Green
        Write-Host "API Version:  $parsedApiVersion" -ForegroundColor Green
        Write-Host ""

        # Get provider info from Azure CLI for more details
        if (Get-Command az -ErrorAction SilentlyContinue) {
            Write-Host "Fetching detailed schema from Azure..." -ForegroundColor Gray

            $providerInfo = az provider show --namespace $parsedProvider --query "resourceTypes[?resourceType=='$parsedType']" 2>$null | ConvertFrom-Json

            if ($providerInfo -and $providerInfo.Count -gt 0) {
                $rtInfo = $providerInfo[0]

                Write-Host ""
                Write-Host "Available API Versions:" -ForegroundColor Yellow
                $rtInfo.apiVersions | ForEach-Object { Write-Host "  $_" }

                if ($rtInfo.locations) {
                    Write-Host ""
                    Write-Host "Available Locations:" -ForegroundColor Yellow
                    $rtInfo.locations | Select-Object -First 10 | ForEach-Object { Write-Host "  $_" }
                    if ($rtInfo.locations.Count -gt 10) {
                        Write-Host "  ... and $($rtInfo.locations.Count - 10) more"
                    }
                }

                if ($rtInfo.capabilities) {
                    Write-Host ""
                    Write-Host "Capabilities:" -ForegroundColor Yellow
                    $rtInfo.capabilities | ForEach-Object { Write-Host "  $($_.name): $($_.value)" }
                }
            }
        }

    } finally {
        # Clean up temp file
        Remove-Item $tempFile -ErrorAction SilentlyContinue
    }
}

# Show example Bicep code
Write-Host ""
Write-Host "Example Bicep Declaration:" -ForegroundColor Cyan
Write-Host "==========================" -ForegroundColor Cyan
Write-Host ""

$exampleCode = @"
@description('The name of the $parsedType resource')
param resourceName string

@description('The location for the resource')
param location string = resourceGroup().location

resource myResource '$ResourceType' = {
  name: resourceName
  location: location
  // Add required properties here
  properties: {
    // Resource-specific properties
  }
}

output resourceId string = myResource.id
"@

Write-Host $exampleCode -ForegroundColor Gray

# Additional helpful information
Write-Host ""
Write-Host "Documentation Links:" -ForegroundColor Cyan
Write-Host "===================" -ForegroundColor Cyan
$docsUrl = "https://learn.microsoft.com/azure/templates/$($parsedProvider.ToLower())/$parsedType"
Write-Host "ARM Template Reference: $docsUrl" -ForegroundColor Blue

Write-Host ""
Write-Host "Tip: Use VS Code with the Bicep extension for IntelliSense and auto-completion" -ForegroundColor Yellow
