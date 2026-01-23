---
name: speckit.plan
description: Execute the implementation planning workflow using the plan template to generate design artifacts including research, data models, and API contracts.
mode: agent
tools:
  - filesystem
  - terminal
handoffs:
  - label: Create Tasks
    agent: speckit.tasks
    prompt: Break the plan into tasks
  - label: Create Checklist
    agent: speckit.checklist
    prompt: Create a checklist for the following domain...
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). The user input typically contains the tech stack and architecture choices.

## Purpose

Create a technical implementation plan from the feature specification. Generate design artifacts including research documentation, data models, and API contracts.

## Execution Flow

### 1. Setup

Run setup script:

```powershell
# PowerShell
.specify/scripts/powershell/setup-plan.ps1 -Json

# Bash
.specify/scripts/bash/setup-plan.sh --json
```

Parse JSON for `FEATURE_SPEC`, `IMPL_PLAN`, `SPECS_DIR`, `BRANCH`.

### 2. Load Context

- Read `FEATURE_SPEC` (spec.md)
- Read `.specify/memory/constitution.md`
- Load `IMPL_PLAN` template (already copied by script)

### 3. Fill Technical Context

Fill in the plan template with tech stack from user input:

```markdown
**Language/Version**: [e.g., Python 3.11, C# .NET 8]
**Primary Dependencies**: [e.g., FastAPI, ASP.NET Core]
**Storage**: [e.g., PostgreSQL, CosmosDB]
**Testing**: [e.g., pytest, xUnit]
**Target Platform**: [e.g., Linux container, Azure]
**Project Type**: [single/web/mobile]
**Performance Goals**: [e.g., 1000 req/s, <200ms p95]
**Constraints**: [e.g., <100MB memory, offline-capable]
**Scale/Scope**: [e.g., 10k users, 1M LOC]
```

Mark unknowns as "NEEDS CLARIFICATION".

### 4. Constitution Check

Extract MUST/SHOULD rules from constitution and verify:
- All constitution principles are addressed
- Any violations are explicitly justified
- Add to Complexity Tracking table if violations exist

### 5. Phase 0: Outline & Research

For each "NEEDS CLARIFICATION" in Technical Context:
1. Create research task
2. Find best practices for chosen technologies
3. Research integration patterns

Consolidate findings in `research.md`:

```markdown
# Research: [FEATURE NAME]

## Decision Log

### [Decision Topic]
- **Decision**: [what was chosen]
- **Rationale**: [why chosen]
- **Alternatives considered**: [what else evaluated]
- **Sources**: [documentation, examples referenced]
```

**Output**: `specs/<feature>/research.md` with all NEEDS CLARIFICATION resolved

### 6. Phase 1: Design & Contracts

**Prerequisites**: research.md complete

#### Generate Data Model (`data-model.md`)

Extract entities from feature spec:

```markdown
# Data Model: [FEATURE NAME]

## Entities

### [Entity Name]
- **Purpose**: [what it represents]
- **Fields**:
  - `id`: [type] - Primary identifier
  - `field1`: [type] - [description]
- **Validation Rules**: [constraints]
- **Relationships**: [connections to other entities]
- **State Transitions**: [if applicable]
```

#### Generate API Contracts (`contracts/`)

For each user action, generate endpoint:

```markdown
# API Contracts: [FEATURE NAME]

## Endpoints

### [Action Name]
- **Method**: GET/POST/PUT/DELETE
- **Path**: /api/v1/[resource]
- **Request**: [parameters, body schema]
- **Response**: [success schema, error codes]
- **Authentication**: [requirements]
```

For REST APIs, generate OpenAPI spec in `contracts/api-spec.json`.

#### Generate Quickstart (`quickstart.md`)

```markdown
# Quickstart: [FEATURE NAME]

## Prerequisites
- [Required tools]
- [Environment setup]

## Getting Started
1. [Step 1]
2. [Step 2]

## Test Scenarios
1. [Scenario 1]: [Expected outcome]
2. [Scenario 2]: [Expected outcome]
```

### 7. Update Agent Context

Run agent context update script:

```powershell
# PowerShell
.specify/scripts/powershell/update-agent-context.ps1 -AgentType copilot

# Bash
.specify/scripts/bash/update-agent-context.sh copilot
```

### 8. Determine Project Structure

Based on project type, define structure:

```markdown
## Project Structure

### Single Project (default)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

### Web Application (frontend + backend)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/
```

### 9. Re-evaluate Constitution Check

After design phase, verify:
- All principles still satisfied
- No new violations introduced
- Update Complexity Tracking if needed

### 10. Report Completion

Output:
- Branch name
- Implementation plan path
- Generated artifacts:
  - research.md
  - data-model.md
  - contracts/
  - quickstart.md
- Next step: `/speckit.tasks`

## Key Rules

- Use absolute paths
- ERROR on gate failures or unresolved clarifications
- All NEEDS CLARIFICATION must be resolved before proceeding
- Constitution violations must be explicitly justified
