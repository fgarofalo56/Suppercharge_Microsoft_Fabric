---
name: harness-ralph
description: Integrate Ralph Wiggum iterative loops with The Long Run Harness for autonomous multi-session development.
mode: agent
tools:
  - filesystem
  - terminal
  - archon-find_projects
  - archon-find_tasks
  - archon-find_documents
  - archon-manage_task
  - archon-manage_document
handoffs:
  - label: Start Ralph Loop
    agent: ralph-loop
    prompt: Start the Ralph-powered harness session
  - label: Check Harness Status
    agent: harness-coder
    prompt: Check harness session status
---

## User Input

```text
$ARGUMENTS
```

## Purpose

Combine Ralph Wiggum's iterative persistence with The Long Run Harness's multi-session structure for enhanced autonomous development.

## Integration Modes

### Mode 1: Ralph Wraps Harness-Coder

Ralph provides the iteration loop, harness-coder does the actual work:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    RALPH + HARNESS                                  │
│                                                                     │
│    ┌──────────────────────────────────────────────────────────┐     │
│    │  RALPH LOOP                                               │     │
│    │                                                           │     │
│    │    ┌─────────────────────────────────────────────┐       │     │
│    │    │  HARNESS-CODER SESSION                      │       │     │
│    │    │                                              │       │     │
│    │    │  1. Orient & Get Bearings                    │       │     │
│    │    │  2. Verify Health                            │       │     │
│    │    │  3. Implement Feature                        │       │     │
│    │    │  4. Test & Review                            │       │     │
│    │    │  5. Update Archon                            │       │     │
│    │    │  6. Commit                                   │       │     │
│    │    └─────────────────────────────────────────────┘       │     │
│    │                                                           │     │
│    │    [Check Completion] ─► [Continue or Exit]              │     │
│    └──────────────────────────────────────────────────────────┘     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Mode 2: Enhanced Session Continuation

Ralph ensures harness sessions continue until project completion:

```python
# Ralph manages the outer loop
while not project_complete:
    # Each iteration runs a harness-coder session
    run_harness_coder_session()
    
    # Ralph checks overall project progress
    check_project_completion()
    
    # Continue until all features done
```

## Execution Flow

### 1. Check Harness Configuration

```bash
# Verify harness is set up
cat .harness/config.json
```

### 2. Load Harness Project from Archon

```python
# Get project from harness config
harness_config = read_file(".harness/config.json")
project_id = harness_config["project_id"]

# Get all tasks
tasks = find_tasks(
    filter_by="project",
    filter_value=project_id
)

# Find remaining TODO tasks
todo_tasks = [t for t in tasks if t["status"] == "todo"]
```

### 3. Create Ralph Loop for Harness

```python
# Create Ralph config that targets harness workflow
ralph_config = {
    "loop_id": f"ralph-harness-{timestamp}",
    "archon_project_id": project_id,
    "archon_task_id": None,  # Ralph works on project, not single task
    "mode": "harness_integration",
    "prompt_file": ".ralph/prompts/harness-loop.md",
    "max_iterations": len(todo_tasks) * 5,  # Allow 5 iterations per task
    "completion_promise": "PROJECT_COMPLETE",
    "integration": {
        "harness": True,
        "use_session_notes": True,
        "sync_with_meta_task": True
    }
}
```

### 4. Generate Harness-Aware Prompt

```markdown
# Ralph-Powered Harness Session

## Objective
Continue development on harness project until all features complete.

## Per-Iteration Protocol

### 1. Session Startup
- Read `.harness/config.json` for project context
- Query Archon for session notes and current state
- Check META task for handoff notes

### 2. Task Selection
- Find highest-priority TODO task
- If task in "doing", continue that task
- Mark selected task as "doing"

### 3. Implementation
Follow harness-coder protocol:
- Orient and verify health
- Implement one feature
- Run tests
- Update Archon

### 4. Session Handoff
- Update session notes in Archon
- Update META task with progress
- Commit all changes

### 5. Completion Check
- All tasks done? → <promise>PROJECT_COMPLETE</promise>
- Tasks remaining? → Continue to next iteration

## Validation
```bash
npm test       # All tests must pass
npm run build  # Build must succeed
```

## Escape Hatch
After 3 iterations stuck on same task:
1. Mark task as blocked
2. Document blocker in Archon
3. Move to next task or <promise>BLOCKED</promise>
```

### 5. Start Ralph Loop

```bash
# Start Ralph with harness integration
& @ralph-loop --config .ralph/config.json
```

## Commands

```bash
# Start Ralph-powered harness
/harness-ralph

# Start with specific task focus
/harness-ralph --task "Authentication"

# Background mode
& /harness-ralph

# Check combined status
/harness-ralph --status
```

## Output

```markdown
## 🔄 Ralph + Harness Integration Started

### Configuration
| Setting | Value |
|---------|-------|
| Project | [PROJECT_NAME] |
| Total Tasks | 15 |
| Remaining | 8 |
| Max Iterations | 40 |
| Mode | Background |

### First Target
- Task: [FIRST_TODO_TASK]
- Priority: [ORDER]
- Feature: [FEATURE_GROUP]

### Monitor Progress
```bash
/ralph-status          # Ralph loop status
/harness-status        # Harness project status
```

### Cancel
```bash
/ralph-cancel
```

---
🚀 Ralph loop started. Development will continue until all tasks complete.
```

## Status Integration

When checking status, combine both views:

```markdown
## 🔄 Ralph + Harness Status

### Ralph Loop
- Iteration: 5/40
- Mode: Running
- Duration: 1h 15m

### Harness Progress
- Completed: 3/15 tasks (20%)
- Current: User Authentication
- Next: API Endpoints

### Session Notes
Last session completed OAuth integration.
Currently working on JWT tokens.

### Test Status
- Unit: ✅ 45/45
- Integration: ✅ 12/12
- E2E: ⚠️ 3/5

### Commands
- `/ralph-iterate` - Manual iteration
- `/harness-next` - Direct harness session
```
