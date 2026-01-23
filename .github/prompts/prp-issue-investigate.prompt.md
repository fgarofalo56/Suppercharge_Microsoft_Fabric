---
mode: agent
description: "Investigate GitHub issue, analyze root cause, create implementation plan"
tools: ["filesystem", "terminal", "changes", "githubRepo"]
---

# PRP Issue Investigation

**Issue**: {{ input }}

---

## Your Mission

Analyze the GitHub issue thoroughly, identify root cause, and create a comprehensive implementation plan for the fix.

**Core Principle**: Understand before you fix. Root cause analysis prevents whack-a-mole debugging.

---

## Phase 1: LOAD - Gather Issue Context

### 1.1 Fetch Issue Details

Get the full issue content:
- Issue title and description
- Comments and discussion
- Labels and assignees
- Linked PRs or issues
- Reporter information

### 1.2 Extract Key Information

| Field | Value |
|-------|-------|
| Issue # | {number} |
| Title | {title} |
| Type | Bug / Feature / Enhancement |
| Reporter | {username} |
| Reproduction Steps | {if bug} |
| Expected Behavior | {description} |
| Actual Behavior | {description} |

### 1.3 Assess Severity

| Severity | Criteria |
|----------|----------|
| Critical | Production broken, data loss, security |
| High | Major feature broken, affects many users |
| Medium | Feature degraded, workaround exists |
| Low | Minor issue, cosmetic, edge case |

---

## Phase 2: INVESTIGATE - Root Cause Analysis

### 2.1 Locate Relevant Code

Search the codebase for:
- Files mentioned in the issue
- Functions or components referenced
- Error messages from stack traces
- Related functionality

### 2.2 Apply 5 Whys Methodology

```markdown
**Problem**: {Observable symptom}

**Why 1**: Why does this happen?
→ {First-level cause}

**Why 2**: Why does that happen?
→ {Second-level cause}

**Why 3**: Why does that happen?
→ {Third-level cause}

**Why 4**: Why does that happen?
→ {Fourth-level cause}

**Why 5**: Why does that happen?
→ {ROOT CAUSE identified}
```

### 2.3 Document Findings

| Finding | Evidence |
|---------|----------|
| Root Cause | {description with file:line} |
| Contributing Factors | {list} |
| Impact Scope | {what's affected} |
| Related Code | {file paths} |

---

## Phase 3: ANALYZE - Solution Design

### 3.1 Identify Solution Options

| Option | Approach | Pros | Cons |
|--------|----------|------|------|
| A | {description} | {benefits} | {drawbacks} |
| B | {description} | {benefits} | {drawbacks} |
| C | {description} | {benefits} | {drawbacks} |

### 3.2 Select Best Approach

**Chosen**: Option {X}

**Rationale**:
- {Why this approach}
- {Alignment with codebase patterns}
- {Risk assessment}

### 3.3 Scope the Fix

**In Scope**:
- {What will be fixed}
- {Files to change}

**Out of Scope**:
- {Related issues to address separately}
- {Nice-to-haves for later}

---

## Phase 4: PLAN - Create Investigation Artifact

**Output Path**: `PRPs/issues/{issue-number}-investigation.md`

```markdown
# Issue #{number} Investigation

## Issue Summary

| Field | Value |
|-------|-------|
| Issue | #{number} |
| Title | {title} |
| Type | Bug / Feature / Enhancement |
| Severity | Critical / High / Medium / Low |
| Reporter | {username} |

## Problem Description

{2-3 sentence summary of the issue}

## Reproduction Steps

1. {Step 1}
2. {Step 2}
3. {Step 3}

**Expected**: {what should happen}
**Actual**: {what happens instead}

---

## Root Cause Analysis

### 5 Whys

1. **Problem**: {symptom}
2. **Why**: {cause 1}
3. **Why**: {cause 2}
4. **Why**: {cause 3}
5. **Why**: {cause 4}
6. **Root Cause**: {fundamental issue}

### Technical Details

**Location**: `{file:lines}`

**Problem Code**:
```
{code snippet showing the issue}
```

**Root Cause Explanation**:
{Detailed technical explanation}

---

## Impact Analysis

| Area | Impact |
|------|--------|
| Users Affected | {scope} |
| Functionality | {what's broken} |
| Data | {any data implications} |
| Performance | {any performance implications} |

---

## Solution Design

### Approach

{Description of the fix approach}

### Files to Change

| File | Change Type | Description |
|------|-------------|-------------|
| `{path}` | UPDATE | {what changes} |
| `{path}` | CREATE | {new file purpose} |

### Implementation Steps

1. {Step with file reference}
2. {Step with validation}
3. {Step with testing}

### Fix Code

**Before**:
```
{current problematic code}
```

**After**:
```
{corrected code}
```

---

## Testing Strategy

### Reproduction Test

```
{Command or steps to reproduce}
```

### Verification Test

```
{Command or steps to verify fix}
```

### Regression Tests

- [ ] {Existing test that should still pass}
- [ ] {New test to prevent regression}

---

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| {risk} | H/M/L | {how to handle} |

---

## Recommendation

**Confidence**: {1-10}/10

{Summary of recommended approach and next steps}

---

*Investigated: {timestamp}*
*Investigator: GitHub Copilot*
```

---

## Phase 5: OUTPUT - Summary

```markdown
## Investigation Complete

**Issue**: #{number} - {title}
**Severity**: {level}
**Root Cause**: {one-line summary}

### Key Findings

- **Problem**: {symptom}
- **Root Cause**: {file:line} - {brief explanation}
- **Impact**: {scope of affected users/functionality}

### Recommended Fix

{2-3 sentence summary of the solution}

### Affected Files

- `{file1}` - {change type}
- `{file2}` - {change type}

### Confidence

{1-10}/10 - {rationale}

### Artifacts

- Investigation: `PRPs/issues/{number}-investigation.md`

### Next Steps

1. Review investigation findings
2. Run: `#prp-issue-fix {number}` to implement the fix
```

---

## Success Criteria

- **ISSUE_UNDERSTOOD**: Clear understanding of the problem
- **ROOT_CAUSE_FOUND**: Fundamental cause identified, not just symptoms
- **SOLUTION_DESIGNED**: Clear fix approach documented
- **FILES_IDENTIFIED**: All affected files listed
- **TESTS_PLANNED**: Verification strategy defined
- **ARTIFACT_CREATED**: Investigation document saved
