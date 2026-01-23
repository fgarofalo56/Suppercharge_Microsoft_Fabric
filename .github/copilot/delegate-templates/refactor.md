---
name: Refactoring
description: Template for delegating refactoring tasks to Copilot coding agent
---

# Refactoring Task

## Refactoring Objective
<!-- What improvement we're making -->
[Describe the refactoring goal]

## Current State
<!-- What exists now and its problems -->

**Current Implementation:**
```typescript
// Example of current code
```

**Problems with Current State:**
- [Problem 1: e.g., code duplication]
- [Problem 2: e.g., poor readability]
- [Problem 3: e.g., tight coupling]

## Desired State
<!-- What we want after refactoring -->

**Target Implementation:**
```typescript
// Example of desired code structure
```

**Benefits:**
- [Benefit 1: e.g., reduced duplication]
- [Benefit 2: e.g., improved readability]
- [Benefit 3: e.g., better testability]

## Refactoring Type
<!-- Check applicable types -->
- [ ] Extract method/function
- [ ] Extract class/module
- [ ] Rename for clarity
- [ ] Simplify conditionals
- [ ] Remove duplication (DRY)
- [ ] Introduce design pattern
- [ ] Improve type safety
- [ ] Other: [describe]

## Files to Refactor
<!-- List files and expected changes -->
| File | Current Issue | Refactoring Needed |
|------|---------------|-------------------|
| `path/to/file1.ts` | [Issue] | [Change] |
| `path/to/file2.ts` | [Issue] | [Change] |

## Scope Boundaries
<!-- What to change and what NOT to change -->

**In Scope:**
- [File/module 1]
- [File/module 2]

**Out of Scope:**
- [File/module that should not change]
- [Functionality to preserve as-is]

## Acceptance Criteria
<!-- How to verify refactoring is successful -->
- [ ] All existing tests pass without modification
- [ ] No change in external behavior
- [ ] Code smell addressed
- [ ] No new warnings or errors
- [ ] Improved code metrics (if measurable)

## Testing Requirements
- [ ] Run all existing tests
- [ ] Add tests if refactoring reveals untested code
- [ ] Verify no regression in functionality

## Constraints
<!-- Important limitations -->
- **Must preserve**: All existing functionality
- **Must not break**: Public API, external contracts
- **Time constraint**: Keep changes minimal and focused
- **Do not**: Change unrelated code

## Verification Steps
<!-- How to confirm the refactoring worked -->
1. Run test suite: `npm test`
2. Check for regressions: [specific checks]
3. Verify improved metrics: [if applicable]

## Rollback Plan
<!-- If something goes wrong -->
Refactoring should be atomic and easily revertible.
If issues found, revert the PR entirely.

---

**Labels:** `copilot-delegate`, `type:refactor`
