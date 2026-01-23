---
name: speckit.analyze
description: Perform non-destructive cross-artifact consistency and quality analysis across spec.md, plan.md, and tasks.md after task generation.
mode: agent
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

Identify inconsistencies, duplications, ambiguities, and underspecified items across the three core artifacts (`spec.md`, `plan.md`, `tasks.md`) before implementation.

**STRICTLY READ-ONLY**: Do NOT modify any files. Output a structured analysis report.

## Execution Flow

### 1. Initialize Analysis Context

Run prerequisite check:

```powershell
# PowerShell
.specify/scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks

# Bash
.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
```

Parse JSON for `FEATURE_DIR` and `AVAILABLE_DOCS`. Derive paths:
- SPEC = FEATURE_DIR/spec.md
- PLAN = FEATURE_DIR/plan.md
- TASKS = FEATURE_DIR/tasks.md

Abort with error if any required file is missing.

### 2. Load Artifacts

**From spec.md**:
- Overview/Context
- Functional Requirements
- Non-Functional Requirements
- User Stories
- Edge Cases

**From plan.md**:
- Architecture/stack choices
- Data Model references
- Phases
- Technical constraints

**From tasks.md**:
- Task IDs
- Descriptions
- Phase grouping
- Parallel markers [P]
- Referenced file paths

**From constitution**:
- Load `.specify/memory/constitution.md`
- Extract principle names and MUST/SHOULD statements

### 3. Build Semantic Models

Create internal representations:
- **Requirements inventory**: Each requirement with stable key
- **User story/action inventory**: Actions with acceptance criteria
- **Task coverage mapping**: Map each task to requirements/stories
- **Constitution rule set**: Principle names and normative statements

### 4. Detection Passes

Focus on high-signal findings. Limit to 50 findings total.

#### A. Duplication Detection
- Identify near-duplicate requirements
- Mark lower-quality phrasing for consolidation

#### B. Ambiguity Detection
- Flag vague adjectives (fast, scalable, secure, intuitive, robust) lacking measurable criteria
- Flag unresolved placeholders (TODO, TKTK, ???, `<placeholder>`)

#### C. Underspecification
- Requirements with verbs but missing object or measurable outcome
- User stories missing acceptance criteria alignment
- Tasks referencing files/components not defined in spec/plan

#### D. Constitution Alignment
- Any requirement or plan element conflicting with MUST principle
- Missing mandated sections or quality gates

#### E. Coverage Gaps
- Requirements with zero associated tasks
- Tasks with no mapped requirement/story
- Non-functional requirements not reflected in tasks

#### F. Inconsistency
- Terminology drift (same concept named differently)
- Data entities in plan but absent in spec (or vice versa)
- Task ordering contradictions
- Conflicting requirements

### 5. Severity Assignment

| Severity | Criteria |
|----------|----------|
| **CRITICAL** | Violates constitution MUST, missing core artifact, requirement with zero coverage blocking baseline |
| **HIGH** | Duplicate/conflicting requirement, ambiguous security/performance, untestable acceptance criterion |
| **MEDIUM** | Terminology drift, missing non-functional coverage, underspecified edge case |
| **LOW** | Style/wording improvements, minor redundancy |

### 6. Produce Analysis Report

```markdown
# Specification Analysis Report

## Findings

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| A1 | Duplication | HIGH | spec.md:L120 | Two similar requirements... | Merge phrasing |
| B1 | Ambiguity | MEDIUM | spec.md:L45 | "Fast" not quantified | Add metric |
| ... | ... | ... | ... | ... | ... |

## Coverage Summary

| Requirement Key | Has Task? | Task IDs | Notes |
|-----------------|-----------|----------|-------|
| user-can-login | ✓ | T012, T013 | |
| user-can-export | ✗ | - | No coverage |

## Constitution Alignment Issues

[List any CRITICAL violations]

## Unmapped Tasks

[Tasks with no requirement/story mapping]

## Metrics

- **Total Requirements**: X
- **Total Tasks**: X
- **Coverage %**: X% (requirements with ≥1 task)
- **Ambiguity Count**: X
- **Duplication Count**: X
- **Critical Issues**: X
```

### 7. Provide Next Actions

At end of report:

```markdown
## Next Actions

### If CRITICAL Issues Exist
⚠️ Recommend resolving before `/speckit.implement`:
- [Specific actions for each critical issue]

### If Only LOW/MEDIUM Issues
✓ May proceed to `/speckit.implement` with:
- [Improvement suggestions]

### Recommended Commands
- Run `/speckit.specify` with refinement for scope issues
- Run `/speckit.plan` to adjust architecture
- Edit tasks.md manually for coverage gaps
```

### 8. Offer Remediation

Ask: "Would you like me to suggest concrete remediation edits for the top N issues?" (Do NOT apply automatically)

## Operating Principles

### Context Efficiency
- Minimal high-signal tokens
- Progressive disclosure: load incrementally
- Token-efficient output: limit to 50 rows
- Deterministic results: consistent IDs

### Analysis Guidelines
- **NEVER modify files** (read-only)
- **NEVER hallucinate missing sections**
- **Prioritize constitution violations** (always CRITICAL)
- **Use examples over exhaustive rules**
- **Report zero issues gracefully** (emit success with stats)
