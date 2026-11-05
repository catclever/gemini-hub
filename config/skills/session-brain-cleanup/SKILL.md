---
name: session-brain-cleanup
description: Safely cleans up temporary scratch files, temp media, agent specs, and transient task logs from the current session's brain directory. Use this when the user asks to clean up the workspace, delete temporary files, or tidy up the current session.
---

# Session Brain Cleanup

This skill safely cleans temporary files, compiler caches, temporary media, and transient command logs from the current session's brain directory, without harming the core transcript (`.system_generated/logs/transcript.jsonl`) or user uploads (`.user_uploaded/`).

## Cleanup Modes

1. **Standard Safe Cleanup (Default)**:
   - Cleans `scratch/` (including nested compiler/runtime caches like `gocache`, `gotmp`).
   - Removes `.tempmediaStorage/` (temporary generated images).
   - Removes `.agents/` (in-session agent definition templates).
   - Clears background command logs in `.system_generated/tasks/*.log`.
   - **PRESERVES** user-facing markdown artifacts (`*.md`) and deliverables.
   - Run command:
     ```bash
     python3 /Users/kael/.gemini/config/skills/session-brain-cleanup/scripts/clean_session.py <your-conversation-id>
     ```

2. **Full Reset (`--all`)**:
   - Performs standard cleanup PLUS removes all root-level artifacts (`*.md`, `*.metadata.json`, etc.).
   - Use ONLY when the user explicitly requests to wipe/reset all artifacts and deliverables from the current session.
   - Run command:
     ```bash
     python3 /Users/kael/.gemini/config/skills/session-brain-cleanup/scripts/clean_session.py <your-conversation-id> --all
     ```

## Workflow
1. Obtain the current conversation ID from your `<user_information>` context.
2. Check user intent:
   - If the user asks for a routine tidy-up or cleaning temporary files, run default safe mode.
   - If the user explicitly asks for a complete reset or to delete all session artifacts, pass `--all`.
3. Execute the script via `run_command`.
4. Report a concise summary of what was cleaned and what was preserved to the user.
