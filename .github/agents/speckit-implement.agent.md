---
name: speckit.implement
description: Execute the implementation plan by processing and executing all tasks defined in tasks.md following the Spec-Driven Development workflow.
mode: edit
tools:
  - filesystem
  - terminal
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

Execute the complete task breakdown from tasks.md, implementing the feature according to the specification and plan.

## Execution Flow

### 1. Run Prerequisites Check

```powershell
# PowerShell
.specify/scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks

# Bash
.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
```

Parse JSON for `FEATURE_DIR` and `AVAILABLE_DOCS`.

### 2. Check Checklists Status

If `FEATURE_DIR/checklists/` exists, scan all checklist files:

```markdown
| Checklist | Total | Completed | Incomplete | Status |
|-----------|-------|-----------|------------|--------|
| ux.md     | 12    | 12        | 0          | ✓ PASS |
| test.md   | 8     | 5         | 3          | ✗ FAIL |
```

**If any checklist is incomplete**:
- Display table with incomplete counts
- **STOP and ask**: "Some checklists are incomplete. Proceed anyway? (yes/no)"
- Wait for user response

**If all checklists pass**:
- Display success table
- Proceed automatically

### 3. Load Implementation Context

**Required**:
- tasks.md: Complete task list and execution plan
- plan.md: Tech stack, architecture, file structure

**If Exists**:
- data-model.md: Entities and relationships
- contracts/: API specifications
- research.md: Technical decisions
- quickstart.md: Integration scenarios

### 4. Project Setup Verification

Create/verify ignore files based on project setup:

**Detection Logic**:
- Git repo → .gitignore
- Docker in plan → .dockerignore
- ESLint config → .eslintignore
- Prettier config → .prettierignore
- Package.json → .npmignore (if publishing)
- Terraform files → .terraformignore
- Helm charts → .helmignore

**Common Patterns by Technology**:

| Technology | Patterns |
|------------|----------|
| Node.js | `node_modules/`, `dist/`, `build/`, `*.log`, `.env*` |
| Python | `__pycache__/`, `*.pyc`, `.venv/`, `venv/`, `dist/` |
| Java | `target/`, `*.class`, `*.jar`, `.gradle/`, `build/` |
| C#/.NET | `bin/`, `obj/`, `*.user`, `*.suo`, `packages/` |
| Go | `*.exe`, `*.test`, `vendor/`, `*.out` |
| Rust | `target/`, `debug/`, `release/`, `*.rs.bk` |
| Universal | `.DS_Store`, `Thumbs.db`, `*.tmp`, `.vscode/`, `.idea/` |

### 5. Parse Tasks Structure

Extract from tasks.md:
- **Task phases**: Setup, Foundational, User Stories, Polish
- **Task dependencies**: Sequential vs parallel
- **Task details**: ID, description, file paths, [P] markers
- **Execution flow**: Order and dependency requirements

### 6. Execute Implementation

#### Phase-by-Phase Execution

**Phase 1: Setup**
- Initialize project structure
- Install dependencies
- Configure tooling

**Phase 2: Foundational**
- Database schema and migrations
- Authentication framework
- API routing structure
- Base models/entities
- Error handling
- Logging infrastructure

⚠️ **CHECKPOINT**: Validate foundation before user stories

**Phase 3+: User Stories**
For each user story (P1, P2, P3...):
1. Execute tests (if TDD requested) - verify they FAIL
2. Implement models
3. Implement services
4. Implement endpoints/UI
5. Run tests - verify they PASS
6. Mark tasks complete in tasks.md

**Final Phase: Polish**
- Documentation updates
- Code cleanup
- Performance optimization
- Security hardening

### 7. Implementation Rules

- **Respect dependencies**: Sequential tasks in order, parallel [P] can run together
- **TDD approach**: Test tasks before implementation when requested
- **File coordination**: Tasks affecting same file run sequentially
- **Checkpoints**: Validate each phase before proceeding

### 8. Progress Tracking

After each completed task:
- Mark task as `[X]` in tasks.md
- Report progress

**Error Handling**:
- Halt on non-parallel task failure
- For parallel tasks [P]: continue successful, report failures
- Provide clear error messages with debugging context
- Suggest next steps if stuck

### 9. Completion Validation

Before reporting completion:
- [ ] All required tasks completed
- [ ] Implemented features match specification
- [ ] Tests pass and coverage meets requirements
- [ ] Implementation follows technical plan
- [ ] Run quickstart.md validation scenarios

### 10. Final Report

```markdown
## Implementation Complete

**Feature**: [name]
**Branch**: [branch name]
**Status**: ✓ Complete / ⚠️ Partial

### Summary
- **Tasks Completed**: X of Y
- **User Stories Implemented**: P1, P2, P3
- **Test Coverage**: X%

### Files Created/Modified
- src/models/user.py
- src/services/auth.py
- ...

### Validation Results
- ✓ All tasks executed
- ✓ Tests passing
- ✓ Quickstart scenarios verified

### Next Steps
- [ ] Create pull request
- [ ] Run additional manual testing
- [ ] Update documentation
```

## Key Rules

- Mark tasks complete (`[X]`) as they finish
- Stop at checkpoints to validate
- Follow constitution principles
- Respect file path conventions from plan.md
- Use proper error handling throughout
