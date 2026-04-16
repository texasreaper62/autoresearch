---
name: results-logging
version: 2026-04-16
triggers: ["log result", "record experiment", "update results.tsv"]
tools: [bash]
preconditions: ["results.tsv exists with header"]
constraints: ["tab-separated, never comma", "never git-add results.tsv", "5 columns, in order"]
category: research
---

# Results logging

## Schema
```
commit	val_bpb	memory_gb	status	description
```

- `commit`: short (7-char) git hash.
- `val_bpb`: 6 decimals. Use `0.000000` for crashes.
- `memory_gb`: `peak_vram_mb / 1024`, rounded to .1f. Use `0.0` for crashes.
- `status`: `keep`, `discard`, or `crash`.
- `description`: short. No commas (commas break downstream). No tabs.

## Example rows
```
a1b2c3d	0.997900	44.0	keep	baseline
b2c3d4e	0.993200	44.2	keep	lr 0.02 -> 0.04
c3d4e5f	1.005000	44.0	discard	swap to GeLU
d4e5f6g	0.000000	0.0	crash	2x width OOM
```

## Rules
- `results.tsv` is **untracked** by git. It is a ledger, not source.
- Same commit may appear multiple times if rerun for variance.
- Append-only. Never rewrite past rows.

## Promotion path
The memory-manager skill reads `results.tsv` during dream cycles and
promotes recurring patterns (e.g. "depth>10 always OOMs on this GPU")
into `memory/semantic/LESSONS.md`.
