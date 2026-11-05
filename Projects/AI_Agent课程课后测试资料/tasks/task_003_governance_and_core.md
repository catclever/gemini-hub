---
title: Implement Runtime Governance, Tool Wrappers and Core Engines
status: completed
priority: high
tags:
- governance
- tools
- policy
- a2a
- memory
id: task_003_governance_and_core
---
## Description
- Implement `src/tools/governance.py`: Runtime interceptor for side-effects, enforcing manager/finance approval rules, budget checks, risk status checks, and UNKNOWN timeout recovery with `get_purchase_order`.
- Implement `src/tools/wrappers.py` and `src/tools/registry.py`: Wrap `mock_services.py` and expose typed tools.
- Implement `src/core/policy_engine.py`: Date and region-based policy selection (V2 expired, V3 active, V4 future, EAST notice).
- Implement `src/core/a2a_manager.py`: Minimal context delegation to `SecurityReviewAgent`, handle `input-required`, supplement attachment handling, artifact verification.
- Implement `src/core/memory_manager.py`: Parse `memory.jsonl`, separate confirmed vs unverified facts, enforce tool override for unverified clues.
