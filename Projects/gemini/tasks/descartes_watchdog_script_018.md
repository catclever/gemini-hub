---
id: descartes_watchdog_script_018
title: 新建 descartes_watchdog.sh（Descartes+EnginEdge 看门狗，替代 jules_watchdog.sh）
status: completed
priority: high
tags:
- descartes
- enginedge
- jules-replacement
session: conversation://bc3c9452-05a5-4ae7-b7fa-42fdc574e8e3
---

# 新建 descartes_watchdog.sh（Descartes+EnginEdge 看门狗，替代 jules_watchdog.sh）

## 任务目标与背景
在 ~/.gemini/config/scripts/ 新建 descartes_watchdog.sh。运行于 PVE：创建 git worktree 隔离 -> enginedge run -> 独立验证 -> 提交 -> 默认保留分支 descartes/<Task_ID>，--auto-merge 才 squash 合并。沿用 /tmp/<Task_ID>.signal 的 IN_PROGRESS/DONE/FAILED 契约。完整规格见 ~/.gemini/Projects/gemini/design/tentative/2026-11-02_descartes_watchdog_replace_jules.md。不修改 jules_watchdog.sh（并行期保留）。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
