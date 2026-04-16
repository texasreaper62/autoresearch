---
name: subagent-dispatcher
version: 2026-04-16
triggers: ["spawn subagent", "delegate iteration", "run experiment in subagent", "fresh context"]
tools: []
preconditions: []
constraints: ["parent only ingests the final TSV row + keep/discard decision", "subagents inherit permissions"]
category: meta
---

# Subagent-per-iteration

The biggest context-rot defense in overnight runs. Without this, ~30
experiments of stack traces and run.log excerpts poison the parent.

## When to spawn
- **Every experiment iteration in the autoresearch loop.**
- Any task that will produce >20k tokens of intermediate output the parent
  doesn't need again.

## Contract
The parent passes the subagent:
1. **Goal**: "Run one iteration of experiment-loop: idea = <X>".
2. **Inputs**: current branch/commit, contents of `train.py`, prior best
   `val_bpb` from `results.tsv`.
3. **Return format**: the single TSV row + a 1-line summary of what was
   tried + keep/discard recommendation. Nothing else.
4. **Budget**: 15 minutes wall-clock, 30 tool calls.

The subagent handles:
- Editing `train.py`
- Running `uv run train.py > run.log 2>&1`
- Grepping metrics, or reading stack traces on crash
- Appending the TSV row

The parent ingests ONLY the return value. It never sees `run.log`.

## Anti-pattern
Do not spawn a subagent for "decide what to try next" — that's cheap,
low-output, and benefits from parent context. Delegate the expensive,
bloaty work, not the thinking.

## Reference
See `protocols/delegation.md` for the generic handoff envelope.
