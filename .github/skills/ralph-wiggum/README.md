# Ralph Wiggum for GitHub Copilot

> **"Ralph is a Bash loop"** - Iterative AI development that keeps working until the job is done.

## Overview

Ralph Wiggum is an iterative development methodology that enables AI agents to work persistently on tasks until completion. This integration brings Ralph's power to GitHub Copilot with:

- **Archon-based state management** for context preservation
- **Integration with The Long Run Harness, Spec Kit, and PRP** frameworks
- **Multiple execution modes** (background, manual, hybrid)
- **Full wizard setup** for easy configuration

## Quick Start

```bash
# Start the setup wizard
/ralph-start

# Or quick start with auto-detection
/ralph-start --auto

# Check status of running loop
/ralph-status

# Cancel if needed
/ralph-cancel
```

## Core Concept

Ralph creates a self-referential feedback loop where:

1. AI receives the same prompt each iteration
2. Previous work persists in files and git history
3. Each iteration sees modified files from previous work
4. AI improves by reading its own past work
5. Loop continues until completion criteria met

```
┌────────────────────────────────────────────────────┐
│                RALPH LOOP                          │
│                                                    │
│    PROMPT ──► WORK ──► VALIDATE ──► CHECK         │
│       ▲                              │             │
│       │         ┌────────────────────┤             │
│       │         │                    │             │
│       │     CONTINUE              COMPLETE         │
│       │         │                    │             │
│       └─────────┘                    ▼             │
│                                   [EXIT]           │
└────────────────────────────────────────────────────┘
```

## Available Commands

| Command | Description |
|---------|-------------|
| `/ralph-start` | Launch setup wizard |
| `/ralph-iterate` | Run single iteration manually |
| `/ralph-status` | Check loop status |
| `/ralph-cancel` | Cancel active loop |
| `/harness-ralph` | Ralph + Long Run Harness |
| `/speckit-ralph` | Ralph + Spec Kit |
| `/prp-ralph` | Ralph + PRP Framework |

## Components

### Agents

| Agent | Purpose |
|-------|---------|
| `@ralph-wizard` | Interactive setup wizard |
| `@ralph-loop` | Main loop controller |
| `@ralph-monitor` | Progress monitoring |

### Skills

- **SKILL.md** - Complete feature overview
- **reference.md** - Detailed configuration reference

### Templates

- **config.template.json** - Loop configuration template
- **prompt.template.md** - Iteration prompt template
- **archon-state.template.json** - Archon state document template

## Archon Integration

Ralph uses Archon MCP for state management:

```python
# State is tracked in Archon documents
find_documents(project_id=PROJECT, query="Ralph Loop State")

# Task progress is synced
manage_task("update", task_id=TASK, status="doing")

# Clean handoffs between sessions
manage_document("update", document_id=DOC, content={...})
```

## Framework Integration

### With The Long Run Harness

```bash
/harness-ralph
```

Ralph wraps harness-coder sessions, providing iteration until project complete.

### With Spec Kit

```bash
/speckit-ralph specs/123-feature/spec.md
```

Ralph iterates until all spec requirements are implemented and validated.

### With PRP Framework

```bash
/prp-ralph PRPs/plans/feature.plan.md
```

Ralph executes PRP plans task by task with persistent iteration.

## Execution Modes

### Background Mode

```bash
& /ralph-loop "Build REST API" --max-iterations 50
```

Fully autonomous - run until complete.

### Manual Mode

```bash
/ralph-iterate  # Run one iteration
/ralph-iterate  # Run another
/ralph-iterate  # Continue as needed
```

Full control over each iteration.

### Hybrid Mode (Recommended)

```bash
/ralph-iterate  # Watch first few iterations
/ralph-iterate  # Verify direction
& /ralph-continue --remaining  # Go autonomous
```

Supervised start, autonomous finish.

## Loop Termination

Ralph stops when ANY of these conditions are met:

1. **Completion Promise** - Agent outputs `<promise>COMPLETE</promise>`
2. **Archon Task Done** - Task status changes to "done"
3. **Max Iterations** - Configured limit reached
4. **Manual Cancel** - User runs `/ralph-cancel`

## Best Practices

### Prompt Writing

✅ **Good:**
```markdown
Build a REST API for todos.

When complete:
- All CRUD endpoints working
- Input validation in place
- Tests passing (coverage > 80%)
- Output: <promise>COMPLETE</promise>
```

❌ **Bad:**
```
Build a todo API and make it good.
```

### Always Set Limits

```bash
/ralph-loop "..." --max-iterations 50
```

This prevents infinite loops on impossible tasks.

### Include Escape Hatches

```markdown
After 15 iterations without progress:
- Document what's blocking
- Output: <promise>BLOCKED</promise>
```

## When to Use Ralph

### ✅ Good For

- Well-defined tasks with clear success criteria
- TDD/BDD development with automated verification
- Greenfield projects where you can walk away
- Tasks with automatic validation (tests, lints)

### ❌ Not Good For

- Tasks requiring human judgment
- Design decisions
- One-shot operations
- Unclear success criteria

## Configuration

### Main Config: `.ralph/config.json`

```json
{
  "loop_id": "ralph-20260122-150000",
  "max_iterations": 50,
  "completion_promise": "COMPLETE",
  "mode": "hybrid",
  "validation": {
    "build": "npm run build",
    "test": "npm test"
  },
  "integration": {
    "harness": true,
    "speckit": false,
    "prp": true
  }
}
```

### Archon State Document

Ralph maintains state in Archon for:
- Session recovery
- Progress monitoring
- Context handoffs

## Learn More

- [Ralph Wiggum SKILL.md](./SKILL.md) - Complete feature reference
- [Configuration Reference](./reference.md) - All options documented
- [Original Ralph Technique](https://ghuntley.com/ralph/) - Geoffrey Huntley's article
- [Ralph Orchestrator](https://github.com/mikeyobrien/ralph-orchestrator) - Related project

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Loop never completes | Add clearer completion criteria |
| Stuck in loop | Add escape hatch instructions |
| Context lost | Check Archon connection |
| Tests keep failing | Review prompt for clarity |

### Recovery

```bash
# Check state
cat .ralph/config.json
/ralph-status

# Resume from checkpoint
/ralph-start --resume

# Reset and start fresh
/ralph-cancel --cleanup
/ralph-start
```

---

## Credits

Based on [Geoffrey Huntley's Ralph technique](https://ghuntley.com/ralph/).

Adapted for GitHub Copilot with Archon integration.
