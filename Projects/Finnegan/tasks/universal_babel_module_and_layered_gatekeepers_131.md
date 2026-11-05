---
id: universal_babel_module_and_layered_gatekeepers_131
title: Universal Babel Module with Layered Gatekeeper System
status: completed
priority: high
tags:
- babel
- backend
- architecture
- night-shift
session: 34fd952a-c2fe-491e-be53-488c3ec6081a
---

# Universal Babel Module with Layered Gatekeeper System

## 任务目标与背景
Refactor Babel into a universal module with layered gatekeepers (universal base translator/spam filter + Bugu deep reasoning gate + Bluesky inspiration social gate) and decouple frontend babelSession.

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1

## 验证结论
- [x] 建立 core/models/babel.go 统一 BabelCard 模型，并重构 modules/bugu/models/babel.go 为其类型别名。
- [x] 建立通用 Babel 翻译与分层门禁流水线 core/babel/（防垃圾/防乱码/防纯链接通用底座 + Bugu 四维思辨锚点门禁 + Bluesky 社交轻量锚点门禁）。
- [x] 正名与标准化 Wails 事件为 babel:card_spawned 与 babel:session_completed，双向兼容旧事件别名。
- [x] 前端抽离 frontend/src/modules/babel/（types.ts, babelSession.ts），将卡片队列与视口自适应排布从 buguSession 中彻底解耦。
- [x] 后端测试 go test -v ./... 与前端测试 npm --prefix frontend test 全部通过（172/172 pass）。
