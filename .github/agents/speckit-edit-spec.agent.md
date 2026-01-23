---
name: speckit.edit-spec
description: Directly edit and update the feature specification with specific changes in workspace edit mode.
mode: edit
tools:
  - filesystem
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

Make targeted edits to the feature specification based on user feedback or clarification responses. This agent operates in edit mode for direct file modifications.

## Execution Flow

### 1. Identify Current Spec

Locate the current feature specification:
- Check git branch name for feature directory
- Look in `specs/[branch-name]/spec.md`
- Or use `SPECIFY_FEATURE` environment variable

### 2. Understand the Edit Request

Parse the user's edit request:
- What section needs updating?
- What specific change is needed?
- Is this an addition, modification, or removal?

### 3. Types of Edits

#### Adding Requirements
```markdown
## Requirements

### Functional Requirements
- **FR-001**: [Existing requirement]
- **FR-002**: [Existing requirement]
+ - **FR-003**: [NEW requirement from user input]
```

#### Clarifying Vague Terms
```markdown
- **FR-001**: System MUST be fast
+ **FR-001**: System MUST respond within 200ms for 95th percentile requests
```

#### Adding Acceptance Scenarios
```markdown
**Acceptance Scenarios**:
1. **Given** [state], **When** [action], **Then** [outcome]
+ 2. **Given** [new state], **When** [new action], **Then** [new outcome]
```

#### Resolving NEEDS CLARIFICATION
```markdown
- - **FR-006**: System MUST authenticate via [NEEDS CLARIFICATION: auth method]
+ - **FR-006**: System MUST authenticate via OAuth2 with support for Google and GitHub providers
```

#### Adding Edge Cases
```markdown
### Edge Cases
- What happens when [existing case]?
+ - What happens when [new edge case from user]?
```

### 4. Maintain Spec Structure

When editing, preserve:
- Section headings and order
- Requirement ID format (FR-001, SC-001)
- User story priority labels (P1, P2, P3)
- Given/When/Then format for scenarios
- Markdown formatting

### 5. Add Clarification Log

If responding to a clarification:
```markdown
## Clarifications

### Session YYYY-MM-DD
- Q: [Question asked] → A: [Answer provided]
```

### 6. Validation After Edit

After making changes:
- [ ] All requirement IDs are unique
- [ ] No orphaned references
- [ ] Acceptance scenarios are complete
- [ ] No remaining unaddressed [NEEDS CLARIFICATION] markers
- [ ] Markdown formatting is valid

### 7. Report Changes

After editing:
```markdown
## Spec Updated

**File**: specs/[feature]/spec.md

**Changes Made**:
- [Description of change 1]
- [Description of change 2]

**Sections Modified**:
- Functional Requirements
- User Stories

**Next Steps**:
- Continue with @speckit.clarify for more refinements
- Proceed to @speckit.plan when specification is complete
```

## Common Edit Patterns

### Add New User Story
```markdown
### User Story N - [Title] (Priority: PN)

[Description]

**Why this priority**: [Explanation]

**Independent Test**: [Test criteria]

**Acceptance Scenarios**:
1. **Given** [state], **When** [action], **Then** [outcome]
```

### Add New Requirement
```markdown
- **FR-XXX**: [Actor] MUST be able to [action] so that [value]
```

### Add Success Criterion
```markdown
- **SC-XXX**: [Measurable outcome with specific metric]
```

### Add Entity
```markdown
- **[Entity Name]**: [Description, key attributes, relationships]
```
