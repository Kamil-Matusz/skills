# Install via `npx skills`

Preferred way to install skills from this repo is the open [skills CLI](https://github.com/vercel-labs/skills) (`npx skills`). It copies each skill into the directories your agent already reads (Cursor, Claude Code, Codex, …).

Requires **Node.js** and network access to GitHub.

Repo shorthand used below: `Kamil-Matusz/skills`.

## List skills in this repo

```bash
npx skills add Kamil-Matusz/skills --list
```

## Install one skill

Project scope (default — lands in the current repo, e.g. `.agents/skills/` / `.claude/skills/`):

```bash
npx skills add Kamil-Matusz/skills --skill <skill-name>
```

Global scope (available in every project):

```bash
npx skills add Kamil-Matusz/skills --skill <skill-name> -g
```

Skip prompts (CI / scripts):

```bash
npx skills add Kamil-Matusz/skills --skill <skill-name> -g -y
```

### Per-skill commands

| Skill | Command |
|-------|---------|
| `gateway-mapping-check` | `npx skills add Kamil-Matusz/skills --skill gateway-mapping-check` |
| `given-when-then-tests` | `npx skills add Kamil-Matusz/skills --skill given-when-then-tests` |
| `no-em-dash` | `npx skills add Kamil-Matusz/skills --skill no-em-dash` |
| `prefer-final-variables` | `npx skills add Kamil-Matusz/skills --skill prefer-final-variables` |
| `skills-index` | `npx skills add Kamil-Matusz/skills --skill skills-index` |

Global variants — add `-g` (and optionally `-y`):

```bash
npx skills add Kamil-Matusz/skills --skill prefer-final-variables -g -y
npx skills add Kamil-Matusz/skills --skill given-when-then-tests -g -y
npx skills add Kamil-Matusz/skills --skill no-em-dash -g -y
npx skills add Kamil-Matusz/skills --skill gateway-mapping-check -g -y
npx skills add Kamil-Matusz/skills --skill skills-index -g -y
```

### Direct path to one skill

Same result, pinned to a tree path:

```bash
npx skills add https://github.com/Kamil-Matusz/skills/tree/main/skills/prefer-final-variables
npx skills add https://github.com/Kamil-Matusz/skills/tree/main/skills/given-when-then-tests
npx skills add https://github.com/Kamil-Matusz/skills/tree/main/skills/no-em-dash
npx skills add https://github.com/Kamil-Matusz/skills/tree/main/skills/gateway-mapping-check
npx skills add https://github.com/Kamil-Matusz/skills/tree/main/skills/skills-index
```

## Install several or all skills

```bash
# Two skills
npx skills add Kamil-Matusz/skills --skill prefer-final-variables --skill given-when-then-tests

# Everything in the repo
npx skills add Kamil-Matusz/skills --skill '*'
```

## Target a specific agent

By default the CLI may prompt which agents to install into. Pin them with `-a` / `--agent`:

```bash
# Cursor only (global)
npx skills add Kamil-Matusz/skills --skill prefer-final-variables -g -a cursor -y

# Claude Code only (global)
npx skills add Kamil-Matusz/skills --skill prefer-final-variables -g -a claude-code -y

# Both
npx skills add Kamil-Matusz/skills --skill prefer-final-variables -g -a cursor -a claude-code -y
```

Useful agent ids: `cursor`, `claude-code`, `codex`, `opencode`, `github-copilot`. Full list: `npx skills --help` or the [skills README](https://github.com/vercel-labs/skills).

## After install

- **Cursor** — skills under `.agents/skills/` (project) or `~/.cursor/skills/` (global); restart Agent chat or start a new one if needed.
- **Claude Code** — skills under `.claude/skills/` or `~/.claude/skills/`; run `/reload` or restart, then confirm with `/skills`.

For `gateway-mapping-check`, ensure the helper script is executable on Unix:

```bash
chmod +x ~/.claude/skills/gateway-mapping-check/scripts/check_mappings.py
# or, for Cursor global:
chmod +x ~/.cursor/skills/gateway-mapping-check/scripts/check_mappings.py
```

Per-project config for that skill: see [skills/gateway-mapping-check/README.md](skills/gateway-mapping-check/README.md).

## Manual install (no `npx`)

Copy from a clone instead — see the [README](README.md#install).