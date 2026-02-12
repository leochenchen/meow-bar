---
name: meow
description: Check MeowBar status and control your menu bar cat companion
---

# MeowBar Status

Show the current state of your pixel cat companion in the menu bar.

## Instructions

When the user runs /meow, do the following:

1. Read the file at ~/.claude/meow-state.json
2. Display the current cat state with the appropriate emoji:
   - idle (sleeping): The cat is sleeping... zzz
   - starting (waking up): The cat is stretching awake!
   - thinking (typing): The cat is typing furiously on its keyboard!
   - working (running): The cat is running at full speed!
   - error (scared): The cat got startled! Check what went wrong.
   - complete (celebrating): The cat is wagging its tail, waiting for praise! Tell it "good kitty"!
   - ending (waving): The cat is waving goodbye!
   - compacting (thinking): The cat is deep in thought...

3. Show the recent events from the events_log array (last 5)
4. If the user says "reset", delete ~/.claude/meow-state.json to reset the cat to idle
5. If the user says "status", just show the current state

Present the information in a fun, cat-themed way. Keep it brief and playful.
