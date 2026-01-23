---
description: Review a GitHub Pull Request - analyze changes, provide feedback
---

# Review Pull Request

Review a GitHub Pull Request using the gh CLI.

## Find PR to Review

```bash
# List PRs requesting your review
gh pr list --search "review-requested:@me"

# List all open PRs
gh pr list

# View specific PR
gh pr view {input}
```

## View PR Details

```bash
# View PR summary
gh pr view <number>

# View diff
gh pr diff <number>

# View in browser
gh pr view <number> --web
```

## Checkout Locally (Optional)

```bash
gh pr checkout <number>
```

## Review Checklist

Analyze the PR for:

| Area              | Check                           |
| ----------------- | ------------------------------- |
| **Code Quality**  | Style, patterns, best practices |
| **Functionality** | Does it work as intended?       |
| **Tests**         | Adequate test coverage?         |
| **Security**      | Any vulnerabilities?            |
| **Performance**   | Any concerns?                   |
| **Documentation** | Updated if needed?              |

## Submit Review

```bash
# Approve
gh pr review <number> --approve --body "LGTM! Nice work."

# Request changes
gh pr review <number> --request-changes --body "Please address:
- Issue 1
- Issue 2"

# Comment only
gh pr review <number> --comment --body "Some thoughts..."
```

## Review Templates

**Approval:**

```markdown
Looks good! ✅

## Summary

- Code follows conventions
- Tests pass and cover changes
- No security concerns
```

**Request Changes:**

```markdown
Thanks for the PR! A few things to address:

## Required Changes

- [ ] [Issue and suggestion]
- [ ] [Issue and suggestion]

## Suggestions (Optional)

- [Nice to have]
```

## Check CI Status

```bash
gh pr checks <number>
gh pr checks <number> --watch
```

## Merge After Approval

```bash
# Standard merge
gh pr merge <number>

# Squash merge
gh pr merge <number> --squash

# Rebase merge
gh pr merge <number> --rebase

# Delete branch after
gh pr merge <number> --delete-branch
```

## Arguments

{input}

- No args: Review PR for current branch
- `<number>`: Review specific PR
- `list`: List PRs needing review
- `approve <number>`: Quick approve
- `request-changes <number>`: Request changes
