# autoresearch

Autonomous LLM research. Hill-climb `val_bpb` by editing `train.py`.

## Brain

This repo uses the portable `.agent/` brain. Read in this order before you act:

1. `.agent/AGENTS.md` — the map.
2. `.agent/memory/personal/PREFERENCES.md` — user's stable conventions.
3. `.agent/memory/semantic/LESSONS.md` — distilled patterns from prior runs.
4. `.agent/skills/_index.md` — discover skills. Load full `SKILL.md` only when triggers match.
5. `.agent/protocols/permissions.md` — check before any tool call.

## Getting started

When the human says *"kick off a new experiment"*:

1. Load `skills/branch-hygiene/SKILL.md` and follow setup.
2. Confirm with the human.
3. Enter `skills/experiment-loop/SKILL.md`.
4. Every iteration MUST run inside a fresh-context subagent — see `skills/subagent-dispatcher/SKILL.md`.
5. Never stop until the human interrupts.

## Scope

- **Edit:** `train.py` only.
- **Read-only:** `prepare.py`, the entire evaluation harness.
- **Metric:** `val_bpb` (lower is better). Fixed 5-minute training budget.
- **Ledger:** `results.tsv`, tab-separated, untracked by git.

Everything else — the loop structure, logging format, keep/discard rules,
subagent contract, simplicity tie-breaker — lives in the skills.
