---
name: ralph-cancel
description: Cancel an active Ralph Wiggum loop.
mode: agent
tools:
  - filesystem
  - terminal
  - archon-find_tasks
  - archon-find_documents
  - archon-manage_task
  - archon-manage_document
---

## User Input

```text
$ARGUMENTS
```

## Purpose

Cancel an active Ralph Wiggum loop gracefully.

## Execution Flow

### 1. Find Active Loop

```python
# Check local state
config = read_file(".ralph/config.json")

# Verify loop is running
state = find_documents(
    project_id=config["archon_project_id"],
    query=f"Ralph Loop State: {config['loop_id']}"
)

if state["content"]["status"] != "running":
    print("No active loop to cancel")
    exit()
```

### 2. Update Archon State

```python
manage_document("update",
    project_id=PROJECT_ID,
    document_id=STATE_DOC_ID,
    content={
        **state["content"],
        "status": "cancelled",
        "cancelled_at": NOW,
        "cancelled_by": "user",
        "final_iteration": state["content"]["current_iteration"]
    }
)
```

### 3. Update Task

```python
manage_task("update",
    task_id=TASK_ID,
    status="todo",  # Reset to todo
    description=f"""[ORIGINAL_DESCRIPTION]

---
## Ralph Loop Cancelled

### Progress at Cancellation
- Iterations: {CURRENT}/{MAX}
- Tests: {PASSING}/{TOTAL}

### Work Completed
{SUMMARY}

### Resume Options
- Restart: `/ralph-start --resume`
- Continue manually
- Reassign to different approach

---
Cancelled: {NOW}
"""
)
```

### 4. Cleanup (Optional)

```bash
# With --cleanup flag: revert changes
git checkout .
git clean -fd

# With --keep flag (default): preserve changes
# Just update state, keep files
```

### 5. Commit State

```bash
git add .ralph/
git commit -m "Ralph loop cancelled

Loop: [LOOP_ID]
Iteration: [N]/[MAX]
Reason: User cancelled
"
```

## Options

```bash
/ralph-cancel              # Cancel and preserve changes
/ralph-cancel --force      # Cancel without state updates
/ralph-cancel --cleanup    # Cancel and revert all changes
/ralph-cancel --loop <id>  # Cancel specific loop
```

## Output

```markdown
## 🛑 Ralph Loop Cancelled

### Loop: ralph-20260122-150000
- Final Iteration: 12/50
- Duration: 25m
- Changes Preserved: Yes

### Task Status
- Task: Build REST API
- Status: Reset to "todo"
- Assignee: Unassigned

### Files Changed (Preserved)
- src/api.ts
- tests/api.test.ts
- package.json

### Next Steps
- Review changes: `git status`
- Resume later: `/ralph-start --resume`
- Start fresh: `/ralph-start`
```
