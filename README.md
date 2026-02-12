# MeowBar

A pixel cat lives in your macOS menu bar, reflecting Claude Code's real-time state.

Inspired by ClashX's running cat — but this one sleeps, runs, celebrates, and gets scared based on what Claude Code is doing.

![macOS](https://img.shields.io/badge/macOS-13%2B-blue)
![Swift](https://img.shields.io/badge/Swift-5.9-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## Cat States

| State | Color | Animation | When |
|-------|-------|-----------|------|
| Sleeping | White | Curled up with Zzz | Idle / No session |
| Running | Green | Full sprint | Claude is working |
| Celebrating | Gold | Tail wagging + sparkles | Task complete (waiting for praise!) |
| Scared | Red | Arched back, fur raised | Tool error / failure |

## Features

- **Animated pixel cat** in the macOS menu bar with colored state indicators
- **4 clear states** — white (idle), green (working), gold (done), red (error)
- **macOS notifications** on task completion and errors
- **Dropdown menu** showing session info, recent events, and last tool used
- **Auto-idle** — cat falls asleep after 2 minutes of inactivity
- **Praise mode** — cat stays in celebration state until your next prompt

## Requirements

- macOS 13 (Ventura) or later
- Swift 5.9+ (Xcode Command Line Tools)
- [jq](https://jqlang.github.io/jq/) (`brew install jq`)
- Claude Code with plugin support
- Python 3 + Pillow (only if regenerating pixel art frames)

## Installation

### Quick Install

```bash
git clone https://github.com/leochenchen/meow-bar.git
cd meow-bar
./install.sh
```

The installer will:
1. Generate pixel cat frames (if needed)
2. Build the Swift menu bar app
3. Create `MeowBar.app` at `~/.meow-bar/`
4. Initialize the state file

### Enable the Plugin

```bash
claude plugin add /path/to/meow-bar
claude plugin enable meow-bar
```

### Launch

```bash
open ~/.meow-bar/MeowBar.app
```

To auto-start on login: **System Settings > General > Login Items > Add MeowBar.app**

## How It Works

```
Claude Code Hooks ──write──> ~/.claude/meow-state.json ──watch──> MeowBar.app
    (bash)                      (JSON state file)                  (Swift)
```

1. **Claude Code Plugin** registers hooks for 8 lifecycle events
2. Hook script maps all events to 4 cat states and atomically updates `~/.claude/meow-state.json`
3. **MeowBar.app** watches the state file via FSEvents and cycles through pixel art animation frames

### Event → State Mapping

| Events | Cat State |
|--------|-----------|
| SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, PreCompact | **working** (green) |
| Stop | **complete** (gold) |
| PostToolUseFailure | **error** (red) |
| SessionEnd | **idle** (white) |

## Project Structure

```
meow-bar/
├── .claude-plugin/plugin.json    # Claude Code plugin manifest
├── hooks/hooks.json              # 8 lifecycle event registrations
├── scripts/update-state.sh       # Hook script (maps events → 4 states)
├── commands/meow.md              # /meow slash command
├── app/MeowBar/                  # Swift menu bar application
│   ├── Package.swift
│   └── Sources/
│       ├── MeowBarApp.swift
│       ├── StatusBarController.swift
│       ├── StateWatcher.swift
│       ├── MeowState.swift
│       └── NotificationManager.swift
├── resources/generate-frames.py  # Pixel art generator (Python + Pillow)
└── app/MeowBar/Resources/Frames/ # 17 pre-generated PNG frames
```

## Customization

### Regenerate Cat Frames

Edit `resources/generate-frames.py` and run:

```bash
pip3 install Pillow
python3 resources/generate-frames.py
cp app/MeowBar/Resources/Frames/*.png ~/.meow-bar/frames/
```

### Menu Bar Controls

Click the cat to see: current state, session ID, last tool, recent events, and notification toggle.

## Troubleshooting

**Cat not changing state?**
- Check plugin: `claude plugin list`
- Check state file: `cat ~/.claude/meow-state.json | jq .`
- Test hook: `echo '{"session_id":"test"}' | bash scripts/update-state.sh SessionStart`

**App not in menu bar?**
- Check: `ps aux | grep MeowBar`
- Launch manually: `~/.meow-bar/MeowBar.app/Contents/MacOS/MeowBar`

## License

MIT
