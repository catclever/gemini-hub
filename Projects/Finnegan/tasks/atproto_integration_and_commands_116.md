---
id: atproto_integration_and_commands_116
title: ATProto 模块总线装配、OmniBar 命令集成与回声接驳
status: completed
priority: high
tags:
- integration
- atproto
- omnibar
- bus
session: conversation://34fd952a-c2fe-491e-be53-488c3ec6081a
---

# ATProto 模块总线装配、OmniBar 命令集成与回声接驳

## 任务目标与背景
完成 ATProto 模块与 Finnegan 核心总线、OmniBar 命令系统及前端回声链路的收网装配。
1. 在 GitHub main 分支上合入 PR 11、PR 14、PR 15；
2. 在 modules/atproto/atproto.go 中实现 module.CommandProvider，声明 /bsky echo 与 /bsky post 命令契约；
3. 在 app.go 启动流水线中通用加载 atproto 模块与配置，并接驳 atproto:fetch_comments 评论回声监听；
4. 全量编译与单元测试验证。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
