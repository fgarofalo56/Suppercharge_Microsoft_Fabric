---
name: ralph-start
description: Start the Ralph Wiggum setup wizard to configure an iterative development loop.
mode: agent
tools:
  - filesystem
  - terminal
handoffs:
  - label: Start Ralph Loop
    agent: ralph-loop
    prompt: Start executing the configured Ralph loop
  - label: Check Status
    agent: ralph-monitor
    prompt: Check the current Ralph loop status
---

## User Input

```text
$ARGUMENTS
```

## Purpose

Launch the Ralph Wiggum setup wizard to configure a new iterative development loop.

## Execution

Invoke the `@ralph-wizard` agent to guide the user through:

1. **Project Selection** - Choose or create Archon project
2. **Task Selection** - Choose task to work on or create new
3. **Prompt Configuration** - Set up the iteration prompt
4. **Options** - Max iterations, completion criteria, mode
5. **Framework Integration** - Harness, SpecKit, PRP options
6. **Create & Start** - Generate config and optionally start

## Quick Options

If the user provides arguments, parse them:

```bash
# Full wizard
/ralph-start

# Quick with defaults
/ralph-start --quick

# Auto-detect everything
/ralph-start --auto

# Specify task directly
/ralph-start --task "Build REST API for todos"

# With options
/ralph-start "Implement auth" --max-iterations 30 --mode background
```

## Output

After wizard completion:
- Configuration saved to `.ralph/config.json`
- Prompt saved to `.ralph/prompts/current.md`
- Archon state document created
- Task updated to "doing" status

Offer to start the loop immediately or wait for manual start.
