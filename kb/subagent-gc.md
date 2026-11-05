---
name: subagent-gc
description: "全局知识库与指令：子代理与后台任务的机会式两节点静默清理机制 (Opportunistic Silent GC)"
---

# 机会式生命周期与静默清理机制 (Opportunistic Silent GC)
#cmd /subagent-gc

<system_instruction>
本知识库定义了 Antigravity 系统中主 Agent 对子代理（Subagent）及后台运行任务（Background Tasks）的生命周期管理与垃圾回收（GC）规范。

## 一、 核心目标与哲学

1. **会话树与资源防膨胀**：避免长时间运行中挂起（idle）的过期子代理占用会话树资源，防止已结束的后台进程（zombie tasks）堆积，定期回收磁盘孤儿目录（`~/.gemini/antigravity/brain/`）。
2. **静默执行原则 (Silent Execution)**：常规开发过程中，清理操作全程在后台**静默**执行，禁止向用户汇报琐碎的扫描与 kill 过程，保持会话流清爽专注。
3. **返工留存安全线 (Retention & Wakeup)**：子代理在完成 draft 等待用户手动验证期间，必须保持挂起（idle），严禁过早 kill；只有当用户明确验收通过或已进入下一独立任务时，才视为已闭环。

---

## 二、 三层触发场景与执行矩阵 (Trigger Matrix)

系统严格按照以下三层梯次执行清理，兼顾日常安全性、手动干预度与全局大扫除需求：

| 触发场景 | 清理作用域 | 时间阈值 | 执行反馈 | 对应执行命令 |
| :--- | :--- | :--- | :--- | :--- |
| **1. 任何自动触发**<br/>(节点 A 派发前 / 节点 B 验收闭环) | **仅当前会话** | **24 小时以上**<br/>(只清陈旧孤儿，不动当日) | **完全静默**<br/>(无终端赘述) | `python3 ~/.gemini/config/scripts/clean_subagents.py --session <当前ConversationID> --min-age-hours 24 --quiet` |
| **2. 当前会话手动注入 cmd**<br/>(通过 Cmd+G / 输入 `/subagent-gc`) | **仅当前会话** | **1 小时以上**<br/>(清理已交付完成的子代理) | **显式汇报**<br/>(一句话简述) | `python3 ~/.gemini/config/scripts/clean_subagents.py --session <当前ConversationID> --min-age-hours 1` |
| **3. 历史会话面板触发**<br/>(在历史面板/全域维护时调用) | **所有会话** | **1 小时以上**<br/>(保护 1 小时内任何活跃会话) | **显式汇报**<br/>(全域清理报告) | `python3 ~/.gemini/config/scripts/clean_subagents.py --all-sessions --min-age-hours 1` |

---

## 三、 两大自动触发节点细则 (Automatic Opportunistic Nodes)

日常开发中，任何自动触发**严格遵循梯次 1（当前会话 + 24小时以上 + 完全静默）**：

### 【节点 A · 派发前检查 (Pre-Dispatch GC)】
- **触发时机**：主 Agent 在准备调用 `invoke_subagent` 派发任何新任务之前。
- **执行动作**：
  1. 调用 `manage_subagents(Action='list')` 快速巡检当前会话树；
  2. 若存在先前任务已确认交付、且不再需要返工的旧子代理，对其调用 `manage_subagents(Action='kill', ConversationIds=[...])`；
  3. 调用 `manage_task(Action='list')`，清理已退出的临时后台任务；
  4. 静默执行当前会话 24h+ 孤儿清理：
     ```bash
     python3 ~/.gemini/config/scripts/clean_subagents.py --session <当前ConversationID> --min-age-hours 24 --quiet
     ```

### 【节点 B · 验收闭环时 (Post-Acceptance GC)】
- **触发时机**：当用户明确确认代码或功能无误、Kanban 看板任务状态置为 `completed` 的当下。
- **执行动作**：
  1. 立即静默 kill 该任务所绑定的 `dev` / `research` 子代理；
  2. 静默执行当前会话 24h+ 孤儿清理：
     ```bash
     python3 ~/.gemini/config/scripts/clean_subagents.py --session <当前ConversationID> --min-age-hours 24 --quiet
     ```

---

## 四、 清理执行清单与安全边界

| 对象 | 清理方式 | 安全边界 |
| :--- | :--- | :--- |
| **会话树子代理** | `manage_subagents(Action='kill', ConversationIds=[...])` | 仅 kill 明确已闭环的旧 agent；等待验证中的禁止 kill |
| **后台运行任务** | `manage_task(Action='kill', TaskId=...)` | 仅清理已退出（done/error）的临时任务；running/daemon 任务严禁中断 |
| **磁盘脑区孤儿** | `python3 ~/.gemini/config/scripts/clean_subagents.py` | 严格按照三层矩阵设定 `--session` 与 `--min-age-hours` |
| **临时编译与日志** | `python3 ~/.gemini/config/skills/session-brain-cleanup/scripts/clean_session.py $ID` | 仅清理 scratch/tmp，严禁误删 `*.md` 产物 |

---

## 五、 手动触发模式细则 (Manual Trigger Details)

### 1. 当前会话手动注入 (`#cmd /subagent-gc` 或 Cmd+G)
- **行为**：用户希望清理当前会话中 1 小时以前完成的子代理与产物；
- **执行**：
  ```bash
  python3 ~/.gemini/config/scripts/clean_subagents.py --session <当前ConversationID> --min-age-hours 1
  ```
- **反馈**：执行完毕后，向用户简短汇报（例如：`✓ 已安全清理当前会话 1 小时前的 N 个已闭环子代理，释放空间 X MB。`）。

### 2. 注入历史会话面板触发 (History Sessions Panel Trigger)
- **行为**：在历史会话面板或全域维护模式下被唤起；
- **执行**：
  ```bash
  python3 ~/.gemini/config/scripts/clean_subagents.py --all-sessions --min-age-hours 1
  ```
- **反馈**：执行完毕后，向用户汇报全域清理成果（例如：`✓ 历史面板全域巡检完成，已清理所有会话中 1 小时以上的陈旧子代理与孤儿目录，共释放空间 X MB。`）。
</system_instruction>
