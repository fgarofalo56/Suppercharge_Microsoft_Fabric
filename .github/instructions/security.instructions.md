---
applyTo:
  - "**/*"
excludeAgent: []
description: "Security requirements that apply to all code"
---

# Security Standards

## Core Principles
- Security is everyone's responsibility
- Defense in depth - multiple layers of protection
- Least privilege - minimal permissions needed
- Fail securely - errors should not expose vulnerabilities
- Never trust user input

## Input Validation

### Validate all external input
```typescript
// ✅ Always validate and sanitize
const createUserSchema = z.object({
  email: z.string().email().max(255),
  name: z.string().min(1).max(100).regex(/^[\w\s-]+$/),
  age: z.number().int().min(0).max(150),
});

const validatedData = createUserSchema.parse(req.body);
```

### Prevent injection attacks
```typescript
// ✅ SQL - Use parameterized queries
const user = await db.query(
  'SELECT * FROM users WHERE id = $1',
  [userId]
);

// ❌ Never concatenate user input
const user = await db.query(
  `SELECT * FROM users WHERE id = '${userId}'` // VULNERABLE
);

// ✅ NoSQL - Use typed queries
const user = await collection.findOne({ _id: new ObjectId(userId) });

// ✅ Command execution - Use allowlists
const allowedCommands = ['status', 'version', 'health'];
if (!allowedCommands.includes(command)) {
  throw new Error('Invalid command');
}
```

### Sanitize output (prevent XSS)
```typescript
// ✅ HTML encoding for user content
import { escape } from 'html-escaper';
const safeContent = escape(userContent);

// ✅ React automatically escapes
<div>{userContent}</div>  // Safe

// ❌ Avoid dangerouslySetInnerHTML
<div dangerouslySetInnerHTML={{ __html: userContent }} />  // Dangerous
```

## Authentication

### Password requirements
```typescript
const passwordSchema = z.string()
  .min(12, 'Minimum 12 characters')
  .regex(/[A-Z]/, 'At least one uppercase letter')
  .regex(/[a-z]/, 'At least one lowercase letter')
  .regex(/[0-9]/, 'At least one number')
  .regex(/[^A-Za-z0-9]/, 'At least one special character');
```

### Secure password storage
```typescript
import { hash, verify } from '@node-rs/argon2';

// Hash with Argon2id (recommended)
const hashedPassword = await hash(password, {
  memoryCost: 65536,  // 64 MiB
  timeCost: 3,
  parallelism: 4,
});

// Verify password
const isValid = await verify(hashedPassword, inputPassword);
```

### Token management
```typescript
// JWT with short expiration
const token = jwt.sign(
  { userId, role },
  process.env.JWT_SECRET,
  { 
    expiresIn: '15m',  // Short-lived access tokens
    algorithm: 'HS256',
  }
);

// Refresh tokens with rotation
const refreshToken = generateSecureToken();
await storeRefreshToken(userId, refreshToken, { 
  expiresAt: addDays(new Date(), 7),
  rotateOnUse: true,
});
```

### Multi-factor authentication
```typescript
// TOTP implementation
import { authenticator } from 'otplib';

// Generate secret for user
const secret = authenticator.generateSecret();

// Verify token
const isValid = authenticator.verify({ token: userToken, secret });
```

## Authorization

### Implement proper access control
```typescript
// Role-based access control
const PERMISSIONS = {
  admin: ['read', 'write', 'delete', 'manage'],
  editor: ['read', 'write'],
  viewer: ['read'],
};

function authorize(requiredPermission: string) {
  return (req: Request, res: Response, next: NextFunction) => {
    const userPermissions = PERMISSIONS[req.user.role] || [];
    
    if (!userPermissions.includes(requiredPermission)) {
      return res.status(403).json({ error: 'Forbidden' });
    }
    
    next();
  };
}

// Resource-level authorization
async function canAccessResource(userId: string, resourceId: string) {
  const resource = await getResource(resourceId);
  return resource.ownerId === userId || resource.sharedWith.includes(userId);
}
```

### Check authorization at every layer
```typescript
// Controller layer
app.delete('/api/posts/:id', 
  authenticate,
  authorize('delete'),
  async (req, res) => {
    // Service layer also verifies
    await postService.delete(req.params.id, req.user);
  }
);

// Service layer
class PostService {
  async delete(postId: string, user: User) {
    const post = await this.repo.findById(postId);
    
    if (post.authorId !== user.id && user.role !== 'admin') {
      throw new ForbiddenError('Cannot delete this post');
    }
    
    await this.repo.delete(postId);
  }
}
```

## Secrets Management

### Never hardcode secrets
```typescript
// ❌ Never do this
const API_KEY = 'sk_live_abc123xyz';
const DB_PASSWORD = 'supersecret';

// ✅ Use environment variables
const API_KEY = process.env.API_KEY;
const DB_URL = process.env.DATABASE_URL;

// ✅ Validate required secrets at startup
const requiredEnvVars = ['DATABASE_URL', 'JWT_SECRET', 'API_KEY'];
for (const envVar of requiredEnvVars) {
  if (!process.env[envVar]) {
    throw new Error(`Missing required environment variable: ${envVar}`);
  }
}
```

### Use secret management services
```typescript
// AWS Secrets Manager
import { SecretsManager } from '@aws-sdk/client-secrets-manager';

async function getSecret(secretName: string) {
  const client = new SecretsManager();
  const response = await client.getSecretValue({ SecretId: secretName });
  return JSON.parse(response.SecretString!);
}

// Azure Key Vault
import { SecretClient } from '@azure/keyvault-secrets';

const client = new SecretClient(vaultUrl, credential);
const secret = await client.getSecret('database-password');
```

## Data Protection

### Encrypt sensitive data at rest
```typescript
import { createCipheriv, createDecipheriv, randomBytes } from 'crypto';

function encrypt(text: string, key: Buffer): string {
  const iv = randomBytes(16);
  const cipher = createCipheriv('aes-256-gcm', key, iv);
  
  let encrypted = cipher.update(text, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  
  const authTag = cipher.getAuthTag();
  
  return `${iv.toString('hex')}:${authTag.toString('hex')}:${encrypted}`;
}
```

### Protect data in transit
```typescript
// Enforce HTTPS
app.use((req, res, next) => {
  if (req.headers['x-forwarded-proto'] !== 'https') {
    return res.redirect(`https://${req.hostname}${req.url}`);
  }
  next();
});

// HSTS header
app.use(helmet.hsts({
  maxAge: 31536000,
  includeSubDomains: true,
  preload: true,
}));
```

### Handle sensitive data carefully
```typescript
// Don't log sensitive data
logger.info('User logged in', { 
  userId: user.id,
  email: user.email,
  // ❌ password: user.password,
  // ❌ token: authToken,
});

// Mask sensitive data in responses
function maskEmail(email: string): string {
  const [local, domain] = email.split('@');
  return `${local[0]}***@${domain}`;
}
```

## HTTP Security Headers

### Configure security headers
```typescript
import helmet from 'helmet';

app.use(helmet());

// Content Security Policy
app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'", "'strict-dynamic'"],
    styleSrc: ["'self'", "'unsafe-inline'"],
    imgSrc: ["'self'", "data:", "https:"],
    connectSrc: ["'self'", "https://api.example.com"],
    frameSrc: ["'none'"],
    objectSrc: ["'none'"],
  },
}));

// Prevent clickjacking
app.use(helmet.frameguard({ action: 'deny' }));

// Prevent MIME type sniffing
app.use(helmet.noSniff());
```

## Rate Limiting

### Protect against abuse
```typescript
import rateLimit from 'express-rate-limit';

// General API rate limit
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100,
  standardHeaders: true,
  legacyHeaders: false,
});

// Stricter limit for auth endpoints
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  message: { error: 'Too many login attempts' },
});

app.use('/api/', apiLimiter);
app.use('/api/auth/login', authLimiter);
```

## Security Logging

### Log security-relevant events
```typescript
const securityLogger = logger.child({ type: 'security' });

// Authentication events
securityLogger.info('login_success', { userId, ip: req.ip });
securityLogger.warn('login_failure', { email, ip: req.ip, reason });
securityLogger.warn('invalid_token', { ip: req.ip });

// Authorization events
securityLogger.warn('unauthorized_access', { 
  userId, 
  resource, 
  action,
  ip: req.ip,
});

// Suspicious activity
securityLogger.error('rate_limit_exceeded', { ip: req.ip, endpoint });
securityLogger.error('invalid_input_detected', { 
  ip: req.ip, 
  pattern: 'sql_injection',
});
```

## Dependency Security

### Keep dependencies updated
```bash
# Check for vulnerabilities
npm audit
pip-audit
cargo audit

# Update dependencies regularly
npm update
pip install --upgrade
cargo update
```

### Use lockfiles
- `package-lock.json` for npm
- `poetry.lock` for Python
- `Cargo.lock` for Rust
- `go.sum` for Go

## Security Checklist

Before deploying:
- [ ] All user input validated and sanitized
- [ ] Authentication implemented correctly
- [ ] Authorization checked at all levels
- [ ] No secrets in code or logs
- [ ] HTTPS enforced
- [ ] Security headers configured
- [ ] Rate limiting in place
- [ ] Dependencies audited for vulnerabilities
- [ ] Security logging enabled
- [ ] Error messages don't leak sensitive info
