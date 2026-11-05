# Post-Mortem: SPA Route Navigation CSS Variable Loss

## Context
In the Antigravity IDE browser extension (`com.google.antigravity`), we inject custom CSS variables (like `--topbar-bg-color`) into `document.documentElement` to theme the top title bar based on the active project. A `MutationObserver` watches `document.body` for DOM changes to detect when the project name in the UI changes, and triggers a theme sync.

## What Was Tried
The original implementation solely checked if the extracted project name had changed:
```javascript
if (foundProject && foundProject !== currentProject) {
    syncTopbarTheme(foundProject);
}
```

## Why It Failed
When navigating to the "New Chat" page via SPA routing (without a full page refresh):
1. **Inline Style Wiping:** The React framework cleared the inline styles on `document.documentElement`, instantly deleting our custom CSS variables. Since the project name didn't officially change (or momentarily became a generic UI text), the `if` condition failed, and the variables were never re-injected.
2. **Selector Mismatch:** The CSS rules targeting the topbar relied heavily on the presence of chat-specific elements (like breadcrumbs or the "More Actions" button). On an empty "New Chat" page, these elements didn't exist, causing the CSS rules to completely detach from the topbar element.
3. **Generic UI Text Extraction:** The project name extractor inadvertently picked up "New Chat" from generic UI spans, causing the extension to fetch a theme color for a non-existent project named "New Chat", resulting in a fallback to transparent.

## What NOT To Do
1. **Don't assume inline styles are persistent in SPAs.** Always verify the presence of critical injected CSS variables during DOM mutations, not just state changes.
2. **Don't use overly restrictive CSS selectors for persistent UI elements.** Always include fallback anchors that are guaranteed to be present (e.g., static IDE launch buttons `[data-testid="install-editor"]`).
3. **Don't blindly trust text extraction in SPAs.** Always maintain a blacklist of known generic UI strings (e.g., "New Chat", "Untitled") when scraping state from the DOM.
