---
id: fix_preview_readme_save_and_raw_mode_limitation_056
title: 修复带有预览的Readme面板保存未生效及Raw模式限制问题
status: completed
priority: high
tags:
- file-editor
- bugfix
- preview-panel
session: 426dd4ce-86f0-44a3-83f1-811899047778
---

# 修复带有预览的Readme面板保存未生效及Raw模式限制问题

## 任务目标与背景
排查并修复带有预览的 Readme 面板保存未生效与仅 Raw 模式可编辑问题：1. 提升 React Fiber 与 URL tab 物理绝对路径优先级，解决路径退化为纯文件名 README.md 存错目录问题；2. 增加脑区 Brain Artifact 候选路径探测；3. 保存后同步回写底层 DOM 内容并通知组件刷新，彻底消除视觉未生效割裂；4. 优化 Preview 模式双击与文本提取。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
