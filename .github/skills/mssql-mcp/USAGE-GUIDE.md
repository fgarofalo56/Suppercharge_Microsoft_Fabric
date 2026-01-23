# MssqlMcp - Complete Usage Guide

Comprehensive guide to using the MssqlMcp skill with Claude Code for natural language SQL Server queries, schema exploration, and data analysis.

## Table of Contents

- [How to Invoke This Skill](#how-to-invoke-this-skill)
- [Natural Language Queries](#natural-language-queries)
- [Complete Use Cases](#complete-use-cases)
- [Security Features](#security-features)
- [Configuration](#configuration)
- [Best Practices](#best-practices)

---

## How to Invoke This Skill

### Automatic Activation

Claude automatically activates this skill when you use these **trigger keywords**:

- `SQL Server`, `MSSQL`, `SQL database`
- `query`, `select`, `table`, `database`
- `show me data`, `find records`, `get rows`
- `create table`, `insert`, `update`, `delete`
- `schema`, `columns`, `table structure`
- `data analysis`, `aggregate`, `group by`

### Explicit Requests

Use natural language to describe what you want from the database:

```
✅ GOOD: "Show me all users from the Customers table"
✅ GOOD: "What tables are in this database?"
✅ GOOD: "Find orders placed in the last 7 days"
✅ GOOD: "Calculate total revenue by product category"

⚠️ VAGUE: "Get data"
⚠️ VAGUE: "Show me stuff"
```

### Example Invocation Patterns

```bash
# Data retrieval
"Show me all employees in the Sales department"
"Get the top 10 highest-value orders"
"Find customers who haven't ordered in 6 months"

# Schema exploration
"What tables exist in this database?"
"Show me the structure of the Orders table"
"List all columns in the Customers table"

# Data analysis
"Calculate average order value by month"
"Show sales trends over the last year"
"Find the best-selling products"

# Data modification (if not read-only)
"Create a table for storing product reviews"
"Insert a new customer record"
"Update the status of order 12345"
```

---

## Natural Language Queries

### Simple Retrieval

**Natural Language**: `"Show me all users"`

**Generated SQL**:
```sql
SELECT * FROM Users;
```

---

**Natural Language**: `"Get the first 10 customers"`

**Generated SQL**:
```sql
SELECT TOP 10 * FROM Customers;
```

---

### Filtering

**Natural Language**: `"Show me users from New York"`

**Generated SQL**:
```sql
SELECT * FROM Users
WHERE City = 'New York';
```

---

**Natural Language**: `"Find orders placed after January 1, 2024"`

**Generated SQL**:
```sql
SELECT * FROM Orders
WHERE OrderDate > '2024-01-01';
```

---

**Natural Language**: `"Get active users with email verified"`

**Generated SQL**:
```sql
SELECT * FROM Users
WHERE IsActive = 1 AND EmailVerified = 1;
```

---

### Aggregation

**Natural Language**: `"Count users by city"`

**Generated SQL**:
```sql
SELECT City, COUNT(*) as UserCount
FROM Users
GROUP BY City
ORDER BY UserCount DESC;
```

---

**Natural Language**: `"Calculate total sales by product"`

**Generated SQL**:
```sql
SELECT ProductId, SUM(Amount) as TotalSales
FROM Orders
GROUP BY ProductId
ORDER BY TotalSales DESC;
```

---

**Natural Language**: `"Show average order value by month"`

**Generated SQL**:
```sql
SELECT
    YEAR(OrderDate) as Year,
    MONTH(OrderDate) as Month,
    AVG(TotalAmount) as AvgOrderValue
FROM Orders
GROUP BY YEAR(OrderDate), MONTH(OrderDate)
ORDER BY Year, Month;
```

---

### Joins

**Natural Language**: `"Show orders with customer names"`

**Generated SQL**:
```sql
SELECT
    o.OrderId,
    o.OrderDate,
    o.TotalAmount,
    c.CustomerName,
    c.Email
FROM Orders o
INNER JOIN Customers c ON o.CustomerId = c.CustomerId;
```

---

**Natural Language**: `"Get employees and their department names"`

**Generated SQL**:
```sql
SELECT
    e.EmployeeId,
    e.EmployeeName,
    d.DepartmentName
FROM Employees e
LEFT JOIN Departments d ON e.DepartmentId = d.DepartmentId;
```

---

### Complex Queries

**Natural Language**: `"Find the top 5 customers by total purchase amount"`

**Generated SQL**:
```sql
SELECT TOP 5
    c.CustomerId,
    c.CustomerName,
    SUM(o.TotalAmount) as TotalPurchases,
    COUNT(o.OrderId) as OrderCount
FROM Customers c
INNER JOIN Orders o ON c.CustomerId = o.CustomerId
GROUP BY c.CustomerId, c.CustomerName
ORDER BY TotalPurchases DESC;
```

---

**Natural Language**: `"Show products that haven't been ordered in the last 30 days"`

**Generated SQL**:
```sql
SELECT p.*
FROM Products p
WHERE p.ProductId NOT IN (
    SELECT DISTINCT ProductId
    FROM Orders
    WHERE OrderDate > DATEADD(day, -30, GETDATE())
);
```

---

## Complete Use Cases

### Use Case 1: Business Intelligence Queries

**Scenario**: Generate sales reports and business insights

**Step-by-step workflow**:

1. **Explore available data**:
```
Request: "What tables are in this database?"

Response:
Available tables (15):
- Customers
- Orders
- OrderItems
- Products
- Categories
- Employees
- Departments
- Inventory
- Suppliers
- Shipments
...
```

2. **Check table structure**:
```
Request: "Show me the columns in the Orders table"

Response:
Table: Orders
Columns:
- OrderId (int, PRIMARY KEY)
- CustomerId (int, FOREIGN KEY)
- OrderDate (datetime)
- ShipDate (datetime, nullable)
- TotalAmount (decimal(10,2))
- Status (varchar(20))
- PaymentMethod (varchar(50))
- ShippingAddress (varchar(200))
- CreatedAt (datetime)
- UpdatedAt (datetime)
```

3. **Run analysis queries**:

```
Request: "Show me total revenue by month for 2024"

Response:
Month          Revenue
------------------------
January        $284,592
February       $301,445
March          $318,207
April          $295,883
May            $342,109
June           $359,421
July           $378,044
August         $391,273
September      $367,821
October        $382,546
November       $401,829
December       $429,183
Total 2024:    $4,252,353
```

```
Request: "What are the top 10 products by sales volume?"

Response:
Product Name            Units Sold    Revenue
-------------------------------------------------
Laptop Pro 15          2,847         $3,987,580
Wireless Mouse         8,392         $251,760
USB-C Cable           12,459         $186,885
Keyboard Mechanical    3,124         $467,460
Monitor 27" 4K         1,893         $1,231,950
...
```

```
Request: "Show customer lifetime value for top 20 customers"

Response:
Customer Name        Orders   Total Spent   Avg Order   Last Order
------------------------------------------------------------------------
Acme Corporation     156      $892,430      $5,721      2024-12-15
Global Industries    142      $784,920      $5,528      2024-12-17
Tech Solutions       128      $698,340      $5,456      2024-12-18
...
```

4. **Drill down into specifics**:

```
Request: "Show me orders from Acme Corporation in the last 30 days"

Response:
Order ID   Date         Amount      Status      Payment
----------------------------------------------------------
ORD-45821  2024-11-20   $12,450    Delivered   Credit
ORD-46102  2024-11-25   $8,920     Delivered   Invoice
ORD-46784  2024-12-01   $15,680    Shipped     Credit
ORD-47203  2024-12-08   $9,340     Delivered   Credit
ORD-47891  2024-12-15   $11,230    Processing  Invoice
```

**Expected outcome**:
- Business metrics generated
- Sales trends identified
- Customer insights revealed
- Data-driven decisions enabled

---

### Use Case 2: Data Quality Assessment

**Scenario**: Check data quality and identify issues

**Step-by-step workflow**:

1. **Check for missing values**:
```
Request: "Find customers with missing email addresses"

Response:
Found 234 customers with missing emails:
Customer ID   Name                    Phone          City
-------------------------------------------------------------
CUST-1025    Johnson & Associates    555-0123       Seattle
CUST-1847    Williams Corp           (missing)      Portland
CUST-2103    Brown Industries        555-0456       Denver
...

Action needed: Update contact information for these customers
```

2. **Find duplicate records**:
```
Request: "Find duplicate customer records based on email"

Response:
Found 18 potential duplicates:

Email: john.smith@example.com
- CUST-3421 (created 2023-05-12)
- CUST-8834 (created 2024-02-18)

Email: sarah.jones@company.com
- CUST-4102 (created 2023-08-20)
- CUST-7921 (created 2024-01-09)
...

Action needed: Review and merge duplicate accounts
```

3. **Check referential integrity**:
```
Request: "Find orders that reference non-existent customers"

Response:
Found 5 orphaned orders:
Order ID   Date         Amount    Customer ID (invalid)
--------------------------------------------------------
ORD-42891  2024-11-15   $5,420    CUST-9999 (deleted)
ORD-43102  2024-11-20   $2,890    CUST-8888 (not found)
...

Action needed: Archive or reassign these orders
```

4. **Identify data anomalies**:
```
Request: "Find orders with negative amounts or amounts over $100,000"

Response:
Anomalies found (7):

Negative amounts (2):
- ORD-44521: -$150.00 (likely refund recorded incorrectly)
- ORD-45103: -$89.50 (adjustment error)

Unusually high amounts (5):
- ORD-43890: $287,450 (bulk enterprise order - verified)
- ORD-44203: $198,320 (annual contract - verified)
- ORD-46712: $523,100 (⚠ needs review - may be error)
...

Action needed: Review flagged transactions
```

**Expected outcome**:
- Data quality issues identified
- Missing data flagged
- Duplicates detected
- Anomalies surfaced
- Cleanup actions defined

---

### Use Case 3: Database Schema Exploration

**Scenario**: Understand database structure for development

**Step-by-step workflow**:

1. **List all tables**:
```
Request: "What tables exist in this database?"

Response:
Database: ProductionDB
Tables (23):

Core Tables:
- Customers
- Orders
- Products
- Categories

Support Tables:
- OrderItems
- ProductReviews
- Inventory
- Suppliers

User Management:
- Users
- Roles
- Permissions
...
```

2. **Get table relationships**:
```
Request: "Show me how the Orders, Customers, and OrderItems tables relate"

Response:
Table Relationships:

Customers (1) ←→ (Many) Orders
  CustomerId = CustomerId

Orders (1) ←→ (Many) OrderItems
  OrderId = OrderId

OrderItems (Many) ←→ (1) Products
  ProductId = ProductId

Data Flow:
Customer → Orders → OrderItems → Products
```

3. **Analyze table sizes**:
```
Request: "How many records are in each table?"

Response:
Table Sizes:

Large Tables (>1M rows):
- Orders: 3,482,094 rows
- OrderItems: 8,921,342 rows
- ProductReviews: 2,193,482 rows

Medium Tables (100K-1M):
- Customers: 892,103 rows
- Products: 45,829 rows

Small Tables (<100K):
- Categories: 182 rows
- Suppliers: 1,247 rows
- Employees: 523 rows
```

4. **Check indexes**:
```
Request: "Show me the indexes on the Orders table"

Response:
Indexes on Orders table:

Primary Key:
- PK_Orders on OrderId (Clustered)

Foreign Keys:
- FK_Orders_CustomerId on CustomerId
- FK_Orders_EmployeeId on EmployeeId

Additional Indexes:
- IX_Orders_OrderDate on OrderDate (Non-clustered)
- IX_Orders_Status on Status (Non-clustered)
- IX_Orders_CustomerId_OrderDate on (CustomerId, OrderDate)

Performance: Well-indexed for common queries
```

**Expected outcome**:
- Database structure understood
- Relationships mapped
- Data volumes known
- Index strategy clear
- Development ready

---

### Use Case 4: Report Generation

**Scenario**: Create recurring business reports

**Step-by-step workflow**:

1. **Monthly sales summary**:
```
Request: "Generate a monthly sales summary report for December 2024"

Response:
========================================
MONTHLY SALES SUMMARY - DECEMBER 2024
========================================

Overall Performance:
- Total Revenue: $429,183
- Total Orders: 1,847
- Average Order Value: $232.37
- New Customers: 234
- Returning Customers: 1,289

Top Performing Categories:
1. Electronics: $187,420 (43.7%)
2. Accessories: $98,230 (22.9%)
3. Software: $67,890 (15.8%)
4. Services: $45,123 (10.5%)
5. Other: $30,520 (7.1%)

Top Sales Representatives:
1. Sarah Johnson: $89,430 (208 orders)
2. Michael Chen: $76,890 (189 orders)
3. Emily Rodriguez: $68,920 (176 orders)

Payment Methods:
- Credit Card: $287,450 (67%)
- Invoice: $98,340 (23%)
- ACH: $43,393 (10%)

YoY Comparison:
December 2024: $429,183 (+8.3% vs Dec 2023)
December 2023: $396,284

Status: ✅ Exceeded monthly target ($400,000)
========================================
```

2. **Customer churn analysis**:
```
Request: "Show customers who haven't ordered in 90 days but were previously active"

Response:
At-Risk Customers (163):

High-Value Churned:
Customer Name          Last Order   Lifetime Value   Status
----------------------------------------------------------------
Premium Corp           2024-09-10   $124,580         ⚠ HIGH RISK
Enterprise Solutions   2024-09-15   $98,340          ⚠ HIGH RISK
Global Services        2024-09-20   $87,920          ⚠ HIGH RISK

Medium-Value Churned: 45 customers ($892,340 total LTV)
Low-Value Churned: 115 customers ($124,580 total LTV)

Recommended Actions:
1. Re-engagement campaign for high-value customers
2. Survey to understand churn reasons
3. Special offer for reactivation
```

3. **Inventory report**:
```
Request: "Show inventory status with low stock alerts"

Response:
========================================
INVENTORY STATUS REPORT
========================================

Critical (Out of Stock): 12 items
⚠ Laptop Pro 15: 0 units (avg weekly sales: 45)
⚠ Wireless Keyboard: 0 units (avg weekly sales: 89)
⚠ USB Hub 7-Port: 0 units (avg weekly sales: 34)
...

Low Stock (< 2 weeks supply): 34 items
⚠ Monitor 27": 67 units (2 weeks @ current rate)
⚠ Mouse Pad: 145 units (1.5 weeks @ current rate)
...

Adequate Stock: 234 items
Overstocked (>12 weeks supply): 18 items

Actions Required:
- Immediate reorder: 12 items
- Review pricing on overstock items
- Contact suppliers for critical items
========================================
```

**Expected outcome**:
- Automated report generation
- Business insights delivered
- Action items identified
- Decision support enabled

---

## Security Features

### Read-Only Mode

**Configuration**:
```env
READONLY=true
```

**What it prevents**:
- INSERT statements
- UPDATE statements
- DELETE statements
- DROP statements
- ALTER statements
- TRUNCATE statements

**What it allows**:
- SELECT queries
- Schema exploration
- Data analysis
- Views and functions

**Example**:
```
Request: "Delete all orders from 2023"

Response:
❌ ERROR: Database is in read-only mode
DELETE operations are not permitted
Please contact your administrator if data modification is required
```

---

### Mandatory WHERE Clauses

**Security Rule**: All UPDATE and DELETE must have WHERE clause

**Prevents**:
```sql
-- ❌ BLOCKED: Would affect all rows
DELETE FROM Orders;
UPDATE Customers SET Status = 'Inactive';
```

**Requires**:
```sql
-- ✅ ALLOWED: Has specific WHERE clause
DELETE FROM Orders WHERE OrderId = 12345;
UPDATE Customers SET Status = 'Inactive' WHERE CustomerId = 789;
```

**Example**:
```
Request: "Delete all customers"

Response:
❌ ERROR: Safety check failed
DELETE operations require WHERE clause to prevent accidental data loss
Please specify which customers to delete

Example: "Delete customers where AccountStatus = 'Closed'"
```

---

### Connection Security

**Required Configuration**:
```env
SERVER_NAME=your-server.database.windows.net
DATABASE_NAME=your-database
AUTHENTICATION=AzureActiveDirectory
# Or
USER_NAME=your-username
PASSWORD=your-secure-password
```

**Security Features**:
- Encrypted connections (TLS)
- Azure AD authentication support
- Connection pooling
- Timeout configuration
- Connection retry logic

---

## Configuration

### Environment Variables

**Required**:
```env
# Server connection
SERVER_NAME=sql-server-prod.database.windows.net
DATABASE_NAME=ProductionDB

# Authentication (choose one)
AUTHENTICATION=AzureActiveDirectory
# or
USER_NAME=dbuser
PASSWORD=SecurePassword123!

# Optional settings
READONLY=false
CONNECTION_TIMEOUT=30
COMMAND_TIMEOUT=60
POOL_SIZE=10
```

---

### Connection String

**Alternative configuration**:
```env
CONNECTION_STRING=Server=sql-server.database.windows.net;Database=ProductionDB;User Id=dbuser;Password=***;Encrypt=true;TrustServerCertificate=false;Connection Timeout=30;
```

---

### Testing Configuration

```
Request: "Test database connection"

Response:
Database Connection Test
========================
✓ Server reachable: sql-server-prod.database.windows.net
✓ Authentication successful
✓ Database accessible: ProductionDB
✓ Permissions verified: Read + Write
✓ Connection pool: 10 connections available
Status: ✅ Connected successfully
```

---

## Best Practices

### Query Performance

```
✅ GOOD: Specific queries
"Show me orders from the last 7 days"
→ Uses date filter, fast

❌ BAD: Unbounded queries
"Show me all orders"
→ Could return millions of rows, slow
```

---

### Natural Language Clarity

```
✅ GOOD: Clear and specific
"Find customers in California who ordered in December 2024"

❌ VAGUE: Ambiguous
"Get some customer stuff"
```

---

### Data Modification

```
✅ GOOD: Specific and verified
"Update the email for customer ID 12345 to newemail@example.com"

❌ RISKY: Broad modifications
"Update all customer emails"
```

---

### Schema Changes

```
✅ GOOD: Well-defined structure
"Create a table ProductReviews with columns: ReviewId, ProductId, UserId, Rating, Comment, CreatedAt"

❌ BAD: Incomplete specification
"Create a reviews table"
```

---

## Additional Resources

- [SKILL.md](SKILL.md) - Main skill instructions
- [reference.md](reference.md) - Complete reference
- [SQL Server Documentation](https://learn.microsoft.com/sql/sql-server/)
- [T-SQL Reference](https://learn.microsoft.com/sql/t-sql/)

---

## Quick Reference

### Common Commands

```bash
# Schema exploration
"What tables are in this database?"
"Show columns in {table}"
"How many rows in {table}?"

# Data retrieval
"Show me all {records} where {condition}"
"Get top 10 {records} by {column}"
"Find {records} from {time period}"

# Analysis
"Calculate {aggregation} by {group}"
"Show trends over {time period}"
"Compare {metric} between {groups}"

# Data modification (if not read-only)
"Insert {record} into {table}"
"Update {record} where {condition}"
"Delete {record} where {condition}"
```

---

## Troubleshooting

### Issue: "Connection failed"
- Verify SERVER_NAME and DATABASE_NAME
- Check network connectivity
- Confirm firewall rules allow connection
- Validate credentials
- Test connection string manually

### Issue: "Query timeout"
- Simplify query
- Add WHERE clause to filter data
- Check table indexes
- Increase COMMAND_TIMEOUT
- Consider query optimization

### Issue: "Permission denied"
- Verify user has required permissions
- Check role assignments
- Confirm authentication method
- Review security policies

### Issue: "Table not found"
- Verify table name spelling
- Check database schema
- Confirm table exists in specified database
- Check user has access to table

---

## Questions?

**Q: Can I use this with Azure SQL Database?**
A: Yes! Works with SQL Server, Azure SQL, and Azure SQL Managed Instance.

**Q: How do I enable write operations?**
A: Set `READONLY=false` in configuration (requires appropriate permissions).

**Q: Does it support stored procedures?**
A: Yes, you can execute stored procedures using natural language.

**Q: Can I connect to multiple databases?**
A: You can switch databases by updating configuration and reconnecting.

**Q: Is my query data secure?**
A: Yes - connections use TLS encryption and support Azure AD authentication.

**Q: Can I save queries for reuse?**
A: The skill generates SQL from natural language each time. Save the natural language request instead.
