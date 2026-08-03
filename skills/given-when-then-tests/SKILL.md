---
name: given-when-then-tests
description: >-
  Structure Java tests with `//given` / `//when` / `//then` section comments —
  setup and stubbing under given, the single call under test under when,
  assertions only under then. Use whenever writing, extending, refactoring or
  reviewing a Java test: JUnit, Mockito, AssertJ, `@SpringBootTest`,
  `@DataJpaTest`, `@WebMvcTest`, Testcontainers integration tests. Also use when
  the user mentions "given/when/then", "arrange/act/assert", "BDD test layout",
  "test structure" or "test sections". Apply proactively to every test you write,
  even when the user does not ask about layout.
---

# `//given` / `//when` / `//then` tests

Every test method is split into three labelled sections. Comment style is exactly
`//given`, `//when`, `//then` — no space after the slashes, lowercase — each on
its own line, with a blank line before each label except the first.

```java
@Test
void shouldRejectOrderWhenBalanceIsInsufficient() {
    //given
    final Order order = anOrder().withTotal(new BigDecimal("120.00")).build();
    given(balanceClient.fetch(order.getCustomerId())).willReturn(new BigDecimal("50.00"));

    //when
    final OrderResult result = orderService.process(order);

    //then
    assertThat(result.status()).isEqualTo(REJECTED);
    verify(paymentClient, never()).charge(any());
}
```

## Section rules

- **`//given`** — fixtures, builders, stubbing (`given(...)`/`when(...)`), saved
  test data. Omit the section entirely when there is nothing to set up; never
  leave an empty `//given`.
- **`//when`** — the single call under test. If more than one call is needed to
  reach the state under test, the earlier calls belong in `//given`.
- **`//then`** — assertions and verifications only. No new stubbing here.

## Exceptions under test

Capture the throwable in `//when`, assert in `//then`:

```java
//when
final Throwable thrown = catchThrowable(() -> orderService.process(order));

//then
assertThat(thrown).isInstanceOf(InsufficientBalanceException.class);
```

If the project prefers a single `assertThatThrownBy(...)` chain, label that
section `//when & then` rather than splitting it artificially.

## Other cases

- **Parameterized tests** — same three sections inside the method body; the
  `@ValueSource`/`@MethodSource` arguments are the "given" inputs and need no
  extra comment.
- **Shared setup** — code in `@BeforeEach` is given by definition and takes no
  comment; per-test setup still goes under `//given` in the test method.
- Test method names stay descriptive (`shouldXWhenY`); section comments do not
  replace a good name.

## Existing files

When editing a test that uses a different convention (`// given` with a space,
`// Arrange`), follow the file, not this document — consistency inside the file
wins. Do not rewrite section comments in tests you are not otherwise touching.

## Self-check before finishing

1. Every new or edited test method has `//given` / `//when` / `//then` in order.
2. `//when` holds one call; `//then` holds only assertions and verifications.
3. No empty sections, no stubbing after `//then`.
4. Tests pass.
