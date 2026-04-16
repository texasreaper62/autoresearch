#!/usr/bin/env bash
# Pre-tool-call hook. Reads tool invocation from stdin; exits 2 on deny.
# Claude Code protocol: https://docs.anthropic.com/en/docs/claude-code/hooks
#
# This is a thin shell implementation. For richer matching, upgrade to the
# Python version in this directory (pre_tool_call.py).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PERMS="$ROOT/protocols/permissions.md"
DENY_FILE="$ROOT/harness/hooks/deny_paths.txt"

# Read the hook input JSON from stdin
INPUT="$(cat)"

# Extract tool + target. Works without jq for simple cases.
TOOL_NAME=$(printf '%s' "$INPUT" | sed -n 's/.*"tool_name"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
FILE_PATH=$(printf '%s' "$INPUT" | sed -n 's/.*"file_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
COMMAND=$(printf '%s' "$INPUT" | sed -n 's/.*"command"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')

# Deny specific file paths (repo-configured)
if [[ -n "$FILE_PATH" && -f "$DENY_FILE" ]]; then
  while IFS= read -r pattern; do
    [[ -z "$pattern" || "$pattern" == \#* ]] && continue
    if [[ "$FILE_PATH" == *"$pattern"* ]]; then
      echo "DENY: $TOOL_NAME on '$FILE_PATH' blocked by deny_paths.txt rule: $pattern" >&2
      exit 2
    fi
  done < "$DENY_FILE"
fi

# Deny force-push to protected branches
if [[ "$TOOL_NAME" == "Bash" && "$COMMAND" == *"git push"*"--force"* ]]; then
  for protected in main master production staging; do
    if [[ "$COMMAND" == *"$protected"* ]]; then
      echo "DENY: force-push to protected branch '$protected' blocked" >&2
      exit 2
    fi
  done
fi

# Deny --no-verify on commits
if [[ "$TOOL_NAME" == "Bash" && "$COMMAND" == *"git commit"*"--no-verify"* ]]; then
  echo "DENY: commit --no-verify blocked; fix the hook failure instead" >&2
  exit 2
fi

exit 0
