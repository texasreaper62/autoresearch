# AGENTS — autoresearch

Pointer file for harnesses that look for `AGENTS.md` at the root (OpenCode,
OpenAI Agents SDK, etc.).

The actual agent brain lives at `.agent/`. Start there:

1. `.agent/AGENTS.md` — map of the brain.
2. `.agent/skills/_index.md` — skill registry.
3. `.agent/memory/semantic/LESSONS.md` — distilled patterns.
4. `.agent/protocols/permissions.md` — enforced before tool calls.

Repo-level directive: see `program.md`.
