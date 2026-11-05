# IRON RULES - 采购审批与供应商尽调 Agent

## [Global]
> **Environment**: **PVE-Native**. All development and execution run on the PVE server.
> **Authoritative Git**: Git repository is at `/root/workspace/AI_Agent课程课后测试资料`. All changes must be tracked with clear commit messages.
> **Python Environment**: Python 3.13 with `uv` virtual environment.

### 核心业务铁律
1. **严格依据有效制度**：制度生效时间必须覆盖申请日期（2026-09-21）。V2 已废止不可用；V3 为现行制度（全区适用）；V4 为未来生效（不可作为现行依据）；华东区域额外遵循 E-2026-08 补充通知。
2. **审批门槛铁律**：金额 > 50,000 元时，必须同时取得 manager 和 finance 双审批；华东区域金额 > 30,000 元且供应商风险为 MEDIUM/HIGH 时，额外要求 manager 审批。
3. **高风险供应商 A2A**：`supplier_risk == HIGH` 时必须通过 SecurityReviewAgent 进行独立安全审查。若返回 `input-required`，必须保存原 `task_id`，补全材料后使用同一任务继续，不得视为完成。
4. **副作用治理与超时幂等**：`create_purchase_order` 为副作用写操作。遇到超时 (TimeoutError) 状态记为 `UNKNOWN`，禁止直接盲目重试；必须先调用 `get_purchase_order` 检查业务真实状态。
5. **恢复与版本一致性**：任务中断恢复时，必须重新拉取外部对象（如预算）并比对版本；若版本漂移且预算不足，旧判断直接失效并终止/阻断建单。
6. **可信内存**：`memory.jsonl` 中 `unverified` 仅作线索，不得作为既成事实，更不得覆盖实时工具结果。

## [Main Agent]
1. 负责架构把控、流程调度、文档编写与产物交付。
2. 保持全局状态机的严肃性，所有关键状态变化必须落盘（Checkpoints）。
3. 阶段性完成代码后执行 Git 提交。

## [Dev Agent]
1. 严格按照 `架构设计与实现计划.md` 中的模块划分编写代码。
2. 模块必须解耦：`models`（数据结构）、`core`（制度/内存/A2A）、`tools`（治理与包装）、`agent`（主调度与状态机）。
3. 单元测试与评测脚本覆盖 5 个公开 Case 和 failure trace 诊断。

## [Ops Agent]
1. 运行 `reset_runtime.py`、`admin_simulator.py` 等脚本。
2. 运行 `eval/run_eval.py` 批量验证。
