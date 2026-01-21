# Autonomous Agent Harness - Initialization Script
# Suppercharge Microsoft Fabric - Validation System
# Run this script to initialize or resume an autonomous validation session

param(
    [switch]$Resume,
    [switch]$Status,
    [switch]$Reset
)

$ErrorActionPreference = "Stop"
$HarnessDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = (Get-Item $HarnessDir).Parent.Parent.FullName

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Autonomous Agent Harness - Initializer" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Configuration
$ArchonProjectId = "c4b857a5-051d-4cca-8bdd-c44f5aa71020"
$FeaturesFile = Join-Path $HarnessDir "features.json"
$ProgressFile = Join-Path $HarnessDir "progress.txt"
$PromptsDir = Join-Path $HarnessDir "prompts"

function Get-CurrentStatus {
    Write-Host "Current Harness Status:" -ForegroundColor Yellow
    Write-Host ""

    # Read features.json
    if (Test-Path $FeaturesFile) {
        $features = Get-Content $FeaturesFile | ConvertFrom-Json
        Write-Host "  Total Features: $($features.total_features)" -ForegroundColor White
        Write-Host "  Completed:      $($features.completed)" -ForegroundColor Green
        Write-Host "  Passing:        $($features.passing)" -ForegroundColor Green
        Write-Host "  Failing:        $($features.failing)" -ForegroundColor Red
        Write-Host "  Pending:        $($features.pending)" -ForegroundColor Yellow
        Write-Host ""

        Write-Host "  Categories:" -ForegroundColor White
        foreach ($cat in $features.categories.PSObject.Properties) {
            $name = $cat.Name
            $total = $cat.Value.total
            $completed = $cat.Value.completed
            $status = if ($completed -eq $total) { "[DONE]" } else { "[$completed/$total]" }
            $color = if ($completed -eq $total) { "Green" } elseif ($completed -gt 0) { "Yellow" } else { "White" }
            Write-Host "    $name: $status" -ForegroundColor $color
        }
    } else {
        Write-Host "  Features file not found!" -ForegroundColor Red
    }

    Write-Host ""

    # Check git status
    Write-Host "Git Status:" -ForegroundColor Yellow
    Push-Location $ProjectRoot
    $gitStatus = git status --porcelain
    if ($gitStatus) {
        Write-Host "  Uncommitted changes detected:" -ForegroundColor Yellow
        $gitStatus | ForEach-Object { Write-Host "    $_" -ForegroundColor Gray }
    } else {
        Write-Host "  Working tree clean" -ForegroundColor Green
    }
    Pop-Location
}

function Initialize-Session {
    Write-Host "Initializing new validation session..." -ForegroundColor Yellow
    Write-Host ""

    # Ensure prompts exist
    if (-not (Test-Path (Join-Path $PromptsDir "initializer_prompt.md"))) {
        Write-Host "ERROR: Initializer prompt not found!" -ForegroundColor Red
        exit 1
    }
    if (-not (Test-Path (Join-Path $PromptsDir "coding_prompt.md"))) {
        Write-Host "ERROR: Coding prompt not found!" -ForegroundColor Red
        exit 1
    }

    # Add session entry to progress file
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $sessionEntry = @"

================================================================================
## Session: $(Get-Date -Format "yyyy-MM-dd") (Autonomous Validation)
================================================================================

### Start Time: $timestamp
### Archon Project: $ArchonProjectId
### Status: STARTING

### Instructions:
1. Open Claude Code in this repository
2. Run: find_projects(project_id="$ArchonProjectId")
3. Run: find_tasks(filter_by="project", filter_value="$ArchonProjectId")
4. Start with highest priority todo task (lowest task_order)
5. Follow coding_prompt.md for validation workflow

"@

    Add-Content -Path $ProgressFile -Value $sessionEntry

    Write-Host "Session initialized!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next Steps:" -ForegroundColor Cyan
    Write-Host "  1. Open Claude Code in this repository"
    Write-Host "  2. Load the initializer prompt:"
    Write-Host "     Read: .claude/harness/prompts/initializer_prompt.md"
    Write-Host "  3. Start validation with:"
    Write-Host "     find_tasks(filter_by='project', filter_value='$ArchonProjectId')"
    Write-Host ""
}

function Reset-Harness {
    Write-Host "Resetting harness to initial state..." -ForegroundColor Yellow

    # Reset features.json
    $features = @{
        project_id = $ArchonProjectId
        total_features = 56
        completed = 0
        passing = 0
        failing = 0
        pending = 56
        categories = @{
            data_generators = @{ total = 8; completed = 0 }
            notebooks_bronze = @{ total = 6; completed = 0 }
            notebooks_silver = @{ total = 6; completed = 0 }
            notebooks_gold = @{ total = 6; completed = 0 }
            notebooks_realtime = @{ total = 2; completed = 0 }
            notebooks_ml = @{ total = 2; completed = 0 }
            infrastructure = @{ total = 7; completed = 0 }
            tutorials = @{ total = 10; completed = 0 }
            validation = @{ total = 4; completed = 0 }
            schemas = @{ total = 6; completed = 0 }
        }
        features = @()
    }

    $features | ConvertTo-Json -Depth 10 | Set-Content $FeaturesFile

    Write-Host "Harness reset complete." -ForegroundColor Green
}

# Main execution
if ($Status) {
    Get-CurrentStatus
} elseif ($Reset) {
    Reset-Harness
} elseif ($Resume) {
    Write-Host "Resuming previous session..." -ForegroundColor Yellow
    Get-CurrentStatus
    Write-Host ""
    Write-Host "To continue, open Claude Code and run:" -ForegroundColor Cyan
    Write-Host "  find_tasks(filter_by='status', filter_value='doing')"
} else {
    Get-CurrentStatus
    Write-Host ""
    Initialize-Session
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
