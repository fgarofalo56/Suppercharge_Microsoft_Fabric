---
description: Coding standards for [technology/framework] - replace with your description
patterns:
  - '**/*.ext'            # Replace with your file patterns
  - '**/specific-path/**/*.ext'
  - '**/*.test.ext'       # Example: test files
---

# [Technology/Framework] Development Standards

## Overview
Brief description of what technology/framework these standards cover and their purpose.

## Project Structure
```
recommended-structure/
├── src/
│   ├── directory1/
│   ├── directory2/
│   └── directory3/
├── tests/
└── docs/
```

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Files | [convention] | `example-file.ext` |
| Classes | [convention] | `ExampleClass` |
| Functions | [convention] | `exampleFunction()` |
| Variables | [convention] | `exampleVariable` |
| Constants | [convention] | `EXAMPLE_CONSTANT` |

## Code Style

### DO: [Recommended Pattern Name]
```[language]
// Good example demonstrating best practice
// Include comments explaining why this is good
```

**Why:** [Explanation of benefits and rationale]

**When to use:** [Specific scenarios]

---

### DON'T: [Anti-Pattern Name]
```[language]
// Bad example showing what to avoid
// Include comments explaining the problems
```

**Why to avoid:** [Explanation of issues]

**Alternative:** Use the DO pattern above instead.

---

## Common Patterns

### Pattern 1: [Pattern Name]
**Use when:** [Scenario description]

```[language]
// Pattern implementation
// Include clear comments
```

**Benefits:**
- Benefit 1
- Benefit 2

---

### Pattern 2: [Pattern Name]
**Use when:** [Scenario description]

```[language]
// Pattern implementation
```

**Benefits:**
- Benefit 1
- Benefit 2

---

## Testing Standards

### Test Framework
- **Framework**: [Name and version]
- **Runner**: [Test runner]
- **Coverage Tool**: [Coverage tool]

### Test Structure
```[language]
// Example test structure
// Show typical test organization
```

### Coverage Requirements
- **Minimum**: [percentage]%
- **Target**: [percentage]%
- **Critical paths**: 100%

### Test Naming
```[language]
// Example test names following your convention
```

---

## Documentation Requirements

### Code Comments
- Document **why**, not **what**
- All public APIs must be documented
- Complex algorithms need explanation
- Include usage examples for non-obvious code

### Example:
```[language]
/**
 * [Function description]
 *
 * @param parameter1 [Description]
 * @param parameter2 [Description]
 * @returns [Description]
 *
 * @example
 * // Usage example
 * exampleFunction(arg1, arg2);
 */
```

---

## Error Handling

### DO: Specific Error Handling
```[language]
// Good error handling example
```

### DON'T: Silent Failures
```[language]
// Bad error handling example
```

### Guidelines
- Always validate inputs
- Provide helpful error messages
- Log errors appropriately
- Clean up resources in finally blocks

---

## Performance Considerations

1. **Consideration 1**: [Description and guidance]
2. **Consideration 2**: [Description and guidance]
3. **Consideration 3**: [Description and guidance]

### Performance Patterns
```[language]
// Example of performant code
```

---

## Security Guidelines

1. **Input Validation**: [Guidelines]
2. **Authentication**: [Guidelines]
3. **Authorization**: [Guidelines]
4. **Data Protection**: [Guidelines]
5. **Secure Communication**: [Guidelines]

### Security Checklist
- [ ] All inputs validated
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] CSRF protection
- [ ] Secure password handling
- [ ] Sensitive data encryption

---

## Accessibility (if applicable)

- **WCAG Level**: [A, AA, or AAA]
- **Keyboard Navigation**: [Requirements]
- **Screen Reader Support**: [Requirements]
- **Color Contrast**: [Requirements]

---

## Common Pitfalls

### Pitfall 1: [Name]
**Problem:** [Description]
**Solution:** [How to avoid]

### Pitfall 2: [Name]
**Problem:** [Description]
**Solution:** [How to avoid]

---

## References
- [Official Documentation](url)
- [Style Guide](url)
- [Best Practices](url)
- [Community Resources](url)
