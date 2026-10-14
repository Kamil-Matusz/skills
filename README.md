# skills

Portable agent skills: conventions and checks you install once and reuse across projects. They work with Claude Code, Cursor, Codex and any other agent that reads the `SKILL.md` format.

Each skill is a directory with a `SKILL.md`: YAML frontmatter (`name`, `description`) that tells the agent when to use it, followed by the instructions themselves.

## Skills

### Java / Spring

| Skill | Description |
|-------|-------------|
| [gateway-mapping-check](skills/gateway-mapping-check/) | Verify Spring controller endpoints have matching `apiGateway.mappings` in Helm `values.yaml`. |
| [given-when-then-tests](skills/given-when-then-tests/) | Structure Java tests with `//given` / `//when` / `//then` section comments. |
| [prefer-final-variables](skills/prefer-final-variables/) | Mark Java variables `final` where it compiles and is meaningful; skip Hibernate/Jackson/Spring proxy pitfalls. |

### Security

| Skill | Description |
|-------|-------------|
| [dependency-check](skills/dependency-check/) | Confirm a PyPI or npm package exists, check its age, release history and install scripts before adding it. Guards against slopsquatting and typosquatting. |
| [skill-audit](skills/skill-audit/) | Audit a third-party skill, plugin or MCP server before installing it: hidden instructions, network calls, secret reads, obfuscation, persistence. |

### Agent context

| Skill | Description |
|-------|-------------|
| [context-budget](skills/context-budget/) | Measure how many tokens `AGENTS.md`, `CLAUDE.md` and skill descriptions load at startup and suggest what to trim or move. |
| [no-em-dash](skills/no-em-dash/) | Replace em dashes and en dashes with regular hyphens (`-`) in all written output. |

## Install

### Via `npx` (recommended)

Install one skill, several, or all of them for Claude Code, Cursor or other agents. Full command reference: **[INSTALL.md](INSTALL.md)**.

```bash
npx skills add Kamil-Matusz/skills --list
npx skills add Kamil-Matusz/skills --skill prefer-final-variables -g -y
```

### Manual copy

User-level (available in every project):

```bash
mkdir -p ~/.claude/skills
cp -r skills/<skill-name> ~/.claude/skills/   # one skill
cp -r skills/* ~/.claude/skills/              # all of them
```

Per-project (versioned together with that repo):

```bash
mkdir -p <repo>/.claude/skills
cp -r skills/<skill-name> <repo>/.claude/skills/
```

For Cursor and other agents that use `~/.agents/skills/`, copy into that directory instead.

Restart Claude Code (or run `/reload`) and confirm with `/skills`.

`gateway-mapping-check` ships a script that must be executable, and has its own setup notes in [its README](skills/gateway-mapping-check/README.md):

```bash
chmod +x ~/.claude/skills/gateway-mapping-check/scripts/check_mappings.py
```

## How skills trigger

Most skills need no config and no script. The `description` in the frontmatter lists the situations they apply to, so the agent picks them up on its own: when you write a test, edit Java code, add an endpoint, install a package or pull in a skill from the internet.

You can also invoke a skill explicitly, e.g. `/prefer-final-variables` or `/skill-audit`.

## Adding a skill

1. Create `skills/<name>/SKILL.md` with YAML frontmatter (`name`, `description`, optional `metadata`) and the instructions body.
2. Write the `description` around triggers: what the skill does and exactly when to use it.
3. Put helper scripts in `skills/<name>/scripts/` and add a `README.md` only if the skill needs setup beyond copying.
4. Add a row to the table above.

## License

[MIT](LICENSE)
