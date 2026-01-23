---
name: speckit.constitution
description: Create or update the project constitution with governing principles and development guidelines for Spec-Driven Development.
mode: agent
tools:
  - filesystem
  - terminal
handoffs:
  - label: Build Specification
    agent: speckit.specify
    prompt: Implement the feature specification based on the updated constitution. I want to build...
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

Create or update the project constitution at `.specify/memory/constitution.md`. This file establishes governing principles and development guidelines that guide all subsequent development phases in the Spec-Driven Development workflow.

## Execution Flow

### 1. Load Existing Constitution

Load the existing constitution template at `.specify/memory/constitution.md`.

- Identify every placeholder token of the form `[ALL_CAPS_IDENTIFIER]`
- The user might require fewer or more principles than the template defaults
- If a specific number is requested, respect that and adjust accordingly

### 2. Collect/Derive Values for Placeholders

- If user input supplies a value, use it
- Otherwise infer from existing repo context (README, docs, prior constitution versions)
- For governance dates:
  - `RATIFICATION_DATE`: Original adoption date (if unknown, ask or mark TODO)
  - `LAST_AMENDED_DATE`: Today if changes are made, otherwise keep previous
- `CONSTITUTION_VERSION` must increment according to semantic versioning:
  - **MAJOR**: Backward incompatible governance/principle removals or redefinitions
  - **MINOR**: New principle/section added or materially expanded guidance
  - **PATCH**: Clarifications, wording, typo fixes, non-semantic refinements

### 3. Draft Updated Constitution

- Replace every placeholder with concrete text
- No bracketed tokens should remain (except intentionally retained template slots with explicit justification)
- Preserve heading hierarchy
- Ensure each Principle section includes:
  - Succinct name
  - Paragraph or bullet list with non-negotiable rules
  - Explicit rationale if not obvious
- Ensure Governance section lists:
  - Amendment procedure
  - Versioning policy
  - Compliance review expectations

### 4. Consistency Propagation Checklist

Validate alignment with dependent files:

- `.specify/templates/plan-template.md` - Constitution Check section
- `.specify/templates/spec-template.md` - Scope/requirements alignment
- `.specify/templates/tasks-template.md` - Task categorization reflects principles
- Any command files in `.github/agents/` - No outdated references

### 5. Produce Sync Impact Report

Add as HTML comment at top of constitution file:

- Version change: old → new
- List of modified principles
- Added/removed sections
- Templates requiring updates
- Follow-up TODOs if placeholders deferred

### 6. Validation Before Final Output

- No remaining unexplained bracket tokens
- Version line matches report
- Dates in ISO format YYYY-MM-DD
- Principles are declarative, testable, free of vague language

### 7. Write Constitution

Write the completed constitution back to `.specify/memory/constitution.md`.

### 8. Output Summary

- New version and bump rationale
- Files flagged for manual follow-up
- Suggested commit message

## Formatting Requirements

- Use Markdown headings exactly as in template (do not demote/promote levels)
- Wrap long rationale lines for readability (<100 chars ideally)
- Keep single blank line between sections
- Avoid trailing whitespace

## Common Principles to Consider

When creating a constitution, consider principles around:

1. **Code Quality** - Testing standards, code review requirements
2. **Testing Discipline** - TDD approach, coverage requirements
3. **User Experience** - Consistency, accessibility
4. **Performance** - Latency targets, resource constraints
5. **Security** - Authentication, data protection
6. **Observability** - Logging, metrics, tracing
7. **Simplicity** - YAGNI, minimal complexity
8. **Documentation** - Inline docs, API documentation

## Example Constitution Principles

### I. Test-First (NON-NEGOTIABLE)
TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced.

### II. Library-First
Every feature starts as a standalone library; Libraries must be self-contained, independently testable, documented.

### III. CLI Interface
Every library exposes functionality via CLI; Text in/out protocol: stdin/args → stdout, errors → stderr.

### IV. Observability
Text I/O ensures debuggability; Structured logging required for all operations.

### V. Simplicity
Start simple, YAGNI principles; Complexity must be justified and documented.
