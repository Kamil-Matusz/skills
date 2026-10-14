---
name: context-budget
description: Measures how many tokens a project puts into the agent's context at startup (AGENTS.md, CLAUDE.md with its @ imports, skill descriptions) and how much loads only on demand, then points out what to trim or move. Use when the user asks about context cost, cleans up or reorganizes AGENTS.md or CLAUDE.md, adds new skills, or notices the agent "forgetting" rules during long sessions.
metadata:
  author: "Kamil Matusz"
  version: "1.0"
---

# Context budget

Context is a budget, not a warehouse. Everything that is always loaded competes with the
actual task for the model's attention.

| Layer | What it contains | When it enters context |
|-------|------------------|------------------------|
| always-on | AGENTS.md, CLAUDE.md, files pulled in by `@` imports, name and description of every skill | at the start of every session |
| on demand | SKILL.md body, nested AGENTS.md files in subdirectories | when the agent decides it needs them |
| on use | a skill's scripts, references, templates | only when a skill step points to them |

## Steps
1. Measure the always-on layer (estimate: bytes / 4 = tokens; code, tables and
   non-English text usually come out higher):
   ```bash
   wc -c AGENTS.md CLAUDE.md GEMINI.md 2>/dev/null | awk '{printf "%7d tok  %s\n", $1/4, $2}'
   grep -ohE '(^|\s)@[~./][^ ]+' CLAUDE.md 2>/dev/null   # @ imports, measure these too
   ```
2. Measure skill descriptions (always-on) and skill bodies (on demand). The awk part
   also catches multi-line YAML descriptions:
   ```bash
   for f in .claude/skills/*/SKILL.md .agents/skills/*/SKILL.md; do
     [ -f "$f" ] || continue
     desc=$(awk '/^---$/{n++; next} n==1 && /^description:/{d=1; print; next}
                 n==1 && d && /^[A-Za-z_-]+:/{d=0} n==1 && d' "$f" | wc -c)
     full=$(wc -c < "$f")
     printf "%-45s desc ~%4d tok  body ~%5d tok\n" "$f" $((desc/4)) $((full/4))
   done
   ```
3. Check every always-on file against "Trimming rules" and every skill against
   "Skill checks".
4. Show the user the layer table and the proposals. Do not edit any files without
   their approval.

## Trimming rules
- A rule that can be enforced by configuration (deny list, hook, linter, test) does not
  need a paragraph in AGENTS.md. Keep one sentence and a pointer to the mechanism.
- Knowledge needed only occasionally goes into a skill or `docs/`, with one sentence in
  AGENTS.md saying when to open it.
- Remove anything the agent can read from the repository on its own: file listings,
  descriptions of obvious structure, copies of the README.
- Platitudes ("write clean code", "be thorough", "follow best practices") do not change
  behavior. Replace them with a checkable criterion or delete them.
- Contradictory rules (in AGENTS.md and in an import): remove one; otherwise the model
  picks at random.
- A secret in an always-on file leaks into every log and to every model provider:
  `grep -nEi '(api[_-]?key|token|secret|password)\s*[:=]|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}' AGENTS.md CLAUDE.md`

## Skill checks
- `name`: lowercase letters, digits and hyphens, up to 64 characters, identical to the
  directory name.
- `description`: up to 1,024 characters, says WHAT the skill does and WHEN to use it
  (the words "Use when").
- No "always" or "for every task" in the description: such a skill hijacks invocations
  meant for other skills.
- SKILL.md body up to 500 lines; move anything longer to `references/`.

## Rough thresholds
- Always-on layer in total: up to about 2,000 tokens.
- One skill description: 1-3 sentences.

## Done when
- the user has the layer table with token estimates,
- every proposal says what, where, and how many tokens it saves,
- it is clear which proposals require a configuration change rather than a text edit.
