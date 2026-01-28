# Awesome Copilot - Complete Usage Guide

Comprehensive guide to using the Awesome Copilot skill with Claude Code for creating GitHub Copilot customizations including agents, prompts, instructions, and collections.

## Table of Contents

- [How to Invoke This Skill](#how-to-invoke-this-skill)
- [Component Types Overview](#component-types-overview)
- [Complete Use Cases](#complete-use-cases)
- [Component Examples](#component-examples)
- [Validation Workflows](#validation-workflows)
- [Best Practices](#best-practices)
- [Advanced Patterns](#advanced-patterns)

---

## How to Invoke This Skill

### Automatic Activation

Claude automatically activates this skill when you use these **trigger keywords**:

- `copilot agent`, `GitHub Copilot agent`, `custom agent`
- `copilot prompt`, `custom prompt`, `prompt template`
- `instruction file`, `copilot instructions`, `coding standards`
- `copilot collection`, `customization collection`
- `copilot customization`, `extend copilot`
- `validate agent`, `validate prompt`

### Explicit Requests

Be clear about what type of customization you want to create:

```
✅ GOOD: "Create a GitHub Copilot agent for Python testing with pytest"
✅ GOOD: "Write a custom prompt for generating API documentation"
✅ GOOD: "Make an instruction file for React component best practices"
✅ GOOD: "Build a collection for full-stack TypeScript development"

⚠️ VAGUE: "Help me with Copilot"
⚠️ VAGUE: "Make a custom thing"
```

### Example Invocation Patterns

```bash
# Creating agents
"Create a Copilot agent specialized in Python testing"
"Build an agent for reviewing TypeScript code"

# Creating prompts
"Write a prompt for generating REST API endpoints"
"Create a prompt that helps write unit tests"

# Creating instructions
"Make instructions for React component structure"
"Create coding standards for Python type hints"

# Creating collections
"Build a collection for Django development"
"Create a full-stack React + Node.js collection"
```

---

## Component Types Overview

### 🤖 Agents

**What they are**: Specialized AI assistants with specific expertise, tools, and models

**When to use**:
- Need focused expertise (e.g., security review, testing)
- Want to use specific tools or MCP servers
- Require a particular Claude model (Sonnet, Opus, Haiku)
- Building a specialized workflow

**File format**: `<name>.agent.md`

---

### 💬 Prompts

**What they are**: Reusable task templates invoked with slash commands

**When to use**:
- Repetitive tasks (e.g., "add tests", "write docs")
- Standardized workflows
- Quick one-off tasks
- Team-wide task templates

**File format**: `<name>.prompt.md`
**Usage**: `/awesome-copilot <prompt-name>`

---

### 📋 Instructions

**What they are**: Auto-applying coding standards for specific file patterns

**When to use**:
- Enforce coding standards
- Apply patterns automatically
- Maintain consistency across codebase
- Provide context-specific guidance

**File format**: `<name>.instructions.md`
**Auto-applies**: Based on glob patterns (e.g., `**/*.tsx`)

---

### 📦 Collections

**What they are**: Curated bundles of agents, prompts, and instructions

**When to use**:
- Package related customizations
- Share team workflows
- Provide domain-specific toolkits
- Onboard new team members

**File format**: `<name>.collection.md`

---

## Complete Use Cases

### Use Case 1: Creating a Testing Agent

**Scenario**: Build an agent specialized in writing and reviewing tests

**Step-by-step workflow**:

1. **Request the task**:
```
"Create a GitHub Copilot agent for Python testing with pytest. It should help write unit tests, fixtures, and mocks."
```

2. **Claude will create**:

**File**: `python-testing.agent.md`

```markdown
---
description: 'Expert Python testing assistant using pytest. Writes unit tests, fixtures, mocks, and provides testing best practices.'
model: claude-3-5-sonnet-20241022
tools:
  - mcp-server-pytest
---

# Python Testing Agent

Expert assistant for Python testing with pytest.

## Expertise

- Writing comprehensive unit tests
- Creating pytest fixtures
- Mocking external dependencies
- Parameterized testing
- Test organization and structure
- Coverage analysis

## Guidelines

When writing tests:
1. Use descriptive test names following AAA pattern (Arrange, Act, Assert)
2. Create reusable fixtures in conftest.py
3. Use pytest.mark for test categorization
4. Mock external dependencies appropriately
5. Aim for high code coverage
6. Include edge cases and error scenarios

## Example Test Structure

```python
import pytest
from myapp import User

@pytest.fixture
def user():
    return User(name="Test User", email="test@example.com")

def test_user_creation(user):
    """Test that user is created with correct attributes."""
    assert user.name == "Test User"
    assert user.email == "test@example.com"

def test_user_validation():
    """Test that invalid email raises ValueError."""
    with pytest.raises(ValueError):
        User(name="Test", email="invalid-email")
```

## Common Patterns

- Use `@pytest.mark.parametrize` for multiple test cases
- Use `@pytest.fixture(scope="session")` for expensive setup
- Use `monkeypatch` for environment variables
- Use `tmp_path` for file system tests
```

3. **How to use it**:
```
# Activate agent in conversation
@python-testing "Write tests for my User class"

# Agent will provide comprehensive tests with fixtures
```

**Expected outcome**:
- Specialized agent file created
- Proper YAML frontmatter
- Testing expertise documented
- Example patterns included
- Ready to use in Copilot

---

### Use Case 2: Creating a Documentation Prompt

**Scenario**: Build a reusable prompt for generating API documentation

**Step-by-step workflow**:

1. **Request the task**:
```
"Create a Copilot prompt that generates API documentation for Python FastAPI endpoints"
```

2. **Claude will create**:

**File**: `api-docs.prompt.md`

```markdown
---
title: Generate API Documentation
description: Creates comprehensive API documentation for FastAPI endpoints including parameters, responses, and examples
---

# Generate API Documentation

Analyzes FastAPI endpoint code and generates complete documentation.

## Task

For the provided FastAPI endpoint:

1. Extract endpoint details:
   - HTTP method and path
   - Request parameters (path, query, body)
   - Response models and status codes
   - Authentication requirements

2. Generate documentation including:
   - Endpoint description
   - Parameter specifications with types and examples
   - Response schema
   - Example requests and responses
   - Error responses

3. Format as:
   - OpenAPI/Swagger compatible
   - Markdown for README
   - Inline docstrings

## Example Input

```python
@app.post("/users/{user_id}/posts")
async def create_post(
    user_id: int,
    post: PostCreate,
    current_user: User = Depends(get_current_user)
):
    ...
```

## Expected Output

```markdown
### POST /users/{user_id}/posts

Create a new post for a specific user.

**Authentication**: Required

**Parameters**:
- `user_id` (path, integer): The ID of the user
- `post` (body, PostCreate): Post data including title and content

**Request Body**:
```json
{
  "title": "My Post",
  "content": "Post content here"
}
```

**Responses**:
- `201 Created`: Post created successfully
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: User not authorized
- `404 Not Found`: User not found
```
```

3. **How to use it**:
```
# In Claude Code or Copilot
/awesome-copilot api-docs

# Point to your FastAPI code
# Prompt will generate documentation
```

**Expected outcome**:
- Reusable prompt template
- Slash command ready
- Clear task description
- Example input/output
- Team can use consistently

---

### Use Case 3: Creating React Instructions

**Scenario**: Auto-apply React component best practices to all `.tsx` files

**Step-by-step workflow**:

1. **Request the task**:
```
"Create instructions for React TypeScript components that enforce best practices like prop types, hooks rules, and component structure"
```

2. **Claude will create**:

**File**: `react-components.instructions.md`

```markdown
---
description: Best practices for React TypeScript components including hooks, props, and structure
patterns:
  - "**/*.tsx"
  - "**/*.jsx"
---

# React Component Instructions

Automatically applied to React component files.

## Component Structure

```typescript
// 1. Imports (grouped)
import React, { useState, useEffect } from 'react';
import type { FC } from 'react';

// 2. Type definitions
interface UserProfileProps {
  userId: string;
  onUpdate?: (user: User) => void;
}

// 3. Component definition
export const UserProfile: FC<UserProfileProps> = ({ userId, onUpdate }) => {
  // 4. Hooks (top level, same order)
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadUser(userId);
  }, [userId]);

  // 5. Event handlers
  const handleUpdate = () => {
    if (user && onUpdate) {
      onUpdate(user);
    }
  };

  // 6. Render logic
  if (loading) return <Loading />;
  if (!user) return <NotFound />;

  return (
    <div className="user-profile">
      {/* JSX */}
    </div>
  );
};
```

## Rules to Follow

### Props
- Always define TypeScript interfaces for props
- Use optional props with `?` for non-required
- Provide default values using destructuring
- Document complex props with JSDoc

### Hooks
- Call hooks at top level only
- Don't call hooks conditionally
- List all dependencies in useEffect/useMemo/useCallback
- Extract custom hooks when logic is reused

### State Management
- Use useState for local component state
- Use useReducer for complex state logic
- Lift state up when shared between components
- Use context for deeply nested prop drilling

### Performance
- Memoize expensive calculations with useMemo
- Memoize callbacks passed to children with useCallback
- Use React.memo for pure components
- Avoid inline functions in JSX when possible

### Naming Conventions
- Components: PascalCase (UserProfile)
- Hooks: camelCase starting with 'use' (useUserData)
- Event handlers: 'handle' prefix (handleClick)
- Boolean props: 'is/has/should' prefix (isLoading)

### File Organization
- One component per file
- Co-locate related components in folders
- Name file same as component (UserProfile.tsx)
- Place tests next to components (UserProfile.test.tsx)

## Examples

**Good**:
```typescript
const MyComponent: FC<Props> = ({ data, onUpdate }) => {
  const [state, setState] = useState(0);

  useEffect(() => {
    // effect
  }, [data]);

  return <div>{data}</div>;
};
```

**Bad**:
```typescript
// No types, conditional hooks, inline handlers
const MyComponent = ({ data }) => {
  if (data) {
    useState(0); // ❌ Conditional hook
  }

  return <div onClick={() => alert('hi')}>{data}</div>; // ❌ Inline function
};
```
```

3. **How it works**:
- Automatically activates when editing `.tsx` or `.jsx` files
- Provides context-specific guidance
- Enforces best practices
- No manual invocation needed

**Expected outcome**:
- Instructions file created
- Auto-applies to React files
- Comprehensive best practices
- Examples included
- Consistent code across team

---

### Use Case 4: Creating a Full-Stack Collection

**Scenario**: Bundle agents, prompts, and instructions for full-stack TypeScript development

**Step-by-step workflow**:

1. **Request the task**:
```
"Create a GitHub Copilot collection for full-stack TypeScript development with React, Node.js, and PostgreSQL. Include agents, prompts, and instructions."
```

2. **Claude will create**:

**File**: `fullstack-typescript.collection.md`

```markdown
---
title: Full-Stack TypeScript Development
description: Complete toolkit for React + Node.js + PostgreSQL development with TypeScript
---

# Full-Stack TypeScript Development Collection

Comprehensive customizations for modern full-stack TypeScript development.

## Overview

This collection provides specialized agents, task prompts, and auto-applying instructions for building full-stack applications with:
- **Frontend**: React + TypeScript
- **Backend**: Node.js + Express + TypeScript
- **Database**: PostgreSQL
- **Testing**: Jest + Playwright

## Included Components

### Agents

- **[react-expert](../agents/react-expert.agent.md)**
  - Purpose: Frontend React development specialist
  - Best for: Component design, hooks, state management

- **[backend-api](../agents/backend-api.agent.md)**
  - Purpose: RESTful API development with Express
  - Best for: Endpoints, middleware, validation

- **[database-architect](../agents/database-architect.agent.md)**
  - Purpose: PostgreSQL schema design and optimization
  - Best for: Migrations, queries, indexing

### Prompts

- **[add-api-endpoint](../prompts/add-api-endpoint.prompt.md)**
  - Use: `/awesome-copilot add-api-endpoint`
  - Purpose: Generate new Express API endpoint

- **[create-react-component](../prompts/create-react-component.prompt.md)**
  - Use: `/awesome-copilot create-react-component`
  - Purpose: Scaffold new React component

- **[write-integration-test](../prompts/write-integration-test.prompt.md)**
  - Use: `/awesome-copilot write-integration-test`
  - Purpose: Generate API integration tests

### Instructions

- **[react-components](../instructions/react-components.instructions.md)**
  - Applies to: `**/*.tsx`, `**/*.jsx`
  - Purpose: React component best practices

- **[typescript-backend](../instructions/typescript-backend.instructions.md)**
  - Applies to: `**/api/**/*.ts`, `**/server/**/*.ts`
  - Purpose: Backend code standards

- **[database-migrations](../instructions/database-migrations.instructions.md)**
  - Applies to: `**/migrations/**/*.sql`
  - Purpose: Database migration standards

## Use Cases

### Use Case 1: New Feature Development

**Scenario**: Build a new user authentication feature

**Workflow**:
1. Use `database-architect` agent to design auth schema
   ```
   @database-architect "Design a user authentication schema with email/password"
   ```

2. Create API endpoints with prompt
   ```
   /awesome-copilot add-api-endpoint
   # Describe: POST /api/auth/register and /api/auth/login
   ```

3. Build React components
   ```
   /awesome-copilot create-react-component
   # Component: LoginForm, RegistrationForm
   ```

4. Instructions auto-apply best practices to all files

---

### Use Case 2: Code Review & Refactoring

**Scenario**: Review and improve existing code

**Workflow**:
1. Use `react-expert` for frontend review
   ```
   @react-expert "Review this component for performance issues"
   ```

2. Use `backend-api` for API review
   ```
   @backend-api "Check this endpoint for security vulnerabilities"
   ```

3. Instructions guide refactoring as you edit

---

### Use Case 3: Testing Workflow

**Scenario**: Add comprehensive tests to new feature

**Workflow**:
1. Generate API tests
   ```
   /awesome-copilot write-integration-test
   # Test: User registration and login flow
   ```

2. Create component tests
   ```
   @react-expert "Write tests for the LoginForm component"
   ```

3. Test database queries
   ```
   @database-architect "Create test fixtures for user data"
   ```

## Getting Started

### Prerequisites
- [ ] GitHub Copilot installed
- [ ] Claude Code CLI
- [ ] TypeScript project setup
- [ ] Node.js 18+

### Installation
```bash
# Copy collection to your project
cp -r awesome-copilot/.github/copilot/customizations/ \
      your-project/.github/copilot/

# Or install globally
cp -r awesome-copilot/.github/copilot/customizations/ \
      ~/.github/copilot/
```

### Quick Start

1. **Start with agent**: Pick an agent based on task
   ```
   @react-expert - Frontend work
   @backend-api - API development
   @database-architect - Database design
   ```

2. **Use prompts for common tasks**
   ```
   /awesome-copilot add-api-endpoint
   /awesome-copilot create-react-component
   /awesome-copilot write-integration-test
   ```

3. **Let instructions guide you**: Edit files and instructions auto-apply

## Best Practices

1. **Start broad, then specialize**: Begin with general agent, then use specific prompts
2. **Chain prompts**: Use multiple prompts in sequence for complex tasks
3. **Let instructions work**: They provide context automatically
4. **Validate output**: Use validation tools to check formatting

## Related Collections
- **[Testing Collection](./testing.collection.md)**: Comprehensive testing toolkit
- **[DevOps Collection](./devops.collection.md)**: CI/CD and deployment tools
```

3. **How to use it**:
- Install collection in project or globally
- Access all agents, prompts, instructions
- Follow guided workflows
- Customize as needed

**Expected outcome**:
- Complete collection file
- All components linked
- Use cases documented
- Getting started guide
- Team-ready toolkit

---

## Component Examples

### Complete Agent Example

```markdown
---
description: 'Security code reviewer specializing in OWASP Top 10 vulnerabilities'
model: claude-3-5-sonnet-20241022
tools:
  - mcp-server-security
---

# Security Reviewer Agent

Expert at identifying security vulnerabilities in code.

## Expertise
- OWASP Top 10 vulnerabilities
- SQL injection detection
- XSS prevention
- Authentication/authorization flaws
- Cryptography best practices

## Review Checklist
- [ ] Input validation
- [ ] Output encoding
- [ ] Authentication checks
- [ ] Authorization verification
- [ ] Secure data storage
- [ ] Error handling
- [ ] Dependency vulnerabilities
```

---

### Complete Prompt Example

```markdown
---
title: Add Error Handling
description: Wraps code with comprehensive try-catch error handling
---

# Add Error Handling

Adds proper error handling to existing code.

## Task

1. Analyze the provided code
2. Identify potential error points
3. Add try-catch blocks
4. Include logging
5. Return user-friendly error messages

## Example

**Input**:
```javascript
async function fetchUser(id) {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
}
```

**Output**:
```javascript
async function fetchUser(id) {
  try {
    const response = await fetch(`/api/users/${id}`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Failed to fetch user:', error);
    throw new Error('Failed to load user data. Please try again.');
  }
}
```

---

### Complete Instruction Example

```markdown
---
description: Python type hints and docstring standards
patterns:
  - "**/*.py"
---

# Python Type Hints Instructions

## Type Hints
Always include type hints for:
- Function parameters
- Function return values
- Class attributes
- Module-level variables

## Docstrings
Use Google-style docstrings:

```python
def calculate_total(items: list[Item], tax_rate: float) -> Decimal:
    """Calculate total price including tax.

    Args:
        items: List of items to calculate total for
        tax_rate: Tax rate as decimal (e.g., 0.08 for 8%)

    Returns:
        Total price including tax as Decimal

    Raises:
        ValueError: If tax_rate is negative
    """
```

---

## Validation Workflows

### Validating Agent Files

1. **Request validation**:
```
"Validate my agent file security-reviewer.agent.md"
```

2. **Claude will check**:
- YAML frontmatter syntax
- Required fields present
- Description length (max 1024 chars)
- Model name valid
- Tools array format
- File naming convention

3. **Get results**:
```
✓ Valid YAML frontmatter
✓ Description present and valid length
✓ Model: claude-3-5-sonnet-20241022 (valid)
✓ Tools array properly formatted
✓ Filename follows convention: lowercase-hyphen.agent.md

Status: VALID ✓
```

---

### Validating Prompt Files

1. **Request validation**:
```
"Validate my prompts directory"
```

2. **Claude will check all prompts**:
- Required fields (title, description)
- YAML syntax
- File naming conventions
- No empty descriptions

3. **Get results**:
```
Validating prompts/...

✓ api-docs.prompt.md - Valid
✓ add-tests.prompt.md - Valid
✗ BadName.prompt.md - Error: Must be lowercase with hyphens

2/3 prompts valid
```

---

### Validation Script Usage

```bash
# Validate all customization files
python scripts/validator.py

# Validate specific directory
python scripts/validator.py agents/
python scripts/validator.py prompts/

# Expected output
==========================================
Validation Results: 12/12 files valid
==========================================

✅ All files validated successfully!
```

---

## Best Practices

### 1. Naming Conventions

**Files**:
```
✅ GOOD:
- python-testing.agent.md
- api-docs.prompt.md
- react-components.instructions.md
- fullstack-typescript.collection.md

❌ BAD:
- Python_Testing.agent.md (no underscores)
- ApiDocs.prompt.md (not lowercase)
- react components.instructions.md (no spaces)
```

**Agent/Prompt Names**:
- Use descriptive names: `security-reviewer` not `reviewer1`
- Include domain: `python-testing` not just `testing`
- Keep concise: 2-4 words maximum

---

### 2. Writing Descriptions

**Agents**:
```
✅ GOOD: "Expert Python testing assistant using pytest. Writes unit tests, fixtures, mocks, and provides testing best practices."

❌ VAGUE: "Helps with testing"
```

**Prompts**:
```
✅ GOOD: "Creates comprehensive API documentation for FastAPI endpoints including parameters, responses, and examples"

❌ VAGUE: "Makes docs"
```

---

### 3. Organizing Collections

**Structure**:
```
.github/copilot/customizations/
├── agents/
│   ├── react-expert.agent.md
│   ├── backend-api.agent.md
│   └── database-architect.agent.md
├── prompts/
│   ├── add-api-endpoint.prompt.md
│   ├── create-react-component.prompt.md
│   └── write-integration-test.prompt.md
├── instructions/
│   ├── react-components.instructions.md
│   ├── typescript-backend.instructions.md
│   └── database-migrations.instructions.md
└── collections/
    ├── fullstack-typescript.collection.md
    └── testing.collection.md
```

---

### 4. Choosing the Right Model

**Agents**:
- **Sonnet** (`claude-3-5-sonnet-20241022`): Balanced, most use cases
- **Opus** (`claude-3-opus-20240229`): Complex reasoning, architecture
- **Haiku** (`claude-3-haiku-20240307`): Fast, simple tasks

**Example**:
```yaml
# For complex architectural decisions
model: claude-3-opus-20240229

# For quick code reviews
model: claude-3-haiku-20240307

# For most development tasks
model: claude-3-5-sonnet-20241022
```

---

### 5. Writing Effective Glob Patterns

**Instructions**:
```yaml
# Match all TypeScript React components
patterns:
  - "**/*.tsx"
  - "**/*.jsx"

# Match only API route files
patterns:
  - "**/api/**/*.ts"
  - "**/routes/**/*.ts"

# Match test files
patterns:
  - "**/*.test.ts"
  - "**/*.spec.ts"

# Match configuration files
patterns:
  - "**/.eslintrc.*"
  - "**/tsconfig.json"
```

---

## Advanced Patterns

### Pattern 1: Multi-Agent Workflow

**Scenario**: Complex feature requiring multiple specialists

```
1. @database-architect "Design schema for user notifications"
2. @backend-api "Create API endpoints for notifications"
3. @react-expert "Build notification UI components"
4. @security-reviewer "Review entire notification system"
```

---

### Pattern 2: Prompt Chaining

**Scenario**: Build feature step-by-step with prompts

```
1. /awesome-copilot create-component
   # Create NotificationBell component

2. /awesome-copilot add-api-endpoint
   # Add GET /api/notifications endpoint

3. /awesome-copilot write-tests
   # Generate tests for both

4. /awesome-copilot add-docs
   # Document the feature
```

---

### Pattern 3: Context-Aware Instructions

**Scenario**: Different standards for different parts of codebase

```yaml
# frontend-react.instructions.md
patterns:
  - "**/src/components/**/*.tsx"
  - "**/src/pages/**/*.tsx"
# → React-specific standards

# backend-api.instructions.md
patterns:
  - "**/src/api/**/*.ts"
  - "**/src/services/**/*.ts"
# → Backend-specific standards

# shared-utils.instructions.md
patterns:
  - "**/src/utils/**/*.ts"
  - "**/src/lib/**/*.ts"
# → General utility standards
```

---

### Pattern 4: Team Distribution

**Scenario**: Share customizations with team via git

```bash
# .github/copilot/customizations/ (committed to repo)
agents/
  team-agent-1.agent.md
  team-agent-2.agent.md
prompts/
  team-prompt-1.prompt.md
instructions/
  team-standard-1.instructions.md

# Team members get customizations automatically
git clone repo
cd repo
# Customizations active in this project
```

---

## Additional Resources

- [SKILL.md](SKILL.md) - Main skill instructions and templates
- [GitHub Awesome Copilot](https://github.com/github/awesome-copilot) - Official repository
- [Validator Script](scripts/validator.py) - Validation tool

---

## Common Questions

**Q: Can I use MCP servers with agents?**
A: Yes! List MCP server names in the `tools` array:
```yaml
tools:
  - mcp-server-playwright
  - mcp-server-fetch
```

**Q: How do I test my customizations?**
A: Use them in Copilot:
- Agents: `@agent-name "task"`
- Prompts: `/awesome-copilot prompt-name`
- Instructions: Auto-apply when editing matching files

**Q: Can I modify the templates?**
A: Absolutely! Templates are starting points. Customize for your needs.

**Q: Where should I install customizations?**
A:
- **Personal**: `~/.github/copilot/customizations/` (all your projects)
- **Project**: `<project>/.github/copilot/customizations/` (team-shared)

**Q: How do I share with my team?**
A: Commit `.github/copilot/customizations/` to your repository. Team gets them via git clone/pull.

---

## Troubleshooting

### Agent not activating
- Check file is in `agents/` directory
- Verify YAML frontmatter is valid
- Ensure filename ends with `.agent.md`
- Restart Copilot if needed

### Prompt not showing in slash commands
- Check file is in `prompts/` directory
- Verify frontmatter has `title` and `description`
- Filename must end with `.prompt.md`
- Try `/awesome-copilot --refresh`

### Instructions not auto-applying
- Verify file is in `instructions/` directory
- Check `patterns` glob matches your files
- Filename must end with `.instructions.md`
- Test pattern with: `ls -la <pattern>`

### Validation errors
- Run validator: `python scripts/validator.py`
- Check YAML syntax (3 hyphens, proper indentation)
- Verify all required fields present
- Use lowercase-hyphen naming
