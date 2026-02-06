# Test Data Creation Guidelines

## Overview
This guide explains how to create reusable, maintainable test data structures for complex scenarios using records, builders, and functional-style immutable modifications.

## When to Create Test Data Structures

### Use inline data when:
- Data is simple (1-3 primitive fields)
- Used only once in a single test
- Clarity is not compromised

```java
@Test
@DisplayName("processes simple order")
void testSimpleOrder() {
    var orderId = "ORD-123";
    var amount = 100.0;
    // Direct usage - no need for complex structure
}
```

### Create test data structures when:
- Same data structure used across multiple tests
- Object has many fields (4+)
- Need different variations of similar data
- Complex object graphs (nested objects)
- Want to make test intent clearer

## Test Data Pattern: Records + Builders

### Core Pattern

Use records for immutable test data with default configurations and builders for modifications:

```java
// 1. Define test data record
record UserTestData(
    String name,
    String email,
    Integer age,
    boolean active,
    List<String> roles
) {
    // 2. Empty/minimal configuration
    static UserTestData empty() {
        return new UserTestData(null, null, null, false, List.of());
    }
    
    // 3. Reasonable default configuration
    static UserTestData defaults() {
        return new UserTestData(
            "John Doe",
            "john.doe@example.com",
            30,
            true,
            List.of("USER")
        );
    }
    
    // 4. Named configurations for common scenarios
    static UserTestData admin() {
        return defaults().withRoles(List.of("USER", "ADMIN"));
    }
    
    static UserTestData inactive() {
        return defaults().withActive(false);
    }
    
    // 5. Fluent modification methods (immutable - returns new instance)
    UserTestData withName(String name) {
        return new UserTestData(name, email, age, active, roles);
    }
    
    UserTestData withEmail(String email) {
        return new UserTestData(name, email, age, active, roles);
    }
    
    UserTestData withAge(Integer age) {
        return new UserTestData(name, email, age, active, roles);
    }
    
    UserTestData withActive(boolean active) {
        return new UserTestData(name, email, age, active, roles);
    }
    
    UserTestData withRoles(List<String> roles) {
        return new UserTestData(name, email, age, active, roles);
    }
}
```

### Usage in Tests

```java
@Nested
@DisplayName("createUser()")
class CreateUserScenarios {
    
    @Test
    @DisplayName("rejects empty name")
    void testEmptyName() {
        var userData = UserTestData.defaults().withName("");
        
        assertThatThrownBy(() -> service.createUser(userData))
            .isInstanceOf(ValidationException.class);
    }
    
    @Test
    @DisplayName("accepts valid admin user")
    void testAdminCreation() {
        var userData = UserTestData.admin();
        
        var result = service.createUser(userData);
        
        assertThat(result.roles()).contains("ADMIN");
    }
    
    @Test
    @DisplayName("handles user with multiple modifications")
    void testCustomUser() {
        var userData = UserTestData.defaults()
            .withName("Jane Smith")
            .withAge(25)
            .withRoles(List.of("USER", "MODERATOR"));
        
        var result = service.createUser(userData);
        
        assertThat(result.name()).isEqualTo("Jane Smith");
        assertThat(result.age()).isEqualTo(25);
    }
}
```

## Advanced Patterns

### Nested Object Structures

For complex object graphs with nested objects:

```java
// Address test data
record AddressTestData(
    String street,
    String city,
    String country,
    String zipCode
) {
    static AddressTestData defaults() {
        return new AddressTestData(
            "123 Main St",
            "Springfield",
            "USA",
            "12345"
        );
    }
    
    static AddressTestData minimal() {
        return new AddressTestData(null, null, "USA", null);
    }
    
    AddressTestData withStreet(String street) {
        return new AddressTestData(street, city, country, zipCode);
    }
    
    AddressTestData withCity(String city) {
        return new AddressTestData(street, city, country, zipCode);
    }
    
    AddressTestData withCountry(String country) {
        return new AddressTestData(street, city, country, zipCode);
    }
    
    AddressTestData withZipCode(String zipCode) {
        return new AddressTestData(street, city, country, zipCode);
    }
}

// Order with nested address
record OrderTestData(
    String orderId,
    List<String> items,
    AddressTestData shippingAddress,
    double totalAmount
) {
    static OrderTestData defaults() {
        return new OrderTestData(
            "ORD-001",
            List.of("ITEM-1"),
            AddressTestData.defaults(),
            100.0
        );
    }
    
    OrderTestData withOrderId(String orderId) {
        return new OrderTestData(orderId, items, shippingAddress, totalAmount);
    }
    
    OrderTestData withItems(List<String> items) {
        return new OrderTestData(orderId, items, shippingAddress, totalAmount);
    }
    
    OrderTestData withShippingAddress(AddressTestData shippingAddress) {
        return new OrderTestData(orderId, items, shippingAddress, totalAmount);
    }
    
    OrderTestData withTotalAmount(double totalAmount) {
        return new OrderTestData(orderId, items, shippingAddress, totalAmount);
    }
}

// Usage
@Test
@DisplayName("ships to international address")
void testInternationalShipping() {
    var order = OrderTestData.defaults()
        .withShippingAddress(
            AddressTestData.defaults()
                .withCountry("Canada")
                .withZipCode("A1A 1A1")
        );
    
    var result = service.processOrder(order);
    
    assertThat(result.shippingCost()).isGreaterThan(0);
}
```

### Collections and Multiple Items

For test data involving collections:

```java
record ItemTestData(
    String sku,
    String name,
    double price,
    int quantity
) {
    static ItemTestData defaults() {
        return new ItemTestData("SKU-001", "Product", 10.0, 1);
    }
    
    static ItemTestData withSku(String sku) {
        return defaults().withSku(sku);
    }
    
    ItemTestData withSku(String sku) {
        return new ItemTestData(sku, name, price, quantity);
    }
    
    ItemTestData withName(String name) {
        return new ItemTestData(sku, name, price, quantity);
    }
    
    ItemTestData withPrice(double price) {
        return new ItemTestData(sku, name, price, quantity);
    }
    
    ItemTestData withQuantity(int quantity) {
        return new ItemTestData(sku, name, price, quantity);
    }
}

record CartTestData(
    String cartId,
    String userId,
    List<ItemTestData> items
) {
    static CartTestData empty() {
        return new CartTestData("CART-001", "USER-001", List.of());
    }
    
    static CartTestData withSingleItem() {
        return empty().withItems(List.of(ItemTestData.defaults()));
    }
    
    static CartTestData withMultipleItems() {
        return empty().withItems(List.of(
            ItemTestData.defaults().withSku("SKU-001").withQuantity(2),
            ItemTestData.defaults().withSku("SKU-002").withQuantity(1)
        ));
    }
    
    CartTestData withCartId(String cartId) {
        return new CartTestData(cartId, userId, items);
    }
    
    CartTestData withUserId(String userId) {
        return new CartTestData(cartId, userId, items);
    }
    
    CartTestData withItems(List<ItemTestData> items) {
        return new CartTestData(cartId, userId, items);
    }
    
    // Helper to add single item
    CartTestData addItem(ItemTestData item) {
        var newItems = new ArrayList<>(items);
        newItems.add(item);
        return new CartTestData(cartId, userId, List.copyOf(newItems));
    }
}

// Usage
@Test
@DisplayName("calculates total with multiple items")
void testMultipleItems() {
    var cart = CartTestData.empty()
        .addItem(ItemTestData.defaults().withPrice(10.0).withQuantity(2))
        .addItem(ItemTestData.defaults().withPrice(5.0).withQuantity(3));
    
    var result = service.calculateTotal(cart);
    
    assertThat(result).isEqualTo(35.0); // (10*2) + (5*3)
}
```

### Builder Pattern for Very Complex Objects

For extremely complex objects where record constructors become unwieldy:

```java
// Traditional builder for very complex scenarios
static class PaymentRequestBuilder {
    private String transactionId = "TXN-001";
    private String userId = "USER-001";
    private double amount = 100.0;
    private String currency = "USD";
    private String paymentMethod = "CREDIT_CARD";
    private Map<String, String> metadata = new HashMap<>();
    private AddressTestData billingAddress = AddressTestData.defaults();
    private List<String> items = List.of("ITEM-1");
    
    static PaymentRequestBuilder defaults() {
        return new PaymentRequestBuilder();
    }
    
    static PaymentRequestBuilder minimal() {
        var builder = new PaymentRequestBuilder();
        builder.metadata = Map.of();
        builder.items = List.of();
        return builder;
    }
    
    PaymentRequestBuilder withTransactionId(String transactionId) {
        this.transactionId = transactionId;
        return this;
    }
    
    PaymentRequestBuilder withUserId(String userId) {
        this.userId = userId;
        return this;
    }
    
    PaymentRequestBuilder withAmount(double amount) {
        this.amount = amount;
        return this;
    }
    
    PaymentRequestBuilder withCurrency(String currency) {
        this.currency = currency;
        return this;
    }
    
    PaymentRequestBuilder withPaymentMethod(String paymentMethod) {
        this.paymentMethod = paymentMethod;
        return this;
    }
    
    PaymentRequestBuilder withMetadata(Map<String, String> metadata) {
        this.metadata = new HashMap<>(metadata);
        return this;
    }
    
    PaymentRequestBuilder addMetadata(String key, String value) {
        this.metadata.put(key, value);
        return this;
    }
    
    PaymentRequestBuilder withBillingAddress(AddressTestData billingAddress) {
        this.billingAddress = billingAddress;
        return this;
    }
    
    PaymentRequestBuilder withItems(List<String> items) {
        this.items = new ArrayList<>(items);
        return this;
    }
    
    PaymentRequest build() {
        return new PaymentRequest(
            transactionId,
            userId,
            amount,
            currency,
            paymentMethod,
            Map.copyOf(metadata),
            billingAddress,
            List.copyOf(items)
        );
    }
}

// Usage
@Test
@DisplayName("processes payment with custom metadata")
void testPaymentWithMetadata() {
    var payment = PaymentRequestBuilder.defaults()
        .withAmount(250.0)
        .addMetadata("invoice_id", "INV-123")
        .addMetadata("customer_note", "Rush delivery")
        .build();
    
    var result = service.processPayment(payment);
    
    assertThat(result.status()).isEqualTo("PROCESSED");
}
```

## Organization in Test Files

### Option 1: Bottom of Test Class (Preferred for Small Tests)

```java
@DisplayName("OrderService")
class OrderServiceTest {
    
    @Nested
    @DisplayName("processOrder()")
    class ProcessOrderScenarios {
        
        @Test
        @DisplayName("accepts valid order")
        void testValidOrder() {
            var order = OrderTestData.defaults();
            // test logic
        }
    }
    
    // Test data at bottom of file
    record OrderTestData(String id, double amount) {
        static OrderTestData defaults() {
            return new OrderTestData("ORD-001", 100.0);
        }
        
        OrderTestData withId(String id) {
            return new OrderTestData(id, amount);
        }
        
        OrderTestData withAmount(double amount) {
            return new OrderTestData(id, amount);
        }
    }
}
```

### Option 2: Separate Test Data Class (Preferred for Shared/Complex Data)

```java
// In test/java/.../testdata/OrderTestData.java
package com.example.testdata;

public record OrderTestData(
    String orderId,
    String userId,
    List<ItemTestData> items,
    double totalAmount
) {
    public static OrderTestData defaults() {
        return new OrderTestData(
            "ORD-001",
            "USER-001",
            List.of(ItemTestData.defaults()),
            100.0
        );
    }
    
    public OrderTestData withOrderId(String orderId) {
        return new OrderTestData(orderId, userId, items, totalAmount);
    }
    
    // ... other methods
}

// In test class
import static com.example.testdata.OrderTestData.*;

class OrderServiceTest {
    @Test
    void testOrder() {
        var order = defaults().withOrderId("ORD-999");
        // use order
    }
}
```

### Option 3: Static Factory Methods (For Very Simple Cases)

```java
class UserServiceTest {
    
    @Test
    @DisplayName("creates user")
    void testCreateUser() {
        var user = createValidUser();
        // test logic
    }
    
    @Test
    @DisplayName("rejects invalid user")
    void testInvalidUser() {
        var user = createInvalidUser();
        // test logic
    }
    
    // Simple factory methods at bottom
    private static User createValidUser() {
        return new User("John", "john@example.com", 30);
    }
    
    private static User createInvalidUser() {
        return new User("", "invalid-email", -5);
    }
}
```

## Practical Guidelines

### 1. Start Simple, Evolve as Needed

Don't create elaborate test data structures upfront. Start with inline data and extract when patterns emerge:

```java
// Iteration 1: Inline data
@Test
void testUserCreation() {
    var name = "John";
    var email = "john@example.com";
    // ...
}

// Iteration 2: Same structure repeated in multiple tests
// → Extract to factory method

// Iteration 3: Need variations
// → Introduce record with defaults and modifiers

// Iteration 4: Very complex or shared across test classes
// → Move to separate test data class
```

### 2. Prefer Immutability

Always return new instances, never mutate:

```java
// Good: Immutable modification
UserTestData withName(String name) {
    return new UserTestData(name, email, age, active, roles);
}

// Bad: Mutable modification
void setName(String name) {
    this.name = name; // Don't do this in test data records
}
```

### 3. Named Configurations for Common Scenarios

Provide meaningful named constructors:

```java
record UserTestData(String name, String email, boolean verified) {
    static UserTestData defaults() { /* ... */ }
    static UserTestData unverified() { return defaults().withVerified(false); }
    static UserTestData admin() { return defaults().withEmail("admin@example.com"); }
    static UserTestData newUser() { return defaults().withVerified(false); }
}

// Clear intent in tests
var user = UserTestData.admin();
var user = UserTestData.newUser();
```

### 4. Composition Over Inheritance

Compose test data structures rather than creating hierarchies:

```java
// Good: Composition
record OrderTestData(
    String id,
    UserTestData customer,
    AddressTestData shipping
) { }

// Avoid: Inheritance hierarchies in test data
// class BaseOrderTestData { }
// class PremiumOrderTestData extends BaseOrderTestData { }
```

### 5. Keep Test Data Close to Domain

Test data structure should mirror (but simplify) actual domain objects:

```java
// Domain object
class Order {
    private String orderId;
    private Customer customer;
    private ShippingAddress address;
    private List<OrderItem> items;
    private OrderStatus status;
    private LocalDateTime createdAt;
    // ... many more fields
}

// Test data - simplified, focused on what tests need
record OrderTestData(
    String orderId,
    String customerId,
    String shippingCountry,
    List<String> itemSkus
) {
    // Only essential fields for testing
}
```

## Complete Example

```java
@DisplayName("PaymentService")
class PaymentServiceTest {
    
    @Nested
    @DisplayName("processPayment()")
    class ProcessPaymentScenarios {
        
        @Test
        @DisplayName("processes valid payment")
        void testValidPayment() {
            var payment = PaymentTestData.defaults();
            var service = new PaymentService();
            
            var result = service.processPayment(payment);
            
            assertThat(result.status()).isEqualTo("SUCCESS");
        }
        
        @Test
        @DisplayName("rejects payment exceeding limit")
        void testExceedsLimit() {
            var payment = PaymentTestData.defaults()
                .withAmount(10000.0);
            var service = new PaymentService();
            
            assertThatThrownBy(() -> service.processPayment(payment))
                .isInstanceOf(PaymentLimitException.class);
        }
        
        @Test
        @DisplayName("handles international payment")
        void testInternationalPayment() {
            var payment = PaymentTestData.defaults()
                .withCurrency("EUR")
                .withBillingAddress(
                    AddressTestData.defaults().withCountry("France")
                );
            var service = new PaymentService();
            
            var result = service.processPayment(payment);
            
            assertThat(result.fees()).isGreaterThan(0);
        }
    }
    
    // Test data structures at bottom of file
    
    record PaymentTestData(
        String transactionId,
        double amount,
        String currency,
        AddressTestData billingAddress
    ) {
        static PaymentTestData defaults() {
            return new PaymentTestData(
                "TXN-001",
                100.0,
                "USD",
                AddressTestData.defaults()
            );
        }
        
        PaymentTestData withTransactionId(String transactionId) {
            return new PaymentTestData(transactionId, amount, currency, billingAddress);
        }
        
        PaymentTestData withAmount(double amount) {
            return new PaymentTestData(transactionId, amount, currency, billingAddress);
        }
        
        PaymentTestData withCurrency(String currency) {
            return new PaymentTestData(transactionId, amount, currency, billingAddress);
        }
        
        PaymentTestData withBillingAddress(AddressTestData billingAddress) {
            return new PaymentTestData(transactionId, amount, currency, billingAddress);
        }
    }
    
    record AddressTestData(
        String street,
        String city,
        String country
    ) {
        static AddressTestData defaults() {
            return new AddressTestData("123 Main St", "Springfield", "USA");
        }
        
        AddressTestData withStreet(String street) {
            return new AddressTestData(street, city, country);
        }
        
        AddressTestData withCity(String city) {
            return new AddressTestData(street, city, country);
        }
        
        AddressTestData withCountry(String country) {
            return new AddressTestData(street, city, country);
        }
    }
}
```

## Key Takeaways

1. **Use records** for immutable test data with fluent modification methods
2. **Provide defaults** (empty, minimal, reasonable) as starting points
3. **Create named configurations** for common scenarios
4. **Keep it simple** - don't over-engineer test data structures
5. **Evolve gradually** - start inline, extract when patterns emerge
6. **Organize wisely** - bottom of test file or separate class based on complexity
7. **Mirror domain** - but simplify to what tests actually need
8. **Stay immutable** - always return new instances, never mutate
