[Home](../../README.md) > [PRPs](../README.md) > [Plans](./) > Example Feature Plan

# 🔧 Implementation Plan: JWT & Refresh Tokens (Phase 1)

> **PRD**: [User Authentication System](../prds/example-feature.prd.md)  
> **Phase**: 1 of 4 | **Status**: 🟡 Ready  
> **Estimated Duration**: 2 weeks | **Complexity**: Medium

---

## 📑 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Codebase Context](#codebase-context)
- [Tasks](#tasks)
- [Validation Commands](#validation-commands)
- [Rollback Plan](#rollback-plan)
- [Handoff Notes](#handoff-notes)

---

## Overview

### Goal

Replace the current session-based authentication with JWT access tokens and refresh tokens for improved security and scalability.

### Scope

| In Scope | Out of Scope |
|----------|--------------|
| JWT access token generation | OAuth integration (Phase 2) |
| Refresh token storage (Redis) | MFA (Phase 3) |
| Token refresh endpoint | Session management UI (Phase 4) |
| Token blacklisting | Password reset flow changes |
| Auth middleware updates | |

### Success Criteria

- [ ] All existing tests pass
- [ ] New unit tests for token service (>80% coverage)
- [ ] E2E tests for login/logout/refresh flow
- [ ] No breaking changes to existing API consumers
- [ ] Performance: login < 500ms p95

---

## Prerequisites

### Dependencies

| Dependency | Version | Status | Installation |
|------------|---------|--------|--------------|
| jose | ^5.2.0 | 🟡 To Install | `npm install jose` |
| ioredis | ^5.3.0 | ✅ Installed | - |
| @types/node | ^20.x | ✅ Installed | - |

### Environment Variables

```bash
# Add to .env
JWT_SECRET=your-256-bit-secret          # Generate: openssl rand -base64 32
JWT_ACCESS_EXPIRY=15m
JWT_REFRESH_EXPIRY=7d
REDIS_URL=redis://localhost:6379
```

### Infrastructure

- [ ] Redis instance available (local or managed)
- [ ] Environment variables configured

---

## Codebase Context

### Existing Patterns

#### Authentication Middleware (Current)

```typescript
// src/middleware/auth.ts:15-32
export const authMiddleware = async (req: Request, res: Response, next: NextFunction) => {
  const session = req.session;
  if (!session?.userId) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  req.user = await userService.findById(session.userId);
  next();
};
```

**Pattern to Follow**: Middleware returns 401 with `{ error: string }` format.

#### User Service

```typescript
// src/services/userService.ts:45-58
export const validateCredentials = async (email: string, password: string): Promise<User | null> => {
  const user = await prisma.user.findUnique({ where: { email } });
  if (!user) return null;
  const valid = await bcrypt.compare(password, user.passwordHash);
  return valid ? user : null;
};
```

**Reuse**: `validateCredentials` for login flow.

#### Error Handling Pattern

```typescript
// src/lib/errors.ts:10-20
export class AuthError extends AppError {
  constructor(message: string, code: string) {
    super(message, 401, code);
  }
}

// Usage pattern
throw new AuthError('Invalid credentials', 'INVALID_CREDENTIALS');
```

### File Structure

```
src/
├── services/
│   ├── userService.ts          # Existing - user CRUD
│   └── tokenService.ts         # NEW - JWT operations
├── middleware/
│   └── auth.ts                 # UPDATE - JWT validation
├── routes/
│   └── auth.ts                 # UPDATE - add refresh endpoint
├── lib/
│   ├── redis.ts                # Existing - Redis client
│   └── jwt.ts                  # NEW - JWT utilities
└── types/
    └── auth.ts                 # UPDATE - token types
```

---

## Tasks

### Task 1: Install Dependencies

**File**: `package.json`  
**Validation**: `npm install && npm run build`

```bash
npm install jose
```

---

### Task 2: Create JWT Utilities

**File**: `src/lib/jwt.ts` (NEW)  
**Validation**: `npm test -- jwt.test.ts`

```typescript
// src/lib/jwt.ts
import * as jose from 'jose';

const JWT_SECRET = new TextEncoder().encode(process.env.JWT_SECRET);
const ACCESS_EXPIRY = process.env.JWT_ACCESS_EXPIRY || '15m';
const REFRESH_EXPIRY = process.env.JWT_REFRESH_EXPIRY || '7d';

export interface TokenPayload {
  userId: string;
  email: string;
  type: 'access' | 'refresh';
}

export async function generateAccessToken(payload: Omit<TokenPayload, 'type'>): Promise<string> {
  return new jose.SignJWT({ ...payload, type: 'access' })
    .setProtectedHeader({ alg: 'HS256' })
    .setIssuedAt()
    .setExpirationTime(ACCESS_EXPIRY)
    .sign(JWT_SECRET);
}

export async function generateRefreshToken(payload: Omit<TokenPayload, 'type'>): Promise<string> {
  return new jose.SignJWT({ ...payload, type: 'refresh' })
    .setProtectedHeader({ alg: 'HS256' })
    .setIssuedAt()
    .setExpirationTime(REFRESH_EXPIRY)
    .sign(JWT_SECRET);
}

export async function verifyToken(token: string): Promise<TokenPayload> {
  const { payload } = await jose.jwtVerify(token, JWT_SECRET);
  return payload as unknown as TokenPayload;
}
```

---

### Task 3: Create Token Service

**File**: `src/services/tokenService.ts` (NEW)  
**Validation**: `npm test -- tokenService.test.ts`

```typescript
// src/services/tokenService.ts
import { redis } from '../lib/redis';
import { generateAccessToken, generateRefreshToken, verifyToken } from '../lib/jwt';
import { randomUUID } from 'crypto';

const REFRESH_TOKEN_PREFIX = 'refresh:';
const BLACKLIST_PREFIX = 'blacklist:';
const REFRESH_EXPIRY_SECONDS = 7 * 24 * 60 * 60; // 7 days

export interface TokenPair {
  accessToken: string;
  refreshToken: string;
  expiresIn: number;
}

export async function createTokenPair(userId: string, email: string): Promise<TokenPair> {
  const tokenId = randomUUID();
  const accessToken = await generateAccessToken({ userId, email });
  const refreshToken = await generateRefreshToken({ userId, email });
  
  // Store refresh token in Redis
  await redis.setex(
    `${REFRESH_TOKEN_PREFIX}${userId}:${tokenId}`,
    REFRESH_EXPIRY_SECONDS,
    refreshToken
  );
  
  return {
    accessToken,
    refreshToken,
    expiresIn: 900, // 15 minutes in seconds
  };
}

export async function refreshTokens(refreshToken: string): Promise<TokenPair> {
  const payload = await verifyToken(refreshToken);
  
  if (payload.type !== 'refresh') {
    throw new Error('Invalid token type');
  }
  
  // Check if token is blacklisted
  const isBlacklisted = await redis.exists(`${BLACKLIST_PREFIX}${refreshToken}`);
  if (isBlacklisted) {
    throw new Error('Token has been revoked');
  }
  
  // Blacklist old refresh token (rotation)
  await redis.setex(`${BLACKLIST_PREFIX}${refreshToken}`, REFRESH_EXPIRY_SECONDS, '1');
  
  // Generate new token pair
  return createTokenPair(payload.userId, payload.email);
}

export async function revokeAllUserTokens(userId: string): Promise<void> {
  const keys = await redis.keys(`${REFRESH_TOKEN_PREFIX}${userId}:*`);
  if (keys.length > 0) {
    await redis.del(...keys);
  }
}
```

---

### Task 4: Update Auth Middleware

**File**: `src/middleware/auth.ts` (UPDATE)  
**Validation**: `npm test -- auth.middleware.test.ts`

```typescript
// src/middleware/auth.ts
import { Request, Response, NextFunction } from 'express';
import { verifyToken } from '../lib/jwt';
import { userService } from '../services/userService';

export const authMiddleware = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const authHeader = req.headers.authorization;
    
    if (!authHeader?.startsWith('Bearer ')) {
      return res.status(401).json({ error: 'Missing authorization header' });
    }
    
    const token = authHeader.substring(7);
    const payload = await verifyToken(token);
    
    if (payload.type !== 'access') {
      return res.status(401).json({ error: 'Invalid token type' });
    }
    
    req.user = await userService.findById(payload.userId);
    
    if (!req.user) {
      return res.status(401).json({ error: 'User not found' });
    }
    
    next();
  } catch (error) {
    if (error.code === 'ERR_JWT_EXPIRED') {
      return res.status(401).json({ error: 'Token expired', code: 'TOKEN_EXPIRED' });
    }
    return res.status(401).json({ error: 'Invalid token' });
  }
};
```

---

### Task 5: Update Auth Routes

**File**: `src/routes/auth.ts` (UPDATE)  
**Validation**: `npm test -- auth.routes.test.ts`

```typescript
// src/routes/auth.ts - Add these endpoints

import { Router } from 'express';
import { validateCredentials } from '../services/userService';
import { createTokenPair, refreshTokens, revokeAllUserTokens } from '../services/tokenService';
import { authMiddleware } from '../middleware/auth';

const router = Router();

// POST /auth/login
router.post('/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    
    const user = await validateCredentials(email, password);
    if (!user) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    
    const tokens = await createTokenPair(user.id, user.email);
    
    // Set refresh token as HTTP-only cookie
    res.cookie('refreshToken', tokens.refreshToken, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'strict',
      maxAge: 7 * 24 * 60 * 60 * 1000, // 7 days
    });
    
    return res.json({
      accessToken: tokens.accessToken,
      expiresIn: tokens.expiresIn,
      user: { id: user.id, email: user.email, name: user.name },
    });
  } catch (error) {
    return res.status(500).json({ error: 'Login failed' });
  }
});

// POST /auth/refresh
router.post('/refresh', async (req, res) => {
  try {
    const refreshToken = req.cookies.refreshToken;
    
    if (!refreshToken) {
      return res.status(401).json({ error: 'No refresh token' });
    }
    
    const tokens = await refreshTokens(refreshToken);
    
    res.cookie('refreshToken', tokens.refreshToken, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'strict',
      maxAge: 7 * 24 * 60 * 60 * 1000,
    });
    
    return res.json({
      accessToken: tokens.accessToken,
      expiresIn: tokens.expiresIn,
    });
  } catch (error) {
    return res.status(401).json({ error: 'Token refresh failed' });
  }
});

// POST /auth/logout
router.post('/logout', authMiddleware, async (req, res) => {
  try {
    await revokeAllUserTokens(req.user.id);
    res.clearCookie('refreshToken');
    return res.json({ message: 'Logged out successfully' });
  } catch (error) {
    return res.status(500).json({ error: 'Logout failed' });
  }
});

export default router;
```

---

### Task 6: Add Types

**File**: `src/types/auth.ts` (UPDATE)  
**Validation**: `npm run type-check`

```typescript
// src/types/auth.ts
import { User } from '@prisma/client';

declare global {
  namespace Express {
    interface Request {
      user?: User;
    }
  }
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  accessToken: string;
  expiresIn: number;
  user: {
    id: string;
    email: string;
    name: string;
  };
}

export interface RefreshResponse {
  accessToken: string;
  expiresIn: number;
}
```

---

### Task 7: Write Tests

**File**: `tests/unit/tokenService.test.ts` (NEW)  
**Validation**: `npm test -- tokenService.test.ts`

```typescript
// tests/unit/tokenService.test.ts
import { createTokenPair, refreshTokens, revokeAllUserTokens } from '../../src/services/tokenService';
import { redis } from '../../src/lib/redis';

describe('TokenService', () => {
  const testUser = { userId: 'user-123', email: 'test@example.com' };
  
  afterEach(async () => {
    await redis.flushdb();
  });
  
  describe('createTokenPair', () => {
    it('should generate access and refresh tokens', async () => {
      const tokens = await createTokenPair(testUser.userId, testUser.email);
      
      expect(tokens.accessToken).toBeDefined();
      expect(tokens.refreshToken).toBeDefined();
      expect(tokens.expiresIn).toBe(900);
    });
    
    it('should store refresh token in Redis', async () => {
      await createTokenPair(testUser.userId, testUser.email);
      
      const keys = await redis.keys(`refresh:${testUser.userId}:*`);
      expect(keys.length).toBe(1);
    });
  });
  
  describe('refreshTokens', () => {
    it('should return new token pair for valid refresh token', async () => {
      const original = await createTokenPair(testUser.userId, testUser.email);
      const refreshed = await refreshTokens(original.refreshToken);
      
      expect(refreshed.accessToken).not.toBe(original.accessToken);
      expect(refreshed.refreshToken).not.toBe(original.refreshToken);
    });
    
    it('should blacklist old refresh token', async () => {
      const original = await createTokenPair(testUser.userId, testUser.email);
      await refreshTokens(original.refreshToken);
      
      await expect(refreshTokens(original.refreshToken)).rejects.toThrow('Token has been revoked');
    });
  });
  
  describe('revokeAllUserTokens', () => {
    it('should remove all user refresh tokens', async () => {
      await createTokenPair(testUser.userId, testUser.email);
      await createTokenPair(testUser.userId, testUser.email);
      
      await revokeAllUserTokens(testUser.userId);
      
      const keys = await redis.keys(`refresh:${testUser.userId}:*`);
      expect(keys.length).toBe(0);
    });
  });
});
```

---

## Validation Commands

### Level 1: Static Analysis

```bash
npm run lint && npm run type-check
```

### Level 2: Unit Tests

```bash
npm test -- --coverage --testPathPattern="(jwt|tokenService|auth)"
```

### Level 3: Integration Tests

```bash
npm run test:integration -- --testPathPattern="auth"
```

### Level 4: E2E Tests

```bash
npm run e2e -- --spec="auth/**"
```

### Full Validation (Run Before PR)

```bash
npm run lint && npm run type-check && npm test -- --coverage && npm run e2e
```

---

## Rollback Plan

If issues arise after deployment:

1. **Immediate**: Revert the deployment
   ```bash
   git revert HEAD
   ```

2. **Database**: No schema changes, no rollback needed

3. **Redis**: Clear token data if corrupted
   ```bash
   redis-cli KEYS "refresh:*" | xargs redis-cli DEL
   redis-cli KEYS "blacklist:*" | xargs redis-cli DEL
   ```

4. **Fallback**: Feature flag to switch back to session auth
   ```typescript
   if (process.env.USE_JWT_AUTH === 'false') {
     // Use session middleware
   }
   ```

---

## Handoff Notes

### Completed

- [ ] JWT utilities created and tested
- [ ] Token service with Redis storage
- [ ] Updated auth middleware
- [ ] New auth routes (login, refresh, logout)
- [ ] Unit and integration tests

### Known Issues

*None yet - update during implementation*

### Next Phase

After this plan is complete, proceed to:
- **Phase 2**: OAuth Integration (`#prp-plan "OAuth integration for Google and GitHub"`)

### Context for Next Session

Key decisions made:
- Using `jose` library for JWT (modern, secure defaults)
- Refresh tokens stored in Redis with 7-day TTL
- Token rotation on refresh (old token blacklisted)
- Refresh token sent as HTTP-only cookie

---

> **Execute this plan**: `#prp-implement PRPs/plans/example-feature.plan.md`
