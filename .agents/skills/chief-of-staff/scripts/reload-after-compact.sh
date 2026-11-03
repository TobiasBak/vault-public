#!/usr/bin/env bash
set -euo pipefail

skill_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

slash_command_marker='<command-(name|message)>/?chief-of-staff</command-(name|message)>'

transcript="$(jq -r '.transcript_path // empty' 2>/dev/null || true)"

if [[ -z "$transcript" || ! -f "$transcript" ]]; then
  exit 0
fi

if ! grep -Eq -- "$slash_command_marker" "$transcript"; then
  exit 0
fi

header="Post-compaction reload for the chief of staff: these files are your memory; follow them."

context="${header}"$'\n\n'"$(cat "$skill_dir/SKILL.md")"$'\n\n'"$(cat "$HOME/.local/state/chief-of-staff/state.md")"

jq -n --arg text "$context" \
  '{hookSpecificOutput:{hookEventName:"SessionStart",additionalContext:$text}}'