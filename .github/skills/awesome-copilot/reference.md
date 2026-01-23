## Awesome GitHub Copilot Reference Documentation

Comprehensive reference for creating GitHub Copilot customizations based on the awesome-copilot community toolkit.

## Table of Contents

1. [Agent Reference](#agent-reference)
2. [Prompt Reference](#prompt-reference)
3. [Instruction Reference](#instruction-reference)
4. [Collection Reference](#collection-reference)
5. [Schema Specifications](#schema-specifications)
6. [Example Library](#example-library)
7. [Advanced Patterns](#advanced-patterns)
8. [Troubleshooting](#troubleshooting)

---

## Agent Reference

### Agent File Structure

```markdown
---
description: '[Required] Clear, concise agent purpose (max 1024 chars)'
model: [Recommended] claude-3-5-sonnet-20241022
tools: [Optional]
  - mcp-server-1
  - mcp-server-2
---

# Agent Name

[Agent content and instructions]
```

### Required Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| description | string | Yes | Agent purpose (wrapped in quotes) |
| model | string | Recommended | Claude model identifier |
| tools | array | No | MCP servers used by agent |

### Model Options

| Model ID | Use Case |
|----------|----------|
| `claude-3-5-sonnet-20241022` | Recommended - Best balance of capability and speed |
| `claude-3-opus-20240229` | Maximum capability for complex tasks |
| `claude-3-haiku-20240307` | Fast responses for simple tasks |

### Agent Naming Rules

✅ **Correct:**
- `python-expert.agent.md`
- `database-migration-specialist.agent.md`
- `azure-bicep-architect.agent.md`

❌ **Incorrect:**
- `Python_Expert.agent.md` (no underscores)
- `Database Migration.agent.md` (no spaces)
- `azureBicepArchitect.agent.md` (no camelCase)

### Agent Content Structure

```markdown
# Agent Name

## Role
Brief description of the agent's persona and primary function.

## Expertise
- Area of expertise 1
- Area of expertise 2
- Area of expertise 3

## Approach
How the agent thinks about and solves problems:
1. First consideration
2. Second consideration
3. Third consideration

## Guidelines
Specific rules or standards the agent follows:
- Guideline 1
- Guideline 2
- Guideline 3

## Output Format
Expected structure of agent responses:
- Format specification
- Examples
- Constraints

## Common Tasks
Typical scenarios where this agent excels:
1. Task type 1
2. Task type 2
3. Task type 3

## Examples
### Example 1: [Scenario]
**Input:**
[Example input]

**Expected Output:**
[Example output]
```

---

## Prompt Reference

### Prompt File Structure

```markdown
---
title: Descriptive Action Title
description: What this prompt does and when to use it
---

# Prompt Title

[Detailed instructions for the task]
```

### Required Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | Human-readable prompt name |
| description | string | Yes | Purpose and use case |

### Prompt Invocation

```
/awesome-copilot <prompt-name>
```

Example:
```
/awesome-copilot create-readme
/awesome-copilot generate-tests
/awesome-copilot optimize-code
```

### Prompt Content Patterns

#### Pattern 1: Code Generation

```markdown
# Generate [Component Type]

## Context
You are creating a [component type] for [purpose].

## Requirements
1. Must include [feature 1]
2. Should implement [feature 2]
3. Must follow [standard]

## Structure
```[language]
// Expected structure
```

## Best Practices
- Practice 1
- Practice 2

## Output
Generate complete, production-ready code.
```

#### Pattern 2: Analysis & Review

```markdown
# Review [Artifact Type]

## Analysis Focus
Evaluate the provided [artifact] for:
1. [Criterion 1]
2. [Criterion 2]
3. [Criterion 3]

## Review Process
1. Identify issues
2. Assess severity
3. Provide specific recommendations
4. Include code examples

## Report Format
### Issues Found
- Issue 1: [Description] (Severity: High/Medium/Low)
- Issue 2: [Description]

### Recommendations
1. Recommendation with code example
2. Recommendation with rationale
```

#### Pattern 3: Refactoring & Optimization

```markdown
# Optimize [Code Type]

## Analysis
Review the code for:
- Performance bottlenecks
- Code smells
- Maintainability issues
- Best practice violations

## Optimization Strategy
1. Identify improvements
2. Assess impact vs effort
3. Prioritize changes
4. Provide refactored code

## Output
For each optimization:
- **Before:** [Original code]
- **After:** [Improved code]
- **Benefit:** [Explanation]
- **Trade-offs:** [Any considerations]
```

---

## Instruction Reference

### Instruction File Structure

```markdown
---
description: Coding standards for [technology/framework]
patterns:
  - '**/*.ext'        # Glob patterns for file matching
  - '**/path/**/*.ext'
---

# [Technology] Best Practices

[Comprehensive coding standards]
```

### Required Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| description | string | Yes | What these instructions cover |
| patterns | array | Yes | File glob patterns to match |

### Pattern Matching Syntax

| Pattern | Matches |
|---------|---------|
| `**/*.cs` | All C# files |
| `**/src/**/*.tsx` | TSX files in src directories |
| `**/*.test.js` | All test files |
| `**/components/**/*.vue` | Vue files in components |
| `**/migrations/*.sql` | SQL migration files |

### Instruction Content Structure

```markdown
# [Technology] Development Standards

## Overview
Brief description of the technology and these standards' scope.

## Project Structure
```
recommended-structure/
├── src/
│   ├── components/
│   ├── services/
│   └── utils/
└── tests/
```

## Naming Conventions
- **Files**: [convention]
- **Classes**: [convention]
- **Functions**: [convention]
- **Variables**: [convention]
- **Constants**: [convention]

## Code Style

### DO: [Pattern Name]
```[language]
// Good example with explanation
```
**Why:** [Rationale]

### DON'T: [Anti-pattern Name]
```[language]
// Bad example
```
**Why:** [Reason to avoid]

## Common Patterns

### Pattern 1: [Scenario]
[When to use this pattern]
```[language]
// Implementation
```

### Pattern 2: [Scenario]
[When to use this pattern]
```[language]
// Implementation
```

## Testing Standards
- Test framework: [name]
- Coverage target: [percentage]
- Test structure: [pattern]
```[language]
// Test example
```

## Documentation Requirements
- All public APIs documented
- Complex logic explained
- Usage examples provided

## Performance Considerations
1. [Consideration 1]
2. [Consideration 2]
3. [Consideration 3]

## Security Guidelines
1. [Guideline 1]
2. [Guideline 2]
3. [Guideline 3]

## References
- [Official Documentation](url)
- [Style Guide](url)
- [Best Practices](url)
```

---

## Collection Reference

### Collection File Structure

```markdown
---
title: Collection Display Name
description: What this collection provides
---

# Collection Name

[Collection overview and contents]
```

### Required Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | Human-readable collection name |
| description | string | Yes | Purpose and contents |

### Collection Content Structure

```markdown
# Collection Name

Brief overview of what this collection provides and who should use it.

## Included Agents
- **[agent-name](../agents/agent-name.agent.md)** - One-line description
- **[another-agent](../agents/another-agent.agent.md)** - One-line description

## Included Prompts
- **[prompt-name](../prompts/prompt-name.prompt.md)** - One-line description
- **[another-prompt](../prompts/another-prompt.prompt.md)** - One-line description

## Included Instructions
- **[instruction-name](../instructions/instruction-name.instructions.md)** - One-line description

## Use Cases
1. **Use case 1**: [Description and when to apply]
2. **Use case 2**: [Description and when to apply]
3. **Use case 3**: [Description and when to apply]

## Getting Started

### Prerequisites
- [Requirement 1]
- [Requirement 2]

### Quick Start
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Example Workflow
[Concrete example of using items from this collection]

## Related Collections
- [Collection Name](./related-collection.collection.md)
```

---

## Schema Specifications

### Agent Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["description"],
  "properties": {
    "description": {
      "type": "string",
      "minLength": 1,
      "maxLength": 1024
    },
    "model": {
      "type": "string",
      "enum": [
        "claude-3-5-sonnet-20241022",
        "claude-3-opus-20240229",
        "claude-3-haiku-20240307"
      ]
    },
    "tools": {
      "type": "array",
      "items": {
        "type": "string"
      }
    }
  }
}
```

### Prompt Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["title", "description"],
  "properties": {
    "title": {
      "type": "string",
      "minLength": 1
    },
    "description": {
      "type": "string",
      "minLength": 1
    }
  }
}
```

### Instruction Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["description", "patterns"],
  "properties": {
    "description": {
      "type": "string",
      "minLength": 1
    },
    "patterns": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "minItems": 1
    }
  }
}
```

---

## Example Library

### Complete Agent Example

**File: `agents/python-testing-expert.agent.md`**

```markdown
---
description: 'Expert in Python testing with pytest, focusing on test design, coverage, and best practices'
model: claude-3-5-sonnet-20241022
tools:
  - pytest-mcp
---

# Python Testing Expert

## Role
You are a Python testing specialist with deep expertise in pytest, test-driven development (TDD), and test automation strategies.

## Expertise
- Pytest framework and plugins
- Test fixtures and parametrization
- Mocking and patching strategies
- Coverage analysis and improvement
- Integration and end-to-end testing
- Performance testing
- Test organization and architecture

## Approach
1. **Test-First Mindset**: Consider testability from the design phase
2. **Clear Intent**: Tests should document behavior clearly
3. **Independence**: Tests must run independently and in any order
4. **Fast Execution**: Optimize for quick feedback loops
5. **Comprehensive Coverage**: Balance thoroughness with maintainability

## Guidelines
- Use descriptive test names that explain the scenario
- Follow Arrange-Act-Assert (AAA) pattern
- One assertion per test when possible
- Mock external dependencies
- Use fixtures for common setup
- Parametrize for testing multiple scenarios
- Group related tests in classes
- Maintain test code quality equal to production code

## Common Tasks

### 1. Writing Unit Tests
For a given function or class, generate comprehensive unit tests covering:
- Happy path scenarios
- Edge cases
- Error conditions
- Boundary values

### 2. Test Refactoring
Improve existing tests for:
- Better readability
- Reduced duplication
- Improved maintainability
- Faster execution

### 3. Coverage Analysis
Identify untested code paths and generate tests to improve coverage.

### 4. Test Architecture
Design test structure for complex projects including:
- Fixture organization
- Conftest.py strategy
- Test discovery patterns

## Example

**Given this function:**
```python
def calculate_discount(price, discount_percent, max_discount=50):
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount must be between 0 and 100")
    actual_discount = min(discount_percent, max_discount)
    return price * (1 - actual_discount / 100)
```

**Generate tests:**
```python
import pytest
from decimal import Decimal

class TestCalculateDiscount:
    """Tests for calculate_discount function."""

    def test_no_discount(self):
        """Should return original price when discount is 0."""
        assert calculate_discount(100, 0) == 100

    def test_normal_discount(self):
        """Should apply discount correctly."""
        assert calculate_discount(100, 20) == 80

    def test_discount_capped_at_max(self):
        """Should not exceed maximum discount."""
        assert calculate_discount(100, 75, max_discount=50) == 50

    @pytest.mark.parametrize("discount", [-1, 101, 150])
    def test_invalid_discount_raises_error(self, discount):
        """Should raise ValueError for invalid discount percentages."""
        with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
            calculate_discount(100, discount)

    @pytest.mark.parametrize("price,discount,expected", [
        (100, 10, 90),
        (50, 20, 40),
        (0, 50, 0),
    ])
    def test_various_scenarios(self, price, discount, expected):
        """Should calculate correct discounted price for various inputs."""
        assert calculate_discount(price, discount) == expected
```
```

### Complete Prompt Example

**File: `prompts/create-api-documentation.prompt.md`**

```markdown
---
title: Create API Documentation
description: Generates comprehensive API documentation from code with examples and usage guidelines
---

# API Documentation Generator

Generate complete, professional API documentation for the provided code.

## Documentation Structure

### 1. Overview
- Brief description of the API
- Primary use cases
- Key features

### 2. Authentication
- Required credentials
- Authentication methods
- Example headers

### 3. Endpoints

For each endpoint include:

#### Endpoint Name
**Method:** `GET|POST|PUT|DELETE|PATCH`
**URL:** `/api/path/:param`

**Description:**
[What this endpoint does]

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| param1 | string | Yes | [Description] |
| param2 | number | No | [Description] |

**Request Example:**
```json
{
  "field": "value"
}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "data": {}
}
```

**Error Responses:**
- `400 Bad Request`: [When this occurs]
- `401 Unauthorized`: [When this occurs]
- `404 Not Found`: [When this occurs]
- `500 Internal Server Error`: [When this occurs]

### 4. Data Models
[Define all DTOs and data structures]

### 5. Rate Limiting
[Rate limit policies]

### 6. Code Examples

Provide examples in multiple languages:
- cURL
- JavaScript/TypeScript
- Python
- C#

### 7. Best Practices
- [Practice 1]
- [Practice 2]
- [Practice 3]

### 8. Troubleshooting
Common issues and solutions
```

### Complete Instruction Example

**File: `instructions/react-typescript.instructions.md`**

```markdown
---
description: React + TypeScript best practices for component development, hooks, and state management
patterns:
  - '**/*.tsx'
  - '**/*.ts'
  - '**/components/**'
  - '**/hooks/**'
---

# React + TypeScript Development Standards

## Project Structure
```
src/
├── components/
│   ├── common/
│   ├── features/
│   └── layouts/
├── hooks/
│   ├── useCustomHook.ts
│   └── index.ts
├── types/
│   ├── api.types.ts
│   ├── component.types.ts
│   └── index.ts
├── utils/
└── services/
```

## Component Patterns

### DO: Functional Components with TypeScript
```tsx
import { FC } from 'react';

interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
}

export const Button: FC<ButtonProps> = ({
  label,
  onClick,
  variant = 'primary',
  disabled = false
}) => {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`btn btn-${variant}`}
    >
      {label}
    </button>
  );
};
```

### DON'T: Unclear Props or Missing Types
```tsx
// Bad - no types, unclear props
export const Button = ({ label, onClick, ...rest }) => {
  return <button onClick={onClick} {...rest}>{label}</button>;
};
```

## Hooks Best Practices

### DO: Custom Hooks with Clear Types
```tsx
import { useState, useEffect } from 'react';

interface UseApiOptions<T> {
  url: string;
  initialData: T;
}

interface UseApiReturn<T> {
  data: T;
  loading: boolean;
  error: Error | null;
  refetch: () => Promise<void>;
}

export function useApi<T>({ url, initialData }: UseApiOptions<T>): UseApiReturn<T> {
  const [data, setData] = useState<T>(initialData);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await fetch(url);
      const result = await response.json();
      setData(result);
      setError(null);
    } catch (err) {
      setError(err as Error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [url]);

  return { data, loading, error, refetch: fetchData };
}
```

## State Management

### DO: Discriminated Unions for Complex State
```tsx
type LoadingState = { status: 'loading' };
type SuccessState<T> = { status: 'success'; data: T };
type ErrorState = { status: 'error'; error: Error };

type AsyncState<T> = LoadingState | SuccessState<T> | ErrorState;

function Component() {
  const [state, setState] = useState<AsyncState<User>>({ status: 'loading' });

  // TypeScript knows which properties are available
  if (state.status === 'success') {
    return <div>{state.data.name}</div>;
  }

  if (state.status === 'error') {
    return <div>Error: {state.error.message}</div>;
  }

  return <div>Loading...</div>;
}
```

## Testing Standards
- Use React Testing Library
- Test behavior, not implementation
- Aim for 80%+ coverage
- Mock API calls and external dependencies

```tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<Button label="Click me" onClick={handleClick} />);

    fireEvent.click(screen.getByText('Click me'));

    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('disables button when disabled prop is true', () => {
    render(<Button label="Click me" onClick={() => {}} disabled />);

    expect(screen.getByText('Click me')).toBeDisabled();
  });
});
```

## Performance Optimization
- Use `React.memo()` for expensive components
- Memoize callbacks with `useCallback`
- Memoize computed values with `useMemo`
- Lazy load routes and heavy components
- Use code splitting

## Accessibility
- All interactive elements must be keyboard accessible
- Provide ARIA labels where needed
- Use semantic HTML
- Test with screen readers

## References
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)
- [React Official Docs](https://react.dev/)
```

---

## Advanced Patterns

### Multi-MCP Agent

Create agents that coordinate multiple MCP servers:

```markdown
---
description: 'Full-stack development agent integrating database, API, and frontend MCPs'
model: claude-3-5-sonnet-20241022
tools:
  - database-mcp
  - api-generator-mcp
  - frontend-scaffold-mcp
---

# Full Stack Developer Agent

Coordinates across database design, API development, and frontend implementation.

## Workflow
1. Design database schema using database-mcp
2. Generate API endpoints with api-generator-mcp
3. Scaffold frontend components with frontend-scaffold-mcp
4. Ensure consistent data flow across all layers

[Additional content...]
```

### Contextual Instructions

Instructions that adapt based on project context:

```markdown
---
description: Testing standards that adapt to project type
patterns:
  - '**/*.test.ts'
  - '**/*.spec.ts'
---

# Adaptive Testing Standards

## Project Type Detection
- **Backend API**: Focus on integration tests, API contracts
- **Frontend**: Component tests, user interaction tests
- **Library**: Unit tests, public API tests
- **CLI Tool**: Integration tests, command tests

[Standards that vary by detected project type...]
```

---

## Troubleshooting

### Agent Not Loading

**Problem:** Agent doesn't appear in Copilot
**Solutions:**
1. Check file name follows lowercase-hyphen pattern
2. Verify `.agent.md` extension
3. Validate YAML front matter syntax
4. Ensure description is wrapped in quotes
5. Restart Copilot/IDE

### Prompt Not Accessible

**Problem:** `/awesome-copilot <name>` doesn't work
**Solutions:**
1. Verify file is in `prompts/` directory
2. Check `.prompt.md` extension
3. Validate front matter has title and description
4. Rebuild with `npm run build`
5. Clear Copilot cache

### Instructions Not Auto-Applying

**Problem:** Instructions don't activate for matching files
**Solutions:**
1. Check glob patterns are correct
2. Test pattern matching with test files
3. Ensure patterns array is valid YAML
4. Verify file matches at least one pattern
5. Reload workspace

### Build Failures

**Problem:** `npm run build` fails
**Solutions:**
1. Run `npm run validate` to check syntax
2. Fix YAML front matter errors
3. Ensure all required fields present
4. Check for duplicate files
5. Run `bash scripts/fix-line-endings.sh`

### Line Ending Issues

**Problem:** Git shows unwanted changes
**Solutions:**
1. Run `bash scripts/fix-line-endings.sh`
2. Configure git: `git config core.autocrlf false`
3. Use LF (Unix) line endings
4. Configure editor to use LF

---

## Additional Resources

- [Awesome Copilot Repository](https://github.com/github/awesome-copilot)
- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [Claude Model Documentation](https://docs.anthropic.com/claude/docs)
- [MCP Protocol Specification](https://modelcontextprotocol.org/)
