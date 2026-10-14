---
name: prefer-final-variables
description: Mark Java variables `final` wherever it compiles and is meaningful — locals assigned once, method and constructor parameters, constructor-injected fields, `catch` parameters — while skipping the cases where `final` breaks Hibernate, Jackson or Spring proxies. Use whenever writing or editing Java code: controllers, services, repositories, mappers, DTOs, configuration classes.
Also use when the user mentions "final", "immutability", "immutable", "effectively final", "code style", or asks to clean up / review Java code style. Apply proactively to code you are already touching, even when the user does not ask about style.
metadata:
  author: "Kamil Matusz"
  version: "1.0"
---

# Prefer `final` variables

Every variable that is assigned once gets `final`. It documents intent and turns
an accidental reassignment into a compile error instead of a bug.

## Scope: touch only what you are already editing

Apply this to code you write and to lines you are already changing for another
reason. Do **not** sweep an untouched file, class or module just to add `final` —
that inflates diffs and buries the real change. A file-wide or module-wide pass
happens only when the user explicitly asks for it ("dodaj final w całym pakiecie
payment").

## Apply `final`

- **Local variables assigned once.**
  ```java
  final Order order = orderRepository.findById(id).orElseThrow();
  final BigDecimal total = calculateTotal(order);
  ```
- **Method and constructor parameters.** They are almost never meant to be
  reassigned.
  ```java
  public OrderResponse process(final OrderRequest request, final String tenantId) {
  ```
- **Fields set once** — constructor-injected dependencies and constants.
  ```java
  private final OrderRepository orderRepository;
  private final PaymentClient paymentClient;
  ```
  With Lombok, `@RequiredArgsConstructor` + `final` fields is the idiomatic
  injection style; prefer it over field `@Autowired`.
- **`catch` parameters** and **try-with-resources** resources.
  ```java
  } catch (final PaymentException e) {
  ```
- **Enhanced-for variables**, when the surrounding file already does it.
  ```java
  for (final OrderLine line : order.getLines()) {
  ```

## Do not apply `final`

- Variables that are genuinely reassigned — accumulators, loop state, a value
  built across branches. Do **not** contort code (ternaries, extracted methods,
  `Optional` gymnastics) just to make a variable final; if reassignment is the
  clearest form, leave it mutable.
- The index of a classic `for (int i = 0; ...)` loop.
- Anything where `final` does not compile: a field assigned outside the
  constructor, `@Autowired` field injection, a `@Setter`/mutable field, a
  variable a lambda or anonymous class needs to mutate.
- **JPA `@Entity` fields.** Hibernate needs a no-arg constructor and mutable
  fields for proxying and dirty checking; ids and mapped columns stay non-final.
  Value objects and `@Embeddable`s that are never mutated are fine.
- Fields deserialized by Jackson into a mutable DTO. If the DTO can be
  immutable, prefer a `record` or constructor-bound class with final fields over
  adding `final` to a setter-based class.
- `@ConfigurationProperties` using setter binding. Constructor binding
  (`@ConstructorBinding` / `record`) gets final fields; setter binding does not.
- **Class and method declarations.** This is about variables and fields only.
  `final` methods/classes break Spring CGLIB proxying (`@Transactional`,
  `@Cacheable`, `@Configuration` bean methods), so never make a Spring-managed
  bean's methods final.

## Existing files

Match the file you are in. If a class already writes `final` on locals and
parameters, keep doing it. If the whole file has none and the user has not asked
for a style pass, add `final` to new code only — do not annotate lines you happen
to scroll past.

## Self-check before finishing

1. Every new local and parameter that is never reassigned is `final`.
2. No `final` was added where it breaks compilation, Hibernate, Jackson or a
   Spring proxy.
3. No untouched code was reformatted.
4. The project still compiles and tests pass.