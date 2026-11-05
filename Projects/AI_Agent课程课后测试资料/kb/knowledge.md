# Project Knowledge Base Index

## 1. 核心架构与协议
- **状态机阶段**: `INIT` -> `INFO_GATHERING` -> `POLICY_MATCHING` -> `RISK_REVIEW` -> `APPROVAL_ROUTING` -> `ORDER_CREATION` -> `DONE` / `BLOCKED` / `FAILED`
- **契约定义**: 参照 `contracts/tool_contracts.json`
- **治理原则**: 运行时接管高危动作（`create_purchase_order`），阻断未审批、超预算、高风险或版本不一致操作。
- **超时治理**: `create_purchase_order` 抛出 `TimeoutError` 时，标记状态为 `UNKNOWN`，强制执行 `get_purchase_order` 确认远程是否落盘，禁止盲目重试。
- **A2A 协作**: `SecurityReviewAgent` 返回 `input-required` 时挂起并保留 `task_id`，补充材料（如 ISO27001）后沿用原 `task_id` 继续审查。
- **恢复与版本失效**: 中断恢复时重新获取预算与供应商风险，若版本变化且预算不足，终止流程并标记 `BLOCKED`。
