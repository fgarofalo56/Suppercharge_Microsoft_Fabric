#Requires -Version 5.1
<#
.SYNOPSIS
    Cleanup and teardown Microsoft Fabric POC resources.

.DESCRIPTION
    This script performs cleanup operations:
    - Delete Azure resource group (with confirmation)
    - Clean local generated data
    - Remove Python virtual environment (optional)

.PARAMETER DeleteAzure
    Delete the Azure resource group and all resources

.PARAMETER DeleteData
    Delete local generated data

.PARAMETER DeleteVenv
    Delete Python virtual environment

.PARAMETER All
    Delete everything (Azure, data, venv)

.PARAMETER Force
    Skip confirmation prompts

.PARAMETER Environment
    Target environment: dev, staging, prod (default: dev)

.EXAMPLE
    .\cleanup.ps1 -DeleteData
    .\cleanup.ps1 -DeleteAzure
    .\cleanup.ps1 -All -Force
    .\cleanup.ps1 -DeleteAzure -Environment staging

.NOTES
    Author: Microsoft Fabric POC Team
    Version: 1.0.0
#>

[CmdletBinding(SupportsShouldProcess)]
param(
    [switch]$DeleteAzure,
    [switch]$DeleteData,
    [switch]$DeleteVenv,
    [switch]$All,
    [switch]$Force,
    [ValidateSet("dev", "staging", "prod")]
    [string]$Environment = "dev"
)

# =============================================================================
# Configuration
# =============================================================================
$ErrorActionPreference = "Stop"

$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptRoot
$EnvFile = Join-Path $ProjectRoot ".env"

# =============================================================================
# Helper Functions
# =============================================================================

function Write-Header {
    param([string]$Message)
    Write-Host ""
    Write-Host "=" * 70 -ForegroundColor Cyan
    Write-Host "  $Message" -ForegroundColor Cyan
    Write-Host "=" * 70 -ForegroundColor Cyan
    Write-Host ""
}

function Write-Step {
    param([string]$Message)
    Write-Host "[*] $Message" -ForegroundColor Yellow
}

function Write-Success {
    param([string]$Message)
    Write-Host "[+] $Message" -ForegroundColor Green
}

function Write-Failure {
    param([string]$Message)
    Write-Host "[-] $Message" -ForegroundColor Red
}

function Write-Info {
    param([string]$Message)
    Write-Host "    $Message" -ForegroundColor Gray
}

function Write-Warning-Custom {
    param([string]$Message)
    Write-Host "[!] $Message" -ForegroundColor Red
}

function Load-EnvFile {
    param([string]$Path)

    $envVars = @{}

    if (Test-Path $Path) {
        Get-Content $Path | ForEach-Object {
            $line = $_.Trim()
            if ($line -and -not $line.StartsWith("#")) {
                $parts = $line -split "=", 2
                if ($parts.Count -eq 2) {
                    $key = $parts[0].Trim()
                    $value = $parts[1].Trim() -replace '^["'']|["'']$', ''
                    $envVars[$key] = $value
                }
            }
        }
    }

    return $envVars
}

function Confirm-Action {
    param(
        [string]$Message,
        [string]$DefaultNo = "N"
    )

    if ($Force) {
        return $true
    }

    $response = Read-Host "$Message (y/N)"
    return ($response -eq "y" -or $response -eq "Y")
}

# =============================================================================
# Main Script
# =============================================================================

Write-Header "Microsoft Fabric POC - Cleanup"

# Handle -All flag
if ($All) {
    $DeleteAzure = $true
    $DeleteData = $true
    $DeleteVenv = $true
}

# Check if any action specified
if (-not ($DeleteAzure -or $DeleteData -or $DeleteVenv)) {
    Write-Host "No cleanup action specified." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor White
    Write-Host "  .\cleanup.ps1 -DeleteData        # Delete generated data"
    Write-Host "  .\cleanup.ps1 -DeleteAzure       # Delete Azure resources"
    Write-Host "  .\cleanup.ps1 -DeleteVenv        # Delete virtual environment"
    Write-Host "  .\cleanup.ps1 -All               # Delete everything"
    Write-Host "  .\cleanup.ps1 -All -Force        # Delete everything without prompts"
    Write-Host ""
    exit 0
}

# Display what will be cleaned
Write-Step "Cleanup plan:"
if ($DeleteData) { Write-Info "- Delete generated data" }
if ($DeleteVenv) { Write-Info "- Delete Python virtual environment" }
if ($DeleteAzure) { Write-Info "- Delete Azure resource group ($Environment)" }
Write-Host ""

# =============================================================================
# Delete Generated Data
# =============================================================================
if ($DeleteData) {
    Write-Header "Cleaning Generated Data"

    $dataPaths = @(
        (Join-Path $ProjectRoot "data\generated"),
        (Join-Path $ProjectRoot "output"),
        (Join-Path $ProjectRoot "data\output")
    )

    foreach ($path in $dataPaths) {
        if (Test-Path $path) {
            $fileCount = (Get-ChildItem -Path $path -Recurse -File -ErrorAction SilentlyContinue | Measure-Object).Count
            $size = (Get-ChildItem -Path $path -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum

            Write-Info "Found: $path"
            Write-Info "Files: $fileCount, Size: $([math]::Round($size / 1MB, 2)) MB"

            if (Confirm-Action "Delete $path?") {
                Write-Step "Deleting $path..."
                Remove-Item -Recurse -Force $path
                Write-Success "Deleted"
            } else {
                Write-Info "Skipped"
            }
        }
    }

    # Clean temp files
    $tempFiles = Get-ChildItem -Path $ProjectRoot -Filter "tmpclaude-*" -File -ErrorAction SilentlyContinue
    if ($tempFiles) {
        Write-Step "Found $($tempFiles.Count) temporary files"
        if (Confirm-Action "Delete temporary files?") {
            $tempFiles | Remove-Item -Force
            Write-Success "Temporary files deleted"
        }
    }

    Write-Success "Data cleanup complete"
}

# =============================================================================
# Delete Virtual Environment
# =============================================================================
if ($DeleteVenv) {
    Write-Header "Cleaning Virtual Environment"

    $venvPaths = @(
        (Join-Path $ProjectRoot ".venv"),
        (Join-Path $ProjectRoot "venv")
    )

    $found = $false
    foreach ($path in $venvPaths) {
        if (Test-Path $path) {
            $found = $true
            $size = (Get-ChildItem -Path $path -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum

            Write-Info "Found: $path"
            Write-Info "Size: $([math]::Round($size / 1MB, 2)) MB"

            if (Confirm-Action "Delete virtual environment at $path?") {
                Write-Step "Deleting $path..."

                # Deactivate if active
                if ($env:VIRTUAL_ENV -eq $path) {
                    Write-Info "Deactivating virtual environment..."
                    deactivate 2>$null
                }

                Remove-Item -Recurse -Force $path
                Write-Success "Virtual environment deleted"
            } else {
                Write-Info "Skipped"
            }
        }
    }

    if (-not $found) {
        Write-Info "No virtual environment found"
    }

    # Clean __pycache__ directories
    $pycacheDirs = Get-ChildItem -Path $ProjectRoot -Filter "__pycache__" -Directory -Recurse -ErrorAction SilentlyContinue
    if ($pycacheDirs) {
        Write-Step "Found $($pycacheDirs.Count) __pycache__ directories"
        if (Confirm-Action "Delete __pycache__ directories?") {
            $pycacheDirs | Remove-Item -Recurse -Force
            Write-Success "__pycache__ directories deleted"
        }
    }

    # Clean .pytest_cache
    $pytestCache = Join-Path $ProjectRoot ".pytest_cache"
    if (Test-Path $pytestCache) {
        Write-Step "Found .pytest_cache"
        if (Confirm-Action "Delete .pytest_cache?") {
            Remove-Item -Recurse -Force $pytestCache
            Write-Success ".pytest_cache deleted"
        }
    }

    Write-Success "Virtual environment cleanup complete"
}

# =============================================================================
# Delete Azure Resources
# =============================================================================
if ($DeleteAzure) {
    Write-Header "Cleaning Azure Resources"

    # Load .env for resource group name
    $envVars = @{}
    if (Test-Path $EnvFile) {
        $envVars = Load-EnvFile $EnvFile
    }

    $projectPrefix = $envVars['PROJECT_PREFIX']
    if (-not $projectPrefix) {
        Write-Failure "PROJECT_PREFIX not found in .env file"
        Write-Info "Cannot determine resource group name"
        exit 1
    }

    $resourceGroupName = "$projectPrefix-$Environment-rg"

    Write-Warning-Custom "WARNING: This will permanently delete all Azure resources!"
    Write-Host ""
    Write-Info "Resource Group: $resourceGroupName"
    Write-Info "Environment:    $Environment"
    Write-Host ""

    # Check if logged in
    $account = az account show 2>$null | ConvertFrom-Json
    if (-not $account) {
        Write-Failure "Not logged in to Azure CLI"
        Write-Info "Run 'az login' to authenticate"
        exit 1
    }

    Write-Info "Logged in as: $($account.user.name)"

    # Set subscription if specified
    if ($envVars['AZURE_SUBSCRIPTION_ID']) {
        az account set --subscription $envVars['AZURE_SUBSCRIPTION_ID'] 2>$null
    }

    # Check if resource group exists
    $rgExists = az group exists --name $resourceGroupName
    if ($rgExists -ne "true") {
        Write-Info "Resource group '$resourceGroupName' does not exist"
    } else {
        # List resources in the group
        Write-Step "Resources in $resourceGroupName:"
        $resources = az resource list --resource-group $resourceGroupName --query "[].{Name:name, Type:type}" -o json 2>$null | ConvertFrom-Json
        if ($resources) {
            foreach ($resource in $resources) {
                Write-Info "  - $($resource.Name) ($($resource.Type))"
            }
        }
        Write-Host ""

        Write-Warning-Custom "This action is IRREVERSIBLE!"

        if (-not $Force) {
            Write-Host ""
            Write-Host "Type the resource group name to confirm deletion: " -NoNewline -ForegroundColor Red
            $confirmation = Read-Host

            if ($confirmation -ne $resourceGroupName) {
                Write-Info "Confirmation failed - resource group NOT deleted"
                exit 0
            }
        }

        Write-Step "Deleting resource group: $resourceGroupName"
        Write-Info "This may take several minutes..."

        $startTime = Get-Date

        az group delete --name $resourceGroupName --yes --no-wait 2>$null

        if ($LASTEXITCODE -eq 0) {
            Write-Success "Resource group deletion initiated"
            Write-Info "Deletion is running in the background"
            Write-Info "Check Azure Portal for status"
        } else {
            Write-Failure "Failed to delete resource group"
            exit 1
        }
    }

    # Clean deployment outputs file
    $outputFile = Join-Path $ProjectRoot "deployment-outputs.json"
    if (Test-Path $outputFile) {
        Write-Step "Found deployment-outputs.json"
        if (Confirm-Action "Delete deployment outputs file?") {
            Remove-Item -Force $outputFile
            Write-Success "Deployment outputs deleted"
        }
    }

    Write-Success "Azure cleanup initiated"
}

# =============================================================================
# Summary
# =============================================================================
Write-Header "Cleanup Complete!"

Write-Success "Cleanup operations completed"
Write-Host ""

if ($DeleteAzure) {
    Write-Host "Note: Azure resource group deletion may take several minutes." -ForegroundColor Yellow
    Write-Host "Check the Azure Portal for confirmation." -ForegroundColor Yellow
    Write-Host ""
}

if ($DeleteVenv) {
    Write-Host "To recreate the environment, run:" -ForegroundColor Yellow
    Write-Host "  .\scripts\setup.ps1" -ForegroundColor Cyan
    Write-Host ""
}
