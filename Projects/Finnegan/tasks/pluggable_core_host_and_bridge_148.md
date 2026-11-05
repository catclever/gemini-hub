---
id: pluggable_core_host_and_bridge_148
title: Pluggable Core Host Decoupling & External Plugin Bridge
status: completed
priority: high
tags:
- architecture
- core
- plugin-system
session: conversation://f02d8867-c211-4b1b-9cc3-b201d0775800
---

# Pluggable Core Host Decoupling & External Plugin Bridge

## 任务目标与背景
Refactor Finnegan Core (Backend & Frontend) into a zero-coupling pluggable host supporting both built-in modules and standalone external .plugin files:
1. Expand core/module contracts with ModuleManifest (PromotionStrategySpec, ThemeColor, BeaconType, CardTypes), ManifestProvider, ActionProvider, HostAPI, and ExternalPluginBridge (scanning <home>/.finnegan/plugins/*.plugin via JSON-RPC/stdio or HTTP/socket + /api/plugins/<name>/* asset serving).
2. Extract shared LLM completion helper into core/llm so modules do not cross-import modules/bugu/llm.
3. Decouple package main (app.go, app_events.go, app_search_cmd.go) from direct imports of modules/bugu/* and modules/atproto/* by normalizing card spawning via core/models.BabelCard & reflection/map fallback and routing module actions (such as fetch_comments) through ExecuteModuleAction.
4. Upgrade Frontend (App.svelte, promotionRegistry.ts, UICard.svelte, cardRegistry.ts) to hydrate module manifests dynamically on startup (GetModuleManifests) and dynamically load external plugin UI bundles (/api/plugins/<name>/ui.js) while maintaining full backward compatibility with existing unrefactored modules.

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1

## 实施与验证记录 (Core Host & Bridge)
- **公共 LLM 客户端 (`core/llm/client.go`)**: 提取 `CleanJSONText` 与 `GenerateCompletion`（支持 Gemini 及 OpenAI 兼容接口），单元测试通过。
- **模块自声明清单与外部单文件桥接 (`core/module/manifest.go` & `external_bridge.go`)**:
  - 新增 `ModuleManifest`, `PromotionStrategySpec`, `CardTypeSpec`, `ManifestProvider`, `ActionProvider`, `PromoteHookProvider`, `HostAPI`；
  - 新增 `ExternalModule` 与 `LoadExternalPlugins`（支持 `<home>/.finnegan/plugins/` 下的目录插件与 `.plugin` 单文件二进制插件，支持 NDJSON 流式 `spawn_card` 与 `--finnegan-ui` / `/api/plugins/<name>/ui.js` 前端组件挂载）。
- **主程序零耦合化 (`app.go`, `app_events.go`, `app_search_cmd.go`, `main.go`)**:
  - `go list -f '{{.Imports}}' .` 验证 `package main` 已彻底移除对 `Finnegan/modules/*` 子包的所有直接引用，仅保留顶层 `_` 空导入；
  - 新增 `GetModuleManifests()` 与 `ExecuteModuleAction()` Wails 绑定。
- **前端动态清单水合 (`frontend/src/lib/promotionRegistry.ts` & `cardRegistry.ts` & `App.svelte`)**:
  - 实现 `hydrateModuleManifests`、`getModuleThemeColor`、`getModuleBeaconType` 与 `loadExternalPluginCardComponents`，`node --test src/lib/promotionRegistry.test.ts` 与 `go test . ./core/...` 100% 通过。
