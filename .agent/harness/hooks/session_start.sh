#!/usr/bin/env bash
# SessionStart hook. Emits a brief brain-status banner on Claude Code session open.
# Output goes to the session transcript so the agent can read it.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

# Skill count
if [[ -f "$ROOT/skills/_manifest.jsonl" ]]; then
  skills=$(grep -c '^{' "$ROOT/skills/_manifest.jsonl" || echo 0)
else
  skills=0
fi

# Episodic entries
episodic="$ROOT/memory/episodic/AGENT_LEARNINGS.jsonl"
if [[ -f "$episodic" ]]; then
  episodes=$(wc -l < "$episodic" | tr -d ' ')
else
  episodes=0
fi

# Template version (if pinned)
version_file="$ROOT/.template-version"
if [[ -f "$version_file" ]]; then
  version=$(cut -c1-7 "$version_file")
else
  version="unpinned"
fi

cat <<EOF
.agent brain loaded
  skills:     $skills
  episodic:   $episodes entries
  template:   $version

Read .agent/AGENTS.md before acting. Load skills on demand via
.agent/skills/_index.md. Check .agent/protocols/permissions.md
before any write or shell call.
EOF
