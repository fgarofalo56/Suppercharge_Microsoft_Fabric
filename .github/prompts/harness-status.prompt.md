---
name: harness-status
description: Check the status of an autonomous agent harness project. Shows progress, current tasks, blockers, and health.
mode: agent
agent: harness-coder
---

# 📊 Harness Status Report

Get a comprehensive status report for your autonomous agent harness project.

## What This Shows

### Progress Overview
- Total tasks vs completed
- Progress percentage
- Estimated sessions remaining

### Task Board
```
TODO        DOING       REVIEW      DONE
────────    ────────    ────────    ────────
Task A      Task B                  Task C
Task D                              Task E
Task F                              Task G
```

### Session History
- Last 5 sessions with summaries
- Tasks completed per session
- Blockers encountered

### Health Checks
- [ ] Tests passing
- [ ] Environment working
- [ ] No stale "doing" tasks
- [ ] Git status clean

### Blockers
- Active blockers from session notes
- Failed tests
- Stale tasks

---

## Status Report Generation

I'll query Archon and local files:

```python
# Get project info
project = find_projects(project_id=PROJECT_ID)

# Get all tasks
tasks = find_tasks(filter_by="project", filter_value=PROJECT_ID)

# Get session notes
notes = find_documents(project_id=PROJECT_ID, query="Session Notes")

# Check test status
# npm test / pytest / etc.

# Check git status
# git status
```

---

## Quick Commands After Status

| Situation | Command |
|-----------|---------|
| Ready to continue | `/harness-next` |
| Has blockers | Fix blockers first |
| Tests failing | `/harness-tester health` |
| Need review | `& @harness-reviewer check` |

---

## Run Status Check

Let me check your harness project status...
