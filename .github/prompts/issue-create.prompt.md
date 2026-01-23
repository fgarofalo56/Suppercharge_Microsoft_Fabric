---
description: Create a GitHub issue with proper formatting and labels
---

# Create GitHub Issue

Create a GitHub issue using the gh CLI.

## Issue Types

### Bug Report

```bash
gh issue create \
  --title "Bug: [Brief description]" \
  --label "bug" \
  --body "## Description
[What's happening]

## Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Environment
- OS: [e.g., Windows 11]
- Version: [e.g., 1.2.3]
- Node: [e.g., 20.x]

## Additional Context
[Screenshots, logs, etc.]"
```

### Feature Request

```bash
gh issue create \
  --title "Feature: [Brief description]" \
  --label "enhancement" \
  --body "## Problem Statement
[What problem does this solve?]

## Proposed Solution
[How should it work?]

## Alternatives Considered
[Other approaches]

## Additional Context
[Mockups, examples, etc.]"
```

### Task/Chore

```bash
gh issue create \
  --title "Chore: [Brief description]" \
  --label "chore" \
  --body "## Description
[What needs to be done]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Notes
[Additional context]"
```

## Common Options

| Flag          | Purpose           |
| ------------- | ----------------- |
| `--title`     | Issue title       |
| `--body`      | Issue description |
| `--label`     | Add labels        |
| `--assignee`  | Assign to user    |
| `--milestone` | Add to milestone  |
| `--project`   | Add to project    |

## Managing Issues

```bash
# List issues
gh issue list

# View issue
gh issue view <number>

# Close issue
gh issue close <number>

# Reopen issue
gh issue reopen <number>

# Edit issue
gh issue edit <number> --add-label "priority"
```

## Link to Archon

After creating issue, optionally create matching Archon task:

```
manage_task("create",
  project_id="[PROJECT_ID]",
  title="[Same as issue title]",
  description="GitHub Issue: #[number]\n[description]",
  task_order=80
)
```

## Arguments

{input}

- No args: Interactive issue creation
- `bug <title>`: Create bug report
- `feature <title>`: Create feature request
- `list`: List open issues
