---
name: Test Coverage
description: Template for delegating test writing to Copilot coding agent
---

# Test Coverage Task

## Testing Objective
<!-- What code needs test coverage -->
[Describe what needs to be tested]

## Files to Test
<!-- List files that need test coverage -->
| Source File | Current Coverage | Target Coverage |
|-------------|------------------|-----------------|
| `src/path/file1.ts` | 0% | 80%+ |
| `src/path/file2.ts` | 40% | 80%+ |

## Test Types Required
<!-- Check applicable types -->
- [ ] Unit tests
- [ ] Integration tests
- [ ] End-to-end tests
- [ ] Snapshot tests
- [ ] API tests

## Test Cases to Cover

### Happy Path Tests
<!-- Normal usage scenarios -->
- [ ] [Test case 1: e.g., valid input produces expected output]
- [ ] [Test case 2: e.g., successful operation returns success]
- [ ] [Test case 3]

### Edge Cases
<!-- Boundary conditions -->
- [ ] [Edge case 1: e.g., empty input]
- [ ] [Edge case 2: e.g., maximum values]
- [ ] [Edge case 3: e.g., minimum values]

### Error Cases
<!-- Failure scenarios -->
- [ ] [Error case 1: e.g., invalid input throws error]
- [ ] [Error case 2: e.g., network failure handled]
- [ ] [Error case 3: e.g., unauthorized access rejected]

## Mocking Requirements
<!-- What needs to be mocked -->
| Dependency | Mock Approach |
|------------|---------------|
| Database | In-memory/mock repository |
| External API | Mock HTTP responses |
| File system | Virtual filesystem |
| Time | Fixed/mocked clock |

## Test Structure
<!-- Expected test file organization -->
```typescript
describe('[Module/Component Name]', () => {
  describe('[Method/Function]', () => {
    it('should [expected behavior] when [condition]', () => {
      // Arrange
      // Act
      // Assert
    });
  });
});
```

## Acceptance Criteria
<!-- How to verify testing is complete -->
- [ ] All specified test cases implemented
- [ ] Coverage meets target percentage
- [ ] All tests pass consistently
- [ ] No flaky tests
- [ ] Tests are readable and maintainable
- [ ] Tests document expected behavior

## Test Naming Convention
<!-- How tests should be named -->
- Use descriptive names: `should_returnUser_when_idIsValid`
- Or BDD style: `'should return user when id is valid'`
- Include the condition being tested
- Be specific about expected outcome

## Testing Utilities Available
<!-- Existing test helpers -->
- Test framework: [Jest/Vitest/Mocha]
- Mocking library: [Jest mocks/Sinon/etc]
- Assertion library: [Built-in/Chai/etc]
- Test utilities: `tests/helpers/...`
- Fixtures: `tests/fixtures/...`

## Constraints
<!-- Testing limitations -->
- Do not modify source code (tests only)
- Use existing test patterns in codebase
- Keep tests fast (< 100ms per unit test)
- No network calls in unit tests
- No database calls in unit tests

## References
<!-- Helpful examples -->
- Similar tests: `tests/example.test.ts`
- Test patterns doc: [link]
- Mocking examples: [link]

---

**Labels:** `copilot-delegate`, `type:test`
