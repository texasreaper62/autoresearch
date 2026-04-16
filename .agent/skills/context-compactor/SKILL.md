---
name: context-compactor
version: 2026-04-16
triggers: ["compact", "context window full", "session getting long", "/compact"]
tools: []
preconditions: []
constraints: ["never compact mid-task without a handoff summary", "steer /compact with a focus instruction"]
category: meta
---

# Context compactor

The model is at its least intelligent point when compacting — context rot
has set in. Don't wait for autocompact to fire blindly.

## When to proactively compact
- At ~60% of the context window (well before autocompact).
- After a bloaty investigation you don't need the tools output for.
- Right before a new phase of work where the previous phase's details
  won't help.

## How to steer
Always pass a focus instruction:
- `/compact focus on the auth refactor, drop the test debugging`
- `/compact keep files X, Y, Z read; summarize everything else`

Unsteered `/compact` is often a bad compact, because the model has to
guess what you'll need next and it's at its dumbest when deciding.

## When to prefer /clear over /compact
- You can write down the brief yourself ("we're refactoring X, constraint Y, files A and B, we've ruled out approach Z").
- The task is shifting enough that carrying context is net-negative.
- `/compact` has produced garbage in the past for this kind of work.

## Anti-pattern
Letting autocompact fire after a long debugging session, then pivoting to
a different task. The summary will be about debugging; the new task
details won't be in it. Compact proactively with a forward-looking focus.

## Self-rewrite hook
If ≥3 bad compacts are recorded in episodic memory, update this skill
with the specific failure signatures.
