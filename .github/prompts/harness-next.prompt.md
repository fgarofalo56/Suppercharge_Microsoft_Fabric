---
name: harness-next
description: Start the next coding session in an autonomous agent harness. Picks up where previous session left off, implements one feature, maintains clean handoff.
mode: agent
agent: harness-coder
---

# ▶️ Next Coding Session

Start a new coding session in your autonomous agent harness project.

## Session Protocol

This prompt invokes the **harness-coder** agent which will:

1. **Orient** - Read Archon session notes and git history
2. **Verify** - Run health checks on completed features
3. **Select** - Choose highest priority TODO task
4. **Implement** - Write code for one feature
5. **Test** - Coordinate with testing agent
6. **Review** - Optional code review
7. **Handoff** - Update Archon and commit cleanly

---

## Before Starting

Ensure:
- [ ] Harness is initialized (ran `/harness-init` at least once)
- [ ] Archon MCP is accessible
- [ ] Development environment is ready

---

## Session Execution

The coding agent will:

### 1. Get Bearings
```bash
pwd
cat .harness/config.json
```

### 2. Query Archon
```python
find_tasks(filter_by="project", filter_value=PROJECT_ID)
find_documents(project_id=PROJECT_ID, query="Session Notes")
```

### 3. Check for In-Progress Work
If a task is in "doing" status, continue it rather than starting new.

### 4. Select Next Task
Highest `task_order` value among TODO tasks.

### 5. Implement & Test
Write code, run tests, fix issues.

### 6. Update & Handoff
Update Archon tasks and session notes, commit to git.

---

## Parallel Execution

For background execution:
```bash
& /harness-next
```

This runs the coding session in the background while you do other work.

---

## Expected Output

At session end, you'll see:
- Task completed summary
- Test results
- Progress update (X/Y tasks)
- Next task preview

---

## Starting Session

Beginning coding session...
