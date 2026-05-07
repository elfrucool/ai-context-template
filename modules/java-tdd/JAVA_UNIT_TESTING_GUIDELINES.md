# Java Unit Testing Guidelines

## Overview

These guidelines define how to write JUnit 5 unit tests for Java code. Follow these principles to create maintainable, clear, and effective test suites.

## Core Principles

### 1. Incremental Test Development

- **Start small**: Begin with the simplest test case, not the entire test suite
- **One test at a time**: Write one complete test before moving to the next
- **One scenario at a time**: Don't try to cover all scenarios in the first iteration
- **Gradual complexity**: Add complexity incrementally as you understand the behavior

### 2. Understanding principles

- Ask yourself what is the purpose of the piece of code under test
- If many changes need to be made at once, share with me a plan and let's decide together the course of action
- Don't hesitate to ask for clarification

### 2.1. Mocking Guidelines - Test External Dependencies, Not Internal Methods

**Key Principle**: Mocking should be used for external dependencies only, not for testing internal method behavior.

Ok, there could be exceptions, but when you find that the method under test is not accessible, then ask me. Or if you find yourself thinking "if only this method/field were accessible", then ask me.

**When to Mock**:

- External services (APIs, databases, file systems)
- Third-party libraries
- Network calls
- Time-dependent operations (clocks, timers)

**When NOT to Mock**:

- Private or protected methods within the same class
- Internal business logic
- Data transformation methods

**Alternative Approaches for Internal Methods**:

1. **Make methods more accessible** - Change `private` to `protected` or package-private for testing
2. **Extract to separate classes** - Move complex logic to dedicated service classes
3. **Use static methods** - Reduce dependencies and make testing easier
4. **Test through public interface** - Test the behavior indirectly through public methods

**Benefits**:

- Cleaner, more focused tests
- Less brittle test setup
- Better test coverage of actual implementation
- Easier maintenance and refactoring

**Example**:

```java
// Instead of mocking private method:
@Mock private Service service;
when(service.internalMethod()).thenReturn(result);

// Make method accessible and test directly:
var result = Service.internalMethod(testInput);
assertThat(result).isEqualTo(expected);
```

### 3. Test Progression Order

Test cases should progress from simple to complex:

1. **Early exits first**: Test quick validation failures, null checks, empty inputs
2. **Happy path**: Test the standard successful case
3. **Edge cases**: Test boundary conditions
4. **Deep logic**: Test complex branching and state transitions
5. **Error scenarios**: Test exception handling and failure modes
6. **Tests ordering**: tests should appear from simpler to more complex so anyone who reads the file can gain understanding gradually

### 4. Test Execution

I prefer to be myself who execute the tests, and only when requested, I will let you execute the tests.

## Test Structure

### File and Class Organization

```java
// Testing Foo.java
class FooTest {
    
    // Nested class per method under test
    @Nested
    @DisplayName("bar()")
    class BarScenarios {
        
        @Test
        @DisplayName("returns empty list when input is null")
        void testNullInput() {
            // Simple scenario - start here
        }
        
        @Test
        @DisplayName("processes valid input successfully")
        void testValidInput() {
            // Happy path
        }
        
        // Group structurally similar scenarios with parameterized tests
        @ParameterizedTest
        @DisplayName("handles various empty collections")
        @MethodSource("emptyCollectionCases")
        void testEmptyCollections(Collection<?> input) {
            // Similar test structure, different inputs
        }
        
        // Structurally different scenarios get their own nested class
        @Nested
        @DisplayName("when cache is enabled")
        class WithCacheEnabled {
            
            @Test
            @DisplayName("returns cached result on second call")
            void testCacheHit() {
                // Different setup, different assertions
            }
        }
    }
    
    @Nested
    @DisplayName("baz()")
    class BazScenarios {
        // Tests for Foo.baz() method
    }
}
```

### Naming Conventions

- **Test class**: `FooTest` for testing `Foo`
- **Nested scenario class**: Descriptive names like `BarScenarios`, `WhenInputIsNull`, `GivenValidCache`
- **Test methods**: Short, camelCase names like `testNullInput`, `testValidData`, `testCacheHit`
- **@DisplayName**: Always use for clarity - this is what humans read
  - Make it a complete sentence describing the expected behavior
  - Example: `"returns empty list when input is null"`
  - Example: `"throws IllegalArgumentException when name is blank"`

## Test Implementation

### Assertions

Use AssertJ fluent assertions:

```java
import static org.assertj.core.api.Assertions.*;

// Good
assertThat(result).isNotNull();
assertThat(result).isEmpty();
assertThat(result.size()).isEqualTo(5);
assertThat(result).containsExactly("a", "b", "c");
assertThat(exception).isInstanceOf(IllegalArgumentException.class)
    .hasMessage("Name cannot be blank");

// Avoid JUnit assertions
// assertEquals(5, result.size());  // Don't use this
```

### Mocking

Use programmatic Mockito (not annotations):

```java
import static org.mockito.Mockito.*;

@Test
@DisplayName("fetches data from repository")
void testRepositoryCall() {
    // Create mocks programmatically
    var repository = mock(UserRepository.class);
    var validator = mock(InputValidator.class);
    
    // Setup behavior
    when(repository.findById(123L)).thenReturn(Optional.of(user));
    when(validator.isValid(any())).thenReturn(true);
    
    // Create system under test
    var service = new UserService(repository, validator);
    
    // Execute and verify
    var result = service.getUser(123L);
    
    assertThat(result).isEqualTo(user);
    verify(repository).findById(123L);
}
```

### Test Data Organization

Organize test data by proximity to test logic:

```java
@Nested
@DisplayName("processOrder()")
class ProcessOrderScenarios {
    
    @Test
    @DisplayName("accepts valid order")
    void testValidOrder() {
        // Simple data inline
        var orderId = "ORD-123";
        var amount = 100.0;
        
        // Test logic here
    }
    
    @Test
    @DisplayName("processes complex order with multiple items")
    void testComplexOrder() {
        // Complex data via builder (defined below)
        var order = anOrder()
            .withItems(
                anItem().withSku("SKU-1").withQuantity(2).build(),
                anItem().withSku("SKU-2").withQuantity(1).build()
            )
            .withShipping(aShippingAddress().withCountry("US").build())
            .build();
        
        // Test logic here
    }
    
    // Test builders at bottom of test class or scenario
    private static OrderBuilder anOrder() {
        return new OrderBuilder();
    }
    
    private static ItemBuilder anItem() {
        return new ItemBuilder();
    }
    
    private static class OrderBuilder {
        // Builder implementation
    }
}
```

### Test Isolation and Setup

Prefer complete test isolation:

```java
@Nested
@DisplayName("calculateTotal()")
class CalculateTotalScenarios {
    
    @Test
    @DisplayName("calculates simple total")
    void testSimpleCalculation() {
        // Everything needed for this test is right here
        var calculator = new PriceCalculator();
        var items = List.of(new Item("A", 10.0));
        
        var result = calculator.calculateTotal(items);
        
        assertThat(result).isEqualTo(10.0);
    }
}
```

Use `@BeforeEach` only when complexity increases:

```java
@Nested
@DisplayName("when processing transactions")
class TransactionProcessingScenarios {
    
    private TransactionProcessor processor;
    private AccountRepository accountRepo;
    private AuditLogger auditLogger;
    
    @BeforeEach
    void setUp() {
        // Shared setup for multiple complex tests
        accountRepo = mock(AccountRepository.class);
        auditLogger = mock(AuditLogger.class);
        processor = new TransactionProcessor(accountRepo, auditLogger);
        
        // Common stubbing
        when(accountRepo.findById(any())).thenReturn(Optional.of(new Account()));
    }
    
    @Test
    @DisplayName("logs transaction to audit system")
    void testAuditLogging() {
        // Test-specific data
        var transaction = aTransaction().withAmount(100.0).build();
        
        processor.process(transaction);
        
        verify(auditLogger).log(any(AuditEvent.class));
    }
}
```

### Parameterized Tests

Use for similar test structures with different inputs:

```java
@ParameterizedTest
@DisplayName("validates various invalid email formats")
@ValueSource(strings = {
    "",
    "notanemail",
    "@example.com",
    "user@",
    "user @example.com"
})
void testInvalidEmails(String email) {
    var validator = new EmailValidator();
    
    assertThat(validator.isValid(email)).isFalse();
}

@ParameterizedTest
@DisplayName("calculates discount for different tiers")
@MethodSource("discountTiers")
void testDiscountCalculation(int purchaseAmount, double expectedDiscount) {
    var calculator = new DiscountCalculator();
    
    var result = calculator.calculateDiscount(purchaseAmount);
    
    assertThat(result).isEqualTo(expectedDiscount);
}

private static Stream<Arguments> discountTiers() {
    return Stream.of(
        Arguments.of(50, 0.0),    // Below threshold
        Arguments.of(100, 5.0),   // Bronze tier
        Arguments.of(500, 10.0),  // Silver tier
        Arguments.of(1000, 15.0)  // Gold tier
    );
}
```

## Java 21 Features

Leverage modern Java features in tests:

```java
@Test
@DisplayName("processes different payment methods")
void testPaymentProcessing() {
    var payment = new CreditCardPayment("1234-5678");
    
    // Pattern matching in switch
    var result = switch (payment) {
        case CreditCardPayment cc -> processCard(cc);
        case PayPalPayment pp -> processPayPal(pp);
        case BankTransferPayment bt -> processBankTransfer(bt);
        default -> throw new IllegalArgumentException("Unknown payment type");
    };
    
    assertThat(result).isNotNull();
}

@Test
@DisplayName("validates user record fields")
void testUserRecord() {
    // Records for test data
    record UserData(String name, String email, int age) {}
    
    var user = new UserData("John", "john@example.com", 30);
    var validator = new UserValidator();
    
    assertThat(validator.isValid(user)).isTrue();
}
```

## Testing Approach

### Start Simple

**First test** - Early exit case:

```java
@Test
@DisplayName("returns empty when input is null")
void testNullInput() {
    var processor = new DataProcessor();
    
    var result = processor.process(null);
    
    assertThat(result).isEmpty();
}
```

**Second test** - Happy path:

```java
@Test
@DisplayName("processes valid data successfully")
void testValidData() {
    var processor = new DataProcessor();
    var input = List.of("a", "b", "c");
    
    var result = processor.process(input);
    
    assertThat(result).hasSize(3);
    assertThat(result).containsExactly("A", "B", "C");
}
```

**Then** - Add edge cases and complex scenarios incrementally.

### Incremental Complexity

Don't write this all at once:

```java
// DON'T: Try to build everything in first iteration
@Nested
@DisplayName("processPayment()")
class ProcessPaymentScenarios {
    // 15 different test methods with complex setup
    // Multiple nested classes
    // Extensive mocking
    // ...
}
```

Instead, build step by step:

```java
// Iteration 1: Start with simplest case
@Nested
@DisplayName("processPayment()")
class ProcessPaymentScenarios {
    
    @Test
    @DisplayName("rejects null payment")
    void testNullPayment() {
        var service = new PaymentService();
        
        assertThatThrownBy(() -> service.processPayment(null))
            .isInstanceOf(IllegalArgumentException.class);
    }
}

// Iteration 2: Add happy path
// ... add testValidPayment()

// Iteration 3: Add first error scenario
// ... add testInsufficientFunds()

// And so on...
```

## Unit Test Constraints

- **No Spring**: No `@SpringBootTest`, no dependency injection containers
- **No integration**: No database, no HTTP calls, no file system (unless that's what you're testing)
- **Mockito allowed**: Use `mock()`, `when()`, `verify()` as needed
- **Fast execution**: Tests should run in milliseconds

## Exception Testing

```java
@Test
@DisplayName("throws IllegalArgumentException when amount is negative")
void testNegativeAmount() {
    var calculator = new PriceCalculator();
    
    assertThatThrownBy(() -> calculator.calculate(-10.0))
        .isInstanceOf(IllegalArgumentException.class)
        .hasMessage("Amount must be positive")
        .hasNoCause();
}

@Test
@DisplayName("throws custom exception with proper cause chain")
void testExceptionChain() {
    var service = new PaymentService();
    var payment = aPayment().withInvalidCard().build();
    
    assertThatThrownBy(() -> service.process(payment))
        .isInstanceOf(PaymentProcessingException.class)
        .hasMessageContaining("Failed to process payment")
        .hasCauseInstanceOf(CardValidationException.class);
}
```

## Summary Checklist

When writing tests, ensure:

- [ ] Started with simplest case (early exit/null check)
- [ ] One test written and working before moving to next
- [ ] @DisplayName clearly describes expected behavior
- [ ] AssertJ assertions used throughout
- [ ] Mocks created programmatically (not with annotations)
- [ ] Test data organized by complexity (simple inline, complex external)
- [ ] Test is isolated (can run independently)
- [ ] Test is fast (no external dependencies)
- [ ] Progressing from simple → complex scenarios
- [ ] Not trying to build entire suite at once

## Example Complete Test Structure

```java
package com.example.service;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.Mockito.*;

@DisplayName("UserService")
class UserServiceTest {
    
    @Nested
    @DisplayName("createUser()")
    class CreateUserScenarios {
        
        @Test
        @DisplayName("throws exception when request is null")
        void testNullRequest() {
            var repository = mock(UserRepository.class);
            var service = new UserService(repository);
            
            assertThatThrownBy(() -> service.createUser(null))
                .isInstanceOf(IllegalArgumentException.class);
        }
        
        @Test
        @DisplayName("creates user with valid data")
        void testValidCreation() {
            var repository = mock(UserRepository.class);
            var service = new UserService(repository);
            var request = new CreateUserRequest("John", "john@example.com");
            
            when(repository.save(any())).thenReturn(new User(1L, "John", "john@example.com"));
            
            var result = service.createUser(request);
            
            assertThat(result.id()).isEqualTo(1L);
            assertThat(result.name()).isEqualTo("John");
            verify(repository).save(any(User.class));
        }
        
        @ParameterizedTest
        @DisplayName("rejects invalid email formats")
        @ValueSource(strings = {"", "notanemail", "@example.com"})
        void testInvalidEmails(String email) {
            var repository = mock(UserRepository.class);
            var service = new UserService(repository);
            var request = new CreateUserRequest("John", email);
            
            assertThatThrownBy(() -> service.createUser(request))
                .isInstanceOf(ValidationException.class);
        }
    }
    
    @Nested
    @DisplayName("updateUser()")
    class UpdateUserScenarios {
        // Tests for updateUser() method
        // Start simple, build incrementally
    }
}
```
