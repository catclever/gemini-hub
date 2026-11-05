---
id: bugu_router_target_queries_and_searxng_engine_fix_157
title: Bugu 靶标专属查询规划、SearxNG 引擎参数修复与时间窗口覆盖修复
status: completed
priority: high
tags:
- bugu
- router
- searxng
session: conversation://20e28f53-3575-42ff-b7fb-f69ec7e182aa
---

# Bugu 靶标专属查询规划、SearxNG 引擎参数修复与时间窗口覆盖修复

## 任务目标与背景
重构 Bugu 路由规划、SearxNG 引擎检索与靶标去重：
1. 在 `modules/bugu/models/target.go` 的 `LLMSearchPlan` 中新增 `TargetQueries map[string][]string` (`json:"target_queries,omitempty"`)，保留 `SearchQueries` 向后兼容。
2. 在 `modules/bugu/llm/router.go`：
   - `FormatKeywordsProfile` 自动清洗每个关键词尾部的 `*` 标记（`strings.TrimRight(strings.TrimSpace(w), "*")`）。
   - 支持注入卡片的 `visual_summary` 与 `link_summary`（通过扩展参数或 `BuildFacetSearchPlanPrompt`），让多模态图文卡与外链卡具备完整语境。
   - 升级 Prompt：支持按 target_id 在 `target_queries` 中生成贴合该靶标调性与语言的专属查询词；将原本死板的强制小语种配额升级为语境自适应跨语言路由（本土生活/中文语境母题优先深耕中英与泛亚站点，普世技术/人文议题跨语种发散）。
3. 在 `modules/bugu/fetcher/searxng.go`：
   - 当 `target.Type == "engine"` 时，不再把 `target.Value` 拼进 `q=`，而是将 `target.Value` 作为 `&engines=` 参数传给 SearxNG；
   - 若 `len(target.PreferredEngines) > 0` 且未设置 engine，拼接 `&engines=<comma_joined>`。
4. 在 `modules/bugu/api/radar.go`：
   - 修复第 285 行 `if tr, ok := plan.TargetTimeRanges[target.ID]; ok` 的空字符串覆盖 Bug（移除 `&& tr != ""`，允许显式 `""` 覆盖 `DefaultTimeRange` 实现不限时间检索）。
   - `resolveTargetQueries` 优先读取 `plan.TargetQueries[target.ID]`，若无则平滑回退原有的 `plan.SearchQueries` 语言匹配逻辑。
5. 清理 `modules/bugu/radar_targets.yml` 中的重复 `value` 靶标（确保 `config.LoadConfig` 按 `Value` 去重或清理重复项）。
参考文档：`kb/knowledge.md` 第 12 节。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
