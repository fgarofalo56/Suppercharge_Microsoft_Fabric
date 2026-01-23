---
name: Bug Fix
description: Template for delegating bug fixes to Copilot coding agent
---

# Bug Fix Task

## Issue Reference
<!-- Link to the issue or bug report -->
Related to #[issue_number]

## Bug Description
<!-- What is happening vs what should happen -->

**Current Behavior:**
[Describe what is happening]

**Expected Behavior:**
[Describe what should happen]

**Steps to Reproduce:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Root Cause Analysis
<!-- If known, describe the cause -->
[The bug occurs because...]

## Affected Files
<!-- List files that likely need changes -->
- `path/to/file1.ts`
- `path/to/file2.ts`

## Fix Requirements
<!-- Specific requirements for the fix -->
- [ ] Fix the specific issue described
- [ ] Add test case that reproduces the bug
- [ ] Ensure test passes after fix
- [ ] No regression in related functionality

## Acceptance Criteria
<!-- How to verify the fix is complete -->
- [ ] Bug no longer occurs when following reproduction steps
- [ ] Existing tests still pass
- [ ] New test case added for this bug
- [ ] No new warnings or errors introduced

## Constraints
<!-- Any limitations on the fix -->
- Do not change public API signatures
- Maintain backward compatibility
- Keep fix minimal and focused

## Additional Context
<!-- Any other helpful information -->
- Error messages:
- Stack traces:
- Related code:

---

**Labels:** `copilot-delegate`, `type:bug`
