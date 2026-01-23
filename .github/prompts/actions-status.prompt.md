---
description: Check GitHub Actions status for the current repository
---

# GitHub Actions Status

Check CI/CD workflow status for the current repository.

## Workflow Status

```bash
# List recent workflow runs
gh run list --limit 10

# View specific run
gh run view <run-id>

# View run logs
gh run view <run-id> --log

# Watch a running workflow
gh run watch <run-id>
```

## PR Checks

```bash
# Check PR status
gh pr checks

# Wait for checks to complete
gh pr checks --watch

# View failing checks
gh pr checks --fail
```

## Workflow Management

```bash
# List workflows
gh workflow list

# View workflow details
gh workflow view <workflow-name>

# Run workflow manually
gh workflow run <workflow-name>

# Disable/enable workflow
gh workflow disable <workflow-name>
gh workflow enable <workflow-name>
```

## Status Report

```markdown
## 🔄 CI/CD Status

### Recent Runs

| Workflow | Branch   | Status   | Duration | Link  |
| -------- | -------- | -------- | -------- | ----- |
| [name]   | [branch] | ✅/❌/🔄 | [time]   | [url] |

### Current PR Checks

| Check   | Status   | Details   |
| ------- | -------- | --------- |
| [check] | ✅/❌/🔄 | [message] |

### Issues

- [Any failing workflows with error summary]

### Actions Needed

- [Required actions if failures]
```

## Common Issues

| Issue          | Solution                            |
| -------------- | ----------------------------------- |
| Test failures  | Review test output, fix tests       |
| Lint errors    | Run linter locally, fix issues      |
| Build failures | Check dependencies, build config    |
| Timeout        | Optimize workflow or increase limit |

## Arguments

{input}

- No args: Show recent runs and current PR status
- `<run-id>`: View specific run details
- `watch`: Watch current running workflows
- `logs <run-id>`: View run logs
