---
description: Synchronize local repository with remote - push, pull, or fetch
---

# Git Sync

Synchronize local repository with remote.

## Smart Sync (Default)

When no arguments provided:

### 1. Fetch from all remotes

```bash
git fetch --all --prune
```

### 2. Check current status

```bash
git status -sb
git rev-list --left-right --count HEAD...@{upstream}
```

### 3. Recommend action based on status:

- **Behind only**: Suggest pull
- **Ahead only**: Suggest push
- **Diverged**: Suggest pull --rebase or merge strategy
- **Up to date**: Report clean state

## Push

```bash
# Normal push
git push origin $(git branch --show-current)

# Push and set upstream (for new branches)
git push -u origin $(git branch --show-current)
```

## Pull

```bash
# Standard pull
git pull origin $(git branch --show-current)

# Pull with rebase (cleaner history)
git pull --rebase origin $(git branch --show-current)
```

## Force Push (DANGEROUS)

Only use when:

- Rebased local commits
- Amending pushed commits
- Cleaning up PR branch

```bash
# Safer force push
git push --force-with-lease origin $(git branch --show-current)
```

**NEVER force push to main/master without explicit confirmation**

## Fetch Only

```bash
git fetch --all --prune
git log --oneline HEAD..@{upstream}
```

## Output

Show:

1. Current branch and tracking branch
2. Commits ahead/behind
3. Action taken and result
4. Warnings about conflicts if any

## Arguments

{input}

- No args: Smart sync (fetch, show status, suggest action)
- `push`: Push current branch
- `pull`: Pull current branch
- `fetch`: Fetch without merging
- `force`: Force push (with safety checks)
