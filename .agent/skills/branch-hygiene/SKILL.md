---
name: branch-hygiene
version: 2026-04-16
triggers: ["new experiment run", "setup experiment", "new branch"]
tools: [bash, git]
preconditions: ["clean working tree on master"]
constraints: ["never reuse an existing autoresearch/* branch", "never commit results.tsv"]
category: research
---

# Branch hygiene

## Fresh-run setup
1. Propose a tag based on today's date, e.g. `apr16` or `apr16-gpu0` when
   multiple runs are interleaved.
2. Verify `autoresearch/<tag>` does NOT already exist.
3. `git checkout -b autoresearch/<tag>` from master.
4. Verify `~/.cache/autoresearch/` has data shards + tokenizer. If missing,
   ask the human to run `uv run prepare.py`.
5. Create `results.tsv` with just the header row:
   `commit\tval_bpb\tmemory_gb\tstatus\tdescription`
6. Confirm setup with the human. Once confirmed, enter `experiment-loop`
   and do NOT stop until interrupted.

## Rewind policy
Rewinding (discarding commits on the branch) should be VERY rare. Only when
clearly stuck in a local minimum.
