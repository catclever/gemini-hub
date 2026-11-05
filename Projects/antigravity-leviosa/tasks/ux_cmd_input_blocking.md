---
title: 'Block input during heavy #cmd text insertion to prevent accidental submissions'
status: completed
priority: medium
tags:
- frontend
- UX
- bugfix
session: conversation://010580c3-7e18-49fc-bc23-0ee795bb8072
id: ux_cmd_input_blocking
---
# Issue Description
Even with the performance optimization for `#cmd` insertion, injecting large blocks of markdown into a rich-text editor (Lexical) inherently takes some synchronous processing time. During this fractional-second UI freeze, if the user continues typing or accidentally double-taps the `Enter` key, the browser queues these events. Once the main thread frees up, the queued events fire immediately, potentially causing double-submissions (sending the message prematurely) or scrambling the text.

# Resolution
Introduced an `isProcessing` lock in `web/kb_trigger.js`. 
- Added a global event interceptor (`blockEventsIfProcessing`) in the document's `capture` phase.
- When `insertRuleTag` is called, it immediately sets `isProcessing = true`.
- During this state, any `keydown`, `keyup`, `keypress`, or `click` events are swallowed completely (`preventDefault` and `stopImmediatePropagation`).
- After the insertion completes, a `setTimeout` of 100ms is used to clear the `isProcessing` flag. This pushes the unlock action to the end of the event queue, ensuring that all lingering queued keystrokes/clicks from the freeze period are safely caught and discarded by the interceptor.
