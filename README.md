[English](#english) | [中文](#中文) | [日本語](#日本語)

---

<a name="english"></a>

# MeowBar

A pixel cat lives in your macOS menu bar, reflecting Claude Code's real-time state.

![macOS](https://img.shields.io/badge/macOS-13%2B-blue)
![Swift](https://img.shields.io/badge/Swift-5.9-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## Cat States

The cat changes color and expression based on what Claude Code is doing:

```
    idle            your turn         working          done!            oops
  (no session)    (waiting for you)  (Claude working)  (task complete)  (error!)

   /\_/\            /\_/\            /\_/\    o        /\_/\            /\_/\
  ( o.o )          ( o.o )          ( o.o )  o        ( ^.^ )          ( O.O )
   > ^ <            > ^ <            > ^ <             > w <            > o <
    |/                \|              |/                 |/               |/
   white             yellow          green             green             red
```

| State | Color | Animation | Text | When |
|-------|-------|-----------|------|------|
| **idle** | White | Head tilting | *(none)* | No active session, relaxing |
| **your turn** | Yellow | Head tilting | `your turn` | Session active, waiting for user input |
| **working** | Green | Cat + bouncing ball | `3.2k tokens` | Claude is thinking and using tools |
| **done!** | Green | Happy eyes + sparkles | `done!` | Task complete, tail wagging |
| **oops** | Red | Big O\_O eyes looking right | `oops` | A tool call failed |

## Architecture

```
Claude Code Hooks ──write──> ~/.claude/meow-state.json ──watch──> MeowBar.app
    (bash)                     (JSON state file)                   (Swift)
```

Hook scripts listen to 8 lifecycle events and map them to cat states. The menu bar app watches the state file via FSEvents and animates the corresponding pixel art frames.

### Event-to-State Mapping

```
SessionStart ─────┐
UserPromptSubmit ──┤
PreToolUse ────────┼──> working (green)
PostToolUse ───────┤
PreCompact ────────┘
Stop ──────────────────> complete (green, "done!")
PostToolUseFailure ────> error (red, "oops")
SessionEnd ────────────> idle (white)
```

## Installation

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

### Enable the Hooks

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

MeowBar uses the [Claude Code hooks system](https://docs.anthropic.com/en/docs/claude-code/hooks) to observe Claude's lifecycle events. A lightweight bash script receives event data via stdin, maps each event to one of four cat states, and atomically writes the result to `~/.claude/meow-state.json`. The native Swift menu bar app watches this file and swaps animation frames accordingly.

The "your turn" state is a special visual variant: when Claude goes idle but the session is still active, the app shows yellow "waiting" frames instead of white "idle" frames to signal that it is your turn to type.

## Requirements

| Dependency | Purpose |
|---|---|
| macOS 13 (Ventura)+ | Menu bar app target |
| Swift 5.9+ (Xcode CLI Tools) | Build the app |
| [jq](https://jqlang.github.io/jq/) (`brew install jq`) | JSON processing in hook script |
| Python 3 + [Pillow](https://pillow.readthedocs.io/) | Only if regenerating pixel art frames |

## Project Structure

```
meow-bar/
├── .claude-plugin/plugin.json    # Claude Code plugin manifest
├── hooks/hooks.json              # 8 lifecycle event registrations
├── scripts/update-state.sh       # Hook script (maps events to states)
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

## License

MIT

---

<a name="中文"></a>

# MeowBar

一只像素猫住在你的 macOS 菜单栏里，实时反映 Claude Code 的工作状态。

![macOS](https://img.shields.io/badge/macOS-13%2B-blue)
![Swift](https://img.shields.io/badge/Swift-5.9-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## 猫咪状态

猫咪会根据 Claude Code 的状态改变颜色和表情：

```
     空闲            轮到你了          工作中            完成!             出错
   (无会话)        (等你输入)      (Claude 工作中)     (任务完成)        (出错了!)

   /\_/\            /\_/\            /\_/\    o        /\_/\            /\_/\
  ( o.o )          ( o.o )          ( o.o )  o        ( ^.^ )          ( O.O )
   > ^ <            > ^ <            > ^ <             > w <            > o <
    |/                \|              |/                 |/               |/
    白色              黄色             绿色              绿色              红色
```

| 状态 | 颜色 | 动画 | 文字 | 触发时机 |
|------|------|------|------|----------|
| **空闲** | 白色 | 歪头 | *(无)* | 没有活跃会话，猫咪在放松 |
| **轮到你了** | 黄色 | 歪头 | `your turn` | 会话中，等待你输入 |
| **工作中** | 绿色 | 猫咪 + 弹跳球 | `3.2k tokens` | Claude 正在思考和使用工具 |
| **完成!** | 绿色 | 开心眯眼 + 闪烁 | `done!` | 任务完成，尾巴摇摇 |
| **出错** | 红色 | 瞪大眼睛向右看 | `oops` | 工具调用失败 |

## 架构

```
Claude Code Hooks ──写入──> ~/.claude/meow-state.json ──监听──> MeowBar.app
    (bash)                    (JSON 状态文件)                    (Swift)
```

Hook 脚本监听 8 个生命周期事件，并将它们映射为猫咪状态。菜单栏应用通过 FSEvents 监听状态文件，并播放对应的像素动画帧。

### 事件到状态的映射

```
SessionStart ─────┐
UserPromptSubmit ──┤
PreToolUse ────────┼──> working（绿色）
PostToolUse ───────┤
PreCompact ────────┘
Stop ──────────────────> complete（绿色，"done!"）
PostToolUseFailure ────> error（红色，"oops"）
SessionEnd ────────────> idle（白色）
```

## 安装

```bash
git clone https://github.com/leochenchen/meow-bar.git
cd meow-bar
./install.sh
```

安装脚本会自动完成：
1. 生成像素猫动画帧（如需要）
2. 构建 Swift 菜单栏应用
3. 在 `~/.meow-bar/` 创建 `MeowBar.app`
4. 初始化状态文件

### 启用 Hooks

```bash
claude plugin add /path/to/meow-bar
claude plugin enable meow-bar
```

### 启动

```bash
open ~/.meow-bar/MeowBar.app
```

开机自启：**系统设置 > 通用 > 登录项 > 添加 MeowBar.app**

## 工作原理

MeowBar 利用 [Claude Code hooks 系统](https://docs.anthropic.com/en/docs/claude-code/hooks) 来观察 Claude 的生命周期事件。一个轻量级的 bash 脚本通过 stdin 接收事件数据，将每个事件映射为四种猫咪状态之一，并原子性地写入 `~/.claude/meow-state.json`。原生 Swift 菜单栏应用监听此文件并切换对应的动画帧。

"轮到你了"是一种特殊的视觉变体：当 Claude 空闲但会话仍然活跃时，应用会显示黄色的"等待"帧而非白色的"空闲"帧，提示现在轮到你输入了。

## 系统要求

| 依赖 | 用途 |
|------|------|
| macOS 13 (Ventura)+ | 菜单栏应用运行环境 |
| Swift 5.9+（Xcode 命令行工具） | 构建应用 |
| [jq](https://jqlang.github.io/jq/)（`brew install jq`） | Hook 脚本中的 JSON 处理 |
| Python 3 + [Pillow](https://pillow.readthedocs.io/) | 仅在重新生成像素动画帧时需要 |

## 项目结构

```
meow-bar/
├── .claude-plugin/plugin.json    # Claude Code 插件清单
├── hooks/hooks.json              # 8 个生命周期事件注册
├── scripts/update-state.sh       # Hook 脚本（事件 → 状态映射）
├── commands/meow.md              # /meow 斜杠命令
├── app/MeowBar/                  # Swift 菜单栏应用
│   ├── Package.swift
│   └── Sources/
│       ├── MeowBarApp.swift
│       ├── StatusBarController.swift
│       ├── StateWatcher.swift
│       ├── MeowState.swift
│       └── NotificationManager.swift
├── resources/generate-frames.py  # 像素动画生成器（Python + Pillow）
└── app/MeowBar/Resources/Frames/ # 17 张预生成的 PNG 帧
```

## 许可证

MIT

---

<a name="日本語"></a>

# MeowBar

macOS メニューバーに住むピクセル猫が、Claude Code のリアルタイム状態を映し出します。

![macOS](https://img.shields.io/badge/macOS-13%2B-blue)
![Swift](https://img.shields.io/badge/Swift-5.9-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## 猫の状態

Claude Code の状態に応じて、猫の色と表情が変わります：

```
     待機             あなたの番        作業中             完了!             エラー
  (セッションなし)    (入力待ち)     (Claude 作業中)     (タスク完了)       (失敗!)

   /\_/\            /\_/\            /\_/\    o        /\_/\            /\_/\
  ( o.o )          ( o.o )          ( o.o )  o        ( ^.^ )          ( O.O )
   > ^ <            > ^ <            > ^ <             > w <            > o <
    |/                \|              |/                 |/               |/
    白               黄色             緑                緑                赤
```

| 状態 | 色 | アニメーション | テキスト | タイミング |
|------|-----|--------------|---------|-----------|
| **待機** | 白 | 首かしげ | *(なし)* | アクティブなセッションなし、リラックス中 |
| **あなたの番** | 黄色 | 首かしげ | `your turn` | セッション中、ユーザー入力待ち |
| **作業中** | 緑 | 猫 + 跳ねるボール | `3.2k tokens` | Claude が思考中・ツール使用中 |
| **完了!** | 緑 | 幸せな目 + キラキラ | `done!` | タスク完了、しっぽフリフリ |
| **エラー** | 赤 | 大きな O\_O の目で右を見る | `oops` | ツール呼び出し失敗 |

## アーキテクチャ

```
Claude Code Hooks ──書込──> ~/.claude/meow-state.json ──監視──> MeowBar.app
    (bash)                    (JSON 状態ファイル)                (Swift)
```

Hook スクリプトが 8 つのライフサイクルイベントを監視し、猫の状態にマッピングします。メニューバーアプリは FSEvents で状態ファイルを監視し、対応するピクセルアートのフレームをアニメーション表示します。

### イベントから状態へのマッピング

```
SessionStart ─────┐
UserPromptSubmit ──┤
PreToolUse ────────┼──> working（緑）
PostToolUse ───────┤
PreCompact ────────┘
Stop ──────────────────> complete（緑、"done!"）
PostToolUseFailure ────> error（赤、"oops"）
SessionEnd ────────────> idle（白）
```

## インストール

```bash
git clone https://github.com/leochenchen/meow-bar.git
cd meow-bar
./install.sh
```

インストーラーが自動で行うこと：
1. ピクセル猫のアニメーションフレームを生成（必要な場合）
2. Swift メニューバーアプリをビルド
3. `~/.meow-bar/` に `MeowBar.app` を作成
4. 状態ファイルを初期化

### Hooks を有効化

```bash
claude plugin add /path/to/meow-bar
claude plugin enable meow-bar
```

### 起動

```bash
open ~/.meow-bar/MeowBar.app
```

ログイン時に自動起動：**システム設定 > 一般 > ログイン項目 > MeowBar.app を追加**

## 仕組み

MeowBar は [Claude Code hooks システム](https://docs.anthropic.com/en/docs/claude-code/hooks) を利用して Claude のライフサイクルイベントを観察します。軽量な bash スクリプトが stdin からイベントデータを受け取り、各イベントを 4 つの猫状態のいずれかにマッピングし、`~/.claude/meow-state.json` にアトミックに書き込みます。ネイティブ Swift メニューバーアプリがこのファイルを監視し、対応するアニメーションフレームを切り替えます。

「あなたの番」は特別なビジュアルバリエーションです。Claude がアイドル状態でもセッションがまだアクティブな場合、白い「待機」フレームの代わりに黄色い「待ち」フレームを表示し、入力の順番であることを知らせます。

## 必要環境

| 依存関係 | 用途 |
|---------|------|
| macOS 13 (Ventura)+ | メニューバーアプリの動作環境 |
| Swift 5.9+（Xcode コマンドラインツール） | アプリのビルド |
| [jq](https://jqlang.github.io/jq/)（`brew install jq`） | Hook スクリプトでの JSON 処理 |
| Python 3 + [Pillow](https://pillow.readthedocs.io/) | ピクセルアートフレームの再生成時のみ必要 |

## プロジェクト構成

```
meow-bar/
├── .claude-plugin/plugin.json    # Claude Code プラグインマニフェスト
├── hooks/hooks.json              # 8 つのライフサイクルイベント登録
├── scripts/update-state.sh       # Hook スクリプト（イベント → 状態マッピング）
├── commands/meow.md              # /meow スラッシュコマンド
├── app/MeowBar/                  # Swift メニューバーアプリ
│   ├── Package.swift
│   └── Sources/
│       ├── MeowBarApp.swift
│       ├── StatusBarController.swift
│       ├── StateWatcher.swift
│       ├── MeowState.swift
│       └── NotificationManager.swift
├── resources/generate-frames.py  # ピクセルアート生成スクリプト（Python + Pillow）
└── app/MeowBar/Resources/Frames/ # 17 枚の事前生成済み PNG フレーム
```

## ライセンス

MIT
