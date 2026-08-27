# skills

Portable agent skills — conventions and checks you can install once and reuse across projects.

Each skill is a directory with a `SKILL.md` (what the agent should do and when) and usually a short `README.md` (how to install and use it as a human).

## Skills

| Skill | Description |
|-------|-------------|
| [gateway-mapping-check](skills/gateway-mapping-check/) | Verify Spring controller endpoints have matching `apiGateway.mappings` in Helm `values.yaml`. |
| [given-when-then-tests](skills/given-when-then-tests/) | Structure Java tests with `//given` / `//when` / `//then` section comments. |
| [no-em-dash](skills/no-em-dash/) | Replace em dashes (—) and en dashes (–) with regular hyphens (-) in all written output. |
| [prefer-final-variables](skills/prefer-final-variables/) | Mark Java variables `final` where it compiles and is meaningful; skip Hibernate/Jackson/Spring proxy pitfalls. |
| [skills-index](skills/skills-index/) | Keep a `SKILLS.md` catalog in sync when skills are added, renamed, or removed. |

## Install

**Via `npx` (recommended)** — install one skill, several, or all, for Cursor / Claude Code / other agents. Full commands: **[INSTALL.md](INSTALL.md)**.

```bash
npx skills add Kamil-Matusz/skills --list
npx skills add Kamil-Matusz/skills --skill prefer-final-variables -g -y
```

**Manual copy** — user-level (available in every project):

```bash
mkdir -p ~/.claude/skills
cp -r skills/<skill-name> ~/.claude/skills/
```

Example — install all of them:

```bash
mkdir -p ~/.claude/skills
cp -r skills/* ~/.claude/skills/
```

Restart Claude Code (or `/reload`) and confirm with `/skills`.

**Per-project** (pinned in git with that repo):

```bash
mkdir -p <repo>/.claude/skills
cp -r skills/<skill-name> <repo>/.claude/skills/
```

For `gateway-mapping-check`, also make the script executable:

```bash
chmod +x ~/.claude/skills/gateway-mapping-check/scripts/check_mappings.py
```

Cursor / other agent layouts that use `~/.agents/skills/` work the same way — copy into that directory instead.

## How skills trigger

Most skills have no config and no script. Their `description` frontmatter lists triggers, so the agent picks them up when you write tests, touch Java, add an endpoint, or install another skill.

You can also invoke a skill explicitly, e.g. `/prefer-final-variables` or `/gateway-mapping-check`.

## Adding a skill

1. Create `skills/<name>/SKILL.md` with YAML frontmatter (`name`, `description`) and the instructions body.
2. Add a short `README.md` for install notes if useful.
3. After install elsewhere, run `skills-index` (or let it fire) so `SKILLS.md` stays accurate.

## License

Use and adapt freely in your own projects unless a skill directory says otherwise.