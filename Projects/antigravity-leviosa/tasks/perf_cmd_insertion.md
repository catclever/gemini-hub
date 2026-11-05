---
title: 'Optimize #cmd text insertion performance'
status: completed
priority: medium
tags:
- frontend
- performance
- bugfix
session: conversation://010580c3-7e18-49fc-bc23-0ee795bb8072
id: perf_cmd_insertion
---
# Issue Description
The user reported that inserting the `#cmd` instruction felt slow and laggy. 

# Root Cause
In `web/kb_trigger.js`, the `insertRuleTag` function was removing the trigger text (e.g., `#cmd `) by calling `document.execCommand('delete', false, null)` inside a `for` loop, iterating for the length of the trigger text (e.g., 5-6 times). Because the underlying rich-text editor (Lexical/React) intercepts these native `input` events, it resulted in 5-6 consecutive, full re-render cycles of the editor component before the new text was finally inserted. This triggered noticeable main-thread blocking and UI lag.

# Resolution
Updated `insertRuleTag` to utilize the native Selection API (`window.getSelection().modify('extend', 'backward', 'character')`). We now iteratively extend the selection backwards by the length of the matched trigger string, and then execute a single `document.execCommand('delete', false, null)` to remove it in one go. This reduces the DOM update and React reconciliation cycle from N times to exactly 1 time, drastically improving the insertion speed and eliminating the lag.
