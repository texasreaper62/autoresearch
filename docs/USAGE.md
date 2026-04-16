# Using the agent brain

This repo mounts the portable `.agent/` brain at its root. Every harness
reads the same brain; they differ only in how they dispatch skills and
enforce hooks.

## What loads on session start

Whatever harness you use, the session-start reading order is:

1. `.agent/AGENTS.md` — map of the brain.
2. `.agent/memory/personal/PREFERENCES.md` — stable conventions.
3. `.agent/memory/working/WORKSPACE.md` — live task state (if populated).
4. `.agent/memory/semantic/LESSONS.md` — distilled patterns.
5. `.agent/skills/_index.md` — skill registry (load full SKILL.md only when triggers match).
6. `.agent/protocols/permissions.md` — consulted before any tool call.

## Harness-specific wiring

### Claude Code
- `.claude/settings.json` wires PreToolUse + Stop hooks.
- `.claude/agents/*.md` defines dispatchable subagents (e.g. `experiment-runner`).
- The pre-tool-call hook runs `.agent/harness/hooks/pre_tool_call.sh` and
  exits 2 to deny. The session-end hook appends a 1-line delta to episodic
  memory.

### Cursor
- `.cursor/rules/agent-stack.mdc` is `alwaysApply: true`.
- Cursor has no hook layer, so permissions are advisory (read `permissions.md`
  and respect it). For the strongest enforcement, run with Claude Code.

### Windsurf
- `.windsurfrules` loads at session start.
- Same advisory permissions model as Cursor.

### OpenAI Agents SDK / Claude Agent SDK
- Point the SDK's `cwd` at the repo root; the brain is just files.
- The autoagent repo's `agent.py` + `agent-claude.py` demonstrate this.

### Standalone Python
- `python3 .agent/harness/conductor.py "<prompt>"` runs a thin conductor
  that assembles context (personal + working + top-salience episodic +
  matched skills + permissions) and calls the model.

## Everyday commands

```
bin/validate       # local mirror of CI checks; run before pushing
bin/status         # iterations/hour, best metric, cost (autoresearch/autoagent only)
bin/dream          # run nightly memory compression (or cron it)
bin/agent-sync status  # show pinned template version + drift
bin/agent-sync pull    # pull latest template core from upstream
```

## Adding a new skill

1. `mkdir .agent/skills/<name>` and add `SKILL.md` with YAML frontmatter.
2. Append a one-line JSONL entry to `.agent/skills/_manifest.jsonl`.
3. Add a prose entry to `.agent/skills/_index.md`.
4. Run `bin/validate`. Commit.

Better: prompt Claude Code with *"use skillforge to create a skill for X"*
and it will follow the template.

## Promoting a lesson to semantic memory

The dream cycle (`bin/dream`) does this automatically: patterns that recur
≥2 times in episodic memory with salience ≥7 get appended to
`.agent/memory/semantic/LESSONS.md`.

You can manually edit `LESSONS.md` anytime — tighten wording, delete
obsolete entries, reorganize.

## Switching harnesses

The brain travels. To try the same task in a different harness, just open
the repo in that harness. No migration needed. All skills, memory,
protocols, and preferences load the same way.
