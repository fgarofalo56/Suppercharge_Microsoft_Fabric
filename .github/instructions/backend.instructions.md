---
applyTo:
  - "**/src/api/**"
  - "**/src/controllers/**"
  - "**/src/routes/**"
  - "**/src/services/**"
  - "**/src/middleware/**"
  - "**/api/**"
  - "**/server/**"
excludeAgent:
  - "code-review"  # Remove this line to enable for code review
---

# Backend API Development Standards

## Core Principles
- RESTful design with consistent conventions
- Proper HTTP status codes and error responses
- Input validation at the API boundary
- Structured logging and observability
- Rate limiting and security headers

## API Design

### URL Structure
```
# Resources (nouns, plural)
GET    /api/v1/users           # List users
POST   /api/v1/users           # Create user
GET    /api/v1/users/:id       # Get user
PATCH  /api/v1/users/:id       # Update user
DELETE /api/v1/users/:id       # Delete user

# Nested resources
GET    /api/v1/users/:id/orders    # User's orders
POST   /api/v1/users/:id/orders    # Create order for user

# Actions (when CRUD doesn't fit)
POST   /api/v1/users/:id/activate
POST   /api/v1/orders/:id/cancel

# Filtering, sorting, pagination
GET    /api/v1/users?status=active&sort=-created_at&page=2&limit=20
```

### HTTP Status Codes

| Code | Usage |
|------|-------|
| 200 | Success with body |
| 201 | Created (include Location header) |
| 204 | Success, no content (DELETE) |
| 400 | Bad request (validation error) |
| 401 | Unauthorized (no/invalid auth) |
| 403 | Forbidden (authenticated but not allowed) |
| 404 | Not found |
| 409 | Conflict (duplicate, version mismatch) |
| 422 | Unprocessable entity (semantic error) |
| 429 | Too many requests |
| 500 | Internal server error |

### Response Format

#### Success responses
```json
// Single resource
{
  "data": {
    "id": "usr_123",
    "email": "user@example.com",
    "name": "John Doe",
    "createdAt": "2024-01-15T10:30:00Z"
  }
}

// Collection with pagination
{
  "data": [...],
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 156,
    "totalPages": 8
  },
  "links": {
    "self": "/api/v1/users?page=1",
    "next": "/api/v1/users?page=2",
    "last": "/api/v1/users?page=8"
  }
}
```

#### Error responses
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format",
        "code": "INVALID_FORMAT"
      },
      {
        "field": "password",
        "message": "Must be at least 8 characters",
        "code": "TOO_SHORT"
      }
    ]
  },
  "requestId": "req_abc123"
}
```

## Input Validation

### Validate at the API boundary
```typescript
// Use Zod, Joi, or similar
const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
  password: z.string().min(8).max(72),
  role: z.enum(['user', 'admin']).default('user'),
});

app.post('/api/v1/users', validate(createUserSchema), async (req, res) => {
  // req.body is now typed and validated
});
```

### Sanitize inputs
```typescript
// Strip unknown fields
const sanitized = schema.parse(req.body);

// Escape HTML in user-provided strings
const safeName = sanitizeHtml(input.name);

// Validate IDs
const userId = z.string().uuid().parse(req.params.id);
```

## Authentication & Authorization

### Use middleware for auth
```typescript
// Authentication middleware
const authenticate = async (req, res, next) => {
  const token = req.headers.authorization?.replace('Bearer ', '');
  
  if (!token) {
    return res.status(401).json({
      error: { code: 'UNAUTHORIZED', message: 'Authentication required' }
    });
  }
  
  try {
    req.user = await verifyToken(token);
    next();
  } catch (error) {
    res.status(401).json({
      error: { code: 'INVALID_TOKEN', message: 'Invalid or expired token' }
    });
  }
};

// Authorization middleware
const authorize = (...roles: string[]) => (req, res, next) => {
  if (!roles.includes(req.user.role)) {
    return res.status(403).json({
      error: { code: 'FORBIDDEN', message: 'Insufficient permissions' }
    });
  }
  next();
};

// Usage
app.delete('/api/v1/users/:id', 
  authenticate, 
  authorize('admin'), 
  deleteUser
);
```

## Error Handling

### Use centralized error handling
```typescript
// Custom error classes
class AppError extends Error {
  constructor(
    public statusCode: number,
    public code: string,
    message: string,
    public details?: unknown
  ) {
    super(message);
    this.name = 'AppError';
  }
}

class NotFoundError extends AppError {
  constructor(resource: string, id: string) {
    super(404, 'NOT_FOUND', `${resource} not found: ${id}`);
  }
}

class ValidationError extends AppError {
  constructor(details: ValidationDetail[]) {
    super(400, 'VALIDATION_ERROR', 'Request validation failed', details);
  }
}

// Global error handler
app.use((error: Error, req: Request, res: Response, next: NextFunction) => {
  const requestId = req.headers['x-request-id'];
  
  if (error instanceof AppError) {
    logger.warn('Application error', {
      requestId,
      code: error.code,
      message: error.message,
    });
    
    return res.status(error.statusCode).json({
      error: {
        code: error.code,
        message: error.message,
        details: error.details,
      },
      requestId,
    });
  }
  
  // Unexpected error
  logger.error('Unexpected error', { requestId, error });
  
  res.status(500).json({
    error: {
      code: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred',
    },
    requestId,
  });
});
```

## Logging & Observability

### Use structured logging
```typescript
const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  formatters: {
    level: (label) => ({ level: label }),
  },
});

// Request logging middleware
app.use((req, res, next) => {
  const requestId = req.headers['x-request-id'] || generateId();
  req.requestId = requestId;
  res.setHeader('x-request-id', requestId);
  
  const start = Date.now();
  
  res.on('finish', () => {
    logger.info({
      type: 'request',
      requestId,
      method: req.method,
      path: req.path,
      statusCode: res.statusCode,
      duration: Date.now() - start,
      userId: req.user?.id,
    });
  });
  
  next();
});
```

### Add health check endpoints
```typescript
app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});

app.get('/health/ready', async (req, res) => {
  const checks = {
    database: await checkDatabase(),
    redis: await checkRedis(),
    external: await checkExternalService(),
  };
  
  const healthy = Object.values(checks).every(Boolean);
  
  res.status(healthy ? 200 : 503).json({
    status: healthy ? 'ready' : 'not_ready',
    checks,
  });
});
```

## Security

### Required security headers
```typescript
import helmet from 'helmet';

app.use(helmet());
app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'"],
    styleSrc: ["'self'", "'unsafe-inline'"],
  },
}));
```

### Rate limiting
```typescript
import rateLimit from 'express-rate-limit';

const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100,
  standardHeaders: true,
  legacyHeaders: false,
  message: {
    error: {
      code: 'RATE_LIMITED',
      message: 'Too many requests, please try again later',
    },
  },
});

app.use('/api/', apiLimiter);
```

### CORS configuration
```typescript
import cors from 'cors';

app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || [],
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true,
  maxAge: 86400,
}));
```

## Database Patterns

### Use repository pattern
```typescript
interface UserRepository {
  findById(id: string): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
  create(data: CreateUserData): Promise<User>;
  update(id: string, data: UpdateUserData): Promise<User>;
  delete(id: string): Promise<void>;
}

class PostgresUserRepository implements UserRepository {
  constructor(private db: Database) {}
  
  async findById(id: string): Promise<User | null> {
    const row = await this.db.query(
      'SELECT * FROM users WHERE id = $1',
      [id]
    );
    return row ? mapToUser(row) : null;
  }
}
```

### Use transactions for consistency
```typescript
async function createOrder(data: CreateOrderData): Promise<Order> {
  return db.transaction(async (tx) => {
    const order = await tx.orders.create(data.order);
    
    await tx.orderItems.createMany(
      data.items.map(item => ({ ...item, orderId: order.id }))
    );
    
    await tx.inventory.decrement(data.items);
    
    return order;
  });
}
```

## Testing

### Test API endpoints
```typescript
describe('POST /api/v1/users', () => {
  it('creates a user with valid data', async () => {
    const response = await request(app)
      .post('/api/v1/users')
      .send({
        email: 'new@example.com',
        name: 'New User',
        password: 'secure123',
      })
      .expect(201);
    
    expect(response.body.data).toMatchObject({
      email: 'new@example.com',
      name: 'New User',
    });
    expect(response.headers.location).toMatch(/\/api\/v1\/users\/[\w-]+/);
  });
  
  it('returns 400 for invalid email', async () => {
    const response = await request(app)
      .post('/api/v1/users')
      .send({ email: 'invalid', name: 'User', password: 'pass1234' })
      .expect(400);
    
    expect(response.body.error.code).toBe('VALIDATION_ERROR');
  });
});
```

## File Organization
```
src/
├── api/
│   ├── v1/
│   │   ├── users/
│   │   │   ├── controller.ts
│   │   │   ├── routes.ts
│   │   │   ├── schema.ts
│   │   │   └── service.ts
│   │   └── orders/
│   └── middleware/
├── domain/
│   ├── user.ts
│   └── order.ts
├── infrastructure/
│   ├── database/
│   └── external/
└── lib/
    ├── errors.ts
    └── logger.ts
```
