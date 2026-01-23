---
applyTo:
  - "**/*.cs"
  - "**/*.csx"
  - "**/*.csproj"
  - "**/*.sln"
excludeAgent:
  - "code-review"  # Remove this line to enable for code review
---

# C#/.NET Development Standards

## .NET Version & Configuration
- Use .NET 8+ for all new projects
- Enable nullable reference types (`<Nullable>enable</Nullable>`)
- Enable implicit usings (`<ImplicitUsings>enable</ImplicitUsings>`)
- Use file-scoped namespaces

## Nullable Reference Types

### DO: Handle nullability explicitly
```csharp
public async Task<User?> GetUserAsync(string userId)
{
    var user = await _repository.FindAsync(userId);
    return user; // Explicitly nullable return
}

public async Task ProcessUserAsync(User user)
{
    ArgumentNullException.ThrowIfNull(user);
    // Process...
}
```

### DON'T: Suppress nullable warnings without justification
```csharp
// ❌ Avoid
var user = GetUser()!; // Suppressing without reason

// ✅ Prefer
var user = GetUser() ?? throw new InvalidOperationException("User required");
```

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Namespaces | PascalCase | `Company.Project.Domain` |
| Classes | PascalCase | `UserRepository` |
| Interfaces | PascalCase with I prefix | `IUserService` |
| Methods | PascalCase | `GetUserByIdAsync` |
| Properties | PascalCase | `FirstName` |
| Private fields | _camelCase | `_userRepository` |
| Local variables | camelCase | `userCount` |
| Constants | PascalCase | `MaxRetryCount` |
| Async methods | Suffix with Async | `SaveAsync` |

## Modern C# Features

### Use records for immutable data
```csharp
public record User(
    string Id,
    string Email,
    string Name,
    DateTime CreatedAt);

public record CreateUserRequest(
    string Email,
    string Name);
```

### Use primary constructors (C# 12+)
```csharp
public class UserService(
    IUserRepository repository,
    ILogger<UserService> logger)
{
    public async Task<User?> GetUserAsync(string id)
    {
        logger.LogInformation("Getting user {UserId}", id);
        return await repository.FindAsync(id);
    }
}
```

### Use collection expressions
```csharp
List<string> names = ["Alice", "Bob", "Charlie"];
int[] numbers = [1, 2, 3, 4, 5];
```

### Use pattern matching
```csharp
public decimal CalculateDiscount(Customer customer) => customer switch
{
    { IsPremium: true, YearsActive: > 5 } => 0.25m,
    { IsPremium: true } => 0.15m,
    { YearsActive: > 2 } => 0.10m,
    _ => 0.05m
};
```

## Async/Await

### Always use async/await for I/O operations
```csharp
public async Task<IEnumerable<User>> GetActiveUsersAsync(
    CancellationToken cancellationToken = default)
{
    return await _context.Users
        .Where(u => u.IsActive)
        .ToListAsync(cancellationToken);
}
```

### Pass CancellationToken through the call chain
```csharp
public async Task ProcessOrderAsync(
    Order order, 
    CancellationToken cancellationToken)
{
    await _validator.ValidateAsync(order, cancellationToken);
    await _repository.SaveAsync(order, cancellationToken);
    await _notifier.NotifyAsync(order, cancellationToken);
}
```

## Dependency Injection

### Use constructor injection
```csharp
public class OrderService(
    IOrderRepository repository,
    IPaymentGateway paymentGateway,
    ILogger<OrderService> logger) : IOrderService
{
    // Use injected dependencies
}
```

### Register services with appropriate lifetimes
```csharp
services.AddScoped<IUserService, UserService>();
services.AddSingleton<ICacheService, RedisCacheService>();
services.AddTransient<IEmailService, SmtpEmailService>();
```

## Error Handling

### Use Result pattern for expected failures
```csharp
public record Result<T>
{
    public T? Value { get; init; }
    public string? Error { get; init; }
    public bool IsSuccess => Error is null;

    public static Result<T> Success(T value) => new() { Value = value };
    public static Result<T> Failure(string error) => new() { Error = error };
}
```

### Use exceptions for unexpected failures
```csharp
public class UserNotFoundException(string userId) 
    : Exception($"User not found: {userId}")
{
    public string UserId { get; } = userId;
}
```

### Use structured logging
```csharp
logger.LogInformation(
    "Processing order {OrderId} for user {UserId}",
    order.Id,
    order.UserId);

logger.LogError(
    exception,
    "Failed to process order {OrderId}",
    order.Id);
```

## Entity Framework Core

### Use async methods
```csharp
var users = await _context.Users
    .Where(u => u.IsActive)
    .Include(u => u.Orders)
    .AsNoTracking()
    .ToListAsync(cancellationToken);
```

### Use explicit loading when needed
```csharp
await _context.Entry(order)
    .Collection(o => o.Items)
    .LoadAsync(cancellationToken);
```

## Testing Requirements
- Use xUnit as the test framework
- Use FluentAssertions for assertions
- Use NSubstitute or Moq for mocking
- Use Test containers for integration tests
- Minimum 80% code coverage

```csharp
public class UserServiceTests
{
    [Fact]
    public async Task GetUserAsync_WhenUserExists_ReturnsUser()
    {
        // Arrange
        var repository = Substitute.For<IUserRepository>();
        repository.FindAsync("123").Returns(new User("123", "test@example.com"));
        var sut = new UserService(repository);

        // Act
        var result = await sut.GetUserAsync("123");

        // Assert
        result.Should().NotBeNull();
        result!.Email.Should().Be("test@example.com");
    }
}
```

## Documentation
- Use XML documentation for public APIs
- Include `<summary>`, `<param>`, `<returns>`, `<exception>` tags

```csharp
/// <summary>
/// Retrieves a user by their unique identifier.
/// </summary>
/// <param name="userId">The unique identifier of the user.</param>
/// <param name="cancellationToken">Cancellation token for the operation.</param>
/// <returns>The user if found; otherwise, null.</returns>
/// <exception cref="ArgumentException">Thrown when userId is empty.</exception>
public async Task<User?> GetUserAsync(
    string userId, 
    CancellationToken cancellationToken = default)
```
