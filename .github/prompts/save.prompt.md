---
description: Save current session context as a checkpoint without ending session
---

# Save Checkpoint

Save the current session state without ending the session.

## Save Operations

### 1. Update Archon Session Memory

```
manage_document("update",
  project_id="[PROJECT_ID]",
  document_id="[SESSION_DOC_ID]",
  content={
    "checkpoint_time": "[CURRENT_TIMESTAMP]",
    "current_focus": "[What we're working on]",
    "progress": "[What's been done]",
    "next_steps": "[What's remaining]",
    "discoveries": [...],
    "blockers": [...]
  }
)
```

### 2. Update Task Status (if applicable)

```
manage_task("update", task_id="...", description="Checkpoint: [progress notes]")
```

### 3. Git Status Check

```bash
git status -sb
```

If there are significant changes worth committing:

```bash
git add -A
git commit -m "wip: [description of current work]"
```

## Confirmation

```markdown
## ✅ Checkpoint Saved

### 📝 Session Memory Updated

- Focus: [current focus]
- Progress: [what's done]
- Next: [what's remaining]

### 📋 Task Status

- [Task]: [status/progress]

### 🌿 Git State

- Uncommitted changes: [yes/no]
- Last commit: [if made]

### ⏰ Checkpoint Time

[timestamp]

---

_Session continues. Use `/end` when finished._
```

This is a checkpoint, not end of session. Work can continue.

{input}
