---
id: decommission_jules_skills_and_configs_023
title: 推送主分支并在新分支 chore/decommission-jules 中全面下线 Jules 技能与配置
status: completed
priority: high
tags:
- git
- jules
- decommission
- skills
session: conversation://045a52ed-f25c-47fb-8b86-58968f6af6db
---

# 推送主分支并在新分支 chore/decommission-jules 中全面下线 Jules 技能与配置

## 任务目标与背景
1. 将当前 main 分支（含标准知识管理 MCP 服务端与技能更新）提交并推送至 catclever/gemini-hub；
2. 校验工作区干净后，切出新分支 chore/decommission-jules；
3. 在新分支中全面下线 Google Jules 相关脚本（config/scripts/jules_watchdog.sh）、技能分支（pve-dispatch、night-shift、descartes-dispatch）以及配置文件与各项目 IRON_RULES.md 中的 Jules 残留引用。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1

- `ops` 子代理已将 `main` 分支提交（Commit `3668978`），等待推送确认。
- `dev` 子代理已完成全部 8 个 Jules 下线草案文件编写与沙箱验证（`pve-dispatch`、`night-shift`、`descartes-dispatch`、`descartes_watchdog.sh`、`config.json`、`EnginEdge`/`HollyShit`/`agy-disciple` 的 `IRON_RULES.md`），确认 0 处 `jules` 残留且语法 100% 合法。
- 等待公主唤醒后由 `ops` 一次性执行：推送 `main` -> 切出 `chore/decommission-jules` 分支 -> 合并 8 个草案并删除 `config/scripts/jules_watchdog.sh`。

- `main` 分支（Commit `3668978`）已成功推送至 `catclever/gemini-hub`。
- 已切出新分支 `chore/decommission-jules`（Commit `600db2f`）并推送至远端 `origin/chore/decommission-jules`。
- 物理移除 `config/scripts/jules_watchdog.sh`，完成 `pve-dispatch`、`night-shift`、`descartes-dispatch`、`descartes_watchdog.sh`、`config.json` 及 `EnginEdge`/`HollyShit`/`agy-disciple` 项目 `IRON_RULES.md` 的全量去 Jules 化重构，索引扫描确认 0 残留。
