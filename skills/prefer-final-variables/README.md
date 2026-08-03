# prefer-final-variables (Claude Code skill)

Marks Java variables `final` wherever it compiles and is meaningful — locals,
parameters, constructor-injected fields — and skips the cases where `final`
breaks Hibernate, Jackson or Spring CGLIB proxies.

Companion skill: `given-when-then-tests` (test layout). The two are independent;
install either or both.

## Install once (user-level, all projects)

```bash
mkdir -p ~/.claude/skills && cp -r skills/prefer-final-variables ~/.claude/skills/
```

Restart Claude Code (or `/reload`) and confirm with `/skills`.

Alternative: install per-project by copying into `<repo>/.claude/skills/` so the
convention travels with the repo in git.

## How it triggers

No script, no configuration — the description carries the triggers, so Claude
picks it up automatically when writing or editing Java code. Explicit invocation:
`/prefer-final-variables`.

## Scope guard

Applies to code being written or already edited. A whole-file or whole-module
pass happens only when explicitly requested ("dodaj final w całym pakiecie
payment").

## Want it enforced, not just suggested

A skill is guidance, not a linter. For a hard guarantee add Checkstyle
`FinalLocalVariable` + `FinalParameters` to the build — but suppress it for
packages holding `@Entity` classes and setter-bound DTOs, where `final` is wrong.
