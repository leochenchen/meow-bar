# MeowBar

A pixel cat lives in your macOS menu bar, reflecting Claude Code's real-time state.

Inspired by ClashX's running cat — but this one sleeps, types, runs, celebrates, and gets scared based on what Claude Code is doing.

![macOS](https://img.shields.io/badge/macOS-13%2B-blue)
![Swift](https://img.shields.io/badge/Swift-5.9-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## Cat States

| State | Color | Animation | When |
|-------|-------|-----------|------|
| Sleeping | Gray-blue | Curled up with Zzz | Idle / No session |
| Waking Up | Yellow | Stretching | Session starts |
| Typing | Blue | Paws on keyboard | Processing your prompt |
| Running | Green | Full sprint | Using tools (Bash, Read, Edit...) |
| Scared | Red | Arched back, fur raised | Tool error / failure |
| Celebrating | Gold | Tail wagging + sparkles | Task complete (waiting for praise!) |
| Waving | Purple | Paw wave | Session ending |
| Thinking | Teal | Head tilt + thought dots | Context compaction |

## Features

- **Animated pixel cat** in the macOS menu bar with colored state indicators
- **8 distinct animations** — 32 frames of pixel art, each state has its own color
- **macOS notifications** on task completion and errors
- **Dropdown menu** showing session info, recent events, and last tool used
- **Auto-idle** — cat falls asleep after 2 minutes of inactivity
- **Praise mode** — cat stays in celebration state until your next prompt (it's waiting for you to say "good kitty!")

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
# Add and enable the Claude Code plugin
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

1. **Claude Code Plugin** registers hooks for 8 lifecycle events (SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, PostToolUseFailure, Stop, PreCompact, SessionEnd)
2. Each hook runs `scripts/update-state.sh`, which reads the event payload from stdin and atomically updates `~/.claude/meow-state.json`
3. **MeowBar.app** watches the state file via FSEvents and cycles through the appropriate pixel art animation frames

## Project Structure

```
meow-bar/
├── .claude-plugin/plugin.json    # Claude Code plugin manifest
├── hooks/hooks.json              # 8 lifecycle event registrations
├── scripts/update-state.sh       # Hook script (reads stdin, writes state)
├── commands/meow.md              # /meow slash command
├── app/MeowBar/                  # Swift menu bar application
│   ├── Package.swift
│   └── Sources/
│       ├── MeowBarApp.swift            # App entry point (LSUIElement)
│       ├── StatusBarController.swift   # Animation engine + menu
│       ├── StateWatcher.swift          # FSEvents file watcher
│       ├── MeowState.swift             # State model
│       └── NotificationManager.swift   # macOS notifications
├── resources/generate-frames.py  # Pixel art generator (Python + Pillow)
├── install.sh                    # One-line installer
└── app/MeowBar/Resources/Frames/ # 32 pre-generated PNG frames
```

## Customization

### Regenerate Cat Frames

Want different pixel art? Edit `resources/generate-frames.py` and run:

```bash
pip3 install Pillow
python3 resources/generate-frames.py
cp app/MeowBar/Resources/Frames/*.png ~/.meow-bar/frames/
```

### Menu Bar Controls

Click the cat in the menu bar to see:
- Current state and emoji indicator
- Active session ID
- Last tool used
- Recent event log (last 5 events)
- Toggle notifications on/off

## Troubleshooting

**Cat not changing state?**
- Make sure the plugin is enabled: `claude plugin list`
- Check the state file: `cat ~/.claude/meow-state.json | jq .`
- Test a hook manually: `echo '{"session_id":"test"}' | bash scripts/update-state.sh SessionStart`

**App not showing in menu bar?**
- Check if it's running: `ps aux | grep MeowBar`
- Try launching from terminal: `~/.meow-bar/MeowBar.app/Contents/MacOS/MeowBar`

**No notifications?**
- Check System Settings > Notifications > MeowBar
- Toggle notifications via the menu bar dropdown

## License

MIT
