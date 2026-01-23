---
name: speckit-ralph
description: Integrate Ralph Wiggum iterative loops with Spec Kit for persistent spec-driven development.
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
    prompt: Start the Ralph-powered speckit session
  - label: View Spec
    agent: speckit.specify
    prompt: View the current specification
---

## User Input

```text
$ARGUMENTS
```

## Purpose

Combine Ralph Wiggum's iterative persistence with Spec Kit's specification-driven development for enhanced quality assurance.

## Integration Concept

```
┌─────────────────────────────────────────────────────────────────────┐
│                    RALPH + SPEC KIT                                 │
│                                                                     │
│    SPEC ────────────────────────────────────────────────────┐       │
│    │                                                         │       │
│    │  Defines requirements, acceptance criteria, tests      │       │
│    │                                                         │       │
│    └─────────────────────────────────────────────────────────┘       │
│                           │                                          │
│                           ▼                                          │
│    ┌──────────────────────────────────────────────────────────┐     │
│    │  RALPH LOOP                                               │     │
│    │                                                           │     │
│    │  For each requirement in spec:                           │     │
│    │    1. Implement requirement                               │     │
│    │    2. Run validation                                      │     │
│    │    3. Update checklist                                    │     │
│    │    4. If all checked → COMPLETE                          │     │
│    │    5. Else → Continue iteration                          │     │
│    │                                                           │     │
│    └──────────────────────────────────────────────────────────┘     │
│                           │                                          │
│                           ▼                                          │
│    CHECKLIST ───────────────────────────────────────────────┐       │
│    │                                                         │       │
│    │  - [x] FR-001: User login                              │       │
│    │  - [x] FR-002: Session management                       │       │
│    │  - [ ] FR-003: Password reset  ◄── Current focus       │       │
│    │  - [ ] FR-004: MFA support                              │       │
│    │                                                         │       │
│    └─────────────────────────────────────────────────────────┘       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Execution Flow

### 1. Locate Specification

```bash
# Find spec from user input or detect
SPEC_PATH="$ARGUMENTS"

# If not provided, detect from branch
if [ -z "$SPEC_PATH" ]; then
    BRANCH=$(git branch --show-current)
    SPEC_PATH="specs/${BRANCH}/spec.md"
fi

# Verify spec exists
cat "$SPEC_PATH"
```

### 2. Parse Specification

Extract from spec.md:
- Requirements (FR-XXX)
- Acceptance criteria
- Success criteria
- User scenarios

### 3. Generate/Load Checklist

```bash
# Check for existing checklist
CHECKLIST_PATH="specs/${FEATURE}/checklists/requirements.md"

if [ ! -f "$CHECKLIST_PATH" ]; then
    # Generate checklist from spec
    @speckit.checklist "$SPEC_PATH"
fi

cat "$CHECKLIST_PATH"
```

### 4. Create Ralph Configuration

```python
ralph_config = {
    "loop_id": f"ralph-speckit-{feature_name}-{timestamp}",
    "archon_project_id": PROJECT_ID,
    "archon_task_id": SPEC_TASK_ID,
    "mode": "speckit_integration",
    "prompt_file": ".ralph/prompts/speckit-loop.md",
    "max_iterations": len(requirements) * 3,  # 3 iterations per requirement
    "completion_promise": "SPEC_COMPLETE",
    "integration": {
        "speckit": True,
        "spec_path": SPEC_PATH,
        "checklist_path": CHECKLIST_PATH,
        "validate_against_checklist": True
    }
}
```

### 5. Generate Spec-Aware Prompt

```markdown
# Ralph Loop: Spec Implementation

## Specification
**Path**: [SPEC_PATH]
**Feature**: [FEATURE_NAME]

## Requirements to Implement

[List of requirements from spec]

## Per-Iteration Protocol

### 1. Check Checklist Status
```bash
cat [CHECKLIST_PATH]
```

Find first unchecked requirement.

### 2. Implement Requirement
Following the spec:
- Read requirement details
- Mirror existing patterns
- Write tests first (TDD)
- Implement to pass tests

### 3. Validate
```bash
[VALIDATION_COMMANDS]
```

### 4. Update Checklist
If requirement passes validation:
- Mark checkbox as complete
- Add implementation notes

### 5. Completion Check
- All checklist items checked? → <promise>SPEC_COMPLETE</promise>
- Items remaining? → Continue to next requirement

## Acceptance Criteria
[From spec]

## Validation Commands
```bash
[BUILD_CMD]
[TEST_CMD]
```

## Escape Hatch
If stuck on a requirement for 3 iterations:
1. Document blocker in checklist
2. Mark as [BLOCKED] instead of [x]
3. Move to next requirement or <promise>BLOCKED</promise>
```

### 6. Start Ralph Loop

```bash
& @ralph-loop --config .ralph/config.json
```

## Commands

```bash
# Start Ralph with specific spec
/speckit-ralph specs/123-auth-feature/spec.md

# Auto-detect from current branch
/speckit-ralph

# With options
/speckit-ralph --max-iterations 30 --mode background

# Check status
/speckit-ralph --status
```

## Checklist Integration

### During Iteration

After each successful implementation, Ralph updates the checklist:

```markdown
## Requirements Checklist

- [x] FR-001: User can log in with email/password
  - Implemented: 2026-01-22 (Iteration 3)
  - Tests: `tests/auth/login.test.ts`
  
- [x] FR-002: Session persists across page refresh
  - Implemented: 2026-01-22 (Iteration 5)
  - Tests: `tests/auth/session.test.ts`
  
- [ ] FR-003: User can reset password via email
  - Status: In Progress (Iteration 7)
  - Blocked: Email service not configured
  
- [ ] FR-004: MFA with TOTP support
  - Status: Pending
```

### Completion Detection

Ralph completes when:
1. All `[ ]` are `[x]` in checklist
2. All validation commands pass
3. Spec acceptance criteria met

## Output

```markdown
## 🔄 Ralph + Spec Kit Integration Started

### Specification
- Path: specs/123-auth-feature/spec.md
- Feature: User Authentication
- Requirements: 8

### Checklist Status
| # | Requirement | Status |
|---|-------------|--------|
| FR-001 | User login | ✅ Done |
| FR-002 | Session management | ✅ Done |
| FR-003 | Password reset | 🔄 Current |
| FR-004 | MFA support | ⏳ Pending |
| ... | ... | ... |

### Ralph Configuration
- Max Iterations: 24
- Mode: Background
- Completion: SPEC_COMPLETE

### Monitor
```bash
/ralph-status       # Loop progress
/speckit.checklist  # View checklist
cat specs/123-auth-feature/checklists/requirements.md
```

---
🚀 Ralph will iterate until all spec requirements are implemented and validated.
```

## Status View

```markdown
## 🔄 Ralph + Spec Kit Status

### Specification Progress
- Feature: User Authentication
- Requirements: 5/8 complete (62%)

### Current Requirement
**FR-003: Password reset via email**
- Iteration: 7
- Status: In progress
- Blockers: None

### Ralph Loop
- Iteration: 12/24
- Duration: 35m
- Mode: Running

### Checklist
- [x] FR-001: User login
- [x] FR-002: Session management  
- [~] FR-003: Password reset ◄── Current
- [ ] FR-004: MFA support
- [ ] FR-005: OAuth providers

### Validation
- Tests: ✅ 28/28 passing
- Build: ✅ Success
- Spec Coverage: 62%
```
