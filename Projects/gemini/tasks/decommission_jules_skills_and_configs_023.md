---
id: decommission_jules_skills_and_configs_023
title: 推送主分支并在新分支 chore/decommission-jules 中全面下线 Jules 技能与配置
status: active
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
