# PRP Framework for GitHub Copilot

> **PRP = PRD + curated codebase intelligence + agent/runbook**

The minimum viable packet an AI needs to ship production-ready code on the first pass.

## What is PRP?

**Product Requirement Prompt (PRP)** is a methodology designed to enable AI agents to ship production-ready code on the first pass. It differs from traditional PRDs by adding AI-critical layers:

- **Context**: Precise file paths, library versions, code snippet examples
- **Patterns**: Existing codebase conventions to follow
- **Validation**: Executable commands the AI can run to verify its work

## Quick Start

### For Large Features (PRD → Plan → Implement)

```
1. #prp-prd "user authentication system"
   → Creates PRD with Implementation Phases

2. #prp-plan PRPs/prds/user-auth.prd.md
   → Creates implementation plan for next phase

3. #prp-implement PRPs/plans/user-auth-phase-1.plan.md
   → Executes plan with validation loops

4. Repeat #prp-plan for remaining phases
```

### For Medium Features (Direct to Plan)

```
1. #prp-plan "add pagination to the API"
   → Creates implementation plan directly

2. #prp-implement PRPs/plans/add-pagination.plan.md
   → Executes the plan
```

### For Bug Fixes (Issue Workflow)

```
1. #prp-issue-investigate 123
   → Analyzes issue, finds root cause

2. #prp-issue-fix 123
   → Implements fix from investigation
```

## Available Commands

| Command | Description | Input |
|---------|-------------|-------|
| `#prp-prd` | Interactive PRD generator | Feature description |
| `#prp-plan` | Create implementation plan | PRD path or description |
| `#prp-implement` | Execute plan with validation | Plan file path |
| `#prp-review` | Comprehensive code review | Diff scope |
| `#prp-issue-investigate` | Analyze GitHub issue | Issue number |
| `#prp-issue-fix` | Execute fix from investigation | Issue number |
| `#prp-debug` | Deep root cause analysis | Problem description |

## Directory Structure

```
PRPs/
├── prds/              # Product requirement documents
│   └── example-feature.prd.md  ← Sample PRD (User Auth)
├── plans/             # Implementation plans
│   ├── example-feature.plan.md ← Sample Plan (JWT Tokens)
│   └── completed/     # Archived completed plans
├── reports/           # Implementation reports
├── issues/            # Issue investigations
│   └── completed/     # Archived investigations
└── templates/         # Reusable templates
    ├── prp-base.md    # Base PRP template
    └── prd-template.md # PRD template
```

## Example Artifacts

Get started by reviewing the included examples:

| Example | Description | Link |
|---------|-------------|------|
| **Sample PRD** | User Authentication System (multi-phase) | [example-feature.prd.md](./prds/example-feature.prd.md) |
| **Sample Plan** | JWT & Refresh Tokens (Phase 1 implementation) | [example-feature.plan.md](./plans/example-feature.plan.md) |

## Core Principles

### 1. Context is King

Every PRP must include comprehensive context:
- Documentation URLs with specific sections
- Code examples from the actual codebase
- Known gotchas and pitfalls
- File:line references for every pattern

### 2. Validation Loops

Every task must have executable validation:
- Build commands
- Lint commands
- Test commands
- Integration verification

### 3. Information Dense

Use specific references from the codebase:
- Actual function names
- Real type definitions
- Existing error patterns
- Current naming conventions

### 4. Bounded Scope

Each plan should be completable in one session:
- Clear start and end points
- Explicit out-of-scope items
- Dependencies listed and checked

## Workflow Overview

```
Feature Idea
    │
    ▼
┌───────────────────┐
│     PRD Phase     │  ← Problem definition, user stories, phases
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│    Plan Phase     │  ← Codebase exploration, pattern extraction
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Implement Phase   │  ← Task execution, validation loops
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│   Review Phase    │  ← Code review, quality gates
└─────────┬─────────┘
          │
          ▼
    PR & Merge
```

## Validation Commands by Language

### .NET/C#

```bash
# Level 1: Static Analysis
dotnet build
dotnet format --verify-no-changes

# Level 2: Unit Tests
dotnet test --filter "Category=Unit"

# Level 3: Full Suite
dotnet test && dotnet build --configuration Release
```

### Python

```bash
# Level 1: Static Analysis
ruff check . && mypy .

# Level 2: Unit Tests
pytest tests/unit -v

# Level 3: Full Suite
pytest && python -m build
```

### TypeScript/React

```bash
# Level 1: Static Analysis
npm run lint && npm run type-check

# Level 2: Unit Tests
npm test -- --coverage

# Level 3: Full Suite
npm test && npm run build
```

## Templates

### Base PRP Template

Use `PRPs/templates/prp-base.md` as a starting point for implementation plans.

### PRD Template

Use `PRPs/templates/prd-template.md` for large features requiring multiple phases.

## Best Practices

### DO

- ✅ Start with codebase exploration before planning
- ✅ Include actual code snippets with file:line references
- ✅ Define validation commands for every task
- ✅ Mark out-of-scope items explicitly
- ✅ Update PRD status after each phase completes

### DON'T

- ❌ Create plans without understanding existing patterns
- ❌ Skip validation steps
- ❌ Ignore the structured format
- ❌ Hardcode values that should be configuration
- ❌ Catch all exceptions without specific handling

## Success Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| First-Pass Success | > 80% | Plans implemented without replanning |
| Validation Pass Rate | > 95% | Implementations passing all checks |
| Context Completeness | 100% | All patterns documented with file:line |
| Test Coverage | > 80% | New code covered by tests |

## Related Resources

- **Skill**: `.github/skills/prp-framework/SKILL.md`
- **Agents**: 
  - `.github/agents/prp-orchestrator.md`
  - `.github/agents/prp-codebase-explorer.md`
- **Original PRP Framework**: [Wirasm/PRPs-agentic-eng](https://github.com/Wirasm/PRPs-agentic-eng)

## Credits

This implementation is based on the [PRP Framework by Rasmus Widing](https://github.com/Wirasm/PRPs-agentic-eng), adapted for GitHub Copilot.
