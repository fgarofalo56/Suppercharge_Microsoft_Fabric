---
description: Generate API endpoint specifications from requirements using RESTful conventions.
---

# API Contract Generation

Generate API endpoint specifications from the following requirements:

## Requirements
$ARGUMENTS

## Design Framework

### 1. Resource Identification
- What are the core resources?
- How do they map to entities?
- What are the URL patterns?

### 2. Operations
- What CRUD operations are needed?
- What custom actions are required?
- What are the HTTP methods?

### 3. Request/Response Schemas
- What data is sent in requests?
- What data is returned in responses?
- What are the content types?

### 4. Error Handling
- What error codes are used?
- What error response format?
- What validation errors occur?

### 5. Authentication & Authorization
- What authentication is required?
- What permissions are needed?
- What scopes apply?

## Output Format

```markdown
# API Contracts: [Feature Name]

## Base URL
`/api/v1`

## Authentication
[Authentication requirements]

## Endpoints

### [Resource Name]

#### List [Resources]
- **Method**: GET
- **Path**: `/resources`
- **Query Parameters**:
  - `page`: int (optional, default: 1)
  - `limit`: int (optional, default: 20)
- **Response**: 200 OK
  ```json
  {
    "data": [...],
    "pagination": {...}
  }
  ```

#### Get [Resource]
- **Method**: GET
- **Path**: `/resources/{id}`
- **Response**: 200 OK / 404 Not Found

#### Create [Resource]
- **Method**: POST
- **Path**: `/resources`
- **Request Body**:
  ```json
  {
    "field1": "value",
    "field2": "value"
  }
  ```
- **Response**: 201 Created / 400 Bad Request

## Error Responses

| Code | Description | Response |
|------|-------------|----------|
| 400 | Bad Request | `{"error": "message", "details": [...]}` |
| 401 | Unauthorized | `{"error": "Authentication required"}` |
| 404 | Not Found | `{"error": "Resource not found"}` |
```
