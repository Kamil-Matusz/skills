---
name: "brain-wiki"
description: "Use whenever Kamil works with his Obsidian vault Brain (second brain / LLM Wiki, \"drugi mózg\"): adding knowledge, notes or ideas, asking questions about his wiki, ingesting new material, or linting the vault. Trigger even if he only mentions his notes, his wiki, Obsidian or something he wants to remember, without naming the vault explicitly."
metadata:
  author: "Kamil Matusz"
  version: "1.0"
---

# Brain - Kamil's LLM Wiki

Kamil keeps a personal knowledge base in the Obsidian vault `D:\Obsidian Vaults\Brain`, following the LLM Wiki pattern (Karpathy). The agent is the librarian: the sole author of the wiki pages.

## Always start with
1. Make sure the `Brain` folder is connected (device_list_dir / device_bash in `$HOME/mnt/Brain`). If it is not, request access (device_request_folder_access).
2. Read `CLAUDE.md` in the vault. It is the authoritative schema and takes precedence over this skill.
3. Read `index.md` and the latest log entries: `grep "^## \[" log.md | tail -10`.
4. Check `_inbox/`; if anything is waiting there, propose an ingest.

## Then
- Identify the operation (INGEST, QUESTION / PYTANIE, NOTE / NOTATKA, LINT, SCHEMA CHANGE / ZMIANA SCHEMATU) and carry it out exactly as described in section 6 of `CLAUDE.md`.
- Work on the files directly on Kamil's computer (device_bash), without moving them to the cloud.
- Every operation ends with an update to `index.md` (if any pages changed) and an entry in `log.md`.
- Never delete files (archive them in `_archiwum/` instead), never edit `_raw/`, and never store passwords or account numbers.
- Reply in Polish, concisely, with `[[page]]` links to the wiki sources; keep knowledge from the wiki clearly separate from general knowledge.
