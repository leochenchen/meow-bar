#!/bin/bash
# MeowBar - Claude Code hook script
# Reads lifecycle event data from stdin and updates ~/.claude/meow-state.json

EVENT_NAME="${1:-unknown}"
STATE_FILE="$HOME/.claude/meow-state.json"
TEMP_FILE="$HOME/.claude/meow-state.tmp.$$"

# Read stdin (Claude Code sends JSON payload)
input=$(cat)

# Extract fields using jq
session_id=$(echo "$input" | jq -r '.session_id // ""' 2>/dev/null || echo "")
tool_name=$(echo "$input" | jq -r '.tool_name // ""' 2>/dev/null || echo "")
tool_input_cmd=$(echo "$input" | jq -r '.tool_input.command // ""' 2>/dev/null || echo "")
error_msg=""

# Map event to cat state
case "$EVENT_NAME" in
  SessionStart)
    state="starting"
    ;;
  UserPromptSubmit)
    state="thinking"
    ;;
  PreToolUse)
    state="working"
    ;;
  PostToolUse)
    state="working"
    ;;
  PostToolUseFailure)
    state="error"
    error_msg=$(echo "$input" | jq -r '.error // "Tool failed"' 2>/dev/null | head -c 200)
    ;;
  Stop)
    state="complete"
    ;;
  PreCompact)
    state="compacting"
    ;;
  SessionEnd)
    state="ending"
    ;;
  *)
    state="idle"
    ;;
esac

# Build detail string for event log
detail=""
if [ -n "$tool_name" ] && [ "$tool_name" != "null" ]; then
  if [ -n "$tool_input_cmd" ] && [ "$tool_input_cmd" != "null" ]; then
    detail="${tool_name}: $(echo "$tool_input_cmd" | head -c 80)"
  else
    detail="$tool_name"
  fi
fi

# Get current timestamp
timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Read existing state file or start fresh
if [ -f "$STATE_FILE" ]; then
  existing=$(cat "$STATE_FILE" 2>/dev/null || echo '{}')
else
  existing='{}'
fi

# Build new event log entry and update state atomically
new_event=$(jq -n \
  --arg event "$EVENT_NAME" \
  --arg time "$timestamp" \
  --arg detail "$detail" \
  '{event: $event, time: $time, detail: $detail}')

echo "$existing" | jq \
  --arg state "$state" \
  --arg ts "$timestamp" \
  --arg sid "$session_id" \
  --arg le "$EVENT_NAME" \
  --arg tn "$tool_name" \
  --arg em "$error_msg" \
  --argjson ne "$new_event" \
  '{
    state: $state,
    timestamp: $ts,
    session_id: $sid,
    last_event: $le,
    tool_name: $tn,
    error_message: $em,
    events_log: ((.events_log // []) + [$ne] | .[-20:])
  }' > "$TEMP_FILE" 2>/dev/null

# Atomic replace
if [ -f "$TEMP_FILE" ]; then
  mv "$TEMP_FILE" "$STATE_FILE"
fi

# Never block Claude Code
exit 0
