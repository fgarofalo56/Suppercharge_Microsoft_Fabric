---
name: Feature Implementation
description: Template for delegating new features to Copilot coding agent
---

# Feature Implementation Task

## Feature Description
<!-- Clear description of the feature -->
[Describe the feature to be implemented]

## User Story
<!-- Who benefits and how -->
As a [type of user],
I want [goal/desire],
So that [benefit/value].

## Requirements

### Functional Requirements
<!-- What the feature must do -->
- [ ] [Requirement 1]
- [ ] [Requirement 2]
- [ ] [Requirement 3]

### Non-Functional Requirements
<!-- Performance, security, etc. -->
- [ ] Performance: [requirement]
- [ ] Security: [requirement]
- [ ] Accessibility: [requirement]

## Technical Specification

### Files to Create/Modify
<!-- Expected files and their purpose -->
| File | Action | Purpose |
|------|--------|---------|
| `src/...` | Create | [Purpose] |
| `src/...` | Modify | [Changes needed] |
| `tests/...` | Create | [Tests to add] |

### Data Models
<!-- If applicable -->
```typescript
interface [ModelName] {
  field1: type;
  field2: type;
}
```

### API Endpoints
<!-- If applicable -->
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/...` | [Description] |
| POST | `/api/...` | [Description] |

## Acceptance Criteria
<!-- How to verify feature is complete -->
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]
- [ ] Unit tests written with 80%+ coverage
- [ ] Integration tests for main flows
- [ ] Documentation updated

## UI/UX Specifications
<!-- If applicable -->
- Design mockup: [link]
- User flow: [description]
- Responsive requirements: [details]

## Dependencies
<!-- Any dependencies on other features/systems -->
- Depends on: [feature/system]
- Blocked by: [issue/PR]

## Constraints
<!-- Limitations and restrictions -->
- Must use existing [pattern/library]
- Cannot modify [files/systems]
- Must be backward compatible

## Out of Scope
<!-- What is NOT included -->
- [Feature/capability 1]
- [Feature/capability 2]

## References
<!-- Helpful links and context -->
- Design doc: [link]
- Related PR: [link]
- Similar feature: [link]

---

**Labels:** `copilot-delegate`, `type:feature`
