# Agent Infrastructure

This folder is the portable brain. Any harness (Claude Code, Cursor, Windsurf,
OpenCode, OpenClient, Hermes, standalone Python) can mount it and get the
same memory, skills, and protocols.

## Memory (read in this order)
- `memory/personal/PREFERENCES.md` — stable user conventions
- `memory/working/WORKSPACE.md` — current task state
- `memory/semantic/LESSONS.md` — distilled patterns, read before decisions
- `memory/semantic/DECISIONS.md` — past architectural choices
- `memory/episodic/AGENT_LEARNINGS.jsonl` — raw experience log (top-k by salience)

## Skills
- `skills/_index.md` — read first for discovery
- `skills/_manifest.jsonl` — machine-readable skill metadata
- Load a full `SKILL.md` only when its triggers match the current task
- Every skill has a self-rewrite hook; invoke it after failures

## Protocols
- `protocols/permissions.md` — read before any tool call
- `protocols/tool_schemas/` — typed interfaces for external tools
- `protocols/delegation.md` — rules for sub-agent handoff

## Rules
1. Check memory before decisions you have been corrected on before.
2. Log every significant action to `memory/episodic/AGENT_LEARNINGS.jsonl`.
3. Update `memory/working/WORKSPACE.md` as you work; archive on completion.
4. Follow `protocols/permissions.md` strictly. Blocked means blocked.
5. When a self-rewrite hook fires, propose conservative edits only.
6. The harness is dumb on purpose. Reasoning lives in skills and memory.
