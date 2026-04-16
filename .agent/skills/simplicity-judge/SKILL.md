---
name: simplicity-judge
version: 2026-04-16
triggers: ["keep or discard", "evaluate change", "is this worth keeping"]
tools: []
preconditions: []
constraints: []
category: research
---

# Simplicity judge

All else equal, simpler wins.

## Keep rules
- `val_bpb` improved AND code is not materially uglier → **keep**.
- `val_bpb` unchanged AND code is simpler → **keep**.
- `val_bpb` unchanged AND code is equal → **discard** (no reason to churn history).

## Discard rules
- `val_bpb` worse → **discard**.
- `val_bpb` tiny improvement (<0.002) that adds ≥20 lines of hacky code → **discard**.
- VRAM blows up dramatically → **discard** even if `val_bpb` wins a little.

## Gray zone heuristic
If you're spending more than ~30 seconds on the keep/discard decision,
record the ambiguity in `memory/episodic/AGENT_LEARNINGS.jsonl` and discard.
The loop will produce more data; don't overthink one run.
