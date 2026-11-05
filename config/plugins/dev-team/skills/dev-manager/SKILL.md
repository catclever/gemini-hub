---
name: dev-manager
description: "SOP for delegating tasks to LOCAL sub-agents. Use this for standard Mac projects. Do NOT use for PVE-Native projects."
---
# Dev Manager SOP

This skill defines how the Lead Architect (Main Agent) should orchestrate its sub-agents for coding tasks. 

## Host Boundary & Invocation Standard
> [!CRITICAL]
> **Native Subagent Only**: When delegating tasks on the local Mac (inside the Antigravity client), you MUST exclusively use the native `invoke_subagent` tool to spawn subagents directly in the IDE conversation tree. You are **STRICTLY FORBIDDEN** from running the CLI command `agy` in the local terminal.

## Available Sub-Agents (Located in `agents/`)

### 1. The `dev` Agent
- **Role**: Writes code, fixes bugs, and performs sandboxed verification.
- **Completion Condition**: The `dev` agent is ONLY considered completed AFTER the user has manually tested and explicitly accepted the code changes. Until then, it stays suspended (idle), waiting for you to relay user feedback for further fixes.
- **Invocation Rules**:
  - Pass the `Task ID` in the invocation prompt.
  - Read `~/.gemini/Projects/<project_name>/IRON_RULES.md`. Extract ONLY the `[Global]` and `[Dev Agent]` sections and append them to the `dev` agent's prompt to prevent context pollution.
  - **Knowledge Synthesis & Reading Guidance**: Search `~/.gemini/Projects/<project_name>/kb/knowledge.md` for relevant conventions, schemas, or gotchas. Synthesize them into customized, concrete task requirements (NEVER blindly paste raw markdown documents into the prompt). Explicitly provide the specific paths to the relevant `kb/` documents that the `dev` agent can read for deep context.
  - Inform the `dev` agent of the files it needs to read. Remind it of the suffix rule (`_task_name`) for draft files.
  - **Boundary Restriction**: Explicitly instruct the `dev` agent that it is STRICTLY FORBIDDEN from modifying any task files or metadata in `~/.gemini/Projects/<project_name>/tasks/`. All task state updates must be handled by you (the Main Agent).

### 2. The `merger` Agent
- **Role**: Replaces original source files with the development drafts.
- **Completion Condition**: The `merger` agent is considered completed the moment it successfully finishes backing up and renaming the files. It requires no user verification.
- **Invocation Rules**:
  - Invoke ONLY after the `dev` agent has successfully reported its draft files.
  - Pass the exact mapping of draft files to original files (e.g., "Replace `api.py` with `api_task_001.py`").
  - Instruct the `merger` agent to backup the original files (e.g., `api.bak.py`) before overwriting.

## Delegation Lifecycle

0. **Prerequisite & Pre-Dispatch GC [节点 A]**:
   - You MUST NOT invoke a `dev` agent unless you have already executed the `task-breakdown` skill and created the task in Kanban via MCP.
   - **Silent GC Before Dispatch**: Prior to invoking a new sub-agent, silently check the session tree (`manage_subagents`) and background tasks (`manage_task`). Silently kill any previously closed/completed sub-agents and purge finished zombie tasks to keep the context clean.
1. **Assign**: Main Agent reads the task and invokes the `dev` agent, passing the `Task ID`.
2. **Suspend & Review**: The `dev` agent finishes drafting and suspends itself (goes idle). The Main Agent reviews the results.
3. **Merge (Draft)**: The Main Agent invokes the `merger` agent to apply the drafts. Once merged, the `merger` agent is immediately **killed**.
4. **User Verification & Post-Acceptance Silent GC [节点 B]**: The Main Agent asks the user to manually verify the changes. 
   - *If rework is needed*: Wake up the suspended `dev` agent by sending it a message with the feedback. Repeat from step 2.
   - *If verified*: The task is complete. Mark the Kanban task status as `completed` via MCP, and **immediately and silently kill** the `dev` agent. If multiple agents ran or local scratch files piled up, optionally trigger `python3 ~/.gemini/config/scripts/clean_subagents.py --session <current_conversation_id> --min-age-hours 24 --quiet` silently.
