---
mode: agent
description: "Create comprehensive implementation plan from PRD or feature description with codebase analysis"
tools: ["filesystem", "changes", "githubRepo"]
---

# PRP Implementation Plan Generator

**Input**: {{ input }}

---

## Objective

Transform the input into a battle-tested implementation plan through systematic codebase exploration, pattern extraction, and strategic research.

**Core Principle**: PLAN ONLY - no code written. Create a context-rich document that enables one-pass implementation success.

**Execution Order**: CODEBASE FIRST, RESEARCH SECOND. Solutions must fit existing patterns before introducing new ones.

---

## Phase 0: DETECT - Input Type Resolution

**Determine input type:**

| Input Pattern | Type | Action |
|---------------|------|--------|
| Ends with `.prd.md` | PRD file | Parse PRD, select next phase |
| File path that exists | Document | Read and extract feature description |
| Free-form text | Description | Use directly as feature input |

### If PRD File Detected:

1. **Read the PRD file**
2. **Parse the Implementation Phases table** - find rows with `Status: pending`
3. **Check dependencies** - only select phases whose dependencies are `complete`
4. **Select the next actionable phase**
5. **Report selection to user**

### If Free-form:

Proceed directly to Phase 1 with the input as feature description.

---

## Phase 1: PARSE - Feature Understanding

**EXTRACT from input:**

- Core problem being solved
- User value and business impact
- Feature type: NEW_CAPABILITY | ENHANCEMENT | REFACTOR | BUG_FIX
- Complexity: LOW | MEDIUM | HIGH
- Affected systems list

**FORMULATE user story:**

```
As a <user type>
I want to <action/goal>
So that <benefit/value>
```

**GATE**: If requirements are AMBIGUOUS → STOP and ASK user for clarification.

---

## Phase 2: EXPLORE - Codebase Intelligence

**Thoroughly explore the codebase to find:**

1. **Similar implementations** - find analogous features with file:line references
2. **Naming conventions** - extract actual examples of function/class/file naming
3. **Error handling patterns** - how errors are created, thrown, caught
4. **Logging patterns** - logger usage, message formats
5. **Type definitions** - relevant interfaces and types
6. **Test patterns** - test file structure, assertion styles
7. **Integration points** - where new code connects to existing
8. **Dependencies** - relevant libraries already in use

**DOCUMENT discoveries in table format:**

| Category | File:Lines | Pattern Description | Code Snippet |
|----------|-----------|---------------------|--------------|
| NAMING | `src/X/service.ts:10-15` | camelCase functions | `export function createThing()` |
| ERRORS | `src/X/errors.ts:5-20` | Custom error classes | `class ThingNotFoundError` |
| TESTS | `tests/X.test.ts:1-30` | describe/it blocks | `describe("service", () => {` |

**Return ACTUAL code snippets from codebase, not generic examples.**

---

## Phase 3: RESEARCH - External Documentation

**ONLY AFTER Phase 2** - solutions must fit existing codebase patterns first.

**SEARCH for:**

- Official documentation for involved libraries
- Known gotchas, breaking changes, deprecations
- Security considerations and best practices
- Performance optimization patterns

**FORMAT references with specificity:**

```markdown
- [Library Docs](https://url#specific-section)
  - KEY_INSIGHT: {what we learned}
  - APPLIES_TO: {which task/file this affects}
  - GOTCHA: {potential pitfall and how to avoid}
```

---

## Phase 4: DESIGN - UX Transformation

**CREATE ASCII diagrams showing user experience before and after:**

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

---

## Phase 5: ARCHITECT - Strategic Design

**ANALYZE deeply:**

- ARCHITECTURE_FIT: How does this integrate with the existing architecture?
- EXECUTION_ORDER: What must happen first → second → third?
- FAILURE_MODES: Edge cases, race conditions, error scenarios?
- PERFORMANCE: Will this scale? Database queries optimized?
- SECURITY: Attack vectors? Data exposure risks? Auth/authz?
- MAINTAINABILITY: Will future devs understand this code?

**DECIDE and document:**

```markdown
APPROACH_CHOSEN: [description]
RATIONALE: [why this over alternatives - reference codebase patterns]

ALTERNATIVES_REJECTED:
- [Alternative 1]: Rejected because [specific reason]
- [Alternative 2]: Rejected because [specific reason]

NOT_BUILDING (explicit scope limits):
- [Item 1 - explicitly out of scope and why]
- [Item 2 - explicitly out of scope and why]
```

---

## Phase 6: GENERATE - Implementation Plan File

**OUTPUT_PATH**: `PRPs/plans/{kebab-case-feature-name}.plan.md`

### Plan Structure

```markdown
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
{ASCII diagram - current user experience}

### After State
{ASCII diagram - new user experience}

### Interaction Changes
| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| {path} | {old behavior} | {new behavior} | {what changes} |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `path/to/critical.ts` | 10-50 | Pattern to MIRROR exactly |
| P1 | `path/to/types.ts` | 1-30 | Types to IMPORT |
| P2 | `path/to/test.ts` | all | Test pattern to FOLLOW |

---

## Patterns to Mirror

**NAMING_CONVENTION:**
```
// SOURCE: {file:lines}
// COPY THIS PATTERN:
{actual code snippet from codebase}
```

**ERROR_HANDLING:**
```
// SOURCE: {file:lines}
// COPY THIS PATTERN:
{actual code snippet from codebase}
```

**TEST_STRUCTURE:**
```
// SOURCE: {file:lines}
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
- **MIRROR**: `{file:lines}` - follow existing pattern
- **IMPORTS**: {what to import}
- **GOTCHA**: {known issue to avoid}
- **VALIDATE**: `{validation command}`

### Task 2: {Description}

{Continue for all tasks...}

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

**For .NET/C#:**
```bash
dotnet build
dotnet format --verify-no-changes
```

**For Python:**
```bash
ruff check . && mypy .
```

**For TypeScript/React:**
```bash
npm run lint && npm run type-check
```

### Level 2: UNIT_TESTS

**For .NET/C#:**
```bash
dotnet test --filter "Category=Unit"
```

**For Python:**
```bash
pytest tests/unit -v
```

**For TypeScript/React:**
```bash
npm test -- --coverage
```

### Level 3: FULL_SUITE

**For .NET/C#:**
```bash
dotnet test && dotnet build --configuration Release
```

**For Python:**
```bash
pytest && python -m build
```

**For TypeScript/React:**
```bash
npm test && npm run build
```

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
```

---

## Phase 7: OUTPUT - Report to User

After generating, report:

```markdown
## Plan Created

**File**: `PRPs/plans/{feature-name}.plan.md`

**Summary**: {2-3 sentence feature overview}

**Complexity**: {LOW/MEDIUM/HIGH} - {brief rationale}

**Scope**:
- {N} files to CREATE
- {M} files to UPDATE
- {K} total tasks

**Key Patterns Discovered**:
- {Pattern 1 with file:line}
- {Pattern 2 with file:line}

**UX Transformation**:
- BEFORE: {one-line current state}
- AFTER: {one-line new state}

**Risks**:
- {Primary risk}: {mitigation}

**Confidence Score**: {1-10}/10 for one-pass implementation success
- {Rationale for score}

**Next Step**: Run `#prp-implement PRPs/plans/{feature-name}.plan.md`
```

---

## Verification Checklist

Before saving plan:

- [ ] All patterns from exploration documented with file:line references
- [ ] Every task has at least one executable validation command
- [ ] Tasks ordered by dependency (can execute top-to-bottom)
- [ ] Each task is atomic and independently testable
- [ ] No placeholders - all content is specific and actionable
- [ ] Pattern references include actual code snippets

---

## Success Criteria

- **CONTEXT_COMPLETE**: All patterns, gotchas, integration points documented
- **IMPLEMENTATION_READY**: Tasks executable without questions or clarification
- **PATTERN_FAITHFUL**: Every new file mirrors existing codebase style
- **VALIDATION_DEFINED**: Every task has executable verification command
- **UX_DOCUMENTED**: Before/After transformation is visually clear
- **ONE_PASS_TARGET**: Confidence score 8+ indicates high likelihood of first-attempt success
