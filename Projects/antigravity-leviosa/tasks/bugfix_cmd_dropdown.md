---
title: 'Fix #cmd autocomplete dropdown positioning and hide logic'
status: completed
priority: medium
tags:
- frontend
- ui
- bugfix
session: conversation://010580c3-7e18-49fc-bc23-0ee795bb8072
id: bugfix_cmd_dropdown
---
# Issue Description
1. The #cmd knowledge trigger autocomplete menu was always dropping down statically because the initial tailwind classes (`-top-2 -translate-y-full`) were sometimes purged or overriden by layout constraints.
2. The menu remained open if the user continued typing after the `#cmd ` trigger (e.g. if the user typed `#cmd something else`).

# Resolution
1. **Dynamic positioning**: Replaced static layout classes with dynamic javascript inline styles in `showMenu()`. If the input element is in the lower half of the viewport, it explicitly sets `bottom: 100%` and `marginBottom: 8px` to pop the menu upwards. If in the upper half (like a new session), it explicitly sets `top: 100%` and `marginTop: 8px` to drop the menu downwards.
2. **Auto-hide logic**: Updated the `keyup` event handler so that if `matchScope` is false, it explicitly hides the menu. This ensures the menu is cleanly closed when the input no longer matches the autocomplete trigger.

Fixed in `web/kb_trigger.js`.
