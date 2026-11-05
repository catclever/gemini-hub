## [Global]
- **Environment**: **PVE-Native**. All heavy development tasks MUST be delegated to PVE remote agents using the `pve-dispatch` skill.
- **Thin-Client Git**: The local Mac is a "Dumb Editor" mirrored to the PVE. Do NOT force initialize `git init` locally. All Git operations (status, commit, history) MUST be delegated exclusively to the remote PVE sub-agents.
- **Service Deployment & Ports**:
  - All runtime services MUST be started exclusively on the remote PVE server (`Antigravity`).
  - All services MUST listen on `0.0.0.0` to permit remote access across the local network.
  - **Botanist Studio (造物审查终端)**: Port `18087` (`tools/botanist_studio.py`).
  - **Psy Garden Web (前端预览服务)**: Port `18088` (served via `src/` directory).
  - **Unified Single-Tab Launch**: Both services MUST be launched together using the root script `./start_services.sh` within a single dedicated tab in the PVE `Antiverse` (Zellij) session:
    ```bash
    ssh Antigravity "cd /root/Projects/psy_garden && zellij --session Antiverse action new-tab -n '[psy_garden] env' -- bash -c './start_services.sh; echo \"Services Stopped\"; sleep 86400'"
    ```

## [Main Agent]
- Orchestrate project lifecycle, manage centralized metadata in `~/.gemini/Projects/psy_garden/`.
- Do not execute long-running services or heavy builds on the local Mac. Delegate remote execution to sub-agents via `pve-dispatch` or `ops-manager`.
- Local Mac remains the primary editor; files are synced bidirectionally via Mutagen.

## [Dev Agent]
- All code writing and debugging intended for runtime verification must take place in the PVE Linux environment.
- Respect the assigned non-standard ports (18087, 18088) and `0.0.0.0` binding.

## [Ops Agent]
- When launching services on PVE, use the single-tab unified script:
  `cd /root/Projects/psy_garden && zellij --session Antiverse action new-tab -n '[psy_garden] env' -- bash -c './start_services.sh; echo "Services Stopped"; sleep 86400'`
- Remote Git operations (commit, tag, push) must be executed strictly on the PVE host.
