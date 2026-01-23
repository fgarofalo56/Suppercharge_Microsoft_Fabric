---
applyTo:
  - "**/*.py"
  - "**/*.pyi"
  - "**/pyproject.toml"
  - "**/requirements*.txt"
excludeAgent:
  - "code-review"  # Remove this line to enable for code review
---

# Python Development Standards

## Python Version & Configuration
- Use Python 3.11+ for all new projects
- Use type hints extensively (PEP 484, 585, 604)
- Format with Black, lint with Ruff, type-check with mypy

## Type Hints

### DO: Use modern type hint syntax
```python
def process_users(users: list[User]) -> dict[str, ProcessedUser]:
    return {user.id: process(user) for user in users}

def get_user(user_id: str) -> User | None:
    return db.users.get(user_id)
```

### DON'T: Skip type hints on public functions
```python
# ❌ Avoid
def calculate_total(items):
    return sum(item.price for item in items)

# ✅ Prefer
def calculate_total(items: list[Item]) -> Decimal:
    return sum(item.price for item in items)
```

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Modules | snake_case | `user_service.py` |
| Classes | PascalCase | `UserRepository` |
| Functions | snake_case | `get_user_by_id` |
| Variables | snake_case | `user_count` |
| Constants | UPPER_SNAKE_CASE | `MAX_CONNECTIONS` |
| Private | Leading underscore | `_internal_helper` |
| Type Variables | Single uppercase | `T`, `K`, `V` |

## Modern Patterns

### Use dataclasses or Pydantic for data structures
```python
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class User:
    id: str
    email: str
    created_at: datetime
    is_active: bool = True
```

### Use Pydantic for validation
```python
from pydantic import BaseModel, EmailStr, Field

class CreateUserRequest(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=0, le=150)
```

### Use context managers for resource handling
```python
async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
        return await response.json()
```

## Async/Await

### Use async for I/O-bound operations
```python
async def fetch_user(user_id: str) -> User:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"/users/{user_id}")
        response.raise_for_status()
        return User(**response.json())
```

### Use asyncio.gather for concurrent operations
```python
async def fetch_all_users(user_ids: list[str]) -> list[User]:
    tasks = [fetch_user(uid) for uid in user_ids]
    return await asyncio.gather(*tasks)
```

## Error Handling

### Create specific exception classes
```python
class UserNotFoundError(Exception):
    def __init__(self, user_id: str) -> None:
        self.user_id = user_id
        super().__init__(f"User not found: {user_id}")

class ValidationError(Exception):
    def __init__(self, field: str, message: str) -> None:
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")
```

### Use structured logging
```python
import structlog

logger = structlog.get_logger()

def process_order(order_id: str) -> None:
    logger.info("processing_order", order_id=order_id)
    try:
        result = _do_process(order_id)
        logger.info("order_processed", order_id=order_id, result=result)
    except ProcessingError as e:
        logger.error("order_failed", order_id=order_id, error=str(e))
        raise
```

## Import Organization (isort compatible)
1. Standard library
2. Third-party packages
3. Local application imports

```python
import asyncio
from datetime import datetime
from typing import Any

import httpx
from pydantic import BaseModel

from app.models import User
from app.services import UserService
```

## Testing Requirements
- Use pytest as the test framework
- Use pytest-asyncio for async tests
- Use pytest-cov for coverage (target: 80%+)
- Test file naming: `test_*.py` or `*_test.py`

```python
import pytest
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_fetch_user_success(mock_client: AsyncMock) -> None:
    mock_client.get.return_value = MockResponse({"id": "123", "email": "test@example.com"})
    
    user = await fetch_user("123")
    
    assert user.id == "123"
    assert user.email == "test@example.com"
```

## Documentation
- Use Google-style docstrings
- Document all public functions, classes, and modules
- Include type information in docstrings for complex cases

```python
def calculate_discount(
    price: Decimal,
    discount_percent: float,
    max_discount: Decimal | None = None,
) -> Decimal:
    """Calculate the discounted price.

    Args:
        price: Original price before discount.
        discount_percent: Discount percentage (0-100).
        max_discount: Maximum discount amount, if any.

    Returns:
        The final price after applying the discount.

    Raises:
        ValueError: If discount_percent is not between 0 and 100.

    Example:
        >>> calculate_discount(Decimal("100"), 10)
        Decimal("90")
    """
```

## Security
- Never hardcode secrets; use environment variables
- Use parameterized queries for database operations
- Validate all user input with Pydantic
- Use secrets module for cryptographic randomness
