---
applyTo:
  - "**/tests/**"
  - "**/test/**"
  - "**/__tests__/**"
  - "**/*.test.*"
  - "**/*.spec.*"
  - "**/cypress/**"
  - "**/playwright/**"
  - "**/e2e/**"
excludeAgent:
  - "code-review"  # Remove this line to enable for code review
---

# Testing Standards

## Core Principles
- Test behavior, not implementation
- Prefer integration tests over unit tests for most code
- Keep tests fast, deterministic, and independent
- Use the testing pyramid: many unit, some integration, few E2E
- Treat test code as production code (clean, maintainable)

## Test Organization

### File naming
```
src/
├── services/
│   └── user-service.ts
└── tests/
    └── services/
        └── user-service.test.ts    # Mirror source structure
```

### Test structure (AAA pattern)
```typescript
describe('UserService', () => {
  describe('createUser', () => {
    it('should create user with valid data', async () => {
      // Arrange
      const userData = { email: 'test@example.com', name: 'Test' };
      const mockRepo = createMockRepo();
      const service = new UserService(mockRepo);

      // Act
      const result = await service.createUser(userData);

      // Assert
      expect(result.email).toBe('test@example.com');
      expect(mockRepo.save).toHaveBeenCalledWith(expect.objectContaining(userData));
    });
  });
});
```

## Unit Tests

### Test pure functions thoroughly
```typescript
describe('calculateDiscount', () => {
  it.each([
    { price: 100, percent: 10, expected: 90 },
    { price: 100, percent: 0, expected: 100 },
    { price: 100, percent: 100, expected: 0 },
    { price: 50.50, percent: 20, expected: 40.40 },
  ])('returns $expected for $price with $percent% off', 
    ({ price, percent, expected }) => {
      expect(calculateDiscount(price, percent)).toBe(expected);
    }
  );

  it('throws for negative discount', () => {
    expect(() => calculateDiscount(100, -10)).toThrow('Invalid discount');
  });
});
```

### Mock external dependencies
```typescript
describe('OrderService', () => {
  let service: OrderService;
  let mockPaymentGateway: MockPaymentGateway;
  let mockOrderRepo: MockOrderRepository;

  beforeEach(() => {
    mockPaymentGateway = createMockPaymentGateway();
    mockOrderRepo = createMockOrderRepository();
    service = new OrderService(mockPaymentGateway, mockOrderRepo);
  });

  it('processes payment and creates order', async () => {
    mockPaymentGateway.charge.mockResolvedValue({ transactionId: 'tx_123' });

    const result = await service.createOrder({
      userId: 'user_1',
      items: [{ productId: 'prod_1', quantity: 2 }],
    });

    expect(result.status).toBe('confirmed');
    expect(mockPaymentGateway.charge).toHaveBeenCalledOnce();
    expect(mockOrderRepo.save).toHaveBeenCalledWith(
      expect.objectContaining({ transactionId: 'tx_123' })
    );
  });
});
```

## Integration Tests

### Test with real dependencies where practical
```typescript
describe('UserRepository (integration)', () => {
  let db: TestDatabase;
  let repository: UserRepository;

  beforeAll(async () => {
    db = await TestDatabase.create();
    repository = new UserRepository(db.connection);
  });

  afterAll(async () => {
    await db.destroy();
  });

  beforeEach(async () => {
    await db.truncate('users');
  });

  it('creates and retrieves user', async () => {
    const user = await repository.create({
      email: 'test@example.com',
      name: 'Test User',
    });

    const found = await repository.findById(user.id);

    expect(found).toEqual(user);
  });

  it('returns null for non-existent user', async () => {
    const result = await repository.findById('non-existent-id');
    expect(result).toBeNull();
  });
});
```

### Use Testcontainers for database tests
```typescript
import { PostgreSqlContainer } from '@testcontainers/postgresql';

describe('Database Integration', () => {
  let container: StartedPostgreSqlContainer;
  let db: Database;

  beforeAll(async () => {
    container = await new PostgreSqlContainer()
      .withDatabase('testdb')
      .start();

    db = new Database(container.getConnectionUri());
    await db.migrate();
  }, 60000);

  afterAll(async () => {
    await db.close();
    await container.stop();
  });

  // Tests...
});
```

## API Tests

### Test HTTP endpoints
```typescript
describe('POST /api/users', () => {
  it('creates user with valid data', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({
        email: 'new@example.com',
        name: 'New User',
        password: 'SecurePass123!',
      })
      .expect(201);

    expect(response.body.data).toMatchObject({
      email: 'new@example.com',
      name: 'New User',
    });
    expect(response.body.data.password).toBeUndefined();
  });

  it('returns 400 for missing required fields', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'test@example.com' })
      .expect(400);

    expect(response.body.error.code).toBe('VALIDATION_ERROR');
    expect(response.body.error.details).toContainEqual(
      expect.objectContaining({ field: 'name' })
    );
  });

  it('returns 409 for duplicate email', async () => {
    await createUser({ email: 'existing@example.com' });

    await request(app)
      .post('/api/users')
      .send({
        email: 'existing@example.com',
        name: 'User',
        password: 'Password123!',
      })
      .expect(409);
  });
});
```

## Frontend Component Tests

### Test user interactions
```typescript
import { render, screen, userEvent } from '@testing-library/react';

describe('LoginForm', () => {
  it('submits form with user credentials', async () => {
    const onSubmit = vi.fn();
    render(<LoginForm onSubmit={onSubmit} />);

    await userEvent.type(
      screen.getByLabelText(/email/i), 
      'user@example.com'
    );
    await userEvent.type(
      screen.getByLabelText(/password/i), 
      'password123'
    );
    await userEvent.click(
      screen.getByRole('button', { name: /sign in/i })
    );

    expect(onSubmit).toHaveBeenCalledWith({
      email: 'user@example.com',
      password: 'password123',
    });
  });

  it('displays validation errors', async () => {
    render(<LoginForm onSubmit={vi.fn()} />);

    await userEvent.click(
      screen.getByRole('button', { name: /sign in/i })
    );

    expect(screen.getByText(/email is required/i)).toBeInTheDocument();
    expect(screen.getByText(/password is required/i)).toBeInTheDocument();
  });

  it('disables submit button while loading', async () => {
    render(<LoginForm onSubmit={vi.fn()} isLoading />);

    expect(screen.getByRole('button', { name: /sign in/i })).toBeDisabled();
  });
});
```

## E2E Tests

### Use Playwright for E2E
```typescript
import { test, expect } from '@playwright/test';

test.describe('User Registration', () => {
  test('registers new user and redirects to dashboard', async ({ page }) => {
    await page.goto('/register');

    await page.getByLabel('Email').fill('newuser@example.com');
    await page.getByLabel('Name').fill('New User');
    await page.getByLabel('Password').fill('SecurePass123!');
    await page.getByLabel('Confirm Password').fill('SecurePass123!');
    
    await page.getByRole('button', { name: 'Create Account' }).click();

    await expect(page).toHaveURL('/dashboard');
    await expect(page.getByText('Welcome, New User')).toBeVisible();
  });

  test('shows error for existing email', async ({ page }) => {
    // Seed existing user
    await seedUser({ email: 'existing@example.com' });

    await page.goto('/register');
    await page.getByLabel('Email').fill('existing@example.com');
    await page.getByLabel('Name').fill('User');
    await page.getByLabel('Password').fill('Password123!');
    await page.getByLabel('Confirm Password').fill('Password123!');
    
    await page.getByRole('button', { name: 'Create Account' }).click();

    await expect(page.getByText('Email already registered')).toBeVisible();
  });
});
```

## Test Fixtures & Factories

### Create reusable factories
```typescript
// factories/user.ts
import { faker } from '@faker-js/faker';

export function buildUser(overrides: Partial<User> = {}): User {
  return {
    id: faker.string.uuid(),
    email: faker.internet.email(),
    name: faker.person.fullName(),
    createdAt: faker.date.past(),
    isActive: true,
    ...overrides,
  };
}

export async function createUser(
  db: Database, 
  overrides: Partial<CreateUserData> = {}
): Promise<User> {
  const data = buildUser(overrides);
  return db.users.create(data);
}
```

### Use fixtures for complex setup
```typescript
// fixtures/checkout.ts
export async function setupCheckoutScenario(db: Database) {
  const user = await createUser(db);
  const products = await createProducts(db, 3);
  const cart = await createCart(db, { userId: user.id, products });
  
  return { user, products, cart };
}
```

## Coverage Requirements

| Type | Target | Notes |
|------|--------|-------|
| Statements | 80% | Overall minimum |
| Branches | 75% | Decision coverage |
| Functions | 80% | All public functions |
| Lines | 80% | Line coverage |

### Configure coverage
```json
// vitest.config.ts or jest.config.js
{
  "coverage": {
    "provider": "v8",
    "reporter": ["text", "html", "lcov"],
    "exclude": [
      "**/*.test.ts",
      "**/tests/**",
      "**/migrations/**"
    ],
    "thresholds": {
      "statements": 80,
      "branches": 75,
      "functions": 80,
      "lines": 80
    }
  }
}
```

## Best Practices

### DO
- Write tests before or alongside code (TDD/Test-alongside)
- Test edge cases and error paths
- Use descriptive test names that document behavior
- Keep tests independent (no shared mutable state)
- Clean up test data (use transactions or truncation)

### DON'T
- Test implementation details (private methods, internal state)
- Use `sleep()` or fixed delays (use proper async waiting)
- Write brittle tests tied to UI structure
- Ignore flaky tests (fix root cause)
- Test third-party code (mock it instead)
