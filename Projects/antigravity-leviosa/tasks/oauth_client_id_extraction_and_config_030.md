---
id: oauth_client_id_extraction_and_config_030
title: OAuth凭据外部配置化与二进制提取脚本
status: completed
priority: high
tags:
- security
- oauth
- refactor
session: 44157aad-4084-4968-a259-f9bdb704a293
---

# OAuth凭据外部配置化与二进制提取脚本

## 任务目标与背景
将 account_manager.js 中的 OAuth client_id 和 client_secret 硬编码凭据剥离，改由外部配置文件加载并加入 .gitignore 忽略；编写独立的二进制自动化提取脚本 extract_oauth_clients.py，一键提取并生成配置。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
