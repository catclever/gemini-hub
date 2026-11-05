---
title: Fix Relative Center-Anchor Physics in TentaclesOverlay
status: completed
priority: high
tags:
- frontend
- physics
- tentacles
id: mainline_2_physics_fix
---
# Objective
Fix the `TentaclesOverlay.tsx` in `@agent-k/tentacles` so that it adheres to the Mainline 2 "Relative Center-Anchor Physics" architecture.

# Context
The math logic `LayoutResolver.ts` correctly translates `cx, cy` and `anchor` into absolute `x, y` for rendering. However, the visual editor layer (`TentaclesOverlay.tsx`) is blindly writing the absolute `x` and `y` back to the JSON config upon drag/resize completion via `onUpdate(targetId, { x, y })`. This breaks the relative anchoring system.

# Requirements
1. The drag and resize events in `TentaclesOverlay` must use reverse layout calculation to compute the relative `cx` and `cy` offset based on the component's `anchor` property.
2. Replace the direct `x, y` assignment to `onUpdate` with the computed `cx, cy`.

# References
- See `docs/relative-anchor-physics-plan.md`
- Check `core/src/framework/LayoutResolver.ts` for the reverse calculation logic (already implemented).
