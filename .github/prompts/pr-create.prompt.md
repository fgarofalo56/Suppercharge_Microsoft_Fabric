---
description: Create a GitHub Pull Request with proper description and metadata
---

# Create Pull Request

Create a GitHub Pull Request using the gh CLI.

## Pre-flight Checks

```bash
# Ensure we're not on main/master
git branch --show-current

# Check for uncommitted changes
git status

# Ensure branch is pushed
git push -u origin HEAD
```

## Gather Information

```bash
# Get commits since branching from main
git log --oneline main..HEAD

# Get changed files
git diff --stat main..HEAD
```

## Generate PR Content

**Title Format** (Conventional Commits style):

- `feat: Add user authentication`
- `fix: Resolve login timeout issue`
- `docs: Update API documentation`

**Body Template:**

```markdown
## Summary

[Brief description - 2-3 sentences]

## Changes

- [Key change 1]
- [Key change 2]
- [Key change 3]

## Test Plan

- [ ] [How to test]
- [ ] [Verification step]

## Related Issues

Closes #[issue-number]
```

## Create the PR

```bash
# Standard PR
gh pr create --title "<title>" --body "<body>"

# Draft PR
gh pr create --title "<title>" --body "<body>" --draft

# With reviewers
gh pr create --title "<title>" --body "<body>" --reviewer @user1,@user2

# With labels
gh pr create --title "<title>" --body "<body>" --label "enhancement"
```

## Common Options

| Flag                 | Purpose                       |
| -------------------- | ----------------------------- |
| `--draft`            | Create as draft               |
| `--base <branch>`    | Target branch (default: main) |
| `--reviewer <users>` | Request reviewers             |
| `--assignee <users>` | Assign users                  |
| `--label <labels>`   | Add labels                    |
| `--milestone <name>` | Add to milestone              |

## Output

After creating PR, show:

1. PR URL
2. PR number
3. Reviewers requested
4. CI status check URL

## Arguments

{input}

- No args: Interactive PR creation
- `draft`: Create as draft PR
- `ready`: Create as ready for review
- `<title>`: Use as PR title
