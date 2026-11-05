---
title: Sync canvas property in shoggoth handleUpdate
status: completed
priority: medium
tags:
- shoggoth
- tentacles
- state
id: fix_shoggoth_canvas_sync_004
---
# Objective
Ensure `shoggoth/src/App.tsx` properly synchronizes the `canvas` property in React state `components` when `handleUpdate` is invoked from `TentaclesOverlay`.

# Context & Issues
When `TentaclesOverlay` triggers `onUpdate(targetId, { cx, cy })`, `handleUpdate` merges `updates` directly into `c` in the state array, but does not synchronize `c.canvas = { ...c.canvas, ...updates }`.
Consequently, downstream components or helpers reading `c.canvas` continue reading stale values from initial load.

# Requirements
1. In `shoggoth/src/App.tsx`, inside `handleUpdate`:
   When updating component `c`, ensure that `c.canvas` is also updated:
   ```ts
   const updated = { ...c, ...updates };
   updated.canvas = {
     ...(updated.canvas || {}),
     ...updates
   };
   ```
2. Verify that `shoggoth` builds cleanly (`npm run build -w @agent-k/shoggoth`).
3. When finished, update status in this file to `ready_for_review`.
