<#
.SYNOPSIS
    Git Worktree Helper - PowerShell functions for managing Git worktrees

.DESCRIPTION
    This script provides convenient PowerShell functions for common Git worktree operations:
    - Creating worktrees for features, PRs, experiments
    - Listing and managing worktrees
    - Proper cleanup of worktrees

.NOTES
    Add this to your PowerShell profile or dot-source it:
    . .\scripts\worktree-helper.ps1

.EXAMPLE
    New-FeatureWorktree -Name "user-auth"
    New-PRReviewWorktree -PRNumber 123
    Get-Worktrees
    Remove-Worktree -Name "user-auth"
#>

# Configuration
$script:WorktreeBaseDir = ".."

function Get-RepoName {
    <#
    .SYNOPSIS
        Get the current repository name
    #>
    $repoRoot = git rev-parse --show-toplevel 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Not in a Git repository"
        return $null
    }
    return Split-Path -Leaf $repoRoot
}

function Get-Worktrees {
    <#
    .SYNOPSIS
        List all Git worktrees
    
    .EXAMPLE
        Get-Worktrees
    #>
    [CmdletBinding()]
    param()
    
    git worktree list
}

function New-FeatureWorktree {
    <#
    .SYNOPSIS
        Create a new feature worktree
    
    .PARAMETER Name
        Feature name (will be prefixed with 'feature/')
    
    .PARAMETER BaseBranch
        Base branch to branch from (default: main)
    
    .PARAMETER NoInstall
        Skip running npm install
    
    .EXAMPLE
        New-FeatureWorktree -Name "user-auth"
        New-FeatureWorktree -Name "api-v2" -BaseBranch "develop"
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$Name,
        
        [string]$BaseBranch = "main",
        
        [switch]$NoInstall
    )
    
    $repoName = Get-RepoName
    if (-not $repoName) { return }
    
    $branchName = "feature/$Name"
    $worktreePath = Join-Path $script:WorktreeBaseDir "$repoName-feature-$Name"
    
    Write-Host "Creating feature worktree: $branchName" -ForegroundColor Cyan
    
    # Fetch latest
    git fetch origin $BaseBranch
    
    # Create worktree
    git worktree add -b $branchName $worktreePath "origin/$BaseBranch"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Worktree created at: $worktreePath" -ForegroundColor Green
        
        # Install dependencies if package.json exists
        if (-not $NoInstall -and (Test-Path (Join-Path $worktreePath "package.json"))) {
            Write-Host "Installing dependencies..." -ForegroundColor Yellow
            Push-Location $worktreePath
            npm install
            Pop-Location
        }
        
        Write-Host "`nNext steps:" -ForegroundColor Cyan
        Write-Host "  cd $worktreePath"
        Write-Host "  code ."
    }
}

function New-PRReviewWorktree {
    <#
    .SYNOPSIS
        Create a worktree for reviewing a pull request
    
    .PARAMETER PRNumber
        The pull request number to review
    
    .PARAMETER NoInstall
        Skip running npm install
    
    .EXAMPLE
        New-PRReviewWorktree -PRNumber 123
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [int]$PRNumber,
        
        [switch]$NoInstall
    )
    
    $repoName = Get-RepoName
    if (-not $repoName) { return }
    
    $branchName = "pr-$PRNumber"
    $worktreePath = Join-Path $script:WorktreeBaseDir "$repoName-pr-$PRNumber"
    
    Write-Host "Setting up PR #$PRNumber for review..." -ForegroundColor Cyan
    
    # Fetch PR
    git fetch origin "pull/$PRNumber/head:$branchName"
    
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to fetch PR #$PRNumber"
        return
    }
    
    # Create worktree
    git worktree add $worktreePath $branchName
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ PR review worktree created at: $worktreePath" -ForegroundColor Green
        
        # Install dependencies if package.json exists
        if (-not $NoInstall -and (Test-Path (Join-Path $worktreePath "package.json"))) {
            Write-Host "Installing dependencies..." -ForegroundColor Yellow
            Push-Location $worktreePath
            npm install
            Pop-Location
        }
        
        Write-Host "`nReview checklist:" -ForegroundColor Cyan
        Write-Host "  [ ] Code quality"
        Write-Host "  [ ] Tests pass"
        Write-Host "  [ ] Functionality works"
        Write-Host "  [ ] Documentation updated"
        Write-Host "`nCommands:"
        Write-Host "  cd $worktreePath"
        Write-Host "  npm test"
        Write-Host "  npm start"
    }
}

function New-ExperimentWorktree {
    <#
    .SYNOPSIS
        Create a locked worktree for experiments
    
    .PARAMETER Name
        Experiment name
    
    .PARAMETER Reason
        Reason for the experiment (stored with the lock)
    
    .PARAMETER BaseBranch
        Base branch (default: main)
    
    .EXAMPLE
        New-ExperimentWorktree -Name "graphql-migration" -Reason "Testing GraphQL migration"
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$Name,
        
        [string]$Reason = "Experimental work in progress",
        
        [string]$BaseBranch = "main"
    )
    
    $repoName = Get-RepoName
    if (-not $repoName) { return }
    
    $branchName = "experiment/$Name"
    $worktreePath = Join-Path $script:WorktreeBaseDir "$repoName-experiment-$Name"
    
    Write-Host "Creating experiment worktree: $branchName" -ForegroundColor Cyan
    
    # Fetch latest
    git fetch origin $BaseBranch
    
    # Create worktree
    git worktree add -b $branchName $worktreePath "origin/$BaseBranch"
    
    if ($LASTEXITCODE -eq 0) {
        # Lock the worktree
        git worktree lock --reason $Reason $worktreePath
        
        Write-Host "✅ Locked experiment worktree created at: $worktreePath" -ForegroundColor Green
        Write-Host "🔒 Locked with reason: $Reason" -ForegroundColor Yellow
        
        Write-Host "`nNext steps:" -ForegroundColor Cyan
        Write-Host "  cd $worktreePath"
        Write-Host "  code ."
        Write-Host "`nTo unlock later:"
        Write-Host "  git worktree unlock $worktreePath"
    }
}

function Remove-Worktree {
    <#
    .SYNOPSIS
        Remove a worktree and optionally its branch
    
    .PARAMETER Name
        Worktree suffix (e.g., "feature-auth" or "pr-123")
    
    .PARAMETER DeleteBranch
        Also delete the associated branch
    
    .PARAMETER Force
        Force removal even with uncommitted changes
    
    .EXAMPLE
        Remove-Worktree -Name "feature-auth" -DeleteBranch
        Remove-Worktree -Name "pr-123" -DeleteBranch
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$Name,
        
        [switch]$DeleteBranch,
        
        [switch]$Force
    )
    
    $repoName = Get-RepoName
    if (-not $repoName) { return }
    
    $worktreePath = Join-Path $script:WorktreeBaseDir "$repoName-$Name"
    
    if (-not (Test-Path $worktreePath)) {
        Write-Error "Worktree not found: $worktreePath"
        return
    }
    
    Write-Host "Removing worktree: $worktreePath" -ForegroundColor Yellow
    
    # Check if locked
    $lockStatus = git worktree list --porcelain | Select-String -Pattern "locked" -Context 0,1
    if ($lockStatus) {
        Write-Host "Unlocking worktree first..." -ForegroundColor Yellow
        git worktree unlock $worktreePath
    }
    
    # Remove worktree
    if ($Force) {
        git worktree remove --force $worktreePath
    } else {
        git worktree remove $worktreePath
    }
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Worktree removed" -ForegroundColor Green
        
        # Delete branch if requested
        if ($DeleteBranch) {
            # Determine branch name from worktree name
            $branchName = $Name -replace "^feature-", "feature/" `
                               -replace "^experiment-", "experiment/" `
                               -replace "^pr-", "pr-"
            
            Write-Host "Deleting branch: $branchName" -ForegroundColor Yellow
            git branch -d $branchName 2>$null
            if ($LASTEXITCODE -ne 0) {
                git branch -D $branchName
            }
        }
    }
}

function Invoke-WorktreePrune {
    <#
    .SYNOPSIS
        Clean up stale worktree entries
    
    .PARAMETER DryRun
        Show what would be pruned without actually pruning
    
    .EXAMPLE
        Invoke-WorktreePrune -DryRun
        Invoke-WorktreePrune
    #>
    [CmdletBinding()]
    param(
        [switch]$DryRun
    )
    
    if ($DryRun) {
        Write-Host "Dry run - showing what would be pruned:" -ForegroundColor Yellow
        git worktree prune --dry-run --verbose
    } else {
        Write-Host "Pruning stale worktree entries..." -ForegroundColor Yellow
        git worktree prune --verbose
        Write-Host "✅ Prune complete" -ForegroundColor Green
    }
}

# Aliases
Set-Alias -Name wtls -Value Get-Worktrees
Set-Alias -Name wtadd -Value New-FeatureWorktree
Set-Alias -Name wtpr -Value New-PRReviewWorktree
Set-Alias -Name wtexp -Value New-ExperimentWorktree
Set-Alias -Name wtrm -Value Remove-Worktree
Set-Alias -Name wtprune -Value Invoke-WorktreePrune

# Export functions
Export-ModuleMember -Function @(
    'Get-Worktrees',
    'New-FeatureWorktree',
    'New-PRReviewWorktree',
    'New-ExperimentWorktree',
    'Remove-Worktree',
    'Invoke-WorktreePrune'
) -Alias @(
    'wtls',
    'wtadd',
    'wtpr',
    'wtexp',
    'wtrm',
    'wtprune'
)

Write-Host @"
Git Worktree Helper loaded!

Commands:
  Get-Worktrees (wtls)              - List all worktrees
  New-FeatureWorktree (wtadd)       - Create feature worktree
  New-PRReviewWorktree (wtpr)       - Create PR review worktree  
  New-ExperimentWorktree (wtexp)    - Create locked experiment worktree
  Remove-Worktree (wtrm)            - Remove a worktree
  Invoke-WorktreePrune (wtprune)    - Clean up stale entries

Examples:
  New-FeatureWorktree -Name "user-auth"
  New-PRReviewWorktree -PRNumber 123
  Remove-Worktree -Name "pr-123" -DeleteBranch
"@ -ForegroundColor DarkGray
