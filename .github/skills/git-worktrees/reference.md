# Git Worktrees Reference

> Complete command reference and advanced patterns for Git worktrees

---

## Table of Contents

- [Command Reference](#command-reference)
- [Advanced Patterns](#advanced-patterns)
- [Integration Scripts](#integration-scripts)
- [IDE Configuration](#ide-configuration)
- [Troubleshooting Guide](#troubleshooting-guide)

---

## Command Reference

### git worktree add

Create a new worktree from an existing branch:

```bash
# Basic: Add worktree for existing branch
git worktree add <path> <branch>
git worktree add ../project-feature feature/login

# Create new branch and worktree
git worktree add -b <new-branch> <path> [start-point]
git worktree add -b feature/new ../project-new main

# Add with detached HEAD
git worktree add --detach <path> <commit>
git worktree add --detach ../project-v1.0.0 v1.0.0

# Force add (use carefully)
git worktree add -f <path> <branch>

# Add with checkout options
git worktree add --checkout <path> <branch>
git worktree add --no-checkout <path> <branch>  # Skip checkout

# Track remote branch
git worktree add <path> <remote>/<branch>
git worktree add ../project-upstream origin/develop

# Add with specific reflog expire time
git worktree add --expire <time> <path> <branch>
```

**Options:**

| Option | Description |
|--------|-------------|
| `-b <branch>` | Create new branch |
| `-B <branch>` | Create or reset branch |
| `-d, --detach` | Detached HEAD mode |
| `-f, --force` | Override safeguards |
| `--checkout` | Checkout after adding (default) |
| `--no-checkout` | Don't checkout |
| `--guess-remote` | Guess remote tracking branch |
| `--track` | Set up tracking |
| `--lock` | Lock worktree immediately |

### git worktree list

Show all worktrees:

```bash
# Basic list
git worktree list

# Porcelain format (for scripts)
git worktree list --porcelain

# Example output:
# /home/user/repos/project       abc1234 [main]
# /home/user/repos/project-feat  def5678 [feature/x]
# /home/user/repos/project-pr    ghi9012 [pr-123]
```

### git worktree remove

Remove a worktree:

```bash
# Basic removal
git worktree remove <path>
git worktree remove ../project-feature

# Force removal (with uncommitted changes)
git worktree remove --force <path>

# Remove current worktree (must cd out first)
cd /other/location
git worktree remove /path/to/worktree
```

### git worktree lock/unlock

Prevent accidental removal:

```bash
# Lock worktree
git worktree lock <path>
git worktree lock ../project-experiment

# Lock with reason
git worktree lock --reason "Long-running experiment" <path>

# Unlock worktree
git worktree unlock <path>
```

### git worktree move

Relocate a worktree:

```bash
# Move worktree to new location
git worktree move <worktree> <new-path>
git worktree move ../old-location ../new-location

# Force move
git worktree move --force <worktree> <new-path>
```

### git worktree prune

Clean up stale worktree data:

```bash
# Prune stale worktrees
git worktree prune

# Dry run - show what would be pruned
git worktree prune --dry-run

# Verbose output
git worktree prune --verbose

# Expire old worktrees
git worktree prune --expire <time>
git worktree prune --expire 3.months.ago
```

### git worktree repair

Fix worktree administrative files:

```bash
# Repair all worktrees
git worktree repair

# Repair specific worktree
git worktree repair <path>
```

---

## Advanced Patterns

### Pattern 1: PR Review Workflow

```bash
#!/bin/bash
# review-pr.sh - Create isolated PR review worktree

PR_NUMBER=$1
REPO_NAME=$(basename $(git rev-parse --show-toplevel))

# Fetch PR
git fetch origin pull/$PR_NUMBER/head:pr-$PR_NUMBER

# Create worktree
git worktree add ../${REPO_NAME}-pr-$PR_NUMBER pr-$PR_NUMBER

echo "Review worktree created at ../${REPO_NAME}-pr-$PR_NUMBER"
echo "Run: cd ../${REPO_NAME}-pr-$PR_NUMBER"
```

### Pattern 2: Feature Development Workflow

```bash
#!/bin/bash
# start-feature.sh - Start new feature in worktree

FEATURE_NAME=$1
BASE_BRANCH=${2:-main}
REPO_NAME=$(basename $(git rev-parse --show-toplevel))

# Ensure base is up to date
git fetch origin $BASE_BRANCH

# Create worktree with new branch
git worktree add -b feature/$FEATURE_NAME \
  ../${REPO_NAME}-$FEATURE_NAME origin/$BASE_BRANCH

cd ../${REPO_NAME}-$FEATURE_NAME

# Install dependencies if needed
if [ -f package.json ]; then
  npm install
fi

echo "Feature worktree ready at $(pwd)"
```

### Pattern 3: Compare Two Versions

```bash
#!/bin/bash
# compare-versions.sh - Check out two versions side by side

VERSION_A=$1
VERSION_B=$2
REPO_NAME=$(basename $(git rev-parse --show-toplevel))

git worktree add --detach ../${REPO_NAME}-$VERSION_A $VERSION_A
git worktree add --detach ../${REPO_NAME}-$VERSION_B $VERSION_B

echo "Compare:"
echo "  Version A: ../${REPO_NAME}-$VERSION_A"
echo "  Version B: ../${REPO_NAME}-$VERSION_B"
```

### Pattern 4: Experiment Sandbox

```bash
#!/bin/bash
# experiment.sh - Create experimental worktree

EXPERIMENT_NAME=$1
REPO_NAME=$(basename $(git rev-parse --show-toplevel))

# Create locked experimental worktree
git worktree add -b experiment/$EXPERIMENT_NAME \
  ../${REPO_NAME}-experiment-$EXPERIMENT_NAME

git worktree lock --reason "Experimental work" \
  ../${REPO_NAME}-experiment-$EXPERIMENT_NAME

echo "Locked experiment worktree created"
```

### Pattern 5: Cleanup Script

```bash
#!/bin/bash
# cleanup-worktrees.sh - Remove completed worktrees

REPO_NAME=$(basename $(git rev-parse --show-toplevel))

echo "Current worktrees:"
git worktree list

read -p "Enter worktree suffix to remove (e.g., 'pr-123'): " SUFFIX

WORKTREE_PATH="../${REPO_NAME}-${SUFFIX}"

if [ -d "$WORKTREE_PATH" ]; then
  git worktree remove "$WORKTREE_PATH"
  echo "Removed: $WORKTREE_PATH"
else
  echo "Not found: $WORKTREE_PATH"
fi
```

---

## Integration Scripts

### PowerShell Helper Functions

```powershell
# Add to your PowerShell profile

function New-Worktree {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Branch,
        [string]$BaseBranch = "main"
    )
    
    $RepoName = Split-Path -Leaf (git rev-parse --show-toplevel)
    $WorktreePath = Join-Path ".." "$RepoName-$Branch"
    
    git fetch origin $BaseBranch
    git worktree add -b $Branch $WorktreePath "origin/$BaseBranch"
    
    Set-Location $WorktreePath
    Write-Host "Worktree created at $WorktreePath" -ForegroundColor Green
}

function Remove-Worktree {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Branch
    )
    
    $RepoName = Split-Path -Leaf (git rev-parse --show-toplevel)
    $WorktreePath = Join-Path ".." "$RepoName-$Branch"
    
    git worktree remove $WorktreePath
    Write-Host "Worktree removed: $WorktreePath" -ForegroundColor Yellow
}

function Get-Worktrees {
    git worktree list
}

# Aliases
Set-Alias wtadd New-Worktree
Set-Alias wtrm Remove-Worktree
Set-Alias wtls Get-Worktrees
```

### Bash Helper Functions

```bash
# Add to .bashrc or .zshrc

wt-add() {
    local branch=$1
    local base=${2:-main}
    local repo=$(basename $(git rev-parse --show-toplevel))
    local path="../${repo}-${branch}"
    
    git fetch origin $base
    git worktree add -b $branch $path origin/$base
    cd $path
    echo "Worktree created at $path"
}

wt-rm() {
    local branch=$1
    local repo=$(basename $(git rev-parse --show-toplevel))
    local path="../${repo}-${branch}"
    
    git worktree remove $path
    echo "Worktree removed: $path"
}

wt-ls() {
    git worktree list
}

wt-pr() {
    local pr=$1
    local repo=$(basename $(git rev-parse --show-toplevel))
    
    git fetch origin pull/$pr/head:pr-$pr
    git worktree add ../${repo}-pr-$pr pr-$pr
    cd ../${repo}-pr-$pr
    echo "PR $pr checked out at $(pwd)"
}
```

---

## IDE Configuration

### VS Code Settings

```json
// .vscode/settings.json
{
  // Exclude worktree siblings from search
  "search.exclude": {
    "../*-pr-*": true,
    "../*-feature-*": true,
    "../*-experiment-*": true
  },
  
  // File watcher exclusions
  "files.watcherExclude": {
    "../**/node_modules/**": true
  }
}
```

### VS Code Multi-root Workspace

```json
// my-project.code-workspace
{
  "folders": [
    {
      "path": ".",
      "name": "main"
    },
    {
      "path": "../my-project-feature-a",
      "name": "feature-a"
    },
    {
      "path": "../my-project-pr-123",
      "name": "pr-123"
    }
  ],
  "settings": {
    "git.repositoryScanMaxDepth": 1
  }
}
```

### JetBrains IDEs

1. Open each worktree as a separate project
2. Or use "Attach" to add to current window
3. Configure: Settings → Version Control → Directory Mappings

---

## Troubleshooting Guide

### Common Errors

#### "fatal: 'branch' is already checked out"

```bash
# A branch can only be in one worktree at a time
# Solution: Use a different branch or remove the existing worktree

# Find where it's checked out
git worktree list | grep <branch>

# Remove that worktree or use a different branch
git worktree remove <path>
```

#### "fatal: not a git repository"

```bash
# The worktree link is broken
# Solution: Prune and re-add

git worktree prune
git worktree add <path> <branch>
```

#### "error: unable to remove worktree"

```bash
# Worktree may be locked or have changes
# Check lock status
git worktree list --porcelain | grep -A1 locked

# Unlock if needed
git worktree unlock <path>

# Force remove if necessary
git worktree remove --force <path>
```

#### "error: failed to delete worktree at"

```bash
# Permission issues or file locks
# On Windows, close any programs using files in the worktree
# Then try again

# Or repair first
git worktree repair <path>
git worktree remove <path>
```

### Diagnostic Commands

```bash
# Full worktree status
git worktree list --porcelain

# Check for issues
git fsck

# Verify worktree integrity
git worktree repair

# Clean up stale entries
git worktree prune --verbose --dry-run
git worktree prune --verbose
```

---

## Related Resources

- [SKILL.md](./SKILL.md) - Main skill documentation
- [Worktrees Workflow Guide](../../../docs/guides/worktrees-workflow.md)
- [Worktree Manager Agent](../../agents/worktree-manager.md)
- [Helper Script](../../../scripts/worktree-helper.ps1)
