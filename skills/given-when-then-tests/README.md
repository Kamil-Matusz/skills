# given-when-then-tests (Claude Code skill)

Structures Java tests with `//given` / `//when` / `//then` section comments:
setup and stubbing under given, one call under when, assertions only under then.

Covers JUnit, Mockito, AssertJ, `@SpringBootTest`, `@DataJpaTest`, `@WebMvcTest`
and Testcontainers tests. Not related to Cucumber or Spock — this is about
section comments in ordinary JUnit tests.

Companion skill: `prefer-final-variables` (production code style). The two are
independent; install either or both.

## Install once (user-level, all projects)

```bash
mkdir -p ~/.claude/skills && cp -r skills/given-when-then-tests ~/.claude/skills/
```

Restart Claude Code (or `/reload`) and confirm with `/skills`.

Alternative: install per-project by copying into `<repo>/.claude/skills/` so the
convention travels with the repo in git.

## How it triggers

No script, no configuration — the description carries the triggers, so Claude
picks it up automatically when writing or editing tests. Explicit invocation:
`/given-when-then-tests`.

## Scope guard

Applies to tests being written or already edited, and follows the surrounding
file when it uses a different convention (`// given` with a space, `// Arrange`).
Existing tests are not rewritten unless asked.
