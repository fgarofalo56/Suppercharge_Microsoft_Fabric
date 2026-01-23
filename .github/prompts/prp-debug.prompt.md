---
mode: agent
description: "Deep root cause analysis with 5 Whys methodology"
tools: ["filesystem", "terminal", "changes"]
---

# PRP Debug - Root Cause Analysis

**Problem**: {{ input }}

---

## Your Mission

Perform deep root cause analysis using the 5 Whys methodology. Don't just find what's broken - find WHY it's broken.

**Core Principle**: Symptoms lie, root causes tell the truth. Keep asking "why" until you hit the fundamental issue.

---

## Phase 1: DEFINE - Understand the Problem

### 1.1 Capture the Observable Problem

```markdown
**Observable Symptom**:
{What the user sees/experiences}

**Expected Behavior**:
{What should happen instead}

**When It Occurs**:
{Conditions, triggers, frequency}

**Impact**:
{Who/what is affected}
```

### 1.2 Gather Evidence

- Error messages (exact text)
- Stack traces
- Log entries
- User reports
- Reproduction steps

---

## Phase 2: INVESTIGATE - Trace the Failure

### 2.1 Locate the Failure Point

Search codebase for:
- Error messages
- Function names from stack traces
- Variables or values mentioned
- Related functionality

### 2.2 Trace the Flow

Map the execution path:

```
Input → [Step 1] → [Step 2] → [FAILURE HERE] → Expected Output
                              ↓
                        Actual Output (wrong)
```

### 2.3 Identify the Gap

What's different between expected and actual?

---

## Phase 3: ANALYZE - Apply 5 Whys

### 3.1 Structured Analysis

```markdown
## 5 Whys Analysis

**Problem Statement**: {Observable symptom in one sentence}

---

### Why 1: Why does {symptom} occur?

**Answer**: {First-level cause}

**Evidence**:
- File: `{path}:{lines}`
- Observation: {what the code shows}

---

### Why 2: Why does {cause 1} happen?

**Answer**: {Second-level cause}

**Evidence**:
- File: `{path}:{lines}`
- Observation: {what leads to cause 1}

---

### Why 3: Why does {cause 2} happen?

**Answer**: {Third-level cause}

**Evidence**:
- File: `{path}:{lines}`
- Observation: {what leads to cause 2}

---

### Why 4: Why does {cause 3} happen?

**Answer**: {Fourth-level cause}

**Evidence**:
- File: `{path}:{lines}`
- Observation: {what leads to cause 3}

---

### Why 5: Why does {cause 4} happen?

**Answer**: {FUNDAMENTAL ROOT CAUSE}

**Evidence**:
- File: `{path}:{lines}`
- Observation: {the core issue}

---

## Root Cause Identified

{Clear statement of the fundamental issue}

**Category**: [Design Flaw | Implementation Bug | Configuration Error | External Dependency | Missing Validation | Race Condition | Data Corruption | Other]
```

### 3.2 Validate Root Cause

Ask yourself:
- If we fix this root cause, will the symptom go away?
- Is this the FUNDAMENTAL cause, or just another symptom?
- Could we have stopped earlier, or should we go deeper?

---

## Phase 4: DOCUMENT - Create Debug Report

**Output Path**: `PRPs/reports/{date}-debug-{slug}.md`

```markdown
# Debug Report: {Problem Title}

**Date**: {YYYY-MM-DD}
**Status**: Root Cause Identified

---

## Problem Summary

**Symptom**: {Observable problem}
**Impact**: {Who/what affected}
**Severity**: Critical / High / Medium / Low

---

## Evidence Collected

| Type | Content | Source |
|------|---------|--------|
| Error | {message} | {log/console} |
| Stack Trace | {trace} | {source} |
| User Report | {description} | {reporter} |

---

## Execution Flow

```
[Start] → [Step 1: {desc}] → [Step 2: {desc}] → [FAILURE: {desc}] → [Wrong Output]
   │              │                   │                │
   │              │                   │                └─ {file:line}
   │              │                   └─ {file:line}
   │              └─ {file:line}
   └─ {file:line}
```

---

## 5 Whys Analysis

{Full 5 Whys from Phase 3}

---

## Root Cause

**Statement**: {Clear, specific root cause}

**Location**: `{file}:{lines}`

**Code**:
```
{The problematic code}
```

**Explanation**:
{Why this code causes the problem}

---

## Contributing Factors

- {Factor 1}: {how it contributed}
- {Factor 2}: {how it contributed}

---

## Recommended Fix

### Option A: {Approach Name}
{Description}

**Pros**: {benefits}
**Cons**: {drawbacks}
**Effort**: Low / Medium / High

### Option B: {Approach Name}
{Description}

**Pros**: {benefits}
**Cons**: {drawbacks}
**Effort**: Low / Medium / High

### Recommendation

{Which option and why}

---

## Prevention

To prevent similar issues:

- [ ] {Prevention measure 1}
- [ ] {Prevention measure 2}
- [ ] {Test to add}

---

*Analyzed: {timestamp}*
```

---

## Phase 5: OUTPUT - Summary

```markdown
## Debug Analysis Complete

**Problem**: {One-line symptom}
**Root Cause**: {One-line root cause}
**Location**: `{file}:{lines}`

### 5 Whys Summary

1. {Symptom} → because
2. {Cause 1} → because
3. {Cause 2} → because
4. {Cause 3} → because
5. {Cause 4} → **ROOT CAUSE**: {fundamental issue}

### Recommended Fix

{Brief description of recommended approach}

### Artifacts

- Debug Report: `PRPs/reports/{date}-debug-{slug}.md`

### Next Steps

1. Review the analysis
2. Create implementation plan: `#prp-plan "fix {problem}"`
3. Implement and validate
```

---

## Common Root Cause Categories

| Category | Example | Typical Fix |
|----------|---------|-------------|
| **Design Flaw** | Wrong abstraction | Refactor architecture |
| **Implementation Bug** | Off-by-one error | Fix the logic |
| **Missing Validation** | No null check | Add validation |
| **Race Condition** | Concurrent access | Add synchronization |
| **Configuration Error** | Wrong setting | Fix config |
| **External Dependency** | API changed | Update integration |
| **Data Corruption** | Invalid state | Add constraints |
| **Missing Test** | Untested edge case | Add test coverage |

---

## Tips for Effective 5 Whys

1. **Stay specific** - Avoid vague answers like "it's buggy"
2. **Use evidence** - Every "why" should have supporting code/logs
3. **Go deep enough** - Stop when you hit something actionable
4. **Don't go too deep** - "Why does the language work that way" is too far
5. **Consider multiple paths** - Sometimes there are parallel causes

---

## Success Criteria

- **SYMPTOM_CLEAR**: Observable problem well-defined
- **EVIDENCE_GATHERED**: Logs, traces, reproduction steps collected
- **5_WHYS_COMPLETE**: Each level has evidence and file references
- **ROOT_CAUSE_ACTIONABLE**: Can actually fix the identified cause
- **FIX_IDENTIFIED**: Clear path to resolution
- **REPORT_CREATED**: Debug report saved for reference
