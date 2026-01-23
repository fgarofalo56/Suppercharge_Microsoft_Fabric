---
applyTo:
  - "**/*.sql"
  - "**/migrations/**"
  - "**/seeds/**"
excludeAgent:
  - "code-review"  # Remove this line to enable for code review
---

# SQL & Database Development Standards

## General Principles
- Use parameterized queries to prevent SQL injection
- Prefer explicit column names over `SELECT *`
- Always include appropriate indexes for query patterns
- Use transactions for multi-statement operations
- Document complex queries with comments

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Tables | snake_case, plural | `users`, `order_items` |
| Columns | snake_case | `first_name`, `created_at` |
| Primary keys | `id` or `table_id` | `id`, `user_id` |
| Foreign keys | `referenced_table_id` | `user_id`, `order_id` |
| Indexes | `idx_table_column(s)` | `idx_users_email` |
| Unique constraints | `uq_table_column(s)` | `uq_users_email` |
| Check constraints | `chk_table_description` | `chk_orders_positive_total` |
| Functions | snake_case, verb prefix | `get_user_orders`, `calculate_total` |

## Table Design

### DO: Include standard audit columns
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id)
);

-- Add index for common query patterns
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_is_active ON users(is_active) WHERE is_active = true;
```

### DO: Use appropriate data types
```sql
-- Use UUID for IDs (better for distributed systems)
id UUID PRIMARY KEY DEFAULT gen_random_uuid()

-- Use TIMESTAMPTZ for timestamps (timezone-aware)
created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP

-- Use DECIMAL for money (not FLOAT)
price DECIMAL(10, 2) NOT NULL

-- Use TEXT for unbounded strings, VARCHAR for bounded
description TEXT,
country_code VARCHAR(2) NOT NULL

-- Use JSONB for flexible schema (PostgreSQL)
metadata JSONB DEFAULT '{}'::jsonb
```

## Query Patterns

### DO: Use explicit column lists
```sql
-- ✅ Prefer
SELECT 
    id,
    email,
    name,
    created_at
FROM users
WHERE is_active = true;

-- ❌ Avoid
SELECT * FROM users WHERE is_active = true;
```

### DO: Use CTEs for readability
```sql
WITH active_orders AS (
    SELECT 
        user_id,
        COUNT(*) as order_count,
        SUM(total_amount) as total_spent
    FROM orders
    WHERE status = 'completed'
      AND created_at >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY user_id
),
high_value_customers AS (
    SELECT user_id
    FROM active_orders
    WHERE total_spent > 1000
)
SELECT 
    u.id,
    u.email,
    u.name,
    ao.order_count,
    ao.total_spent
FROM users u
JOIN active_orders ao ON ao.user_id = u.id
WHERE u.id IN (SELECT user_id FROM high_value_customers)
ORDER BY ao.total_spent DESC;
```

### DO: Use appropriate JOINs
```sql
-- Use INNER JOIN when both sides must exist
SELECT o.id, u.name
FROM orders o
INNER JOIN users u ON u.id = o.user_id;

-- Use LEFT JOIN when right side is optional
SELECT u.id, u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
GROUP BY u.id, u.name;
```

## Migrations

### Use sequential, descriptive migration files
```
migrations/
├── 001_create_users_table.sql
├── 002_create_orders_table.sql
├── 003_add_users_email_index.sql
└── 004_add_orders_status_column.sql
```

### Include rollback in migrations
```sql
-- migrations/001_create_users_table.sql

-- Up
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);

-- Down
DROP INDEX IF EXISTS idx_users_email;
DROP TABLE IF EXISTS users;
```

### Make migrations idempotent when possible
```sql
-- Safe to run multiple times
CREATE TABLE IF NOT EXISTS users (...);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

ALTER TABLE orders 
    ADD COLUMN IF NOT EXISTS status VARCHAR(20);
```

## Performance

### DO: Create indexes for query patterns
```sql
-- For WHERE clauses
CREATE INDEX idx_orders_status ON orders(status);

-- For composite lookups
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- For partial indexes (PostgreSQL)
CREATE INDEX idx_orders_pending 
    ON orders(created_at) 
    WHERE status = 'pending';

-- For text search
CREATE INDEX idx_products_name_gin 
    ON products USING gin(to_tsvector('english', name));
```

### DO: Use EXPLAIN ANALYZE
```sql
-- Check query execution plan
EXPLAIN ANALYZE
SELECT u.id, u.name, COUNT(o.id)
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.is_active = true
GROUP BY u.id, u.name;
```

### DON'T: Use functions on indexed columns in WHERE
```sql
-- ❌ Avoid - prevents index usage
WHERE LOWER(email) = 'user@example.com'
WHERE DATE(created_at) = '2024-01-15'

-- ✅ Prefer - uses index
WHERE email = 'user@example.com'
WHERE created_at >= '2024-01-15' AND created_at < '2024-01-16'
```

## Security

### Always use parameterized queries
```sql
-- Application code should use parameterized queries
-- Never concatenate user input into SQL strings

-- Good (using parameters)
SELECT * FROM users WHERE id = $1;

-- Bad (string concatenation - SQL injection risk)
SELECT * FROM users WHERE id = '" + userId + "';
```

### Use appropriate permissions
```sql
-- Create read-only user for reporting
CREATE USER reporting_user WITH PASSWORD 'secure_password';
GRANT SELECT ON ALL TABLES IN SCHEMA public TO reporting_user;

-- Create application user with limited permissions
CREATE USER app_user WITH PASSWORD 'secure_password';
GRANT SELECT, INSERT, UPDATE ON users, orders TO app_user;
```

## Transactions

### Use transactions for related operations
```sql
BEGIN;

-- Insert order
INSERT INTO orders (id, user_id, total_amount, status)
VALUES ($1, $2, $3, 'pending');

-- Insert order items
INSERT INTO order_items (order_id, product_id, quantity, price)
SELECT $1, product_id, quantity, price
FROM cart_items
WHERE cart_id = $4;

-- Clear cart
DELETE FROM cart_items WHERE cart_id = $4;

COMMIT;
```

### Handle errors with savepoints
```sql
BEGIN;

SAVEPOINT before_update;

UPDATE accounts SET balance = balance - 100 WHERE id = $1;

-- Check if balance went negative
DO $$
BEGIN
    IF (SELECT balance FROM accounts WHERE id = $1) < 0 THEN
        ROLLBACK TO before_update;
        RAISE EXCEPTION 'Insufficient funds';
    END IF;
END $$;

COMMIT;
```

## Documentation

### Document complex queries
```sql
/*
 * Get monthly revenue summary by product category.
 *
 * This query:
 * 1. Filters to completed orders in the specified date range
 * 2. Joins with products to get category information
 * 3. Aggregates revenue by month and category
 *
 * Performance notes:
 * - Uses idx_orders_status_date index
 * - Should complete in <100ms for typical data volumes
 */
SELECT 
    DATE_TRUNC('month', o.created_at) AS month,
    p.category,
    SUM(oi.quantity * oi.unit_price) AS revenue,
    COUNT(DISTINCT o.id) AS order_count
FROM orders o
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = oi.product_id
WHERE o.status = 'completed'
  AND o.created_at BETWEEN $1 AND $2
GROUP BY DATE_TRUNC('month', o.created_at), p.category
ORDER BY month, revenue DESC;
```
