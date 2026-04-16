# Skill Registry — autoresearch

Read this file first. Full `SKILL.md` contents load only when a skill's
triggers match the current task. Machine-readable equivalent:
`skills/_manifest.jsonl`.

## Research loop (this repo)

### experiment-loop
The core hill-climb. Runs forever.
Triggers: "run experiment", "kick off experiment", "train.py", "autoresearch loop"

### results-logging
Schema + rules for `results.tsv`.
Triggers: "log result", "record experiment", "update results.tsv"

### branch-hygiene
Fresh-run setup; `autoresearch/<tag>` branch conventions.
Triggers: "new experiment run", "setup experiment", "new branch"

### simplicity-judge
Keep/discard rules including the "simpler wins" tie-breaker.
Triggers: "keep or discard", "evaluate change", "is this worth keeping"

### subagent-dispatcher
Spawn a fresh-context subagent per iteration. Single biggest context-rot defense.
Triggers: "spawn subagent", "delegate iteration", "run experiment in subagent"

## Universal (inherited from template)

### skillforge
Creates new skills from observed patterns.
Triggers: "create skill", "new skill", "I keep doing this manually"

### memory-manager
Reflection cycles. Reads episodic, promotes to semantic.
Triggers: "reflect", "what did I learn", "compress memory"

### git-proxy
All git ops with safety constraints.
Triggers: "commit", "push", "branch", "merge", "rebase"

### debug-investigator
Reproduce → isolate → hypothesize → verify.
Triggers: "debug", "why is this failing", "investigate", "stack trace"

### deploy-checklist
Unused in autoresearch (no deployment). Kept for portability.
