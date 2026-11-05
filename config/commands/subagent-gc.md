---
name: subagent-gc
description: "全局指令：手动触发子代理与任务垃圾回收，释放会话资源与磁盘空间。"
---

# Command: /subagent-gc

## 功能说明
当用户输入 `/subagent-gc` 或要求清理过期子代理和任务时触发。该指令会立即对当前会话的子代理状态、后台任务列表以及脑区磁盘空间进行全量巡检并执行安全清理。

## 执行 SOP

1. **会话子代理清理**
   - 检查 `manage_subagents(Action='list')`，对已完成任务且无挂起依赖的子代理执行 `kill`。

2. **后台任务清理**
   - 检查 `manage_task(Action='list')`，对已退出（done/cancelled/error）的临时任务执行清理。

3. **脑区磁盘孤儿回收**
   - **默认（当前会话手动触发）**：清理当前会话 1 小时以上的陈旧子代理：
   ```bash
   python3 ~/.gemini/config/scripts/clean_subagents.py --session <current_conversation_id> --min-age-hours 1
   ```
   - **历史会话面板触发 / 传参 `--all` 时**：清理所有会话 1 小时以上的陈旧子代理：
   ```bash
   python3 ~/.gemini/config/scripts/clean_subagents.py --all-sessions --min-age-hours 1
   ```

4. **汇报结果**
   - 向用户汇报清理的子代理数量、任务数量以及释放的磁盘存储大小。
