---
name: harness-resume
description: Resume an existing autonomous agent harness project. Queries Archon for current state and offers continuation options.
mode: agent
agent: harness-wizard
---

# 🔄 Resume Harness Project

Continue working on an existing autonomous agent harness project.

## What This Does

1. **Reads** local `.harness/config.json` for project ID
2. **Queries Archon** for current project state
3. **Displays** task progress and session notes
4. **Offers** options to continue

---

## Resume Protocol

I'll check:

```
📁 Local Config → .harness/config.json
📊 Archon Project → find_projects(project_id=...)
📋 Tasks → find_tasks(filter_by="project", ...)
📝 Session Notes → find_documents(query="Session Notes")
```

Then display:

- **Project Status**: Active, paused, or blocked
- **Progress**: X/Y tasks completed (Z%)
- **Current Task**: In-progress task if any
- **Last Session**: Summary of previous session
- **Blockers**: Any issues from previous sessions

---

## Continuation Options

After reviewing state, choose:

### 1. Continue with Next Task
```bash
/harness-next
```
Start a new coding session with the next priority task.

### 2. Continue Current Task
If there's a task in "doing" status from a previous session.

### 3. View All Tasks
```bash
# Shows task board grouped by status
```

### 4. Fix Blockers
If there are blockers from previous sessions, address them first.

### 5. Run Status Report
Get detailed health check of the project.

---

## Let's Check Your Project

I'll now look for a harness configuration and query Archon for the project state.
