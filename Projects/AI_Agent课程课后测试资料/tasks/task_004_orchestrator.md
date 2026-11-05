---
title: Implement Main Orchestrator and CLI Entry
status: completed
priority: high
tags:
- orchestrator
- agent
- cli
id: task_004_orchestrator
---
## Description
- Implement `src/agent/orchestrator.py`: Multi-stage deterministic agent loop (INIT -> INFO_GATHERING -> POLICY_MATCHING -> RISK_REVIEW -> APPROVAL_ROUTING -> ORDER_CREATION -> DONE/BLOCKED). Observation updates plan dynamically. Generates full execution trace.
- Implement `src/agent/prompts.py`: Prompt templates for policy analysis and reasoning justification.
- Implement `src/main.py`: Command-line interface supporting `--case-id`, `--resume`, `--eval`, `--reset`.
