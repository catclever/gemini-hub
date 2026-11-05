---
id: fix_finnegan_yml_trailing_syntax_error_136
title: 修复 finnegan.yml 尾部意外字符 77 导致的 YAML 语法解析失败
status: completed
priority: high
tags:
- config
- bugfix
- yaml
session: b5c8342e-2cbb-4933-866c-87066dbde3ae
---

# 修复 finnegan.yml 尾部意外字符 77 导致的 YAML 语法解析失败

## 变更概述
Removed stray invalid trailing characters '77' on line 21 of ~/Library/Application Support/Finnegan/finnegan.yml which caused YAML parsing syntax failure on app startup.

## 验证结论
- [x] 核心逻辑已实现并通过验证
