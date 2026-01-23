---
mode: agent
description: "Generate comprehensive unit tests for code"
---

# Generate Unit Tests

Create thorough unit tests for the specified code.

## Test Requirements

- Use the project's existing test framework
- Follow AAA pattern (Arrange, Act, Assert)
- Cover happy paths and edge cases
- Include error scenarios
- Use descriptive test names

{{#if selection}}
## Code to Test

```
{{{ selection }}}
```
{{/if}}

## Test Cases to Include

1. **Happy Path** - Normal expected behavior
2. **Edge Cases** - Boundary values, empty inputs
3. **Error Handling** - Invalid inputs, exceptions
4. **Integration Points** - Mock external dependencies

Generate tests that achieve high coverage while remaining maintainable.
