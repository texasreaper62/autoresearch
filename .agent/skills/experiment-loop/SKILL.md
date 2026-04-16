---
name: experiment-loop
version: 2026-04-16
triggers: ["run experiment", "kick off experiment", "train.py", "autoresearch loop", "start hill climb"]
tools: [bash, git]
preconditions: ["on branch autoresearch/<tag>", "results.tsv header row exists"]
constraints: ["never modify prepare.py", "never add dependencies", "never stop the loop unless interrupted"]
category: research
---

# Experiment loop

The core loop. Runs forever until the human interrupts.

## Each iteration (spawn a fresh-context subagent per iteration; see skills/subagent-dispatcher)

1. Check current branch/commit.
2. Edit `train.py` with one experimental idea. Only `train.py`.
3. `git commit -am "<short idea>"`
4. `uv run train.py > run.log 2>&1` (redirect everything; do NOT tee).
5. `grep "^val_bpb:\|^peak_vram_mb:" run.log`
   - Empty → crashed. `tail -n 50 run.log` for traceback. Fix if trivial, else discard.
6. Append a row to `results.tsv` (see skills/results-logging).
7. Decision:
   - Improved → advance the branch (keep commit).
   - Equal or worse → `git reset --hard HEAD~1`.
8. Repeat.

## Timeouts & crashes
- If a run exceeds 10 minutes wall-clock, kill it, mark `crash`, move on.
- Trivial crashes (typos, imports) → fix and re-run.
- Fundamental crashes (architecture broken) → log `crash`, move on.

## Never-stop rule
The human may be asleep. Do not ask "should I continue?" Do not pause at
"good stopping points". If you run out of ideas: re-read the in-scope files,
cross-reference `memory/semantic/LESSONS.md`, combine near-misses, or try
more radical architectural changes. The loop ends when the human interrupts.

## Self-rewrite hook
If the same failure mode appears ≥3 times in `memory/episodic/`, invoke
skillforge to lift it into `skills/known-pitfalls/` so the next iteration
avoids it without rediscovery.
