# PRD Template

Use this template for large features that require multiple implementation phases.

---

# {Product/Feature Name}

## Problem Statement

{2-3 sentences: Who has what problem, and what's the cost of not solving it?}

## Evidence

- {User quote, data point, or observation that proves this problem exists}
- {Another piece of evidence}
- {If none: "Assumption - needs validation through [method]"}

## Proposed Solution

{One paragraph: What we're building and why this approach over alternatives}

## Key Hypothesis

We believe {capability} will {solve problem} for {users}.
We'll know we're right when {measurable outcome}.

## What We're NOT Building

- {Out of scope item 1} - {why}
- {Out of scope item 2} - {why}

## Success Metrics

| Metric | Target | How Measured |
|--------|--------|--------------|
| {Primary metric} | {Specific number} | {Method} |
| {Secondary metric} | {Specific number} | {Method} |

## Open Questions

- [ ] {Unresolved question 1}
- [ ] {Unresolved question 2}

---

## Users & Context

**Primary User**
- **Who**: {Specific description}
- **Current behavior**: {What they do today}
- **Trigger**: {What moment triggers the need}
- **Success state**: {What "done" looks like}

**Job to Be Done**
When {situation}, I want to {motivation}, so I can {outcome}.

**Non-Users**
{Who this is NOT for and why}

---

## Solution Detail

### Core Capabilities (MoSCoW)

| Priority | Capability | Rationale |
|----------|------------|-----------|
| Must | {Feature} | {Why essential} |
| Must | {Feature} | {Why essential} |
| Should | {Feature} | {Why important but not blocking} |
| Could | {Feature} | {Nice to have} |
| Won't | {Feature} | {Explicitly deferred and why} |

### MVP Scope

{What's the minimum to validate the hypothesis}

### User Flow

{Critical path - shortest journey to value}

---

## Technical Approach

**Feasibility**: {HIGH/MEDIUM/LOW}

**Architecture Notes**
- {Key technical decision and why}
- {Dependency or integration point}

**Technical Risks**

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| {Risk} | {H/M/L} | {How to handle} |

---

## Implementation Phases

<!--
  STATUS: pending | in-progress | complete
  PARALLEL: phases that can run concurrently (e.g., "with 3" or "-")
  DEPENDS: phases that must complete first (e.g., "1, 2" or "-")
  PRP: link to generated plan file once created
-->

| # | Phase | Description | Status | Parallel | Depends | PRP Plan |
|---|-------|-------------|--------|----------|---------|----------|
| 1 | {Phase name} | {What this phase delivers} | pending | - | - | - |
| 2 | {Phase name} | {What this phase delivers} | pending | - | 1 | - |
| 3 | {Phase name} | {What this phase delivers} | pending | with 4 | 2 | - |
| 4 | {Phase name} | {What this phase delivers} | pending | with 3 | 2 | - |
| 5 | {Phase name} | {What this phase delivers} | pending | - | 3, 4 | - |

### Phase Details

**Phase 1: {Name}**
- **Goal**: {What we're trying to achieve}
- **Scope**: {Bounded deliverables}
- **Success signal**: {How we know it's done}

**Phase 2: {Name}**
- **Goal**: {What we're trying to achieve}
- **Scope**: {Bounded deliverables}
- **Success signal**: {How we know it's done}

**Phase 3: {Name}**
- **Goal**: {What we're trying to achieve}
- **Scope**: {Bounded deliverables}
- **Success signal**: {How we know it's done}

**Phase 4: {Name}**
- **Goal**: {What we're trying to achieve}
- **Scope**: {Bounded deliverables}
- **Success signal**: {How we know it's done}

**Phase 5: {Name}**
- **Goal**: {What we're trying to achieve}
- **Scope**: {Bounded deliverables}
- **Success signal**: {How we know it's done}

### Parallelism Notes

{Explain which phases can run in parallel and why}

---

## Decisions Log

| Decision | Choice | Alternatives | Rationale |
|----------|--------|--------------|-----------|
| {Decision} | {Choice} | {Options considered} | {Why this one} |

---

## Research Summary

**Market Context**
{Key findings from market research}

**Technical Context**
{Key findings from technical exploration}

---

*Generated: {timestamp}*
*Status: DRAFT - needs validation*
