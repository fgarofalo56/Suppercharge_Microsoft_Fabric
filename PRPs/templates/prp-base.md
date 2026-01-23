# PRP Base Template

Use this template as a starting point for creating comprehensive PRPs.

## How to Use

1. Copy this template
2. Fill in all sections with specific details
3. Replace placeholders with actual values
4. Include real code snippets from the codebase
5. Specify executable validation commands

---

# Feature: {Feature Name}

## Summary

{One paragraph: What we're building and high-level approach}

## User Story

As a {user type}
I want to {action}
So that {benefit}

## Problem Statement

{Specific problem this solves - must be testable}

## Solution Statement

{How we're solving it - architecture overview}

## Metadata

| Field | Value |
|-------|-------|
| Type | NEW_CAPABILITY / ENHANCEMENT / REFACTOR / BUG_FIX |
| Complexity | LOW / MEDIUM / HIGH |
| Systems Affected | {comma-separated list} |
| Dependencies | {external libs/services with versions} |
| Estimated Tasks | {count} |

---

## UX Design

### Before State

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   USER_FLOW: [describe current step-by-step experience]                       ║
║   PAIN_POINT: [what's missing, broken, or inefficient]                        ║
║   DATA_FLOW: [how data moves through the system currently]                    ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### After State

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                               AFTER STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   USER_FLOW: [describe new step-by-step experience]                           ║
║   VALUE_ADD: [what user gains from this change]                               ║
║   DATA_FLOW: [how data moves through the system after]                        ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| {path/component} | {old behavior} | {new behavior} | {what changes for user} |

---

## Mandatory Reading

**CRITICAL: Read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `path/to/critical.ts` | 10-50 | Pattern to MIRROR exactly |
| P1 | `path/to/types.ts` | 1-30 | Types to IMPORT |
| P2 | `path/to/test.ts` | all | Test pattern to FOLLOW |

---

## Patterns to Mirror

**NAMING_CONVENTION:**
```
// SOURCE: {file}:{lines}
// COPY THIS PATTERN:
{actual code snippet from codebase}
```

**ERROR_HANDLING:**
```
// SOURCE: {file}:{lines}
// COPY THIS PATTERN:
{actual code snippet from codebase}
```

**LOGGING_PATTERN:**
```
// SOURCE: {file}:{lines}
// COPY THIS PATTERN:
{actual code snippet from codebase}
```

**TEST_STRUCTURE:**
```
// SOURCE: {file}:{lines}
// COPY THIS PATTERN:
{actual code snippet from codebase}
```

---

## Files to Change

| File | Action | Justification |
|------|--------|---------------|
| `src/features/new/models.ts` | CREATE | Type definitions |
| `src/features/new/service.ts` | CREATE | Business logic |
| `src/core/index.ts` | UPDATE | Add exports |

---

## NOT Building (Scope Limits)

Explicit exclusions to prevent scope creep:

- {Item 1 - explicitly out of scope and why}
- {Item 2 - explicitly out of scope and why}

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: {Description}

- **ACTION**: CREATE/UPDATE {file path}
- **IMPLEMENT**: {specific what to do}
- **MIRROR**: `{file}:{lines}` - follow existing pattern
- **IMPORTS**: {what to import}
- **GOTCHA**: {known issue to avoid}
- **VALIDATE**: `{validation command}`

### Task 2: {Description}

- **ACTION**: {action}
- **IMPLEMENT**: {details}
- **MIRROR**: `{file}:{lines}`
- **IMPORTS**: {imports}
- **GOTCHA**: {gotcha}
- **VALIDATE**: `{command}`

{Continue for all tasks...}

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```bash
# Replace with actual project commands
dotnet build  # or npm run lint && npm run type-check
```

**EXPECT**: Exit 0, no errors

### Level 2: UNIT_TESTS

```bash
# Replace with actual project commands
dotnet test --filter "Category=Unit"  # or npm test
```

**EXPECT**: All tests pass

### Level 3: FULL_SUITE

```bash
# Replace with actual project commands
dotnet test && dotnet build --configuration Release
```

**EXPECT**: All tests pass, build succeeds

---

## Testing Strategy

### Unit Tests to Write

| Test File | Test Cases | Validates |
|-----------|------------|-----------|
| `tests/new.test.ts` | valid input, invalid input | Schemas |
| `tests/service.test.ts` | CRUD ops, access control | Business logic |

### Edge Cases Checklist

- [ ] Empty string inputs
- [ ] Missing required fields
- [ ] Unauthorized access attempts
- [ ] Not found scenarios
- [ ] Duplicate creation attempts
- [ ] {feature-specific edge case}

---

## Acceptance Criteria

- [ ] All specified functionality implemented per user story
- [ ] Validation commands pass with exit 0
- [ ] Unit tests cover >= 80% of new code
- [ ] Code mirrors existing patterns exactly
- [ ] No regressions in existing tests
- [ ] UX matches "After State" diagram

---

## Completion Checklist

- [ ] All tasks completed in dependency order
- [ ] Each task validated immediately after completion
- [ ] Level 1: Static analysis passes
- [ ] Level 2: Unit tests pass
- [ ] Level 3: Full test suite + build succeeds
- [ ] All acceptance criteria met

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| {Risk description} | LOW/MED/HIGH | LOW/MED/HIGH | {Strategy} |

---

## Notes

{Additional context, design decisions, trade-offs, future considerations}
