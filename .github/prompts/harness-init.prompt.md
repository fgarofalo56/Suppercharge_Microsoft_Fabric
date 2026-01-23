---
name: harness-init
description: Run the harness initializer agent. First session only - generates feature tasks from specification and sets up project environment.
mode: agent
agent: harness-initializer
---

# 🎬 Initialize Harness

Run the initializer agent to set up the autonomous coding harness.

## When to Use

Use this prompt **once** after running `/harness-setup`:

1. ✅ You've run `/harness-setup` wizard
2. ✅ Archon project was created
3. ✅ Application specification is stored
4. ⬜ Feature tasks need to be generated

## What Initialization Does

The **harness-initializer** agent will:

### 1. Read Application Specification
From Archon documents (created during setup)

### 2. Generate Feature Tasks
Creates 20-50 detailed tasks in Archon based on the spec:
- Clear acceptance criteria
- Test steps for verification
- Priority ordering
- Feature grouping

### 3. Set Up Project Structure
Creates appropriate directories:
```
src/
tests/
docs/
.harness/
```

### 4. Initialize Environment
Runs `init.sh` to set up dependencies.

### 5. Initialize Git
Creates initial commit with project structure.

### 6. Create Handoff Notes
Updates Archon session notes for coding agent.

---

## Timing Expectations

⏱️ **This takes 5-15 minutes** depending on spec complexity.

The agent is generating detailed tasks - it may appear slow but is working.

---

## After Initialization

When complete, you'll have:
- [ ] Feature tasks in Archon (view with `/harness-status`)
- [ ] Project structure created
- [ ] Git repository initialized
- [ ] Ready for coding sessions

Then run:
```bash
/harness-next   # Start first coding session
```

---

## Starting Initialization

Running harness-initializer agent...
