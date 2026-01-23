---
mode: agent
description: "Execute an implementation plan with rigorous validation loops"
tools: ["filesystem", "terminal", "changes", "githubRepo"]
---

# PRP Plan Implementation

**Plan Path**: {{ input }}

---

## Your Mission

Execute the plan end-to-end with rigorous self-validation. You are autonomous.

**Core Philosophy**: Validation loops catch mistakes early. Run checks after every change. Fix issues immediately. The goal is a working implementation, not just code that exists.

**Golden Rule**: If a validation fails, fix it before moving on. Never accumulate broken state.

---

## Phase 0: DETECT - Project Environment

### 0.1 Identify Project Type

Check for these files to determine the project's toolchain:

| File Found | Project Type | Validation Commands |
|------------|--------------|---------------------|
| `*.csproj`, `*.sln` | .NET/C# | `dotnet build`, `dotnet test` |
| `pyproject.toml` | Python | `ruff check`, `mypy .`, `pytest` |
| `package.json` | Node.js | `npm run lint`, `npm test`, `npm run build` |
| `Cargo.toml` | Rust | `cargo check`, `cargo test` |
| `go.mod` | Go | `go build ./...`, `go test ./...` |

### 0.2 Store Detected Commands

Note the validation commands to use throughout implementation.

---

## Phase 1: LOAD - Read the Plan

### 1.1 Load Plan File

Read the plan file from the input path.

### 1.2 Extract Key Sections

Locate and understand:

- **Summary** - What we're building
- **Patterns to Mirror** - Code to copy from
- **Files to Change** - CREATE/UPDATE list
- **Step-by-Step Tasks** - Implementation order
- **Validation Commands** - How to verify
- **Acceptance Criteria** - Definition of done

### 1.3 Validate Plan Exists

**If plan not found:**

```
Error: Plan not found at {path}

Create a plan first: #prp-plan "feature description"
```

**PHASE_1_CHECKPOINT:**

- [ ] Plan file loaded
- [ ] Key sections identified
- [ ] Tasks list extracted

---

## Phase 2: PREPARE - Git State

### 2.1 Check Current State

```bash
git branch --show-current
git status --porcelain
```

### 2.2 Branch Decision

| Current State | Action |
|---------------|--------|
| On main, clean | Create branch: `git checkout -b feature/{plan-slug}` |
| On main, dirty | STOP: "Stash or commit changes first" |
| On feature branch | Use it (log: "Using existing branch") |

### 2.3 Sync with Remote

```bash
git fetch origin
git pull --rebase origin main 2>/dev/null || true
```

**PHASE_2_CHECKPOINT:**

- [ ] On correct branch (not main with uncommitted work)
- [ ] Working directory ready
- [ ] Up to date with remote

---

## Phase 3: EXECUTE - Implement Tasks

**For each task in the plan's Step-by-Step Tasks section:**

### 3.1 Read Context

1. Read the **MIRROR** file reference from the task
2. Understand the pattern to follow
3. Read any **IMPORTS** specified

### 3.2 Implement

1. Make the change exactly as specified
2. Follow the pattern from MIRROR reference
3. Handle any **GOTCHA** warnings

### 3.3 Validate Immediately

**After EVERY file change, run the appropriate validation:**

**.NET/C#:**
```bash
dotnet build
```

**Python:**
```bash
ruff check {changed_file} && mypy {changed_file}
```

**TypeScript/React:**
```bash
npm run type-check
```

**If validation fails:**

1. Read the error
2. Fix the issue
3. Re-run validation
4. Only proceed when passing

### 3.4 Track Progress

Log each task as you complete it:

```
Task 1: CREATE src/features/x/models.ts ✅
Task 2: CREATE src/features/x/service.ts ✅
Task 3: UPDATE src/routes/index.ts ✅
```

**Deviation Handling:**
If you must deviate from the plan:

- Note WHAT changed
- Note WHY it changed
- Continue with the deviation documented

**PHASE_3_CHECKPOINT:**

- [ ] All tasks executed in order
- [ ] Each task passed validation
- [ ] Deviations documented

---

## Phase 4: VALIDATE - Full Verification

### 4.1 Static Analysis

**.NET/C#:**
```bash
dotnet build
dotnet format --verify-no-changes
```

**Python:**
```bash
ruff check . && mypy .
```

**TypeScript/React:**
```bash
npm run lint && npm run type-check
```

**Must pass with zero errors.**

### 4.2 Unit Tests

**You MUST write or update tests for new code.** This is not optional.

**Test requirements:**

1. Every new function/feature needs at least one test
2. Edge cases identified in the plan need tests
3. Update existing tests if behavior changed

**Run tests:**

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

**If tests fail:**

1. Read failure output
2. Determine: bug in implementation or bug in test?
3. Fix the actual issue
4. Re-run tests
5. Repeat until green

### 4.3 Build Check

**.NET/C#:**
```bash
dotnet build --configuration Release
```

**Python:**
```bash
python -m build
```

**TypeScript/React:**
```bash
npm run build
```

**Must complete without errors.**

### 4.4 Edge Case Testing

Run any edge case tests specified in the plan.

**PHASE_4_CHECKPOINT:**

- [ ] Static analysis passes
- [ ] Lint passes (0 errors)
- [ ] Tests pass (all green)
- [ ] Build succeeds

---

## Phase 5: REPORT - Create Implementation Report

### 5.1 Create Report Directory

```bash
mkdir -p PRPs/reports
```

### 5.2 Generate Report

**Path**: `PRPs/reports/{plan-name}-report.md`

```markdown
# Implementation Report

**Plan**: `{plan-path}`
**Branch**: `{branch-name}`
**Date**: {YYYY-MM-DD}
**Status**: {COMPLETE | PARTIAL}

---

## Summary

{Brief description of what was implemented}

---

## Assessment vs Reality

| Metric | Predicted | Actual | Reasoning |
|--------|-----------|--------|-----------|
| Complexity | {from plan} | {actual} | {Why it matched or differed} |
| Confidence | {from plan} | {actual} | {What we learned} |

---

## Tasks Completed

| # | Task | File | Status |
|---|------|------|--------|
| 1 | {task description} | `src/x.ts` | ✅ |
| 2 | {task description} | `src/y.ts` | ✅ |

---

## Validation Results

| Check | Result | Details |
|-------|--------|---------|
| Build | ✅ | No errors |
| Lint | ✅ | 0 errors |
| Unit tests | ✅ | X passed, 0 failed |
| Integration | ✅/⏭️ | {result or "N/A"} |

---

## Files Changed

| File | Action | Lines |
|------|--------|-------|
| `src/x.ts` | CREATE | +{N} |
| `src/y.ts` | UPDATE | +{N}/-{M} |

---

## Deviations from Plan

{List any deviations with rationale, or "None"}

---

## Issues Encountered

{List any issues and how they were resolved, or "None"}

---

## Tests Written

| Test File | Test Cases |
|-----------|------------|
| `src/x.test.ts` | {list of test functions} |

---

## Next Steps

- [ ] Review implementation
- [ ] Create PR: `#pr-create`
- [ ] Merge when approved
```

### 5.3 Update Source PRD (if applicable)

If the plan was generated from a PRD:

1. Read the PRD file
2. Find the phase in the Implementation Phases table
3. Update Status from `in-progress` to `complete`
4. Save the PRD

### 5.4 Archive Plan

```bash
mkdir -p PRPs/plans/completed
mv {plan-path} PRPs/plans/completed/
```

**PHASE_5_CHECKPOINT:**

- [ ] Report created at `PRPs/reports/`
- [ ] PRD updated (if applicable)
- [ ] Plan moved to completed folder

---

## Phase 6: OUTPUT - Report to User

```markdown
## Implementation Complete

**Plan**: `{plan-path}`
**Branch**: `{branch-name}`
**Status**: ✅ Complete

### Validation Summary

| Check | Result |
|-------|--------|
| Build | ✅ |
| Lint | ✅ |
| Tests | ✅ ({N} passed) |

### Files Changed

- {N} files created
- {M} files updated
- {K} tests written

### Deviations

{If none: "Implementation matched the plan."}
{If any: Brief summary of what changed and why}

### Artifacts

- Report: `PRPs/reports/{name}-report.md`
- Plan archived to: `PRPs/plans/completed/`

### Next Steps

1. Review the report
2. Create PR: `#pr-create`
3. Merge when approved
```

---

## Handling Failures

### Build Fails

1. Read error message carefully
2. Fix the issue
3. Re-run build
4. Don't proceed until passing

### Tests Fail

1. Identify which test failed
2. Determine: implementation bug or test bug?
3. Fix the root cause
4. Re-run tests
5. Repeat until green

### Lint Fails

1. Run auto-fix if available
2. Manually fix remaining issues
3. Re-run lint
4. Proceed when clean

---

## Success Criteria

- **TASKS_COMPLETE**: All plan tasks executed
- **BUILD_PASS**: Build command exits 0
- **LINT_PASS**: Lint command exits 0
- **TESTS_PASS**: All tests green
- **REPORT_CREATED**: Implementation report exists
- **PLAN_ARCHIVED**: Original plan moved to completed
