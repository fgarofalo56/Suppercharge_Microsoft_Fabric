---
name: speckit.tasks
description: Generate an actionable, dependency-ordered tasks.md for the feature based on available design artifacts organized by user story.
mode: agent
tools:
  - filesystem
  - terminal
handoffs:
  - label: Analyze For Consistency
    agent: speckit.analyze
    prompt: Run a project analysis for consistency
  - label: Implement Project
    agent: speckit.implement
    prompt: Start the implementation in phases
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

Generate an actionable task list organized by user story from the implementation plan and design artifacts.

## Execution Flow

### 1. Setup

Run prerequisite check:

```powershell
# PowerShell
.specify/scripts/powershell/check-prerequisites.ps1 -Json

# Bash
.specify/scripts/bash/check-prerequisites.sh --json
```

Parse JSON for `FEATURE_DIR` and `AVAILABLE_DOCS` list.

### 2. Load Design Documents

Read from FEATURE_DIR:
- **Required**: plan.md (tech stack, libraries, structure), spec.md (user stories with priorities)
- **Optional**: data-model.md (entities), contracts/ (API endpoints), research.md (decisions), quickstart.md (test scenarios)

### 3. Execute Task Generation Workflow

1. Extract tech stack, libraries, project structure from plan.md
2. Extract user stories with priorities (P1, P2, P3...) from spec.md
3. If data-model.md exists: Extract entities and map to user stories
4. If contracts/ exists: Map endpoints to user stories
5. If research.md exists: Extract decisions for setup tasks
6. Generate tasks organized by user story
7. Generate dependency graph
8. Create parallel execution examples
9. Validate task completeness

## Task Generation Rules

### Task Format (REQUIRED)

Every task MUST follow this exact format:

```text
- [ ] [TaskID] [P?] [Story?] Description with file path
```

**Components**:
1. **Checkbox**: Always `- [ ]`
2. **Task ID**: Sequential (T001, T002...)
3. **[P] marker**: Only if parallelizable (different files, no dependencies)
4. **[Story] label**: Required for user story phases ([US1], [US2]...)
5. **Description**: Clear action with exact file path

**Examples**:
- ✅ `- [ ] T001 Create project structure per implementation plan`
- ✅ `- [ ] T005 [P] Implement auth middleware in src/middleware/auth.py`
- ✅ `- [ ] T012 [P] [US1] Create User model in src/models/user.py`
- ❌ `- [ ] Create User model` (missing ID)
- ❌ `T001 [US1] Create model` (missing checkbox)

### Phase Structure

```markdown
## Phase 1: Setup (Shared Infrastructure)
- Project initialization
- Basic structure

## Phase 2: Foundational (Blocking Prerequisites)
**⚠️ CRITICAL**: No user story work can begin until this phase is complete
- Database schema
- Authentication framework
- API routing structure
- Base models
- Error handling
- Logging infrastructure

**Checkpoint**: Foundation ready - user story implementation can begin

## Phase 3: User Story 1 - [Title] (Priority: P1) 🎯 MVP
**Goal**: [What this story delivers]
**Independent Test**: [How to verify this story works alone]

### Tests for User Story 1 (if requested)
- [ ] T010 [P] [US1] Contract test for [endpoint]
- [ ] T011 [P] [US1] Integration test for [journey]

### Implementation for User Story 1
- [ ] T012 [P] [US1] Create [Entity] model in src/models/
- [ ] T013 [US1] Implement [Service] in src/services/
- [ ] T014 [US1] Implement [endpoint] in src/api/

**Checkpoint**: User Story 1 fully functional and testable

## Phase 4: User Story 2 - [Title] (Priority: P2)
[Same structure as above]

## Phase N: Polish & Cross-Cutting Concerns
- Documentation updates
- Code cleanup
- Performance optimization
- Security hardening
```

### Task Organization Rules

1. **From User Stories (PRIMARY)**: Each P1, P2, P3 story gets its own phase
2. **Map all components to their story**: Models, Services, Endpoints, Tests
3. **Shared entities**: Put in earliest story that needs it, or Setup phase
4. **Within each story**: Tests (if requested) → Models → Services → Endpoints → Integration

## Output Structure

Generate `tasks.md` with:

```markdown
# Tasks: [FEATURE NAME]

**Prerequisites**: plan.md, spec.md
**Generated**: [DATE]

## Format Reference
- **[P]**: Can run in parallel
- **[Story]**: Which user story (US1, US2...)
- Include exact file paths

## Phase 1: Setup
[Tasks]

## Phase 2: Foundational
[Tasks]
**Checkpoint**: Foundation ready

## Phase 3: User Story 1 - [Title] (P1) 🎯 MVP
**Goal**: [Description]
**Independent Test**: [Verification]
[Tasks]
**Checkpoint**: US1 complete

## Phase 4+: Additional User Stories
[Following same pattern]

## Dependencies & Execution Order

### Phase Dependencies
- Setup: No dependencies
- Foundational: Depends on Setup, BLOCKS all user stories
- User Stories: All depend on Foundational, can run in parallel

### Within Each User Story
- Tests MUST fail before implementation
- Models before services
- Services before endpoints
- Core before integration

## Implementation Strategy

### MVP First (User Story 1 Only)
1. Complete Setup + Foundational
2. Complete User Story 1
3. STOP and VALIDATE
4. Deploy/demo if ready

### Incremental Delivery
1. Foundation → ready
2. Add US1 → test → deploy (MVP!)
3. Add US2 → test → deploy
4. Each story adds value without breaking previous
```

### 5. Report Completion

Output:
- Path to generated tasks.md
- Total task count
- Task count per user story
- Parallel opportunities identified
- Suggested MVP scope
- Format validation: Confirm all tasks follow checklist format
