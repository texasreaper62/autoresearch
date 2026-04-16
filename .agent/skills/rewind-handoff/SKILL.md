---
name: rewind-handoff
version: 2026-04-16
triggers: ["that didn't work", "rewind", "/rewind", "try again", "esc esc"]
tools: []
preconditions: []
constraints: []
category: meta
---

# Rewind-handoff

`/rewind` (or double-tap Esc) jumps back to any previous message and drops
everything after. Often the better move than "that didn't work, try X".

## When to rewind instead of correcting

Classic scenario: Claude reads 5 files, tries approach A, it fails.

- **Don't**: "that didn't work, try B" — now you carry 5 file reads + a
  failed attempt + reasoning about why it failed, all polluting context.
- **Do**: rewind to just after the file reads, then re-prompt with the
  learning: "Don't use approach A, the foo module doesn't expose that —
  go straight to B."

## Summarize-from-here handoff

Before rewinding on a long thread, ask Claude to:

> "Summarize what you learned trying approach A, in a form that a fresh
> Claude could use."

Then rewind and paste the summary into the new prompt. It's a message
from Claude's failed past self to its future self.

## When NOT to rewind
- The failed attempt produced useful artifacts (a test case, a diagram).
- Multiple successful steps preceded the failure; rewinding loses them.
- You're unsure what the "good" prior state was — rewind to a known point
  or start clean with /clear.

## Self-rewrite hook
Track rewind-then-succeed vs rewind-then-fail-again patterns in episodic.
If a rewind pattern has <30% success rate, the problem probably isn't
context — think harder about the approach.
