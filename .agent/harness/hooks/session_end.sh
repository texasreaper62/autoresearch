#!/usr/bin/env bash
# Stop hook. Appends a 1-line session delta to episodic memory.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
EPISODIC="$ROOT/memory/episodic/AGENT_LEARNINGS.jsonl"
mkdir -p "$(dirname "$EPISODIC")"

TS=$(date -Iseconds)
BRANCH=$(git -C "$ROOT/.." rev-parse --abbrev-ref HEAD 2>/dev/null || echo "no-git")
STATUS=$(git -C "$ROOT/.." status --porcelain 2>/dev/null | wc -l | tr -d ' ')

cat >> "$EPISODIC" <<EOF
{"timestamp":"$TS","skill":"session","action":"session-end","result":"success","detail":"branch=$BRANCH dirty=$STATUS","pain_score":2,"importance":4,"reflection":"session ended"}
EOF

exit 0
