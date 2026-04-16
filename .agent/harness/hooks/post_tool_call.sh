#!/usr/bin/env bash
# Post-tool-call hook. Appends a structured entry to episodic memory.
# Reads the hook input JSON from stdin; always exits 0 (observability, not enforcement).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
EPISODIC="$ROOT/memory/episodic/AGENT_LEARNINGS.jsonl"
mkdir -p "$(dirname "$EPISODIC")"

INPUT="$(cat)"
TS=$(date -Iseconds)

TOOL_NAME=$(printf '%s' "$INPUT" | sed -n 's/.*"tool_name"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
# Claude Code hook input nests under tool_input; we just log the tool name + size.
INPUT_SIZE=$(printf '%s' "$INPUT" | wc -c | tr -d ' ')

# JSON-safe the fields (simple sanitization — drop quotes + newlines)
TOOL_NAME_SAFE=$(printf '%s' "$TOOL_NAME" | tr -d '"\n\r')

cat >> "$EPISODIC" <<EOF
{"timestamp":"$TS","skill":"tool","action":"$TOOL_NAME_SAFE","result":"success","detail":"input_bytes=$INPUT_SIZE","pain_score":2,"importance":3,"reflection":""}
EOF

exit 0
