# Session Handoff Template

Use this template to create session handoff notes in Archon documents.

---

## Archon Session Notes Document Structure

```json
{
  "sessions": [
    {
      "session_number": 1,
      "agent": "harness-initializer | harness-coder",
      "date": "2024-01-22T10:00:00Z",
      "status": "completed | partial | blocked",
      "duration_minutes": 45,
      
      "completed": [
        "Description of what was completed",
        "Another completed item"
      ],
      
      "task_completed": {
        "id": "task-uuid",
        "title": "Task title",
        "feature": "Feature group"
      },
      
      "files_changed": [
        "src/services/auth.ts",
        "tests/unit/auth.test.ts"
      ],
      
      "tests_added": [
        "test_user_login",
        "test_invalid_credentials"
      ],
      
      "blockers": [
        {
          "type": "test_failure | dependency | unclear_spec",
          "description": "Description of blocker",
          "resolution": "How it was resolved (or pending)"
        }
      ],
      
      "notes": [
        "Important context for next session",
        "Decisions made during this session"
      ],
      
      "next_priority": {
        "id": "next-task-uuid",
        "title": "Next task to work on"
      }
    }
  ],
  
  "current_focus": "Current or next task title",
  
  "blockers": [
    {
      "type": "blocker type",
      "description": "Active blocker details",
      "since_session": 3
    }
  ],
  
  "next_steps": [
    "Continue with Task X",
    "Fix failing tests",
    "Address review feedback"
  ],
  
  "decisions": [
    {
      "date": "2024-01-22",
      "decision": "Use JWT for authentication",
      "rationale": "Better for stateless API"
    }
  ]
}
```

---

## Session Summary Templates

### Completed Session Template

```markdown
## Session [X] Summary

**Agent**: harness-coder
**Date**: [TIMESTAMP]
**Status**: ✅ Complete

### Task Completed
- **Title**: [Task title]
- **ID**: [task-uuid]
- **Feature**: [Feature group]

### Changes Made
| File | Change |
|------|--------|
| src/... | Added user service |
| tests/... | Added unit tests |

### Tests
- Unit: 15/15 passing
- Integration: 8/8 passing

### Next Session
- **Task**: [Next task title]
- **Priority**: [Priority level]
```

### Partial Session Template

```markdown
## Session [X] Summary

**Agent**: harness-coder
**Date**: [TIMESTAMP]
**Status**: ⚠️ Partial (context limit reached)

### Progress on Task
- **Title**: [Task title]
- **ID**: [task-uuid]
- **Progress**: ~70%

### Completed
- [x] Created service structure
- [x] Implemented main logic
- [ ] Add error handling (pending)
- [ ] Write tests (pending)

### State
- Code is functional but incomplete
- No breaking changes committed
- Ready for continuation

### Next Session
- Continue current task
- Complete error handling and tests
```

### Blocked Session Template

```markdown
## Session [X] Summary

**Agent**: harness-coder
**Date**: [TIMESTAMP]
**Status**: 🚫 Blocked

### Blocker
**Type**: [test_failure | dependency | unclear_spec | environment]
**Description**: [Detailed description]

### Attempted Solutions
1. [What was tried]
2. [What else was tried]

### Needs
- [What help is needed]
- [Decision required from user]

### Task Status
- Task reset to TODO
- Awaiting resolution before continuing
```

---

## META Task Template

```markdown
## Current Session Status
- Session: [X]
- Agent: [agent name]
- Status: [status]

## Session Summary
[Brief summary of session]

## Progress
- Total Tasks: [X]
- Completed: [Y]
- Remaining: [Z]
- Progress: [%]

## Next Session
- Task: [Next task title]
- Task ID: [uuid]
- Priority: [priority]

---
Last Updated: [TIMESTAMP]
```

---

## Git Commit Message Template

```
[FEATURE_GROUP]: [Task title]

Implemented:
- [Change 1]
- [Change 2]

Tests:
- Added [X] unit tests
- Added [X] integration tests

Task: [TASK_ID] - [STATUS]
Session: [X]
Archon Project: [PROJECT_ID]
```

---

## Usage in Agents

### Reading Session Notes

```python
# Get session notes document
notes_doc = find_documents(
    project_id=PROJECT_ID,
    document_type="note",
    query="Session Notes"
)

# Parse current state
current_focus = notes_doc["content"]["current_focus"]
blockers = notes_doc["content"]["blockers"]
last_session = notes_doc["content"]["sessions"][-1]
```

### Updating Session Notes

```python
# Get current notes
notes = find_documents(project_id=PROJECT_ID, query="Session Notes")

# Add new session
new_session = {
    "session_number": len(notes["content"]["sessions"]) + 1,
    "agent": "harness-coder",
    "date": datetime.now().isoformat(),
    "status": "completed",
    "task_completed": {
        "id": completed_task_id,
        "title": completed_task_title,
        "feature": completed_task_feature
    },
    "files_changed": changed_files,
    "notes": session_notes,
    "next_priority": {
        "id": next_task_id,
        "title": next_task_title
    }
}

notes["content"]["sessions"].append(new_session)
notes["content"]["current_focus"] = next_task_title

# Save back to Archon
manage_document("update",
    project_id=PROJECT_ID,
    document_id=notes["id"],
    content=notes["content"]
)
```
