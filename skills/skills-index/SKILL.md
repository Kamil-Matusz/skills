---
name: skills-index
description: >-
  Keep a SKILLS.md catalog in sync with the skills that are actually installed —
  append a one-line description row when a skill is added, update it when a skill
  is renamed or its purpose changes, and drop the row when a skill is removed.
  Use whenever a skill is installed, copied into `~/.claude/skills/`,
  `~/.agents/skills/` or a project's `.claude/skills/`, created from scratch, or
  deleted. Also use when the user mentions "SKILLS.md", "skill index", "skill
  catalog", "lista skilli", "spis skilli", or asks what skills are installed.
  Run it right after installing a skill even when the user does not ask.
allowed-tools: Read, Write, Edit, Glob, Bash
---

# SKILLS.md index

`SKILLS.md` is a one-line-per-skill catalog of what is installed. It is the only
place a person can see the whole set at a glance, so it goes stale the moment a
skill is installed and nobody updates it. Update it in the same turn as the
install — never leave it for later.

## Locating the file

The index lives next to the skills directory it describes, so its relative links
resolve:

| Skills directory | Index file |
|------------------|------------|
| `~/.agents/skills/` | `~/SKILLS.md` |
| `~/.claude/skills/` | `~/SKILLS.md` |
| `<repo>/.claude/skills/` | `<repo>/SKILLS.md` |
| `<repo>/skills/` | `<repo>/SKILLS.md` |

If more than one index exists, update every one whose skills directory received
the skill. If none exists, create it with the header below.

## File shape

```markdown
# Skills

Short descriptions of skills in `.agents/skills/`.

| Skill | Description |
|-------|-------------|
| [efcore-patterns](.agents/skills/efcore-patterns/) | Entity Framework Core best practices: NoTracking by default, query splitting, migrations, and common pitfalls. |
```

- Rows sorted alphabetically by skill name.
- Link target is the skill's directory, relative to `SKILLS.md`, with a trailing
  slash — same prefix as the intro sentence.
- One row per skill. Never two rows for the same name.

## Writing the description

Read the new skill's `SKILL.md` frontmatter and condense its `description` into a
**single sentence, ~100–160 characters**, ending with a period.

- Say what the skill does, not when it fires. Drop "Use whenever…", the trigger
  keyword lists, and "Apply proactively…" — those exist for the model, not for a
  human scanning a table.
- Lead with the subject: `Entity Framework Core best practices: …`, not
  `This skill provides …`.
- Keep a colon-then-list shape when the skill covers several points; it packs the
  most into one line.
- Escape any literal `|` as `\|` so the table does not break.

## Adding, updating, removing

1. Read the existing `SKILLS.md` first — do not overwrite a file you have not read.
2. **Added skill** — insert the row at its alphabetical position with `Edit`,
   anchored on the neighbouring row. Do not rewrite the whole table.
3. **Existing name** — replace that row in place instead of appending a second one.
4. **Renamed** — replace name, link and description in the one row, then re-sort.
5. **Removed skill** — delete its row.
6. Never reorder or reword rows for skills you did not touch.

## Verifying against reality

When the user asks to refresh the whole index, or the table looks out of date,
list what is actually installed and reconcile:

```bash
ls -1 ~/.agents/skills/
```

Every directory containing a `SKILL.md` gets a row; every row needs a matching
directory. Report additions and deletions to the user rather than silently
pruning rows whose directory you could not find.

## Self-check before finishing

1. The installed skill has exactly one row, in alphabetical position.
2. The link points at an existing directory and ends with `/`.
3. The description is one sentence, no trigger keywords, no unescaped `|`.
4. No unrelated row changed.
