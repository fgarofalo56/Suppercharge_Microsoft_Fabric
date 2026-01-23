---
description: Manage git branches - create, switch, delete, list, or cleanup
---

# Git Branch

Manage git branches - create, switch, delete, or list.

## List Branches (Default)

```bash
git branch -a --sort=-committerdate
```

Show local and remote branches sorted by recent activity.

## Create Branch

```bash
git checkout -b <branch-name>
```

**Naming Convention:**
| Prefix | Purpose | Example |
|--------|---------|---------|
| `feat/` | New features | `feat/add-user-auth` |
| `fix/` | Bug fixes | `fix/login-timeout` |
| `docs/` | Documentation | `docs/api-guide` |
| `refactor/` | Refactoring | `refactor/db-layer` |
| `test/` | Test additions | `test/auth-coverage` |
| `chore/` | Maintenance | `chore/deps-update` |

## Switch Branch

```bash
git checkout <branch-name>
# or
git switch <branch-name>
```

If uncommitted changes exist, warn and suggest stashing.

## Delete Branch

```bash
# Local (safe - only if merged)
git branch -d <branch-name>

# Force delete
git branch -D <branch-name>

# Remote
git push origin --delete <branch-name>
```

## Cleanup Merged Branches

```bash
# List merged branches
git branch --merged | grep -v "main\|master\|develop"

# Delete merged branches
git branch --merged | grep -v "main\|master\|develop" | xargs git branch -d
```

## Output

After action, show:

1. Current branch
2. Recent branches (if listing)
3. Warnings about uncommitted changes

## Arguments

{input}

- No args or `list`: List all branches
- `create <name>`: Create and switch to new branch
- `switch <name>`: Switch to existing branch
- `delete <name>`: Delete a branch
- `rename <old> <new>`: Rename a branch
- `clean`: Delete merged branches
