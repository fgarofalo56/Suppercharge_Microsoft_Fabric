---
description: Get current project status briefing - tasks, git state, blockers
---

# Project Status Briefing

Provide a comprehensive status update on the current project.

## Check Current State

### 1. Archon Status

```
find_tasks(filter_by="status", filter_value="doing")
find_tasks(filter_by="status", filter_value="todo")
find_documents(project_id="[PROJECT_ID]", query="Session Memory")
```

### 2. Git Status

```bash
git status -sb
git log --oneline -5
git branch --show-current
git stash list
```

### 3. Check for Issues

- Any failing tests or builds
- Uncommitted changes
- Stashed work

## Status Report

```markdown
## 📊 Current Status

### 🌿 Git State

- **Branch**: [current branch]
- **Tracking**: [ahead/behind status]
- **Uncommitted Changes**: [list or "clean"]
- **Stashes**: [count]

### 📋 Archon Tasks

| Status        | Count | Top Items |
| ------------- | ----- | --------- |
| Doing         | X     | [list]    |
| Review        | X     | [list]    |
| Todo          | X     | [top 3]   |
| Done (recent) | X     | [last 3]  |

### ⚠️ Blockers

- [Any blocking issues]

### 💡 Recent Activity

- [What was done this session]

### 🎯 Recommended Next Steps

1. [Immediate priority]
2. [Secondary priority]
3. [If time permits]
```

Keep the report concise but complete.

{input}
