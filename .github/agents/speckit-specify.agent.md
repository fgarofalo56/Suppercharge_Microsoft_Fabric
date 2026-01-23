---
name: speckit.specify
description: Create or update the feature specification from a natural language feature description using Spec-Driven Development methodology.
mode: agent
tools:
  - filesystem
  - terminal
handoffs:
  - label: Build Technical Plan
    agent: speckit.plan
    prompt: Create a plan for the spec. I am building with...
  - label: Clarify Spec Requirements
    agent: speckit.clarify
    prompt: Clarify specification requirements
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

Create a feature specification from a natural language description. Focus on **WHAT** users need and **WHY** - avoid implementation details (no tech stack, APIs, code structure).

## Execution Flow

### 1. Generate Feature Branch Name

Analyze the feature description and create a 2-4 word short name:

- Use action-noun format when possible (e.g., "add-user-auth", "fix-payment-bug")
- Preserve technical terms and acronyms (OAuth2, API, JWT, etc.)
- Keep concise but descriptive

Examples:
- "I want to add user authentication" → "user-auth"
- "Implement OAuth2 integration for the API" → "oauth2-api-integration"
- "Create a dashboard for analytics" → "analytics-dashboard"

### 2. Check for Existing Branches

```bash
# Fetch all remote branches
git fetch --all --prune

# Find highest feature number for this short-name across:
# - Remote branches: git ls-remote --heads origin | grep -E 'refs/heads/[0-9]+-<short-name>$'
# - Local branches: git branch | grep -E '^[* ]*[0-9]+-<short-name>$'
# - Specs directories: Check for directories matching `specs/[0-9]+-<short-name>`
```

Determine next available number (N+1) for the new branch.

### 3. Create Feature Branch and Spec Directory

```bash
# PowerShell
.specify/scripts/powershell/create-new-feature.ps1 -Json -Number <N+1> -ShortName "<short-name>" "<description>"

# Bash
.specify/scripts/bash/create-new-feature.sh --json --number <N+1> --short-name "<short-name>" "<description>"
```

### 4. Load Spec Template

Load `.specify/templates/spec-template.md` to understand required sections.

### 5. Create Specification

Parse the user description and extract:
- Key concepts: actors, actions, data, constraints
- For unclear aspects, make informed guesses based on context and industry standards
- Only mark with `[NEEDS CLARIFICATION: specific question]` if:
  - Choice significantly impacts feature scope or user experience
  - Multiple reasonable interpretations exist with different implications
  - No reasonable default exists
- **LIMIT: Maximum 3 [NEEDS CLARIFICATION] markers total**

### 6. Fill Required Sections

#### User Scenarios & Testing (MANDATORY)

User stories should be:
- Prioritized as user journeys ordered by importance (P1, P2, P3...)
- Independently testable - each delivers standalone MVP value

For each user story include:
- Brief title and priority
- Plain language description
- Why this priority (explain value)
- Independent test criteria
- Acceptance scenarios (Given/When/Then format)

#### Requirements (MANDATORY)

- **FR-001**: System MUST [specific capability]
- Each requirement must be testable
- Use reasonable defaults for unspecified details

#### Success Criteria (MANDATORY)

Measurable, technology-agnostic outcomes:
- ✅ "Users can complete checkout in under 2 minutes"
- ✅ "System supports 10,000 concurrent users"
- ❌ "API response time under 200ms" (too technical)
- ❌ "Redis cache hit rate above 80%" (technology-specific)

### 7. Write Specification

Write the spec to `specs/<NNN-feature-name>/spec.md`

### 8. Validate and Create Checklist

Create `specs/<NNN-feature-name>/checklists/requirements.md`:

```markdown
# Specification Quality Checklist: [FEATURE NAME]

**Purpose**: Validate specification completeness and quality
**Created**: [DATE]
**Feature**: [Link to spec.md]

## Content Quality
- [ ] No implementation details (languages, frameworks, APIs)
- [ ] Focused on user value and business needs
- [ ] Written for non-technical stakeholders
- [ ] All mandatory sections completed

## Requirement Completeness
- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] Requirements are testable and unambiguous
- [ ] Success criteria are measurable and technology-agnostic
- [ ] All acceptance scenarios are defined
- [ ] Edge cases are identified
- [ ] Scope is clearly bounded
```

### 9. Handle Clarifications

If [NEEDS CLARIFICATION] markers remain, present to user:

```markdown
## Question [N]: [Topic]

**Context**: [Quote relevant spec section]

**What we need to know**: [Specific question]

**Suggested Answers**:

| Option | Answer | Implications |
|--------|--------|--------------|
| A      | [First answer] | [What this means] |
| B      | [Second answer] | [What this means] |
| C      | [Third answer] | [What this means] |

**Your choice**: _[Wait for response]_
```

### 10. Report Completion

Output:
- Branch name
- Spec file path
- Checklist results
- Readiness for next phase (`/speckit.clarify` or `/speckit.plan`)

## Quick Guidelines

- Focus on **WHAT** users need and **WHY**
- Avoid HOW to implement (no tech stack, APIs, code structure)
- Written for business stakeholders, not developers
- DO NOT create checklists embedded in the spec - they are separate files

## Reasonable Defaults (Don't Ask About These)

- Data retention: Industry-standard practices for the domain
- Performance targets: Standard web/mobile app expectations unless specified
- Error handling: User-friendly messages with appropriate fallbacks
- Authentication method: Standard session-based or OAuth2 for web apps
- Integration patterns: RESTful APIs unless specified otherwise
