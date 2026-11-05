# AgentK Knowledge Base Index

## Architecture
- **Monorepo Structure**: Managed via `npm workspaces` (`core`, `shoggoth`, `atoms`, `libs/*`, `apps/*`).
- **Tech Stack**: React, Vite, Tailwind CSS.
- **Remote Environment**: PVE (`Antigravity:/root/Projects/agent_k`), synced via declarative Mutagen (`mutagen.yml`). Symlink `/root/workspace/agent_k` preserved for backward compatibility.

## Guides & Gotchas
- [Monorepo Vite HMR & Ghost Dependencies](./knowledge_monorepo_vite_hmr.md) - Explains the pitfalls of Vite dev server loading stale code from linked packages and how to fix it via exports syncing or watch-mode compilation.
- [Relative Center-Anchor Physics & LayoutResolver](./knowledge_relative_center_anchor_physics.md) - Architectural specification for relative center-anchor coordinates, topological layout resolution, and inverse kinematics editor updates.

## Active Schemas & Specs
- `CanvasPropsSchema`: `{ cx, cy, anchor, width, height, rotation, zIndex, scale, opacity }` in `@agent-k/core/src/schema/app_spec.ts`
