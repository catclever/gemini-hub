---
id: add_railway_json_lock_019
title: 配置 railway.json 强制锁定 Dockerfile 构建器
status: completed
priority: medium
tags:
- railway
- deploy
- docker
- descartes-produit
session: 72c41d87-5423-42bb-9e33-136cae2ea3f3
---

# 配置 railway.json 强制锁定 Dockerfile 构建器

## 变更概述
在 descartes-produit 根目录下新增 railway.json 声明配置（强制锁定 builder 为 DOCKERFILE）以及备用 Procfile，杜绝 Railway UI 自动回弹探测错误。代码已推送到 main。

## 验证结论
- [x] 核心逻辑已实现并通过验证
