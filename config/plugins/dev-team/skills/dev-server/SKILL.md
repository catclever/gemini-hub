---
name: dev-server
description: SOP for managing and launching the project's dev servers, preview environments, or background runtime services across Mac and PVE.
---
# Dev Server & Runtime Services Protocol

This skill dictates the standard operating procedure for launching dev servers, preview environments, or background runtime services for a project.

## Environment-Specific Rules

### 1. On Mac (Local)
- **Rule**: **Manual Start Only**. Do NOT automatically start the dev server during normal development workflows.
- **Action**: You must wait for the user to explicitly ask you to start it (e.g., "打开测试环境", "启动 dev server", "运行预览服务"). Otherwise, assume the user prefers to run it manually in their own terminal.

### 2. On PVE (Remote / Autonomous)
- **Rule**: **Automatic Start via Antiverse**. When handing off tasks to PVE or operating autonomously on PVE, the dev server/preview environment should be started automatically to support the remote working subagents.
- **CRITICAL Network Binding**: When starting any dev server (like Vite, Next.js, Uvicorn, Django, etc.) on PVE, you MUST pass the appropriate flag to bind it to `0.0.0.0` (e.g., `--host 0.0.0.0`, `--bind 0.0.0.0`). This is mandatory so the user can access the preview from their local Mac browser!
- **Action**: Spawn the dev server as a dedicated, isolated Zellij session via `antiverse-run`.
- **Execution Command**:
  Use the `run_command` tool (via SSH if dispatching from Mac, or directly if already on PVE) to launch the dev server in its own dedicated session:
  
  ```bash
  ssh Antigravity "antiverse-run --name '[<project_name>] env' --cwd <project_dir> --force -- <your_start_command>"
  ```
  *(Replace `<your_start_command>` with the project-specific command, e.g., `uvicorn main:app --host 0.0.0.0`, `npm run dev -- --host 0.0.0.0`, etc. `antiverse-run` handles dedicated session creation, dual-logging, keeps the interactive shell alive even if the service stops, and enables quick access via `antiverse a env` or `Alt + s`.)*

## Monitoring & Management
- **List Sessions**: Check running services via `ssh Antigravity "antiverse ls"`.
- **Inspect Logs / Console**: Attach to the service via `ssh Antigravity -t "antiverse a env"` (or switch to it from any session using `Alt + s`).
- **Stop Service**: `ssh Antigravity "antiverse kill env"`.

## Coordination with Night Shift
When executing the `night-shift` handoff, the Main Agent should ensure that the PVE dev server tab is spun up inside the `Antiverse` session so that the autonomous `dev` agents have a live environment to hit if needed.
