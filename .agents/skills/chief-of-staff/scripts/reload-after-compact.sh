#!/usr/bin/env bash
# Re-inject the chief-of-staff memory after a compaction.
#
# The skill sets disable-model-invocation, so Claude Code does not re-inject its
# body on its own. This hook is registered in .claude/settings.json as a
# SessionStart hook with matcher "compact". It stays silent in sessions that
# never invoked the skill, so other threads are unaffected.
set -euo pipefail

skill_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

# Slash-command invocation markers Claude Code records in the transcript. A
# Skill tool_use with "skill":"chief-of-staff" never appears, because the skill
# is only reachable as a slash command.
marker='<command-(name|message)>/?chief-of-staff</command-(name|message)>'

transcript="$(jq -r '.transcript_path // empty' 2>/dev/null || true)"

if [[ -z "$transcript" || ! -f "$transcript" ]]; then
  exit 0
fi

if ! grep -Eq -- "$marker" "$transcript"; then
  exit 0
fi

header="Post-compaction reload for the chief of staff: these files are your memory; follow them."

context="${header}"$'\n\n'"$(cat "$skill_dir/SKILL.md")"$'\n\n'"$(cat "$skill_dir/state.md")"$'\n\n'"$(tail -n 20 "$skill_dir/decisions.md")"

jq -n --arg text "$context" \
  '{hookSpecificOutput:{hookEventName:"SessionStart",additionalContext:$text}}'