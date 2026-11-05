# Qled Ironclad Rules

## [Global]
- **Project Name**: Qled (Quick Look Editor)
- **Workspace**: `/Users/kael/Projects/Qled`
- **Metadata Directory**: `/Users/kael/.gemini/Projects/Qled`
- **Core Philosophy**:
  1. **Zero-Friction HUD Panel**: Agent app (`LSUIElement = true`, no Dock icon, no `Cmd+Tab` pollution), persistent pre-warmed `NSPanel` (`.nonactivatingPanel`, `.canJoinAllSpaces`, `.fullScreenAuxiliary`, `.transient`) with native vibrancy (`NSVisualEffectView`).
  2. **Zero-Conversion Persistence**: The editor's in-memory text buffer IS the single source of truth. Saving to disk MUST write the exact text buffer via Atomic Write without any AST-to-Markdown format conversion or re-serialization.
  3. **Lossless Live Preview**: Use CodeMirror 6 Decoration engine for Typora/Obsidian-style cursor-aware inline preview (raw Markdown syntax revealed on active cursor line/block; rendered typography when cursor leaves).

## [Main Agent]
- Maintain centralized metadata in `/Users/kael/.gemini/Projects/Qled/`. Never create `.gemini/`, `kb/`, `tasks/`, or `docs/` inside `/Users/kael/Projects/Qled`.
- Delegate heavy multi-file implementation to `dev-manager` and app packaging / `.app` bundle installation to `ops-manager`.
- Synchronize every code/environment modification with the `kanban-task-manager` MCP server before ending a turn.

## [Dev Agent]
- Only write source code inside `/Users/kael/Projects/Qled`.
- Target macOS native Swift (AppKit `NSPanel` + `WKWebView` bridge) and lightweight web bundle (CodeMirror 6).
- Ensure `WKWebView` has transparent background (`drawsBackground = false`) so native `NSVisualEffectView` vibrancy shines through.
- Never use AST-rewriting editors (e.g. BlockNote, ProseMirror/Milkdown) that mutate or re-format raw Markdown upon save.

## [Ops Agent]
- Build and package `Qled.app` using Swift Package Manager / `xcodebuild` and register `qled://` URL scheme in LaunchServices when deploying locally.
