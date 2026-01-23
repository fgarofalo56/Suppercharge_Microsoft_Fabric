---
name: speckit.clarify
description: Identify underspecified areas in the current feature spec by asking up to 5 highly targeted clarification questions and encoding answers back into the spec.
mode: agent
tools:
  - filesystem
  - terminal
handoffs:
  - label: Build Technical Plan
    agent: speckit.plan
    prompt: Create a plan for the spec. I am building with...
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

Detect and reduce ambiguity or missing decision points in the active feature specification. Record clarifications directly in the spec file.

**Note**: This workflow should run BEFORE invoking `/speckit.plan`. If explicitly skipping clarification (e.g., exploratory spike), warn that downstream rework risk increases.

## Execution Flow

### 1. Setup

Run prerequisite check script:

```powershell
# PowerShell
.specify/scripts/powershell/check-prerequisites.ps1 -Json -PathsOnly

# Bash
.specify/scripts/bash/check-prerequisites.sh --json --paths-only
```

Parse JSON for `FEATURE_DIR`, `FEATURE_SPEC`.

### 2. Ambiguity & Coverage Scan

Load the current spec file and perform structured analysis using this taxonomy. Mark each category: **Clear** / **Partial** / **Missing**

#### Functional Scope & Behavior
- Core user goals & success criteria
- Explicit out-of-scope declarations
- User roles / personas differentiation

#### Domain & Data Model
- Entities, attributes, relationships
- Identity & uniqueness rules
- Lifecycle/state transitions
- Data volume / scale assumptions

#### Interaction & UX Flow
- Critical user journeys / sequences
- Error/empty/loading states
- Accessibility or localization notes

#### Non-Functional Quality Attributes
- Performance (latency, throughput targets)
- Scalability (horizontal/vertical, limits)
- Reliability & availability (uptime, recovery expectations)
- Observability (logging, metrics, tracing signals)
- Security & privacy (authN/Z, data protection, threat assumptions)
- Compliance / regulatory constraints

#### Integration & External Dependencies
- External services/APIs and failure modes
- Data import/export formats
- Protocol/versioning assumptions

#### Edge Cases & Failure Handling
- Negative scenarios
- Rate limiting / throttling
- Conflict resolution (e.g., concurrent edits)

#### Constraints & Tradeoffs
- Technical constraints (language, storage, hosting)
- Explicit tradeoffs or rejected alternatives

#### Terminology & Consistency
- Canonical glossary terms
- Avoided synonyms / deprecated terms

#### Completion Signals
- Acceptance criteria testability
- Measurable Definition of Done indicators

### 3. Generate Clarification Questions

Generate prioritized queue (max 5 questions). Apply these constraints:

- Maximum 10 total questions across whole session
- Each question must be answerable with:
  - Short multiple-choice selection (2-5 options), OR
  - One-word / short-phrase answer (≤5 words)
- Only include questions that materially impact:
  - Architecture
  - Data modeling
  - Task decomposition
  - Test design
  - UX behavior
  - Operational readiness
  - Compliance validation

### 4. Sequential Questioning Loop

Present **EXACTLY ONE** question at a time.

#### For Multiple-Choice Questions

1. **Analyze all options** and determine best choice based on:
   - Best practices for project type
   - Common patterns in similar implementations
   - Risk reduction (security, performance, maintainability)
   - Alignment with project goals/constraints

2. Present **recommended option prominently**:
   ```markdown
   **Recommended:** Option [X] - <1-2 sentence reasoning>
   ```

3. Render all options as table:
   | Option | Description |
   |--------|-------------|
   | A | Option A description |
   | B | Option B description |
   | C | Option C description |

4. Add: `Reply with option letter (e.g., "A"), accept recommendation by saying "yes", or provide your own answer.`

#### For Short-Answer Questions

1. Provide **suggested answer**:
   ```markdown
   **Suggested:** <your proposed answer> - <brief reasoning>
   ```

2. Add: `Format: Short answer (≤5 words). Accept with "yes" or provide your own.`

### 5. Process Answers

After user answers:
- If "yes", "recommended", or "suggested": use your stated recommendation
- Otherwise validate answer fits constraints
- If ambiguous, ask for quick disambiguation (doesn't count as new question)
- Record in working memory (don't write to disk yet)
- Move to next queued question

**Stop asking when**:
- All critical ambiguities resolved
- User signals completion ("done", "good", "no more")
- 5 questions reached

### 6. Integrate Answers Into Spec

After EACH accepted answer:

1. Ensure `## Clarifications` section exists (create after overview section if missing)
2. Create `### Session YYYY-MM-DD` subheading for today
3. Append: `- Q: <question> → A: <final answer>`
4. Apply clarification to appropriate section:
   - Functional ambiguity → Functional Requirements
   - User interaction → User Stories
   - Data shape/entities → Data Model
   - Non-functional constraint → Quality Attributes (with metric)
   - Edge case → Edge Cases / Error Handling
   - Terminology → Normalize across spec
5. If clarification invalidates earlier statement, replace (don't duplicate)
6. **Save spec file immediately after each integration**

### 7. Validation

After EACH write and final pass:
- Clarifications session contains exactly one bullet per accepted answer
- Total questions ≤ 5
- No lingering vague placeholders the answer resolved
- No contradictory earlier statements remain
- Markdown structure valid
- Terminology consistent

### 8. Report Completion

Output:
- Number of questions asked & answered
- Path to updated spec
- Sections touched
- Coverage summary table:
  | Category | Status |
  |----------|--------|
  | Functional Scope | Resolved/Deferred/Clear/Outstanding |
  | Domain & Data Model | ... |
  | ... | ... |
- Recommendation: proceed to `/speckit.plan` or run `/speckit.clarify` again
- Suggested next command

## Behavior Rules

- If no meaningful ambiguities found: "No critical ambiguities detected. Suggest proceeding."
- If spec file missing: instruct user to run `/speckit.specify` first
- Never exceed 5 asked questions
- Respect early termination signals ("stop", "done", "proceed")
