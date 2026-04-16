---
name: session-boundaries
version: 2026-04-16
triggers: ["new task", "new session", "/clear", "switching tasks"]
tools: []
preconditions: []
constraints: []
category: meta
---

# Session boundaries

Rule of thumb: **a new task = a new session.**

## Why
- Old tool outputs and failed attempts leak attention into unrelated work.
- Context rot starts around 300–400k tokens (highly task-dependent).
- The 1M context window is a capacity, not a target.

## Exceptions (keep the same session)
- Writing docs for the feature you just implemented — re-reading files is
  expensive; the context is still relevant.
- A quick follow-up fix on the same files in the same spirit.
- The immediate next step of a multi-part task you planned together.

## The /clear handoff
When starting clean, write the brief yourself:
- What we're doing (one sentence)
- The constraint that matters (one line)
- The files that matter (explicit paths)
- What we've ruled out (one line, optional)

The /clear version forces you to decide what's relevant. The /compact
version trusts the model to decide, and the model is not at its best
deciding while running out of context.

## Anti-pattern
Treating the session window as the work unit ("I've done a lot, time to
/clear"). Treat the **task** as the work unit. A small task that's done
deserves a fresh session even if you used 10% of the window.
