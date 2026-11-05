---
id: global_candidate_cards_hierarchy_and_viewport_staging_087
title: 全局候选卡片分级检索、命令筛选与视口引力挂载
status: completed
priority: high
tags:
- frontend
- backend
- omnibar
- candidate_hierarchy
- stage
session: 97aa8c6a-1720-45f1-a751-8213e8d557f9
---

## 变更概述
1. **类型与契约定义**（`core/module/command.go` & `src/types/card.ts`）：
   - `ParamSpec` 新增声明式属性：`ExcludedTypes`（排除卡片类型）、`AllowedTypes`（允许卡片类型）、`AutoStageToViewport`（选中离屏卡片自动挂载当前屏）。
   - Bugu 声明 `RequireKeywords: true`, `ExcludedTypes: ["note"]`, `AutoStageToViewport: true`。
2. **纯算法三层候选分级引擎**（`src/lib/paramCandidateEngine.ts`）：
   - `partitionCardTiers()`：精准划分 Tier 1（当前屏幕·零阻碍）、Tier 2（其他屏幕·按距离排序带屏数标签）、Tier 3（历史归档·时间倒序）。
   - `filterCandidateCard()`：声明式规则校验，彻底剔除硬编码。
   - `rankSearchCandidates()`：搜索态下保证屏幕优先级排序。
3. **全局视口引力挂载与级联**（`src/lib/stageDecay.ts`）：
   - 提取公共 `ensureCardStagedInViewport()`，处理视口中心 Mitchell 采样放置与多屏级联。
   - `App.svelte` 统一调用，彻底解耦 `buguSession.ts` 私有母卡召唤逻辑。
4. **下拉菜单交互与下翻 Bug 修复**（`CardCandidateDropdown.svelte` & `OmniBar.svelte`）：
   - 彻底废除 `length >= 6 break` 硬截断。
   - 增加当前屏幕/其他屏幕/历史归档视觉分隔头与来源 Chip。
   - 键盘上下键增加 `scrollIntoView({ block: 'nearest', behavior: 'smooth' })` 确保焦点始终居中跟随。
   - 触底自动触发历史卡片无限增量拉取。

## 验证结论
- [x] Node 原生单元测试全部通过（73 个前序用例 + 8 个引擎新增用例）：`8 pass 0 fail`
- [x] Svelte 严格类型检查通过：`0 errors, 0 warnings`
- [x] 前端 Vite 构建打包成功：`vite build done in 0.45s`
- [x] 本地与 PVE 后端 Go 单元测试全量通过：`ok Finnegan 0.315s, ok Finnegan/modules/bugu 0.213s`
