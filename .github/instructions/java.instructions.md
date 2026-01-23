---
applyTo:
  - "**/*.java"
  - "**/*.kt"
  - "**/*.kts"
  - "**/pom.xml"
  - "**/build.gradle*"
excludeAgent:
  - "code-review"  # Remove this line to enable for code review
---

# Java/Kotlin Development Standards

## Java Version & Configuration
- Use Java 21+ (LTS) for new projects
- Use Spring Boot 3.2+ for web applications
- Enable preview features when beneficial
- Use Maven or Gradle with consistent dependency management

## Modern Java Features

### Use records for data classes
```java
public record User(
    String id,
    String email,
    String name,
    Instant createdAt
) {}

public record CreateUserRequest(
    @NotBlank String email,
    @NotBlank @Size(max = 100) String name
) {}
```

### Use sealed classes for type hierarchies
```java
public sealed interface PaymentResult 
    permits PaymentSuccess, PaymentFailure {
}

public record PaymentSuccess(String transactionId, BigDecimal amount) 
    implements PaymentResult {}

public record PaymentFailure(String errorCode, String message) 
    implements PaymentResult {}
```

### Use pattern matching
```java
public String formatResult(PaymentResult result) {
    return switch (result) {
        case PaymentSuccess s -> "Paid: " + s.amount();
        case PaymentFailure f -> "Failed: " + f.message();
    };
}

if (obj instanceof User user) {
    processUser(user);
}
```

### Use virtual threads (Java 21+)
```java
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    var futures = users.stream()
        .map(user -> executor.submit(() -> processUser(user)))
        .toList();
    // Process results...
}
```

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Packages | lowercase | `com.company.project.domain` |
| Classes | PascalCase | `UserService` |
| Interfaces | PascalCase | `UserRepository` |
| Methods | camelCase | `getUserById` |
| Variables | camelCase | `userCount` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| Type Parameters | Single uppercase | `T`, `K`, `V`, `E` |

## Dependency Injection

### Use constructor injection
```java
@Service
public class OrderService {
    private final OrderRepository repository;
    private final PaymentGateway paymentGateway;
    private final NotificationService notificationService;

    public OrderService(
            OrderRepository repository,
            PaymentGateway paymentGateway,
            NotificationService notificationService) {
        this.repository = repository;
        this.paymentGateway = paymentGateway;
        this.notificationService = notificationService;
    }
}
```

### With Lombok (if used)
```java
@Service
@RequiredArgsConstructor
public class OrderService {
    private final OrderRepository repository;
    private final PaymentGateway paymentGateway;
}
```

## Error Handling

### Use specific exception types
```java
public class UserNotFoundException extends RuntimeException {
    private final String userId;

    public UserNotFoundException(String userId) {
        super("User not found: " + userId);
        this.userId = userId;
    }

    public String getUserId() {
        return userId;
    }
}
```

### Use @ControllerAdvice for API error handling
```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(UserNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleUserNotFound(
            UserNotFoundException ex) {
        return ResponseEntity
            .status(HttpStatus.NOT_FOUND)
            .body(new ErrorResponse("USER_NOT_FOUND", ex.getMessage()));
    }
}
```

## Optional Usage

### DO: Use Optional for potentially absent return values
```java
public Optional<User> findByEmail(String email) {
    return Optional.ofNullable(cache.get(email));
}
```

### DON'T: Use Optional for fields or parameters
```java
// ❌ Avoid
public class User {
    private Optional<String> middleName;
}

// ✅ Prefer
public class User {
    @Nullable
    private String middleName;
}
```

## Stream API

### Use streams for collection processing
```java
var activeEmails = users.stream()
    .filter(User::isActive)
    .map(User::email)
    .sorted()
    .toList();

var usersByDepartment = users.stream()
    .collect(Collectors.groupingBy(User::department));
```

## Logging

### Use SLF4J with structured logging
```java
private static final Logger log = LoggerFactory.getLogger(OrderService.class);

public void processOrder(Order order) {
    log.info("Processing order orderId={} userId={}", 
        order.getId(), order.getUserId());
    
    try {
        // Process...
        log.info("Order processed successfully orderId={}", order.getId());
    } catch (PaymentException e) {
        log.error("Payment failed orderId={} error={}", 
            order.getId(), e.getMessage(), e);
        throw e;
    }
}
```

## Testing

### Use JUnit 5 with AssertJ
```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository repository;

    @InjectMocks
    private UserService userService;

    @Test
    void getUserById_whenUserExists_returnsUser() {
        // Given
        var user = new User("123", "test@example.com", "Test User", Instant.now());
        when(repository.findById("123")).thenReturn(Optional.of(user));

        // When
        var result = userService.getUserById("123");

        // Then
        assertThat(result)
            .isPresent()
            .hasValueSatisfying(u -> {
                assertThat(u.email()).isEqualTo("test@example.com");
                assertThat(u.name()).isEqualTo("Test User");
            });
    }

    @Test
    void getUserById_whenUserNotFound_throwsException() {
        when(repository.findById("999")).thenReturn(Optional.empty());

        assertThatThrownBy(() -> userService.getUserById("999"))
            .isInstanceOf(UserNotFoundException.class)
            .hasMessageContaining("999");
    }
}
```

### Use Testcontainers for integration tests
```java
@SpringBootTest
@Testcontainers
class UserRepositoryIntegrationTest {

    @Container
    static PostgreSQLContainer<?> postgres = 
        new PostgreSQLContainer<>("postgres:16");

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }
}
```

## Documentation
- Use Javadoc for all public APIs
- Include `@param`, `@return`, `@throws` tags

```java
/**
 * Retrieves a user by their unique identifier.
 *
 * @param userId the unique identifier of the user
 * @return the user if found
 * @throws UserNotFoundException if no user exists with the given ID
 * @throws IllegalArgumentException if userId is null or blank
 */
public User getUserById(String userId) {
    // ...
}
```

## Project Structure (Spring Boot)
```
src/
├── main/
│   ├── java/com/company/project/
│   │   ├── Application.java
│   │   ├── config/           # Configuration classes
│   │   ├── controller/       # REST controllers
│   │   ├── service/          # Business logic
│   │   ├── repository/       # Data access
│   │   ├── model/            # Domain models
│   │   ├── dto/              # Data transfer objects
│   │   └── exception/        # Custom exceptions
│   └── resources/
│       ├── application.yml
│       └── db/migration/     # Flyway migrations
└── test/
    └── java/com/company/project/
```
