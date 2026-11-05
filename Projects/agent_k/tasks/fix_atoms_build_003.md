---
title: Fix TypeScript build errors in @agent-k/atoms
status: completed
priority: high
tags:
- atoms
- typescript
- build
id: fix_atoms_build_003
---
# Objective
Fix the TypeScript compilation errors in `@agent-k/atoms` so that `npm run build -w @agent-k/atoms` succeeds cleanly.

# Errors Identified
1. `src/canvas/CanvasEngine.tsx:27:48`:
   `Property 'initialTarget' does not exist on type 'Omit<FullGestureState<"drag">, "event"> & { event: PointerEvent | MouseEvent | TouchEvent | KeyboardEvent; }'.`
   Fix: In `@use-gesture/react`, inspect `event?.target` (e.g. `(event?.target as HTMLElement)?.closest?.('[data-agent-k-id]')`).
2. `src/canvas/DraggableNode.tsx:51:36`:
   `'prev' is declared but its value is never read.`
   Fix: Prefix with underscore `_prev` or omit parameter in `() => ({ ... })`.

# Requirements
1. Fix the typing errors in `atoms/src/canvas/CanvasEngine.tsx` and `atoms/src/canvas/DraggableNode.tsx`.
2. Run `npm run build -w @agent-k/atoms` to confirm clean build with zero TypeScript errors.
3. When finished, update status in this file to `ready_for_review`.
