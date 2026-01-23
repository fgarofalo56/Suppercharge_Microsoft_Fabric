---
applyTo:
  - "**/*.go"
  - "**/go.mod"
  - "**/go.sum"
excludeAgent:
  - "code-review"  # Remove this line to enable for code review
---

# Go Development Standards

## Go Version & Configuration
- Use Go 1.22+ for all new projects
- Use Go modules for dependency management
- Run `go fmt`, `go vet`, and `golangci-lint` before commits

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Packages | lowercase, short | `user`, `httputil` |
| Exported | PascalCase | `UserService`, `GetByID` |
| Unexported | camelCase | `userCache`, `validateInput` |
| Interfaces | -er suffix when single method | `Reader`, `UserStore` |
| Constants | PascalCase or camelCase | `MaxRetries`, `defaultTimeout` |
| Acronyms | All caps | `HTTPClient`, `UserID` |

## Error Handling

### DO: Return errors as the last return value
```go
func GetUser(ctx context.Context, id string) (*User, error) {
    user, err := repo.Find(ctx, id)
    if err != nil {
        return nil, fmt.Errorf("get user %s: %w", id, err)
    }
    return user, nil
}
```

### DO: Wrap errors with context
```go
if err != nil {
    return fmt.Errorf("process order %s: %w", orderID, err)
}
```

### DO: Use sentinel errors for expected conditions
```go
var (
    ErrNotFound     = errors.New("not found")
    ErrUnauthorized = errors.New("unauthorized")
)

func GetUser(id string) (*User, error) {
    user := cache.Get(id)
    if user == nil {
        return nil, ErrNotFound
    }
    return user, nil
}
```

### DO: Check for specific errors
```go
user, err := GetUser(id)
if errors.Is(err, ErrNotFound) {
    return nil, status.NotFound("user not found")
}
if err != nil {
    return nil, status.Internal("failed to get user")
}
```

## Context Usage

### Always pass context as first parameter
```go
func ProcessOrder(ctx context.Context, order *Order) error {
    if err := validate(ctx, order); err != nil {
        return err
    }
    return save(ctx, order)
}
```

### Use context for cancellation and timeouts
```go
ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
defer cancel()

result, err := longRunningOperation(ctx)
```

## Interfaces

### Keep interfaces small
```go
type UserReader interface {
    GetUser(ctx context.Context, id string) (*User, error)
}

type UserWriter interface {
    SaveUser(ctx context.Context, user *User) error
}

type UserStore interface {
    UserReader
    UserWriter
}
```

### Define interfaces where they're used
```go
// In the consumer package, not the provider
type userGetter interface {
    GetUser(ctx context.Context, id string) (*User, error)
}

type OrderService struct {
    users userGetter
}
```

## Struct Design

### Use functional options for complex configuration
```go
type ServerOption func(*Server)

func WithTimeout(d time.Duration) ServerOption {
    return func(s *Server) {
        s.timeout = d
    }
}

func WithLogger(l *slog.Logger) ServerOption {
    return func(s *Server) {
        s.logger = l
    }
}

func NewServer(addr string, opts ...ServerOption) *Server {
    s := &Server{
        addr:    addr,
        timeout: 30 * time.Second,
        logger:  slog.Default(),
    }
    for _, opt := range opts {
        opt(s)
    }
    return s
}
```

## Concurrency

### Use goroutines with proper synchronization
```go
func ProcessItems(ctx context.Context, items []Item) error {
    g, ctx := errgroup.WithContext(ctx)
    
    for _, item := range items {
        item := item // Capture for goroutine
        g.Go(func() error {
            return processItem(ctx, item)
        })
    }
    
    return g.Wait()
}
```

### Close channels from sender side
```go
func producer(ctx context.Context) <-chan int {
    ch := make(chan int)
    go func() {
        defer close(ch)
        for i := 0; ; i++ {
            select {
            case <-ctx.Done():
                return
            case ch <- i:
            }
        }
    }()
    return ch
}
```

## Logging

### Use structured logging (slog)
```go
logger := slog.Default()

logger.Info("processing request",
    slog.String("user_id", userID),
    slog.Int("items", len(items)),
)

logger.Error("failed to process",
    slog.String("error", err.Error()),
    slog.String("order_id", orderID),
)
```

## Testing

### Use table-driven tests
```go
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive", 2, 3, 5},
        {"negative", -1, -1, -2},
        {"zero", 0, 0, 0},
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := Add(tt.a, tt.b)
            if result != tt.expected {
                t.Errorf("Add(%d, %d) = %d; want %d", 
                    tt.a, tt.b, result, tt.expected)
            }
        })
    }
}
```

### Use testify for assertions (optional)
```go
func TestGetUser(t *testing.T) {
    user, err := GetUser(context.Background(), "123")
    
    require.NoError(t, err)
    assert.Equal(t, "123", user.ID)
    assert.NotEmpty(t, user.Email)
}
```

## Documentation
- Document all exported types, functions, and packages
- Start comments with the name of the thing being documented
- Use complete sentences

```go
// Package user provides user management functionality.
package user

// User represents a registered user in the system.
type User struct {
    ID    string
    Email string
}

// GetByID retrieves a user by their unique identifier.
// It returns ErrNotFound if no user exists with the given ID.
func GetByID(ctx context.Context, id string) (*User, error) {
    // ...
}
```

## Project Structure
```
project/
├── cmd/                    # Application entry points
│   └── server/
│       └── main.go
├── internal/               # Private application code
│   ├── domain/            # Business logic
│   ├── repository/        # Data access
│   └── service/           # Application services
├── pkg/                    # Public libraries
├── api/                    # API definitions (proto, OpenAPI)
└── go.mod
```
