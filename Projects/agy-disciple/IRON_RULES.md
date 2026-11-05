# agy-disciple Project Ironclad Rules (项目铁律)

This document is the Single Source of Truth (SSOT) for absolute, non-negotiable project ironclad rules governing all agent behaviors, delegation routing, and upstream synchronization for `agy-disciple`.

---

## [Global]

- **Project Environment**: Dual-Topology support (`standalone` local-first by default; `server-centralized` for remote compute hosts).
- **Default Dev Engine Rule (默认研发引擎铁律)**:
  - **默认始终调度 Native Dev / agy**：在开源版 `agy-disciple` 中，所有模式与技能默认必须优先调用本地或服务器的原生 `dev` / `agy` 智能体。确保开源用户零外部依赖、零门槛开箱即用。
  - **Jules 按需显式唤醒**：仅当用户在对话中**显式要求**使用 Jules 时（例如“*用 jules 跑*”、“*派发给 jules dev*”或“*利用 jules 云端额度*”），主架构师才允许切换至 Google Cloud Jules 流水线。
- **Upstream Migration & Sync Rule (上游迁移铁律)**:
  - **路径动态化**：从上游私有源 (`dev-team`) 迁移改动时，严禁带入本地私人绝对路径 (`/Users/kael`)、私有别名或人设称谓，必须参数化或中立化。
  - **默认引擎收敛**：若上游私有环境存在“自动/优先调度 Jules”的内部偏好，在迁移至开源版时**必须强制收敛为“默认 Native `dev` / `agy`，按需显式 Jules”**，严禁将 Jules 设为默认选项。
- **Strict Virtual Environments**: All Python environments must run under `uv` or isolated virtualenvs.

---

## [Main Agent]

- **Role & Boundary**: Lead Architect & Project Manager. Responsible for top-level system design, blueprint decomposition, knowledge base management, and DoD verification.
- **Draft Suffix Rule**: Dev sub-agents MUST generate drafts (`<basename>_task_<task_id>.<ext>`). Main agent reviews drafts and dispatches `merger` to backup original files (`.bak`) and swap drafts.
- **Engine Delegation Routing**:
  - Default: Dispatch to Native `dev` (`agents/dev.yaml`).
  - Opt-in: Dispatch to `jules-dev` ONLY upon explicit user request AND when the repository is hosted on GitHub with Jules authentication configured.
- **DoD Gatekeeper**: Must synchronize Kanban board via `kanban-task-manager` MCP before concluding any development turn.

---

## [Dev Agent]

- **Sandboxed Draft Isolation**: STRICTLY FORBIDDEN from modifying original production files directly; must create task-suffixed drafts.
- **No Metadata Tampering**: STRICTLY FORBIDDEN from creating, editing, or deleting files in `tasks/` or metadata directories.
- **Sandboxed Verification**: Run unit tests and syntax checks within the sandbox before declaring completion and suspending.

---

## [Ops Agent]

- **Execution Safety**: High-cost, non-idempotent scripts must be strictly verified against the command dictionary before execution.
- **Host Context**: Operate inside the verified virtual environment and target directory.
