---
title: Implement Evaluation Suite and Failure Diagnosis
status: completed
priority: high
tags:
- eval
- diagnosis
- trace
id: task_005_eval_and_diagnosis
---
## Description
- Implement `eval/run_eval.py` to evaluate all 5 public cases, verifying:
  - CASE-001: Unverified memory handled, no excessive approvals, evidence traceable.
  - CASE-002: V3 active, EAST region rule applied, manager+finance approved, MEDIUM risk not invoking security agent.
  - CASE-003: HIGH risk triggers SecurityReviewAgent, handles input-required, reuses task_id, EAST manager approval.
  - CASE-004: Suspend -> admin budget change -> resume re-checks budget and blocks PO creation on version/amount mismatch.
  - CASE-005: Dual approval, handle write-then-timeout to UNKNOWN state, query PO before retry, idempotent single PO created.
- Produce `eval/eval_report.md` detailing end-to-end, trajectory, component results, latency, and tool calls.
- Produce `eval/diagnosis_report.md` analyzing `failure_trace.json`: First Divergence -> Root Cause -> Minimal Change Set -> Replay/Regression.
