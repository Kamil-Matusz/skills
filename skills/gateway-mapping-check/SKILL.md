---
name: gateway-mapping-check
description: >-
  Verify that Spring controller endpoints have a matching apiGateway path mapping
  in a Helm values.yaml. Use this whenever a new @GetMapping / @PostMapping /
  @PutMapping / @DeleteMapping / @PatchMapping (or a new @RequestMapping route) is
  added or changed in a *Controller, before opening a PR, or whenever the user
  mentions "values.yaml", "gateway mapping", "apiGateway", "route", "the endpoint
  404s at the gateway", or asks whether a new endpoint is exposed/routed. A missing
  mapping means the endpoint is unreachable through the gateway, so always run this
  check after adding an endpoint even if the user does not explicitly ask.
allowed-tools: Bash, Read
---

# Gateway mapping check

New controller endpoints only become reachable if the API gateway is told to route
their path to the service. That routing lives in a Helm `values.yaml` under
`app.apiGateway.mappings`. It is easy to add an endpoint and forget the mapping —
the code compiles and unit tests pass, but the endpoint returns 404 at the gateway
in every environment. This skill catches that gap.

## How the two sides line up

- A controller path is `class @RequestMapping base` + `method mapping value`, e.g.
  `@RequestMapping("/api/v2/checkout")` + `@PutMapping("/balance")` →
  `/api/v2/checkout/balance`. The base may be a Spring placeholder
  (`${spring.data.rest.base-path.v2}` = `/api/v2`).
- `values.yaml` sets `apiPathComponent: /api/`, so mapping entries drop the `/api`
  prefix: the entry for the endpoint above is `- path: /v2/checkout/balance`.
- The gateway routes by **string prefix**, so `/v2/checkout/payments` is already
  reachable via a `/v2/checkout/payment` entry. A dedicated entry is only needed
  when you want a distinct timeout or an explicit, self-documenting route.

## Per-project configuration

The script needs to know where the values.yaml and controllers live in the current
project. It looks for `.gateway-mapping-check.yaml` at the repo root:

```yaml
# .gateway-mapping-check.yaml
values_yaml: chart/checkout/values.yaml
application_yml: src/main/resources/application.yml   # optional, for ${...} placeholders
controllers_glob: src/main/java/**/*Controller.java
```

If the file is absent, the script falls back to sensible defaults (see
`--help`). All three keys can also be overridden with CLI flags.

## Running the check

Run from the repo root. Default mode checks every endpoint in controllers touched
on the current branch (vs `origin/master`) — that is the pre-PR gate. Pre-existing
endpoints in a touched file appear too (as ✅/🟡), which also catches mappings
accidentally removed from values.yaml:

```bash
python3 ~/.claude/skills/gateway-mapping-check/scripts/check_mappings.py
```

- `--all` — audit every controller in the repo (surfaces pre-existing gaps too).
- `--base <ref>` — diff against a different base ref.
- `--files <paths...>` — check specific controller files.
- `--values-yaml <path>` / `--controllers-glob <glob>` / `--application-yml <path>`
  — override config for a one-off run.

The script exits non-zero when a gateway-managed endpoint lacks a mapping, so it
can back a pre-push hook or CI step.

## Reading the output

Each endpoint gets one of four statuses:

- ✅ **exact** — a `- path:` entry matches the endpoint exactly. Nothing to do.
- 🟡 **prefix** — no dedicated entry, but a broader entry already routes it
  (gateway prefix match). Usually fine; add a dedicated entry only if it needs its
  own timeout.
- ❌ **missing** — the endpoint is in a gateway-managed area (e.g. `/v2/checkout`)
  but no entry covers it. **This is the real problem — add a mapping.**
- ℹ️ **unmanaged** — the endpoint's area has no gateway mappings at all (e.g.
  `/v1/admin/*`). These are typically internal/admin routes exposed elsewhere;
  confirm that is intended, but it is not treated as a failure.

## Fixing a missing mapping

Add an entry under `app.apiGateway.mappings` in the project's values.yaml, using
the stripped path the script prints (the part after `/api`). Place it next to the
related route to keep the list readable, and mirror the `timeoutMs` of the
sibling/`v1` equivalent unless the endpoint has a different latency profile:

```yaml
      - path: /v2/checkout/payment
        timeoutMs: 20000
      - path: /v2/checkout/balance   # new endpoint
        timeoutMs: 10000
```

Then re-run the script to confirm the endpoint now reports ✅.

## Known limitations (check these by eye)

The script deliberately stays regex-simple. Two Spring patterns it does not fully
handle — when you see them in a diff, verify the mapping manually:

- Path arrays: `@GetMapping({"/a", "/b"})` — only the first path is checked.
- Paths without a leading slash: `@GetMapping("balance")` — skipped entirely.

## Prerequisites

- Python 3.8+
- `git` available on PATH
- Run from within a git checkout of the target project
