# AgentK Iron Rules

## [Global]
- **Environment**: **PVE-Native**. All heavy development tasks MUST be delegated to PVE remote agents using the `pve-dispatch` skill.
- **Thin-Client Git**: The local Mac is a "Dumb Editor" mirrored to the PVE. Do NOT force initialize `git init` locally. All Git operations (status, commit, history) MUST be delegated exclusively to the remote PVE sub-agents.
- **Monorepo Setup**: This project uses `npm workspaces`. The workspaces are structured into `core`, `shoggoth`, `atoms`, `libs/*`, and `apps/*`.
- **Core Tech Stack**: React, Vite, Tailwind CSS.
- **Ghost Dependency Rule**: When modifying a local package (like `@agent-k/tentacles`), you must ensure its `package.json` exports correctly point to the built files, AND you must run its dev/watch script so the consumer app (e.g., `shoggoth`) receives the updated code. Otherwise, Vite HMR will load stale cached code.

## [Main Agent]
- Orchestrate tasks carefully across monorepo packages.
- Ensure that architectural blueprints respect the boundaries between `core`, `apps`, and `libs`.
- Wait for user approval before making major structural changes to the monorepo or creating new packages.

## [Dev Agent]
- **HMR Enforcement**: When developing a shared package, either run it in `--watch` mode or configure the consumer app's `vite.config.ts` `resolve.alias` to point to the package's `src/` directory.
- **Export Consistency**: Never change `vite.config.ts` build output names without synchronously updating the package's `package.json` `main`/`module`/`exports`.
- Only write code within the designated local folders.

## [Ops Agent]
- Use npm workspace commands for execution (e.g., `npm run dev -w @agent-k/shoggoth`).
- If you encounter unexplainable behavior where new code doesn't reflect, clear the `.vite/deps` cache or restart the dev server to break the cache.
