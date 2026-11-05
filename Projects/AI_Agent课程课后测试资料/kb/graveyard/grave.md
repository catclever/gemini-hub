# Negative Knowledge Base (The Graveyard)

1. **Anti-Pattern 1: Trusting Natural Language "Done"**: 不要仅凭大模型自然语言自称“已完成”就退出，必须由运行时校验状态、审批记录与业务后置条件。
2. **Anti-Pattern 2: Blind Retry on Timeout**: 远端写操作（`create_purchase_order`）超时并不代表失败，可能服务端已落盘。盲目重试会导致生成重复订单（Duplicate POs）。
3. **Anti-Pattern 3: Promoting Unverified Clues to Ground Truth**: `memory.jsonl` 中的 `unverified` 线索不能直接当作事实覆盖实时 API 返回。
4. **Anti-Pattern 4: Ignoring Object Version Drift on Resume**: 任务恢复时若不重新拉取外部状态版本，会导致基于陈旧预算/风险通过非法的采购订单。
5. **Anti-Pattern 5: Creating New Task for Input-Required A2A**: 协作者请求输入时，若新建全新 task_id 会导致上下文丢失和审计断裂。
