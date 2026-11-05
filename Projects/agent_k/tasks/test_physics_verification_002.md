---
title: Verify Relative Center-Anchor Physics & Add LayoutResolver Tests
status: completed
priority: high
tags:
- core
- physics
- testing
- tentacles
id: test_physics_verification_002
---
# Objective
Verify that the "Relative Center-Anchor Physics" implemented for Mainline 2 (`LayoutResolver.ts` and `TentaclesOverlay.tsx`) functions correctly, and establish automated unit tests in `@agent-k/core`.

# Context & Issues
1. `tests/hooks.test.tsx` in `core` fails because `@testing-library/dom` is missing from devDependencies.
2. `core/src/framework/LayoutResolver.ts` currently only checks `comp.canvas?.cx` and `comp.canvas?.anchor`. If an application or overlay passes components with flattened properties (`comp.cx`, `comp.anchor`), it falls back to 0 or fails to resolve relative anchors.
3. There are currently no unit tests verifying `resolveAbsoluteLayout` and `inverseKinematics`.

# Requirements
1. In `core/package.json`, ensure `@testing-library/dom` is installed / added to devDependencies.
2. Update `core/src/framework/LayoutResolver.ts`:
   - In `resolveAbsoluteLayout`, gracefully support both `comp.canvas?.cx` and `(comp as any).cx`, `comp.canvas?.anchor` and `(comp as any).anchor`, `comp.canvas?.width` and `(comp as any).width`, etc.
   - In `inverseKinematics`, similarly support both nested `comp.canvas` and root-level fallback.
3. Create `core/tests/LayoutResolver.test.ts` covering:
   - Basic single component resolution (`cx, cy` -> `abs_cx, abs_cy, x, y`).
   - Anchored component offset calculation (B relative to A).
   - Multi-level chained anchors (C anchored to B, B anchored to A).
   - Circular anchor dependency fallback.
   - `inverseKinematics`: dragging an anchored component produces the correct relative `cx, cy` offset.
   - Flattened component format compatibility.
4. Run `npm test -w @agent-k/core -- --run` and ensure all tests pass.
5. Run `npm run build -w @agent-k/core` to ensure production bundle compiles cleanly.
6. When finished, update status in this file to `ready_for_review`.
