---
description: 关于前端 DOM 注入、CSS 和 JS 的操作规范与限制。当涉及修改前端界面或注入脚本时触发。
globs: *.js, *.css, *.html
alwaysApply: false
---

## DOM Manipulation & UI Customization
- **Rule: Prefer Pure CSS over JS DOM Manipulation.** When altering the appearance or text of third-party, framework-driven (e.g., React) UI components, ALWAYS prioritize using pure CSS overrides (e.g., hiding original text with `font-size: 0` and injecting new text with `::after`, or hiding elements with `display: none`). 
- **Reason:** JavaScript-based DOM manipulations (like altering `textContent` or `classList`) are often instantly overwritten or stripped by the Virtual DOM during re-renders. CSS stylesheet injections bypass the VDOM entirely and apply consistently at the browser rendering level, making them vastly more stable and robust.

## React SPA Lifecycle & Persistent Injection
- **Rule: Continuous Observation for Volatile Elements.** When you *must* inject complex HTML components (like buttons) into a React-managed container, NEVER use `disconnect()` on your `MutationObserver` after the first successful injection. React SPA navigation will destroy the old container and your injected elements.
- **Implementation:** Maintain a continuous `MutationObserver` on `document.body` with `subtree: true`. Check if the target container exists AND your custom element is missing (`if (target && !document.getElementById('my-btn')) { inject(); }`).
- **Rule: Global Singletons for Stateful Overlays.** Never mount stateful UI overlays (like sliding panels, dialogs) inside volatile React containers. Mount them as singletons on `document.body`. Only inject the lightweight trigger (e.g. a toggle button) into the volatile React container, and re-bind its click event to the global singleton every time it is re-injected.
- **Rule: Floating Menus Must Use Fixed Viewport Positioning.** When creating floating dropdowns, popovers, or autocomplete menus for inputs, NEVER use `position: absolute` mounted inside the input container or its wrapper. Modern input boxes commonly apply `overflow: hidden` or `overflow: clip` for rounded border clipping, which completely truncates any element extending outside. Always mount floating menus on `document.body` with `position: fixed; z-index: 999999;` and compute coordinates via `getBoundingClientRect()` from the input anchor.
- **Rule: ES Module Strict Mode Hygiene.** All injected web modules run under strict mode (`"use strict"`). Never omit declaration keywords (`let`, `const`) on any local variable (e.g., `badgeText = ...`), as an unhandled `ReferenceError` will immediately halt the rendering loop, causing silent DOM failures where data exists in memory but the UI remains blank.
