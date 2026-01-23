---
description: Analyze a user story and generate acceptance scenarios in Given/When/Then format.
---

# User Story Analysis

Analyze the following user story and generate comprehensive acceptance scenarios:

## User Story
$ARGUMENTS

## Tasks

1. **Extract Core Elements**
   - Identify the user/actor
   - Identify the action/goal
   - Identify the value/benefit

2. **Generate Acceptance Scenarios**
   For each scenario, use the format:
   - **Given** [initial state/context]
   - **When** [action is performed]
   - **Then** [expected outcome]

3. **Identify Edge Cases**
   - What happens with invalid input?
   - What happens at boundaries?
   - What happens with concurrent access?

4. **Define Testability**
   - How can this story be independently tested?
   - What is the minimum viable verification?

## Output Format

```markdown
### [Story Title] (Priority: P[N])

[Story description in plain language]

**Why this priority**: [Value explanation]

**Independent Test**: [How to verify independently]

**Acceptance Scenarios**:

1. **Given** [state], **When** [action], **Then** [outcome]
2. **Given** [state], **When** [action], **Then** [outcome]

**Edge Cases**:
- [Edge case 1]
- [Edge case 2]
```
