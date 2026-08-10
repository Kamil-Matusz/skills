# skills-index (Claude Code skill)

Keeps a `SKILLS.md` catalog in sync with the skills that are actually installed:
one row per skill, alphabetical, with a one-sentence description distilled from
the skill's own `SKILL.md` frontmatter.

Fires on install, creation, rename and removal of a skill — so the catalog is
updated in the same turn, not "later".

## Install once (user-level, all projects)

```bash
mkdir -p ~/.claude/skills && cp -r skills/skills-index ~/.claude/skills/
```

Restart Claude Code (or `/reload`) and confirm with `/skills`.

## Where SKILLS.md lives

Next to the skills directory it describes, so relative links resolve:
`~/.agents/skills/` → `~/SKILLS.md`, `<repo>/.claude/skills/` →
`<repo>/SKILLS.md`. The skill creates the file with a header if it is missing.

## How it triggers

No script — the description carries the triggers, so Claude updates the index
right after installing a skill. Explicit invocation: `/skills-index`.

## Scope guard

Only the row for the skill being added, renamed or removed is touched. Rows for
other skills are never reordered or reworded. A full refresh (reconciling the
table against `ls ~/.agents/skills/`) happens only when asked.
