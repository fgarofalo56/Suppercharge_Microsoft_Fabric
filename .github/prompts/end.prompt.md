---
description: Execute end of session protocol - save state, update Archon, commit changes
---

# End of Session Protocol

Execute the complete end-of-session checklist to save all work and state.

## End Session Steps

### 1. Update Archon Task Status

Update any tasks that were worked on:

```
manage_task("update", task_id="...", status="review", description="Session notes...")
```

### 2. Update Session Memory Document

Update the session context document in Archon:

```
manage_document("update",
  project_id="[PROJECT_ID]",
  document_id="[SESSION_DOC_ID]",
  content={
    "last_session": "[TODAY'S DATE]",
    "current_focus": "[What was worked on]",
    "blockers": [...],
    "decisions_made": [...],
    "next_steps": [...]
  }
)
```

### 3. Git Operations

Stage and commit any uncommitted changes:

```bash
git status
git add -A
git commit -m "[appropriate conventional commit message]"
```

**Note**: Do NOT push unless explicitly requested.

### 4. Provide Session Summary

```markdown
## 📋 Session Summary

### ⏱️ Work Completed

- [List of completed items]

### 🚧 Work In Progress

- [List of WIP items with status]

### 💡 Discoveries & Decisions

- [New discoveries made]
- [Decisions documented]

### ❌ Issues Encountered

- [Any blockers or failed attempts]

### 📁 Files Modified

- [Key files changed]

### 🎯 Recommended Next Session Focus

1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

### ✅ Checklist

- [ ] Archon tasks updated
- [ ] Session memory saved
- [ ] Changes committed
- [ ] No uncommitted work
```

Confirm all updates have been made.

{input}
