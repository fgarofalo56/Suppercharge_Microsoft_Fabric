---
description: Create a well-structured git commit using Conventional Commits format
---

# Git Commit

Create a well-structured git commit using Conventional Commits format.

## Process

### 1. Review Changes

```bash
git status
git diff --staged
```

If nothing is staged, show unstaged changes:

```bash
git diff
```

### 2. Stage Changes (if needed)

If no changes are staged, suggest what to stage or offer:

```bash
git add -A
```

### 3. Analyze and Commit

Determine the appropriate commit type based on changes:

**Conventional Commits Format:**

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Types:**
| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Code style (formatting, semicolons) |
| `refactor` | Code change (no new feature or fix) |
| `perf` | Performance improvement |
| `test` | Adding or updating tests |
| `build` | Build system or dependencies |
| `ci` | CI configuration |
| `chore` | Maintenance tasks |
| `revert` | Reverts a previous commit |

**Scope** (optional): Module or component affected (e.g., `auth`, `api`, `ui`)

### 4. Execute Commit

```bash
git commit -m "<type>(<scope>): <description>"
```

**For breaking changes:**

```bash
git commit -m "feat(api)!: change authentication flow

BREAKING CHANGE: API now requires Bearer token instead of API key"
```

### 5. Show Result

After committing, display:

- Commit hash
- Files changed summary
- Full commit message used

## Arguments

{input}

If arguments provided, use them as context for the commit message.
If arguments say "amend", use `git commit --amend` instead.
