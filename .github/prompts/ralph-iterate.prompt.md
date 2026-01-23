---
name: ralph-iterate
description: Run a single iteration of the Ralph Wiggum loop manually.
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

Execute a single iteration of the Ralph loop manually. Useful for:
- Supervised iteration during early loop phases
- Debugging loop behavior
- Testing prompt effectiveness

## Execution Flow

### 1. Load State

```python
# Load config
config = read_file(".ralph/config.json")

# Load Archon state
state = find_documents(
    project_id=config["archon_project_id"],
    query=f"Ralph Loop State: {config['loop_id']}"
)
```

### 2. Read Previous Work

```bash
# Check what changed
git --no-pager log -1 --stat
git status
```

### 3. Execute Prompt

Read `.ralph/prompts/current.md` and execute the work.

### 4. Run Validation

```bash
# Build
[BUILD_CMD]

# Test
[TEST_CMD]
```

### 5. Update State

```python
# Increment iteration
state["current_iteration"] += 1

# Add iteration record
state["iterations"].append({
    "n": state["current_iteration"],
    "summary": "...",
    "files_changed": [...],
    "tests_passed": N,
    "tests_failed": N
})

# Save to Archon
manage_document("update", ...)
```

### 6. Commit

```bash
git add .
git commit -m "Ralph iteration [N]: [Summary]"
```

### 7. Check Completion

If completion criteria met:
- Update task to "done"
- Report completion

If not complete:
- Report progress
- Suggest next iteration

## Options

```bash
/ralph-iterate              # Run next iteration
/ralph-iterate --verbose    # Detailed output
/ralph-iterate --dry-run    # Show what would happen
/ralph-iterate --skip-commit # Don't commit after iteration
```

## Output

```markdown
## 🔄 Ralph Iteration [N]/[MAX] Complete

### Work Done
[Summary]

### Files Changed
- file1.ts
- file2.ts

### Tests
✅ 15/15 passing

### Progress
[==========----------] 50%

### Next
Run `/ralph-iterate` for next iteration
or `/ralph-status` to check progress
```
