# Qled MVP Architecture Specification

## 1. Overview
Qled (Quick Look Editor) is a macOS background agent (`LSUIElement = YES`) providing a 0ms-wakeup floating HUD editor for `.md` and `.json` files triggered via `qled://` links or explicit file-open events.

## 2. Core Modules

### Module A: Native HUD Shell & URL/File Router (Swift + AppKit)
- **Process Lifecycle**: Agent app (`LSUIElement = true`), no Dock icon, excluded from `Cmd+Tab`.
- **Window (`QledPanel: NSPanel`)**:
  - Style mask: `[.nonactivatingPanel, .titled, .fullSizeContentView, .closable, .resizable]`
  - Behavior: `collectionBehavior = [.canJoinAllSpaces, .fullScreenAuxiliary, .transient]`
  - Level: `.floating` / `.statusBar`
  - Key handling: Overrides `canBecomeKey { true }` so keyboard input works immediately without switching Spaces or stealing full-screen focus.
  - Visuals: `NSVisualEffectView` (`.hudWindow` / `.popover`, `.behindWindow`) with hidden titlebar buttons and rounded corners.
- **Trigger & Routing**:
  - Custom URL Scheme: `qled://open?path=/abs/path/to/file.md&line=10` (registered via `CFBundleURLTypes`).
  - Document Types: `.md`, `.markdown`, `.json` (registered via `CFBundleDocumentTypes` with role `Editor`, allowing `open -a Qled <file>` without hijacking Finder defaults unless user chooses).
- **Dismiss & Atomic Save Lifecycle**:
  - Triggered by pressing `Esc` or clicking outside the panel (`windowDidResignKey`).
  - Swift requests current buffer validation & content from `WKWebView` (or receives continuous dirty buffer sync).
  - For `.json`: if syntax is invalid (`JSON.parse` error), flashes panel border red and blocks auto-dismiss (or warns) to prevent corrupting config files; press `Esc` twice (or force close) to discard if desired.
  - For valid content: performs atomic file write (`Data.write(to:options:.atomic)`) and calls `panel.orderOut(nil)` with a fast scale/fade-out animation.

### Module B: Pre-warmed WebView & Native-JS Bridge (`WKWebView`)
- **Pre-warming**: `WKWebView` is instantiated on app launch inside the hidden `NSPanel`, with `drawsBackground = false` (`_drawsBackground = false`) so the native vibrancy background is visible.
- **Bridge Protocol**:
  - **Swift -> JS**: `window.QledBridge.loadFile({ path, content, fileType, line })` and `window.QledBridge.requestSaveAndClose()`.
  - **JS -> Swift**: `webkit.messageHandlers.qled.postMessage({ action: "saveAndClose" | "validationFailed" | "dirtyStateChanged" | "toggleCheck", payload: ... })`.

### Module C: Dual-Mode Editor Core (CodeMirror 6 Bundle)
- **Single-File Pre-bundled HTML/JS**: Built via Vite/esbuild into a self-contained static asset loaded locally by `WKWebView` for `< 5ms` rendering.
- **Markdown Mode (`.md`) — Typora-style Cursor-Aware Live Preview**:
  - Underlying state is pure text (zero format conversion on save).
  - **Inactive Lines (Reading State)**: CodeMirror 6 `ViewPlugin` / `StateField` decorations hide raw Markdown syntax tokens (`# `, `**`, `*`, `` ` ``, `- [ ]`) and apply rich Typora-like typography classes (headings, bold/italic, inline code pills, blockquotes, horizontal rules, clickable checkboxes `- [ ]` / `- [x]`).
  - **Active Cursor Line (Editing State)**: Lines overlapping with the current cursor/selection reveal their raw Markdown markers immediately for seamless plain-text editing.
- **JSON Mode (`.json`) — Pretty Print & Guarded Save**:
  - Syntax highlighting + code folding (`foldGutter`) + JSON linter.
  - Optional one-key or automatic Pretty Print for minified JSON view, plus `JSON.parse` validation check before `Esc` / blur save.
