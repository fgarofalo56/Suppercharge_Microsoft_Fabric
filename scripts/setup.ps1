#Requires -Version 5.1
<#
.SYNOPSIS
    Complete environment setup for Microsoft Fabric Casino/Gaming POC.

.DESCRIPTION
    This script performs the following:
    - Checks prerequisites (Python 3.10+, Azure CLI, Bicep, Git)
    - Creates Python virtual environment
    - Installs dependencies from requirements.txt
    - Validates Azure login
    - Displays next steps

.PARAMETER SkipAzureLogin
    Skip Azure CLI login validation.

.PARAMETER VenvPath
    Path for virtual environment (default: .venv)

.EXAMPLE
    .\setup.ps1
    .\setup.ps1 -SkipAzureLogin
    .\setup.ps1 -VenvPath "C:\envs\fabric-poc"

.NOTES
    Author: Microsoft Fabric POC Team
    Version: 1.0.0
#>

[CmdletBinding()]
param(
    [switch]$SkipAzureLogin,
    [string]$VenvPath = ".venv"
)

# =============================================================================
# Configuration
# =============================================================================
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

$MinPythonVersion = [Version]"3.10.0"
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptRoot

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

function Test-CommandExists {
    param([string]$Command)
    $oldPreference = $ErrorActionPreference
    $ErrorActionPreference = "SilentlyContinue"
    try {
        if (Get-Command $Command) { return $true }
    } catch {
        return $false
    } finally {
        $ErrorActionPreference = $oldPreference
    }
    return $false
}

function Get-PythonVersion {
    param([string]$PythonCmd)
    try {
        $output = & $PythonCmd --version 2>&1
        if ($output -match "Python (\d+\.\d+\.\d+)") {
            return [Version]$Matches[1]
        }
    } catch {
        return $null
    }
    return $null
}

# =============================================================================
# Main Script
# =============================================================================

Write-Header "Microsoft Fabric Casino/Gaming POC - Environment Setup"

Write-Host "Project Root: $ProjectRoot" -ForegroundColor Gray
Write-Host "Script Root:  $ScriptRoot" -ForegroundColor Gray
Write-Host ""

# Change to project root
Set-Location $ProjectRoot

# =============================================================================
# Step 1: Check Prerequisites
# =============================================================================
Write-Header "Step 1: Checking Prerequisites"

$PrerequisitesMet = $true
$PythonCmd = $null

# Check Python
Write-Step "Checking Python 3.10+..."
$pythonCommands = @("python", "python3", "py")
foreach ($cmd in $pythonCommands) {
    if (Test-CommandExists $cmd) {
        $version = Get-PythonVersion $cmd
        if ($version -and $version -ge $MinPythonVersion) {
            $PythonCmd = $cmd
            Write-Success "Found $cmd version $version"
            break
        }
    }
}

if (-not $PythonCmd) {
    Write-Failure "Python 3.10+ not found"
    Write-Info "Please install Python 3.10 or later from https://www.python.org/downloads/"
    $PrerequisitesMet = $false
}

# Check Git
Write-Step "Checking Git..."
if (Test-CommandExists "git") {
    $gitVersion = (git --version) -replace "git version ", ""
    Write-Success "Found Git version $gitVersion"
} else {
    Write-Failure "Git not found"
    Write-Info "Please install Git from https://git-scm.com/downloads"
    $PrerequisitesMet = $false
}

# Check Azure CLI
Write-Step "Checking Azure CLI..."
if (Test-CommandExists "az") {
    $azVersion = (az version --query '\"azure-cli\"' -o tsv 2>$null)
    Write-Success "Found Azure CLI version $azVersion"
} else {
    Write-Failure "Azure CLI not found"
    Write-Info "Please install Azure CLI from https://docs.microsoft.com/cli/azure/install-azure-cli"
    $PrerequisitesMet = $false
}

# Check Bicep
Write-Step "Checking Bicep..."
if (Test-CommandExists "az") {
    $bicepVersion = az bicep version 2>$null
    if ($bicepVersion) {
        Write-Success "Found Bicep: $($bicepVersion -replace 'Bicep CLI version ', '')"
    } else {
        Write-Info "Bicep not installed, attempting to install..."
        try {
            az bicep install
            Write-Success "Bicep installed successfully"
        } catch {
            Write-Failure "Failed to install Bicep"
            Write-Info "Run 'az bicep install' manually"
            $PrerequisitesMet = $false
        }
    }
} else {
    Write-Info "Skipping Bicep check (Azure CLI not available)"
}

# Check pip
Write-Step "Checking pip..."
if ($PythonCmd) {
    try {
        $pipVersion = & $PythonCmd -m pip --version 2>&1
        if ($pipVersion -match "pip (\d+\.\d+)") {
            Write-Success "Found pip version $($Matches[1])"
        }
    } catch {
        Write-Failure "pip not available"
        $PrerequisitesMet = $false
    }
}

if (-not $PrerequisitesMet) {
    Write-Host ""
    Write-Failure "Prerequisites check failed. Please install missing components."
    exit 1
}

Write-Success "All prerequisites met!"

# =============================================================================
# Step 2: Create Virtual Environment
# =============================================================================
Write-Header "Step 2: Creating Python Virtual Environment"

$VenvFullPath = Join-Path $ProjectRoot $VenvPath

if (Test-Path $VenvFullPath) {
    Write-Info "Virtual environment already exists at $VenvFullPath"
    $response = Read-Host "Do you want to recreate it? (y/N)"
    if ($response -eq "y" -or $response -eq "Y") {
        Write-Step "Removing existing virtual environment..."
        Remove-Item -Recurse -Force $VenvFullPath
    } else {
        Write-Info "Using existing virtual environment"
    }
}

if (-not (Test-Path $VenvFullPath)) {
    Write-Step "Creating virtual environment at $VenvFullPath..."
    & $PythonCmd -m venv $VenvFullPath
    if ($LASTEXITCODE -ne 0) {
        Write-Failure "Failed to create virtual environment"
        exit 1
    }
    Write-Success "Virtual environment created"
}

# =============================================================================
# Step 3: Activate Virtual Environment and Install Dependencies
# =============================================================================
Write-Header "Step 3: Installing Dependencies"

$VenvActivate = Join-Path $VenvFullPath "Scripts\Activate.ps1"
$VenvPython = Join-Path $VenvFullPath "Scripts\python.exe"
$VenvPip = Join-Path $VenvFullPath "Scripts\pip.exe"

if (-not (Test-Path $VenvActivate)) {
    Write-Failure "Virtual environment activation script not found"
    exit 1
}

Write-Step "Activating virtual environment..."
& $VenvActivate

Write-Step "Upgrading pip..."
& $VenvPython -m pip install --upgrade pip --quiet
Write-Success "pip upgraded"

# Install main requirements
$RequirementsFile = Join-Path $ProjectRoot "requirements.txt"
if (Test-Path $RequirementsFile) {
    Write-Step "Installing requirements from requirements.txt..."
    & $VenvPip install -r $RequirementsFile --quiet
    if ($LASTEXITCODE -ne 0) {
        Write-Failure "Failed to install requirements"
        exit 1
    }
    Write-Success "Main dependencies installed"
} else {
    Write-Failure "requirements.txt not found"
    exit 1
}

# Install dev requirements if exists
$DevRequirementsFile = Join-Path $ProjectRoot "requirements-dev.txt"
if (Test-Path $DevRequirementsFile) {
    Write-Step "Installing development dependencies..."
    & $VenvPip install -r $DevRequirementsFile --quiet
    if ($LASTEXITCODE -ne 0) {
        Write-Info "Warning: Some dev dependencies failed to install"
    } else {
        Write-Success "Development dependencies installed"
    }
}

# =============================================================================
# Step 4: Validate Azure Login
# =============================================================================
if (-not $SkipAzureLogin) {
    Write-Header "Step 4: Validating Azure Login"

    Write-Step "Checking Azure CLI login status..."
    $account = az account show 2>$null | ConvertFrom-Json

    if ($account) {
        Write-Success "Logged in to Azure"
        Write-Info "Subscription: $($account.name)"
        Write-Info "Tenant ID:    $($account.tenantId)"
        Write-Info "User:         $($account.user.name)"
    } else {
        Write-Info "Not logged in to Azure CLI"
        $response = Read-Host "Do you want to log in now? (y/N)"
        if ($response -eq "y" -or $response -eq "Y") {
            Write-Step "Opening Azure login..."
            az login
            if ($LASTEXITCODE -ne 0) {
                Write-Failure "Azure login failed"
            } else {
                Write-Success "Azure login successful"
            }
        } else {
            Write-Info "Skipping Azure login"
            Write-Info "Run 'az login' before deploying infrastructure"
        }
    }
} else {
    Write-Info "Skipping Azure login validation (--SkipAzureLogin specified)"
}

# =============================================================================
# Step 5: Setup .env File
# =============================================================================
Write-Header "Step 5: Environment Configuration"

$EnvFile = Join-Path $ProjectRoot ".env"
$EnvSampleFile = Join-Path $ProjectRoot ".env.sample"

if (-not (Test-Path $EnvFile)) {
    if (Test-Path $EnvSampleFile) {
        Write-Step "Creating .env from .env.sample..."
        Copy-Item $EnvSampleFile $EnvFile
        Write-Success ".env file created"
        Write-Info "Please edit .env and fill in your configuration values"
    } else {
        Write-Info ".env.sample not found, skipping .env creation"
    }
} else {
    Write-Info ".env file already exists"
}

# =============================================================================
# Summary and Next Steps
# =============================================================================
Write-Header "Setup Complete!"

Write-Host "Environment is ready for development." -ForegroundColor Green
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  1. Activate the virtual environment:" -ForegroundColor White
Write-Host "     $VenvActivate" -ForegroundColor Cyan
Write-Host ""
Write-Host "  2. Edit .env with your Azure configuration:" -ForegroundColor White
Write-Host "     code .env" -ForegroundColor Cyan
Write-Host ""
Write-Host "  3. Generate sample data:" -ForegroundColor White
Write-Host "     .\scripts\generate-data.ps1 --quick" -ForegroundColor Cyan
Write-Host ""
Write-Host "  4. Deploy infrastructure (requires .env configuration):" -ForegroundColor White
Write-Host "     .\scripts\deploy-infrastructure.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "  5. Validate environment:" -ForegroundColor White
Write-Host "     .\scripts\validate-environment.ps1" -ForegroundColor Cyan
Write-Host ""

Write-Host "For help, see scripts\README.md" -ForegroundColor Gray
Write-Host ""
