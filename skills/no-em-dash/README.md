# no-em-dash (Claude Code skill)

Replaces em dashes (—) and en dashes (–) with regular hyphens (-) in all
generated text: prose, comments, commit messages, markdown, and PR descriptions.

Applies to every written output, not only when you ask about punctuation.

## Install once (user-level, all projects)

```bash
mkdir -p ~/.claude/skills && cp -r skills/no-em-dash ~/.claude/skills/
```

Restart Claude Code (or `/reload`) and confirm with `/skills`.

Alternative: install per-project by copying into `<repo>/.claude/skills/` so the
convention travels with the repo in git.

Via `npx` (see [INSTALL.md](../../INSTALL.md)):

```bash
npx skills add Kamil-Matusz/skills --skill no-em-dash -g -y
```

## How it triggers

No script, no configuration. The description carries the triggers, so the agent
applies it automatically whenever it writes text. Explicit invocation:
`/no-em-dash`.

## What it changes

- Sentence breaks: an em dash becomes a spaced hyphen (` - `), a comma, a colon,
  or two sentences, whichever reads best.
- Ranges: an en dash becomes a hyphen (`10-20`, `Mon-Fri`, `pages 5-8`).
- Scope: all text the agent writes (prose, comments, docstrings, commits,
  markdown, PR descriptions).

## Examples

- Wrong: "The service was down—users couldn't log in."
- Right: "The service was down - users couldn't log in." or "The service was down, and users couldn't log in."

- Wrong: "See sections 3–5."
- Right: "See sections 3-5."