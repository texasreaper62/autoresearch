# Major Decisions

> Record architectural or workflow choices that would be costly to re-debate.
> Use this template for each entry:

## YYYY-MM-DD: Decision title
**Decision:** _what was chosen_
**Rationale:** _why, in one or two sentences_
**Alternatives considered:** _what else was on the table and why rejected_
**Status:** active | revisited | superseded

## 2026-01-01: Four-layer memory separation
**Decision:** Split memory into working / episodic / semantic / personal rather than one flat folder.
**Rationale:** Each layer has different retention and retrieval needs. Flat memory breaks at ~6 weeks.
**Alternatives considered:** Flat directory (fails at scale), vector store (over-engineered for single user).
**Status:** active
## 2026-04-16: Adopted agentic-stack .agent/ brain
**Decision:** Rolled out the portable `.agent/` brain (memory + skills + protocols + hooks + tools) from upstream agentic-stack, with repo-specific skills layered on top.
**Rationale:** Moves monolithic `program.md` knowledge into discrete progressive-disclosure skills, adds subagent-per-iteration context-rot defense, and makes the same brain portable across Claude Code, Cursor, Windsurf, OpenAI/Claude SDKs.
**Alternatives considered:** Keeping `program.md` monolithic (simple but re-reads full directive every session and can't enforce permissions); a homegrown mini-framework (more work, no portability).
**Status:** active

## 2026-04-16: Subagent-per-iteration as context-rot defense
**Decision:** Every hill-climb iteration runs in a fresh-context subagent. The parent only ingests the compact return value (TSV row + 1-line summary).
**Rationale:** Overnight 100-experiment runs hit ~300–400k tokens of context rot by iteration ~30 without this. With it, the parent stays lean indefinitely.
**Alternatives considered:** Aggressive `/compact` only (lossy, unreliable at low-intelligence compact point); subagents only for triage (doesn't help the main run's context).
**Status:** active
