---
mode: agent
description: "Execute fix from investigation artifact with validation"
tools: ["filesystem", "terminal", "changes", "githubRepo"]
---

# PRP Issue Fix

**Issue Number**: {{ input }}

---

## Your Mission

Execute the fix documented in the investigation artifact with rigorous validation.

**Core Principle**: Follow the investigation, validate thoroughly, don't introduce new issues.

---

## Phase 1: LOAD - Read Investigation

### 1.1 Find Investigation Artifact

```
PRPs/issues/{issue-number}-investigation.md
```

If not found:
```
Error: No investigation found for issue #{number}

Run: #prp-issue-investigate {number}
```

### 1.2 Extract Fix Details

From the investigation artifact, extract:
- Root cause location
- Solution design
- Files to change
- Implementation steps
- Testing strategy

---

## Phase 2: PREPARE - Setup Branch

### 2.1 Create Fix Branch

```bash
git checkout main
git pull origin main
git checkout -b fix/issue-{number}-{short-description}
```

### 2.2 Verify Clean State

```bash
git status --porcelain
```

Must be clean before starting.

---

## Phase 3: IMPLEMENT - Execute Fix

### 3.1 Follow Investigation Steps

Execute each implementation step from the investigation:

1. Read the current problematic code
2. Apply the "After" code from the fix design
3. Validate immediately after each change

### 3.2 Validate Each Change

After each file modification:

**.NET/C#:**
```bash
dotnet build
```

**Python:**
```bash
ruff check {file} && mypy {file}
```

**TypeScript/React:**
```bash
npm run type-check
```

### 3.3 Track Progress

```
Step 1: Update {file} ✅
Step 2: Add {file} ✅
Step 3: Update {tests} ✅
```

---

## Phase 4: TEST - Verify Fix

### 4.1 Reproduction Test

Run the reproduction steps from the investigation.

**Before Fix**: Issue should be reproducible (if not already fixed)
**After Fix**: Issue should be resolved

### 4.2 Verification Test

Run the verification test from the investigation.

### 4.3 Regression Tests

Run existing test suite:

**.NET/C#:**
```bash
dotnet test
```

**Python:**
```bash
pytest -v
```

**TypeScript/React:**
```bash
npm test
```

**All tests must pass.**

### 4.4 Add New Test (if needed)

If the investigation identified a missing test:
1. Create the test
2. Verify it catches the original bug
3. Verify it passes with the fix

---

## Phase 5: DOCUMENT - Create Fix Report

### 5.1 Update Investigation Artifact

Add fix completion status to the investigation file:

```markdown
---

## Fix Implementation

**Status**: Complete
**Branch**: `fix/issue-{number}-{description}`
**Date**: {YYYY-MM-DD}

### Changes Made

| File | Change | Verification |
|------|--------|--------------|
| `{path}` | {description} | ✅ Build passes |
| `{path}` | {description} | ✅ Tests pass |

### Test Results

| Test | Result |
|------|--------|
| Reproduction | ✅ Fixed |
| Verification | ✅ Passes |
| Regression | ✅ All pass |

### New Tests Added

- `{test file}`: {test description}
```

### 5.2 Archive Investigation

```bash
mkdir -p PRPs/issues/completed
mv PRPs/issues/{number}-investigation.md PRPs/issues/completed/
```

---

## Phase 6: COMMIT - Prepare for PR

### 6.1 Stage Changes

```bash
git add -A
```

### 6.2 Create Commit

```bash
git commit -m "fix: {short description} (fixes #{number})

- Root cause: {brief explanation}
- Solution: {what was changed}
- Tests: {added/updated}"
```

### 6.3 Push Branch

```bash
git push -u origin fix/issue-{number}-{description}
```

---

## Phase 7: OUTPUT - Report to User

```markdown
## Fix Complete

**Issue**: #{number}
**Branch**: `fix/issue-{number}-{description}`
**Status**: ✅ Ready for PR

### Summary

{One sentence describing the fix}

### Changes

| File | Change |
|------|--------|
| `{path}` | {description} |

### Validation

| Check | Result |
|-------|--------|
| Build | ✅ |
| Tests | ✅ ({N} passed) |
| Reproduction | ✅ Fixed |

### Artifacts

- Investigation: `PRPs/issues/completed/{number}-investigation.md`

### Next Steps

1. Create PR: `#pr-create`
2. Link to issue #{number}
3. Request review
4. Merge when approved

### PR Description Template

```markdown
## Summary

Fixes #{number}

### Root Cause

{Brief explanation from investigation}

### Changes

- {Change 1}
- {Change 2}

### Testing

- [x] Reproduction verified
- [x] Fix verified
- [x] Regression tests pass
- [x] New test added (if applicable)
```
```

---

## Handling Issues

### Build Fails

1. Check error message
2. Fix the issue
3. Re-run build
4. Don't proceed until clean

### Tests Fail

1. Check if related to fix or pre-existing
2. If related to fix, review the change
3. If pre-existing, document but don't fix (out of scope)
4. Ensure fix doesn't introduce new failures

### Fix Doesn't Work

1. Review investigation analysis
2. Check if root cause was correct
3. If not, re-run investigation
4. If yes, refine the solution approach

---

## Success Criteria

- **INVESTIGATION_FOLLOWED**: Fix matches the documented solution
- **BUILD_PASSES**: No compilation errors
- **TESTS_PASS**: All tests green (including new ones)
- **ISSUE_RESOLVED**: Original problem no longer reproducible
- **NO_REGRESSIONS**: Existing functionality preserved
- **BRANCH_PUSHED**: Ready for PR
