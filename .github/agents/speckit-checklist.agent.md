---
name: speckit.checklist
description: Generate a custom requirements quality checklist ("unit tests for English") to validate specification completeness, clarity, and consistency.
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

## Purpose: Unit Tests for English

Checklists are **UNIT TESTS FOR REQUIREMENTS WRITING** - they validate the quality, clarity, and completeness of requirements in a given domain.

**NOT for verification/testing**:
- ❌ NOT "Verify the button clicks correctly"
- ❌ NOT "Test error handling works"
- ❌ NOT "Confirm the API returns 200"

**FOR requirements quality validation**:
- ✅ "Are visual hierarchy requirements defined for all card types?" (completeness)
- ✅ "Is 'prominent display' quantified with specific sizing?" (clarity)
- ✅ "Are hover state requirements consistent across elements?" (consistency)
- ✅ "Are accessibility requirements defined for keyboard navigation?" (coverage)

**Metaphor**: If your spec is code written in English, the checklist is its unit test suite.

## Execution Flow

### 1. Setup

Run prerequisite check:

```powershell
# PowerShell
.specify/scripts/powershell/check-prerequisites.ps1 -Json

# Bash
.specify/scripts/bash/check-prerequisites.sh --json
```

Parse JSON for `FEATURE_DIR` and `AVAILABLE_DOCS`.

### 2. Clarify Intent

Derive up to THREE contextual clarifying questions based on user input:

1. **Scope refinement**: "Should this include integration touchpoints or stay limited to local module?"
2. **Risk prioritization**: "Which risk areas should receive mandatory gating checks?"
3. **Depth calibration**: "Lightweight pre-commit sanity list or formal release gate?"
4. **Audience framing**: "Used by author only or peers during PR review?"

Present questions with option tables when applicable.

### 3. Understand Request

Combine `$ARGUMENTS` + clarifying answers:
- Derive checklist theme (security, review, deploy, ux, api, performance)
- Consolidate must-have items mentioned by user
- Map focus selections to categories
- Infer missing context from spec/plan/tasks

### 4. Load Feature Context

Read from FEATURE_DIR:
- spec.md: Feature requirements and scope
- plan.md (if exists): Technical details
- tasks.md (if exists): Implementation tasks

### 5. Generate Checklist

Create `FEATURE_DIR/checklists/[domain].md` (e.g., `ux.md`, `api.md`, `security.md`)

#### Category Structure

Group items by requirement quality dimensions:
- **Requirement Completeness**: Are all necessary requirements documented?
- **Requirement Clarity**: Are requirements specific and unambiguous?
- **Requirement Consistency**: Do requirements align without conflicts?
- **Acceptance Criteria Quality**: Are success criteria measurable?
- **Scenario Coverage**: Are all flows/cases addressed?
- **Edge Case Coverage**: Are boundary conditions defined?
- **Non-Functional Requirements**: Performance, Security, Accessibility specified?
- **Dependencies & Assumptions**: Are they documented and validated?
- **Ambiguities & Conflicts**: What needs clarification?

#### Item Structure

Each item follows this pattern:

```markdown
- [ ] CHK001 - [Question about requirement quality] [Quality Dimension, Reference]
```

**Examples by Quality Dimension**:

**Completeness**:
- `- [ ] CHK001 - Are error handling requirements defined for all API failure modes? [Completeness, Gap]`
- `- [ ] CHK002 - Are accessibility requirements specified for all interactive elements? [Completeness]`

**Clarity**:
- `- [ ] CHK003 - Is 'fast loading' quantified with specific timing thresholds? [Clarity, Spec §NFR-2]`
- `- [ ] CHK004 - Are 'related episodes' selection criteria explicitly defined? [Clarity, Spec §FR-5]`

**Consistency**:
- `- [ ] CHK005 - Do navigation requirements align across all pages? [Consistency, Spec §FR-10]`
- `- [ ] CHK006 - Are card components consistent between pages? [Consistency]`

**Coverage**:
- `- [ ] CHK007 - Are requirements defined for zero-state scenarios? [Coverage, Edge Case]`
- `- [ ] CHK008 - Are concurrent user scenarios addressed? [Coverage, Gap]`

**Measurability**:
- `- [ ] CHK009 - Are visual hierarchy requirements measurable? [Measurability, Spec §FR-1]`
- `- [ ] CHK010 - Can 'balanced visual weight' be objectively verified? [Measurability]`

#### Traceability

- ≥80% of items MUST include traceability reference
- Use: `[Spec §X.Y]`, `[Gap]`, `[Ambiguity]`, `[Conflict]`, `[Assumption]`

### 🚫 PROHIBITED Patterns

These make it an implementation test, not requirements test:
- ❌ "Verify", "Test", "Confirm", "Check" + implementation behavior
- ❌ References to code execution, user actions, system behavior
- ❌ "Displays correctly", "works properly", "functions as expected"
- ❌ "Click", "navigate", "render", "load", "execute"

### ✅ REQUIRED Patterns

These test requirements quality:
- ✅ "Are [requirement type] defined/specified/documented for [scenario]?"
- ✅ "Is [vague term] quantified/clarified with specific criteria?"
- ✅ "Are requirements consistent between [section A] and [section B]?"
- ✅ "Can [requirement] be objectively measured/verified?"
- ✅ "Are [edge cases/scenarios] addressed in requirements?"
- ✅ "Does the spec define [missing aspect]?"

## Output Format

```markdown
# [Domain] Requirements Quality Checklist: [FEATURE NAME]

**Purpose**: Validate [domain] requirement quality for implementation readiness
**Created**: [DATE]
**Feature**: [Link to spec.md]
**Focus**: [Selected focus areas]
**Depth**: [Standard/Rigorous/Lightweight]

## Requirement Completeness

- [ ] CHK001 - [Question] [Quality, Reference]
- [ ] CHK002 - [Question] [Quality, Reference]

## Requirement Clarity

- [ ] CHK003 - [Question] [Quality, Reference]
...

## Scenario Coverage

...

## Edge Case Coverage

...

## Notes

- Items marked incomplete require spec updates before `/speckit.implement`
```

### 6. Report Completion

Output:
- Full path to created checklist
- Item count
- Focus areas selected
- Depth level
- Remind user each run creates a new file
