---
name: no-em-dash
description: Use whenever generating any prose, documentation, comments, commit messages, or other text output. Replaces em dashes (—) and en dashes (–) with regular hyphens (-). Apply proactively to all written output, even when the user does not explicitly ask about punctuation.
---

# No em dashes

Never use em dashes (—) or en dashes (–) in any output.

## Rules

- Instead of an em dash for a break in a sentence, use a regular hyphen with spaces around it ( - ), a comma, a colon, or split into two sentences — whichever reads best.
- Instead of an en dash for ranges, use a regular hyphen: write "10-20", "Mon-Fri", "pages 5-8".
- This applies to ALL text: prose, code comments, docstrings, commit messages, markdown, PR descriptions.

## Examples

- Wrong: "The service was down—users couldn't log in."
- Right: "The service was down - users couldn't log in." or "The service was down, and users couldn't log in."

- Wrong: "See sections 3–5."
- Right: "See sections 3-5."