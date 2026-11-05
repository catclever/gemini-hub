---
id: modular_border_beam_registry_and_injection_decoupling_143
title: 流转边框引擎 Layer 2 注册表抽象与模块内聚注入解耦
status: completed
priority: medium
tags:
- refactor
- modular
- ui
session: a7bf5827-3993-452d-b349-56f141101111
---

# 流转边框引擎 Layer 2 注册表抽象与模块内聚注入解耦

## 变更概述
1. 独立通用核心层：创建 frontend/src/lib/borderBeamRegistry.ts 定义通用的 BorderBeamPreset 注册表与 resolveCardBorderBeam 纯函数分发器；
2. 模块内聚自治注入：在 frontend/src/modules/bugu/beam.ts 中自治注册琥珀金单段彗尾，在 frontend/src/modules/atproto/beam.ts 中自治注册冰蓝单段彗尾；
3. 通用渲染层极致瘦身：CardAuraGlow.svelte 彻底转型为无业务逻辑的纯呈现组件（代码缩减至 75 行），完全由 activeBeam 配置驱动；
4. 测试覆盖：新增 borderBeamRegistry.test.ts（包含 5 项深度测试，198 项全绿通过），Vite 生产构建编译通过。

## 验证结论
- [x] 核心逻辑已实现并通过验证
