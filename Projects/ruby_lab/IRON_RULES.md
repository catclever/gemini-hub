## [Global]
**Environment**: **PVE-Native**. All heavy development tasks MUST be delegated to PVE remote agents using the `pve-dispatch` skill.
**Thin-Client Git**: The local Mac is a "Dumb Editor" mirrored to the PVE. Do NOT force initialize `git init` locally at the root level. All Git operations (status, commit, history) MUST be delegated exclusively to the remote PVE sub-agents.
**Multi-Repo Architecture**: The root `ruby_lab` directory is a container. Each sub-project (like `amber`, `ruby_llm`, etc.) MUST remain an independent git repository. Do NOT initialize a git repo in the root folder. Maintain this logic for all future sub-projects.

## [Main Agent]
- After local verification, you must trigger ops to sync.

## [Dev Agent]
- Only write code to the local folder.

## [Ops Agent]
- Use appropriate PVE commands.
