---
applyTo:
  - "**/*.md"
  - "**/docs/**"
  - "**/README*"
  - "**/CHANGELOG*"
  - "**/CONTRIBUTING*"
  - "**/*.mdx"
excludeAgent:
  - "code-review"  # Remove this line to enable for code review
---

# Documentation Standards

## Core Principles
- Documentation is part of the product, not an afterthought
- Keep documentation close to code (same repo)
- Write for your audience (user vs developer vs operator)
- Update docs when code changes
- Use clear, concise language

## Document Types

| Type | Purpose | Audience |
|------|---------|----------|
| README | Project overview, quick start | Everyone |
| API Docs | Endpoint reference | Developers |
| Guides | How to accomplish tasks | Users/Developers |
| Architecture | System design decisions | Developers/Architects |
| Runbooks | Operational procedures | Operations |
| ADRs | Decision records | Team members |

## README Structure

Every project should have a README with:

```markdown
# Project Name

> Brief one-line description

## Overview
What this project does and why it exists. 2-3 sentences max.

## Quick Start
\`\`\`bash
# Get running in under 5 minutes
npm install
npm run dev
\`\`\`

## Features
- Feature 1
- Feature 2
- Feature 3

## Documentation
- [Getting Started](./docs/getting-started.md)
- [API Reference](./docs/api.md)
- [Contributing](./CONTRIBUTING.md)

## Requirements
- Node.js 20+
- PostgreSQL 16+

## Installation
Step-by-step installation instructions.

## Configuration
Environment variables and configuration options.

## Usage
Common usage examples.

## Contributing
How to contribute to this project.

## License
MIT License - see [LICENSE](./LICENSE)
```

## Writing Style

### DO
- Use active voice: "The system creates a log entry" not "A log entry is created"
- Use present tense: "The function returns" not "The function will return"
- Be specific: "Takes 2-3 seconds" not "Takes some time"
- Use second person: "You can configure" not "Users can configure"
- Include examples for every concept

### DON'T
- Use jargon without explanation
- Assume knowledge not previously documented
- Write walls of text without structure
- Leave TODOs in published documentation
- Use vague language: "might", "probably", "sometimes"

## Markdown Formatting

### Headers
```markdown
# H1 - Document Title (one per document)
## H2 - Major Sections
### H3 - Subsections
#### H4 - Minor Points (use sparingly)
```

### Code Blocks
Always specify the language:
```markdown
\`\`\`typescript
const greeting: string = "Hello, World!";
\`\`\`
```

### Links
```markdown
[Descriptive text](./path/to/file.md)  # Relative links preferred
[External resource](https://example.com)
```

### Tables
```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data     | Data     | Data     |
```

### Callouts/Admonitions
```markdown
> **Note**: Important information

> **Warning**: Critical warnings

> **Tip**: Helpful suggestions

> **Example**: Usage examples
```

## API Documentation

### Document all endpoints
```markdown
## Create User

Creates a new user account.

### Request

\`POST /api/v1/users\`

#### Headers

| Header | Required | Description |
|--------|----------|-------------|
| Authorization | Yes | Bearer token |
| Content-Type | Yes | application/json |

#### Body

\`\`\`json
{
  "email": "user@example.com",
  "name": "John Doe",
  "role": "user"
}
\`\`\`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string | Yes | Valid email address |
| name | string | Yes | Full name (1-100 chars) |
| role | string | No | User role (default: "user") |

### Response

#### Success (201 Created)

\`\`\`json
{
  "data": {
    "id": "usr_abc123",
    "email": "user@example.com",
    "name": "John Doe",
    "role": "user",
    "createdAt": "2024-01-15T10:30:00Z"
  }
}
\`\`\`

#### Errors

| Code | Description |
|------|-------------|
| 400 | Validation error |
| 409 | Email already exists |
| 401 | Invalid authentication |

### Example

\`\`\`bash
curl -X POST https://api.example.com/api/v1/users \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "name": "John Doe"}'
\`\`\`
```

## Code Documentation

### Function/Method Documentation
```typescript
/**
 * Calculates the total price including tax and discounts.
 *
 * @param items - Array of cart items with price and quantity
 * @param taxRate - Tax rate as decimal (e.g., 0.08 for 8%)
 * @param discountCode - Optional discount code to apply
 * @returns The total price after tax and discounts
 * @throws {InvalidDiscountError} If discount code is invalid
 *
 * @example
 * const total = calculateTotal(
 *   [{ price: 10, quantity: 2 }],
 *   0.08,
 *   'SAVE10'
 * );
 * // Returns: 19.44 (after 10% discount + 8% tax)
 */
function calculateTotal(
  items: CartItem[],
  taxRate: number,
  discountCode?: string
): number
```

## Architecture Documentation

### Architecture Decision Records (ADRs)
```markdown
# ADR-001: Use PostgreSQL for Primary Database

## Status
Accepted

## Context
We need a primary database for storing user data and transactions.
Requirements:
- ACID compliance
- Complex query support
- Horizontal scaling capability
- Strong community and tooling

## Decision
We will use PostgreSQL 16 as our primary database.

## Consequences

### Positive
- Excellent query performance for complex queries
- Strong data integrity with ACID compliance
- Rich ecosystem of tools and extensions
- Team familiarity

### Negative
- Requires more operational expertise than managed NoSQL
- Horizontal scaling requires additional tooling (Citus, etc.)

## Alternatives Considered
- MySQL: Less feature-rich for our use case
- MongoDB: ACID limitations, different query patterns
- CockroachDB: Higher operational complexity
```

## Changelog

### Keep a CHANGELOG
```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New feature description

### Changed
- Changed behavior description

### Deprecated
- Deprecated feature description

### Removed
- Removed feature description

### Fixed
- Bug fix description

### Security
- Security fix description

## [1.0.0] - 2024-01-15

### Added
- Initial release with core features
```

## Documentation Organization

```
docs/
├── README.md              # Documentation index
├── getting-started/
│   ├── installation.md
│   ├── configuration.md
│   └── quick-start.md
├── guides/
│   ├── authentication.md
│   ├── deployment.md
│   └── troubleshooting.md
├── api/
│   ├── overview.md
│   ├── authentication.md
│   └── endpoints/
│       ├── users.md
│       └── orders.md
├── architecture/
│   ├── overview.md
│   ├── decisions/
│   │   ├── adr-001-database.md
│   │   └── adr-002-auth.md
│   └── diagrams/
└── contributing/
    ├── development.md
    ├── testing.md
    └── style-guide.md
```

## Review Checklist

Before publishing documentation:
- [ ] Spell check completed
- [ ] Links verified (internal and external)
- [ ] Code examples tested and working
- [ ] Screenshots are current
- [ ] No sensitive information included
- [ ] Table of contents updated
- [ ] Version numbers accurate
