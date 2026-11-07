---
id: deregister_project_search_module_064
title: 注销 project_search 模块（官方原生已支持）
status: completed
priority: medium
tags:
- mod
- refactor
- cleanup
session: ffed3263-6a8c-4185-9f91-b306e47f1090
---

# 注销 project_search 模块（官方原生已支持）

## 变更概述
由于 Antigravity 官方已原生内置项目选择器搜索框（data-testid="project-selector-search"），在 web/main.js 中注销不再需要的自定义 project_search.js 模块。

## 验证结论
- [x] 核心逻辑已实现并通过验证
