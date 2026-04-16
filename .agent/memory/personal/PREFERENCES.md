# Personal Preferences — autoresearch

## Workflow
- Hill-climb on `val_bpb` (lower is better).
- Every experiment gets its own commit; keep it only if `val_bpb` improved.
- Log every run to `results.tsv` (tab-separated, 5 columns). Never git-commit `results.tsv`.
- Branch per run: `autoresearch/<tag>`.
- When the experiment loop has begun, never stop to ask the human — run until interrupted.

## Constraints
- Single NVIDIA GPU target. Fixed 5-minute training budget (wall clock).
- `prepare.py` is read-only. Evaluation harness is ground truth — never touch it.
- No new dependencies. Only what's already in `pyproject.toml`.
- VRAM is a soft constraint — modest increase OK for real gains, no blow-ups.

## Simplicity criterion
Equal `val_bpb` with simpler code is a WIN. A 0.001 win that adds 20 lines of
hacky code is a LOSS. Deletions that don't regress are always keep.

## Communication
- Be direct. Skip pleasantries.
- Surface tradeoffs explicitly. Don't hide them.
