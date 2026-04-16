# Claude Code pointer — autoresearch

This repo's agent context lives in `.agent/`. It's the portable brain used
across harnesses (Claude Code, Cursor, Windsurf, OpenAI/Claude SDKs,
standalone Python).

## On session start

1. Read `.agent/AGENTS.md`.
2. Read `.agent/memory/personal/PREFERENCES.md` + `.agent/memory/semantic/LESSONS.md`.
3. Read `.agent/skills/_index.md`. Load individual `SKILL.md` files on demand.
4. Check `.agent/protocols/permissions.md` before any write or shell call.

## Session management (context hygiene)

- Every experiment iteration goes in a **fresh-context subagent**. See
  `.agent/skills/subagent-dispatcher/SKILL.md`.
- Prefer `/rewind` + summarize over "that didn't work, try X" in the same context.
- Proactively `/compact` around 60% of the window with a focus instruction.
- A new task = a new session. Overlap is OK only when re-reading the same files.

## Directive

See `program.md` at the repo root for the top-level task framing.
