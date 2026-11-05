---
status: completed
date: 2026-10-10
id: fix_settings_button_click
---
# Fix Settings Button Click and Hover Events

## Background
The user reported issues and requested adjustments for the central small circle (`SettingsButton`) on the Taichi floating panel.

## Changes Made
1. **Right-Click Fix**: Added `rightMouseDown` override to `RightClickNSView` in `Components.swift` so that it correctly receives the `rightMouseUp` event and triggers the right-click action on macOS.
2. **Hover Delay Adjustment**: Migrated the `Timer` based hover logic to Swift `Task` and `Task.sleep`, and adjusted the long-hover delay to switch to the TaiChi icon from 1 second to 2 seconds.
3. **Hover Rotation Animation**: Introduced a `rotationCount` state. Now, when the TaiChi icon is hovered, it rotates. If the user long-hovers for 2 seconds and it switches from an App Icon to the TaiChi icon, it rotates immediately upon revealing itself to provide clear visual feedback.

## Resolution
The task is fully resolved and the `ops` agent has packaged the latest `.app` successfully.


4. **Right-Click Architecture Overhaul**: The initial fix revealed that SwiftUI's `Button` swallowed macOS mouse events aggressively, meaning `RightClickNSView` placed in a `.background()` could still miss clicks. We fully removed the `Button` wrapper for `SettingsButton` and replaced it with a custom `MouseInteractionView` applied as an overlay. This custom view:
   - Evaluates `acceptsFirstMouse` to natively bypass macOS focus swallowing.
   - Handles `rightMouseUp` robustly.
   - Distinguishes left double-clicks reliably via `event.clickCount == 2`, eliminating the clunky manual timestamp comparison.
