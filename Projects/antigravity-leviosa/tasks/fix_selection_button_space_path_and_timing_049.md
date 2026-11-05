---
id: fix_selection_button_space_path_and_timing_049
title: 修复带空格及波浪号路径拦截与选中文本注入时序问题
status: completed
priority: high
tags:
- file_editor
- bugfix
- path_resolution
session: 426dd4ce-86f0-44a3-83f1-811899047778
---

# 修复带空格及波浪号路径拦截与选中文本注入时序问题

## 任务目标与背景
修复 isCandidateFilePath 误将带有空格的路径（如 ~/Library/Application Support/...）拦截的缺陷，放行包含斜杠且以 ~/ 或 / 开头的合法带空格路径，增强路径清洗并增加渲染多阶段时序重试。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
