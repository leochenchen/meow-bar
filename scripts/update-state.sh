#!/bin/bash
# MeowBar - Claude Code hook script
# Maps lifecycle events to 4 cat states: idle, working, complete, error
# Tracks session stats: tool calls, prompts, errors, duration

EVENT_NAME="${1:-unknown}"
STATE_FILE="$HOME/.claude/meow-state.json"
TEMP_FILE="$HOME/.claude/meow-state.tmp.$$"

# Read stdin
input=$(cat)

# Extract fields
session_id=$(echo "$input" | jq -r '.session_id // ""' 2>/dev/null || echo "")
tool_name=$(echo "$input" | jq -r '.tool_name // ""' 2>/dev/null || echo "")
tool_input_cmd=$(echo "$input" | jq -r '.tool_input.command // ""' 2>/dev/null || echo "")
# Try to extract token usage (input_tokens + output_tokens)
input_tokens=$(echo "$input" | jq -r '.input_tokens // 0' 2>/dev/null || echo "0")
output_tokens=$(echo "$input" | jq -r '.output_tokens // 0' 2>/dev/null || echo "0")
inc_tokens=$(( ${input_tokens:-0} + ${output_tokens:-0} ))
error_msg=""

# Map events to 4 states
case "$EVENT_NAME" in
  SessionStart|UserPromptSubmit|PreToolUse|PostToolUse|PreCompact)
    state="working"
    ;;
  PostToolUseFailure)
    state="error"
    error_msg=$(echo "$input" | jq -r '.error // "Tool failed"' 2>/dev/null | head -c 200)
    ;;
  Stop)
    state="complete"
    ;;
  SessionEnd)
    state="idle"
    ;;
  *)
    state="idle"
    ;;
esac

# Build detail string
detail=""
if [ -n "$tool_name" ] && [ "$tool_name" != "null" ]; then
  if [ -n "$tool_input_cmd" ] && [ "$tool_input_cmd" != "null" ]; then
    detail="${tool_name}: $(echo "$tool_input_cmd" | head -c 80)"
  else
    detail="$tool_name"
  fi
fi

timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Read existing or start fresh
if [ -f "$STATE_FILE" ]; then
  existing=$(cat "$STATE_FILE" 2>/dev/null || echo '{}')
else
  existing='{}'
fi

# Calculate stat increments
inc_tools=0
inc_prompts=0
inc_errors=0
session_start_time=$(echo "$existing" | jq -r '.session_start_time // ""' 2>/dev/null)

case "$EVENT_NAME" in
  SessionStart)
    session_start_time="$timestamp"
    # Reset counters on new session
    existing=$(echo "$existing" | jq '.tool_call_count = 0 | .prompt_count = 0 | .error_count = 0 | .token_count = 0 | .events_log = []')
    ;;
  UserPromptSubmit)
    inc_prompts=1
    ;;
  PostToolUse)
    inc_tools=1
    ;;
  PostToolUseFailure)
    inc_tools=1
    inc_errors=1
    ;;
esac

# Build event log entry and update state
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
  --arg sst "$session_start_time" \
  --argjson it "$inc_tools" \
  --argjson ip "$inc_prompts" \
  --argjson ie "$inc_errors" \
  --argjson itkn "$inc_tokens" \
  --argjson ne "$new_event" \
  '{
    state: $state,
    timestamp: $ts,
    session_id: $sid,
    last_event: $le,
    tool_name: $tn,
    error_message: $em,
    session_start_time: $sst,
    tool_call_count: ((.tool_call_count // 0) + $it),
    prompt_count: ((.prompt_count // 0) + $ip),
    error_count: ((.error_count // 0) + $ie),
    token_count: ((.token_count // 0) + $itkn),
    events_log: ((.events_log // []) + [$ne] | .[-20:])
  }' > "$TEMP_FILE" 2>/dev/null

if [ -f "$TEMP_FILE" ]; then
  mv "$TEMP_FILE" "$STATE_FILE"
fi

exit 0
