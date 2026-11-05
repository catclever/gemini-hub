# Ironclad Rules

## [Global]
- Project: Hammerspoon Configuration
- Workspace: /Users/kael/Library/Services/hammerspoon
- Architecture: TaiChi v3 structure (modular). Legacy modules are in v3/legacy/ (if any).

## [Main Agent]
- Manage tasks in the centralized `~/.gemini/Projects/hammerspoon/` directory.

## [Dev Agent]
- Use Lua 5.4+ compatible syntax (Hammerspoon standard).
- New modules should follow the TaiChi v3 component structure (`actions`, `core`, `atelier`).

## [Ops Agent]
- Reload Hammerspoon configuration with `hs.reload()` or by triggering it via the UI if requested.
- The v2 directory is completely DEPRECATED. All new development MUST go to v3.
