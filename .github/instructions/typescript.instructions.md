---
applyTo:
  - "**/*.ts"
  - "**/*.tsx"
  - "**/*.mts"
  - "**/*.cts"
  - "**/*.js"
  - "**/*.jsx"
  - "**/*.mjs"
  - "**/*.cjs"
excludeAgent:
  - "code-review"  # Remove this line to enable for code review
---

# TypeScript/JavaScript Development Standards

## Language Version & Configuration
- Use TypeScript 5.0+ with strict mode enabled
- Target ES2022+ for modern JavaScript features
- Enable `strictNullChecks`, `noImplicitAny`, `strictFunctionTypes`

## Type Safety

### DO: Use explicit types for function signatures
```typescript
function processUser(user: User): ProcessedUser {
  return { ...user, processed: true };
}
```

### DON'T: Use `any` type
```typescript
// ❌ Avoid
function process(data: any): any { ... }

// ✅ Prefer
function process<T extends BaseData>(data: T): ProcessedData<T> { ... }
```

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Files (components) | PascalCase | `UserProfile.tsx` |
| Files (utilities) | camelCase | `formatDate.ts` |
| Interfaces | PascalCase with `I` prefix optional | `User` or `IUser` |
| Types | PascalCase | `UserResponse` |
| Enums | PascalCase | `UserStatus` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| Functions | camelCase | `getUserById` |
| Variables | camelCase | `userCount` |

## Modern Patterns

### Prefer async/await over callbacks
```typescript
// ✅ Prefer
async function fetchUser(id: string): Promise<User> {
  const response = await api.get(`/users/${id}`);
  return response.data;
}
```

### Use nullish coalescing and optional chaining
```typescript
const name = user?.profile?.name ?? 'Anonymous';
```

### Use const assertions for literal types
```typescript
const CONFIG = {
  endpoint: '/api/v1',
  timeout: 5000,
} as const;
```

## Error Handling

### Use typed error handling
```typescript
class ApiError extends Error {
  constructor(
    message: string,
    public readonly statusCode: number,
    public readonly code: string
  ) {
    super(message);
    this.name = 'ApiError';
  }
}
```

### Always handle Promise rejections
```typescript
try {
  await riskyOperation();
} catch (error) {
  if (error instanceof ApiError) {
    logger.error(`API Error: ${error.code}`, { statusCode: error.statusCode });
  } else {
    logger.error('Unexpected error', { error });
  }
  throw error;
}
```

## Import Organization
1. External packages (node_modules)
2. Internal packages (@company/*)
3. Absolute imports from src
4. Relative imports
5. Type-only imports last

```typescript
import { useState } from 'react';
import { Button } from '@company/ui';
import { api } from 'src/lib/api';
import { formatDate } from '../utils';
import type { User } from '../types';
```

## React-Specific (if applicable)

### Prefer functional components with hooks
```typescript
const UserProfile: React.FC<UserProfileProps> = ({ userId }) => {
  const [user, setUser] = useState<User | null>(null);
  // ...
};
```

### Use proper event typing
```typescript
const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
  event.preventDefault();
  // ...
};
```

## Testing Requirements
- Use Jest or Vitest for unit tests
- Use React Testing Library for component tests
- Minimum 80% code coverage for new code
- Test file naming: `*.test.ts` or `*.spec.ts`

## Documentation
- Use JSDoc for public APIs
- Include `@param`, `@returns`, `@throws`, `@example` tags
- Document complex business logic inline

```typescript
/**
 * Calculates the user's subscription tier based on usage.
 *
 * @param usage - Monthly usage metrics
 * @returns The calculated tier and pricing
 * @throws {InvalidUsageError} When usage data is malformed
 *
 * @example
 * const tier = calculateTier({ apiCalls: 10000, storage: 5 });
 */
```
