---
title: Implement State Models and Checkpoint Persistence
status: completed
priority: high
tags:
- models
- state
- checkpoint
id: task_002_models_and_state
---
## Description
- Define Pydantic models for Case, Budget, Supplier, Approval, Order, State, Trace in `src/models/state.py` and `src/models/trace.py`.
- Implement `src/agent/state_manager.py` to handle state transitions, serialization, disk checkpointing (`data/checkpoints/<case_id>_state.json`), and loading for resume.
