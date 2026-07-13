# gateway-mapping-check (Claude Code skill)

Portable skill for verifying that Spring controller endpoints have matching
`apiGateway.mappings` entries in a Helm `values.yaml`.

## Install once (user-level, all projects)

```bash
mkdir -p ~/.claude/skills
cp -r gateway-mapping-check ~/.claude/skills/
chmod +x ~/.claude/skills/gateway-mapping-check/scripts/check_mappings.py
```

Restart Claude Code (or `/reload`) and confirm with `/skills` — you should see
`gateway-mapping-check` listed.

Alternative: install per-project by copying into `<repo>/.claude/skills/` instead.
User-level wins for portability; project-level wins if you want the skill pinned
to that repo and shared via git.

## Configure per project

Drop a `.gateway-mapping-check.yaml` at the repo root:

```yaml
values_yaml: chart/checkout/values.yaml
application_yml: src/main/resources/application.yml
controllers_glob: src/main/java/**/*Controller.java
```

Any key can be omitted; defaults match the layout above. If your project follows
these defaults, no config file is needed.

## Run manually

```bash
python3 ~/.claude/skills/gateway-mapping-check/scripts/check_mappings.py         # changed endpoints only
python3 ~/.claude/skills/gateway-mapping-check/scripts/check_mappings.py --all   # full audit
```

Or just tell Claude "sprawdź mapowanie gateway dla nowego endpointu" — the skill
description contains triggers so Claude picks it up automatically.

## Optional: pre-push hook

`.githooks/pre-push`:

```bash
#!/usr/bin/env bash
python3 "$HOME/.claude/skills/gateway-mapping-check/scripts/check_mappings.py" || exit 1
```

Then `git config core.hooksPath .githooks` in the project.
