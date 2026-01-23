---
name: ralph-status
description: Check the status of active or completed Ralph Wiggum loops.
mode: agent
tools:
  - filesystem
  - terminal
  - archon-find_tasks
  - archon-find_documents
handoffs:
  - label: Continue Iteration
    agent: ralph-loop
    prompt: Continue the Ralph loop
  - label: Cancel Loop
    agent: ralph-loop
    prompt: Cancel the active Ralph loop
---

## User Input

```text
$ARGUMENTS
```

## Purpose

Query and display the status of Ralph Wiggum loops.

## Execution

Invoke the `@ralph-monitor` agent to:

1. Query Archon for Ralph state documents
2. Read local `.ralph/` state
3. Format and display status report

## Options

```bash
/ralph-status              # Quick status of active loop
/ralph-status --full       # Detailed status report
/ralph-status --history    # Show completed loops
/ralph-status --watch      # Continuous monitoring
/ralph-status --json       # JSON output
/ralph-status --check      # Verify configuration
```

## Quick Status Format

```
🔄 Ralph: Iteration 12/50 | 67% | Tests ✅ 15/15 | Duration 25m
```

## Full Status Format

```markdown
## 🔄 Ralph Loop Status

### Loop: ralph-20260122-150000
| Property | Value |
|----------|-------|
| Status | 🟢 Running |
| Iteration | 12/50 |
| Duration | 25m 30s |
| Task | Build REST API |

### Progress
[====================----------] 67%

### Recent Iterations
| # | Time | Summary | Tests |
|---|------|---------|-------|
| 12 | 2m ago | Added validation | ✅ 15/15 |
| 11 | 8m ago | Fixed edge case | ⚠️ 14/15 |

### Validation
- Build: ✅ | Tests: ✅ | Lint: ⚠️

### Commands
- Continue: `/ralph-iterate`
- Cancel: `/ralph-cancel`
```

## No Active Loop

If no loop is running:

```markdown
## Ralph Status

No active Ralph loop found.

### Recent Loops
| Loop | Task | Status | When |
|------|------|--------|------|
| ralph-001 | Auth API | ✅ Complete | 2h ago |

### Start New Loop
Run `/ralph-start` to begin a new loop.
```
