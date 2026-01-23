---
applyTo:
  - "**/*.rs"
  - "**/Cargo.toml"
  - "**/Cargo.lock"
excludeAgent:
  - "code-review"  # Remove this line to enable for code review
---

# Rust Development Standards

## Rust Edition & Configuration
- Use Rust 2024 edition for new projects
- Enable `#![deny(unsafe_code)]` unless unsafe is necessary
- Run `cargo fmt`, `cargo clippy`, and `cargo test` before commits
- Use `cargo audit` for security vulnerability checks

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Crates | snake_case | `my_awesome_lib` |
| Modules | snake_case | `user_service` |
| Types | PascalCase | `UserRepository` |
| Traits | PascalCase | `IntoResponse` |
| Functions | snake_case | `get_user_by_id` |
| Variables | snake_case | `user_count` |
| Constants | UPPER_SNAKE_CASE | `MAX_CONNECTIONS` |
| Lifetimes | short lowercase | `'a`, `'de` |
| Type parameters | Single uppercase | `T`, `E`, `K`, `V` |

## Error Handling

### Use thiserror for library errors
```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum UserError {
    #[error("user not found: {0}")]
    NotFound(String),
    
    #[error("invalid email format: {0}")]
    InvalidEmail(String),
    
    #[error("database error")]
    Database(#[from] sqlx::Error),
}
```

### Use anyhow for application errors
```rust
use anyhow::{Context, Result};

pub async fn process_user(id: &str) -> Result<User> {
    let user = get_user(id)
        .await
        .context("failed to fetch user")?;
    
    validate_user(&user)
        .context("user validation failed")?;
    
    Ok(user)
}
```

### Use Result for all fallible operations
```rust
pub fn parse_config(path: &Path) -> Result<Config, ConfigError> {
    let content = fs::read_to_string(path)
        .map_err(ConfigError::ReadError)?;
    
    toml::from_str(&content)
        .map_err(ConfigError::ParseError)
}
```

## Ownership & Borrowing

### Prefer borrowing over ownership when possible
```rust
// ✅ Prefer - takes reference
pub fn validate_email(email: &str) -> bool {
    email.contains('@')
}

// Only take ownership when needed
pub fn process_request(request: Request) -> Response {
    // Takes ownership because it needs to consume the request
}
```

### Use Cow for flexible ownership
```rust
use std::borrow::Cow;

pub fn normalize_name(name: &str) -> Cow<'_, str> {
    if name.chars().all(|c| c.is_lowercase()) {
        Cow::Borrowed(name)
    } else {
        Cow::Owned(name.to_lowercase())
    }
}
```

## Structs & Enums

### Use builder pattern for complex construction
```rust
#[derive(Debug, Clone)]
pub struct ServerConfig {
    host: String,
    port: u16,
    timeout: Duration,
    max_connections: usize,
}

impl ServerConfig {
    pub fn builder() -> ServerConfigBuilder {
        ServerConfigBuilder::default()
    }
}

#[derive(Default)]
pub struct ServerConfigBuilder {
    host: Option<String>,
    port: Option<u16>,
    timeout: Option<Duration>,
    max_connections: Option<usize>,
}

impl ServerConfigBuilder {
    pub fn host(mut self, host: impl Into<String>) -> Self {
        self.host = Some(host.into());
        self
    }
    
    pub fn port(mut self, port: u16) -> Self {
        self.port = Some(port);
        self
    }
    
    pub fn build(self) -> Result<ServerConfig, ConfigError> {
        Ok(ServerConfig {
            host: self.host.ok_or(ConfigError::MissingField("host"))?,
            port: self.port.unwrap_or(8080),
            timeout: self.timeout.unwrap_or(Duration::from_secs(30)),
            max_connections: self.max_connections.unwrap_or(100),
        })
    }
}
```

### Use newtype pattern for type safety
```rust
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct UserId(String);

impl UserId {
    pub fn new(id: impl Into<String>) -> Self {
        Self(id.into())
    }
    
    pub fn as_str(&self) -> &str {
        &self.0
    }
}
```

## Async/Await

### Use tokio for async runtime
```rust
use tokio::time::{timeout, Duration};

pub async fn fetch_with_timeout<T>(
    future: impl Future<Output = Result<T>>,
    duration: Duration,
) -> Result<T> {
    timeout(duration, future)
        .await
        .map_err(|_| anyhow!("operation timed out"))?
}
```

### Use proper cancellation handling
```rust
use tokio_util::sync::CancellationToken;

pub async fn worker(token: CancellationToken) {
    loop {
        tokio::select! {
            _ = token.cancelled() => {
                tracing::info!("worker cancelled");
                break;
            }
            result = do_work() => {
                if let Err(e) = result {
                    tracing::error!(?e, "work failed");
                }
            }
        }
    }
}
```

## Traits

### Design traits for extensibility
```rust
pub trait Repository: Send + Sync {
    type Error: std::error::Error + Send + Sync + 'static;
    
    async fn find(&self, id: &str) -> Result<Option<User>, Self::Error>;
    async fn save(&self, user: &User) -> Result<(), Self::Error>;
    async fn delete(&self, id: &str) -> Result<bool, Self::Error>;
}
```

### Use extension traits for adding methods
```rust
pub trait StringExt {
    fn truncate_ellipsis(&self, max_len: usize) -> String;
}

impl StringExt for str {
    fn truncate_ellipsis(&self, max_len: usize) -> String {
        if self.len() <= max_len {
            self.to_string()
        } else {
            format!("{}...", &self[..max_len.saturating_sub(3)])
        }
    }
}
```

## Logging

### Use tracing for structured logging
```rust
use tracing::{info, error, instrument};

#[instrument(skip(repo))]
pub async fn get_user(
    repo: &impl UserRepository,
    user_id: &str,
) -> Result<User> {
    info!("fetching user");
    
    let user = repo.find(user_id).await.map_err(|e| {
        error!(?e, "failed to fetch user");
        e
    })?;
    
    match user {
        Some(u) => Ok(u),
        None => {
            info!("user not found");
            Err(UserError::NotFound(user_id.to_string()).into())
        }
    }
}
```

## Testing

### Write unit tests in the same file
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_validate_email_valid() {
        assert!(validate_email("user@example.com"));
    }

    #[test]
    fn test_validate_email_invalid() {
        assert!(!validate_email("invalid"));
    }

    #[tokio::test]
    async fn test_fetch_user_success() {
        let repo = MockRepository::new();
        repo.expect_find()
            .returning(|_| Ok(Some(User::default())));
        
        let result = get_user(&repo, "123").await;
        assert!(result.is_ok());
    }
}
```

### Use proptest for property-based testing
```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn test_parse_roundtrip(s in "\\PC*") {
        let parsed = parse(&s);
        if let Ok(value) = parsed {
            assert_eq!(format(&value), s);
        }
    }
}
```

## Documentation
- Document all public items
- Include examples in doc comments
- Use `#![warn(missing_docs)]`

```rust
/// A user in the system.
///
/// # Examples
///
/// ```
/// use mylib::User;
///
/// let user = User::new("123", "alice@example.com");
/// assert_eq!(user.email(), "alice@example.com");
/// ```
#[derive(Debug, Clone)]
pub struct User {
    id: UserId,
    email: String,
}
```

## Project Structure
```
src/
├── lib.rs              # Library root
├── main.rs             # Binary entry point (optional)
├── config.rs           # Configuration
├── error.rs            # Error types
├── domain/             # Domain models
├── repository/         # Data access
├── service/            # Business logic
└── api/                # HTTP handlers
```
