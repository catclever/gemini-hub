---
title: Sub-Agent BypassSandbox Prompt Timeout Gotcha
description: Interactive BypassSandbox permission prompts inside sub-agents do not
  surface on the main chat tab and time out after 60s; run interactive host approvals
  in Main Agent.
date: '2026-11-06'
---

# Sub-Agent Unsandboxed Permission Prompt Visibility Gotcha

## 1. Context & Problem Attempted
Delegated `git push` and file move operations requiring `BypassSandbox: true` (`run_command` outside sandbox) to `ops` / `merger` sub-agents while the user was viewing the parent (Main Agent) conversation tab.

## 2. What Failed & Why
The `run_command(BypassSandbox: true)` permission approval dialog triggered inside a sub-agent is scoped to that sub-agent's own conversation view and does not reliably surface in the user's active parent conversation window, causing a 60-second permission timeout.

## 3. Strict Rule (What NOT to Do)
- **DO NOT** rely on background sub-agents to trigger interactive `BypassSandbox: true` permission prompts when the user is watching the main conversation tab.
- Have sub-agents use native file tools (`write_file` / `edit_file`) or sandboxed commands in their scratch/workspace directories, and execute any final host-level command requiring interactive `BypassSandbox: true` user approval directly from the Main Agent after sub-agent drafts are verified.
