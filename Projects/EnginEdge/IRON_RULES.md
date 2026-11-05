# EnginEdge Ironclad Rules

## [Global]
> **Environment**: **PVE-Native**. All heavy development tasks MUST be delegated to PVE remote agents using the `pve-dispatch` skill.
> **Thin-Client Git**: The local Mac is a "Dumb Editor" mirrored to the PVE. Do NOT force initialize `git init` locally. All Git operations (status, commit, history) MUST be delegated exclusively to the remote PVE sub-agents.

- **Project Core**: Native edge execution engine and Model Context Protocol (MCP) server for the Descartes & Dalembert ecosystem.
- **Language & Runtime**: Pure Rust (Edition 2021+), Tokio async runtime.
- **Remote Host & Repo**: Antigravity PVE server (`/root/Projects/EnginEdge`), GitHub (`git@github.com:catclever/EnginEdge.git`).
- **MCP Output Hygiene**: MCP JSON-RPC 2.0 frames run exclusively on `stdout`. Internal logs, tracing, and diagnostic output MUST strictly route to `stderr`.

## [Main Agent]
- Act as Lead Architect & Project Manager.
- Maintain centralized project materials in `~/.gemini/Projects/EnginEdge/`.
- Manage all tasks via `kanban-task-manager` MCP.
- Dispatch heavy development tasks via `pve-dispatch` (Mode A: Google Jules Watchdog for GitHub PRs, or Mode B: Bifrost PVE `agy` for remote terminal execution).

## [Dev Agent]
- Develop exclusively in Rust with zero-warning compilations (`cargo check`, `cargo clippy`).
- Tree-sitter AST queries must be strictly validated; never rely on line-number arithmetic.
- Enforce Anti-Leak Security Jail: All file access must be strictly scoped to `$PWD`. Absolute path escapes or `../` traversals must be rejected. Block sensitive files (`.env*`, `id_rsa*`, `*.pem`, `*.key`, `~/.ssh`).

## [Ops Agent]
- Execute remote verification on PVE (`cargo test`, `cargo build --release`).
- Manage remote Git commits and pushes on PVE.
