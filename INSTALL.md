# Install via `npx skills`

The preferred way to install skills from this repo is the open [skills CLI](https://github.com/vercel-labs/skills) (`npx skills`). It copies each skill into the directories your agent already reads (Claude Code, Cursor, Codex and others).

Requires **Node.js** and network access to GitHub.

## List skills in this repo

```bash
npx skills add Kamil-Matusz/skills --list
```

## Install one skill

Project scope (default; lands in the current repo, e.g. `.claude/skills/` or `.agents/skills/`):

```bash
npx skills add Kamil-Matusz/skills --skill <skill-name>
```

Global scope (available in every project):

```bash
npx skills add Kamil-Matusz/skills --skill <skill-name> -g
```

Add `-y` to skip prompts (CI, scripts):

```bash
npx skills add Kamil-Matusz/skills --skill <skill-name> -g -y
```

Or point at the skill's directory on GitHub directly:

```bash
npx skills add https://github.com/Kamil-Matusz/skills/tree/main/skills/<skill-name>
```

### Available skills

| Skill | Command |
|-------|---------|
| `context-budget` | `npx skills add Kamil-Matusz/skills --skill context-budget` |
| `dependency-check` | `npx skills add Kamil-Matusz/skills --skill dependency-check` |
| `gateway-mapping-check` | `npx skills add Kamil-Matusz/skills --skill gateway-mapping-check` |
| `given-when-then-tests` | `npx skills add Kamil-Matusz/skills --skill given-when-then-tests` |
| `no-em-dash` | `npx skills add Kamil-Matusz/skills --skill no-em-dash` |
| `prefer-final-variables` | `npx skills add Kamil-Matusz/skills --skill prefer-final-variables` |
| `skill-audit` | `npx skills add Kamil-Matusz/skills --skill skill-audit` |

What each skill does: see the [README](README.md#skills).

## Install several or all skills

```bash
# Selected skills
npx skills add Kamil-Matusz/skills --skill dependency-check --skill skill-audit

# Everything in the repo
npx skills add Kamil-Matusz/skills --skill '*'
```

## Target a specific agent

By default the CLI may ask which agents to install into. Pin them with `-a` / `--agent`:

```bash
# Claude Code only (global)
npx skills add Kamil-Matusz/skills --skill prefer-final-variables -g -a claude-code -y

# Cursor only (global)
npx skills add Kamil-Matusz/skills --skill prefer-final-variables -g -a cursor -y

# Both
npx skills add Kamil-Matusz/skills --skill prefer-final-variables -g -a claude-code -a cursor -y
```

Useful agent ids: `claude-code`, `cursor`, `codex`, `opencode`, `github-copilot`. Full list: `npx skills --help` or the [skills CLI README](https://github.com/vercel-labs/skills).

## After install

- **Claude Code**: skills land in `.claude/skills/` (project) or `~/.claude/skills/` (global). Run `/reload` or restart, then confirm with `/skills`.
- **Cursor**: skills land in `.agents/skills/` (project) or `~/.cursor/skills/` (global). Start a new Agent chat if they don't show up.

`gateway-mapping-check` ships a helper script that must be executable on Unix:

```bash
chmod +x ~/.claude/skills/gateway-mapping-check/scripts/check_mappings.py
# or, for Cursor global:
chmod +x ~/.cursor/skills/gateway-mapping-check/scripts/check_mappings.py
```

Per-project config for that skill: see [its README](skills/gateway-mapping-check/README.md).

## Manual install (no `npx`)

Copy from a clone instead; see [README](README.md#manual-copy).
