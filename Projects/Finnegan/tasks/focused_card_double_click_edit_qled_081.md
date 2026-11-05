---
id: focused_card_double_click_edit_qled_081
title: 聚焦态卡片双击编辑（优先 qled 协议，回退系统默认打开）
status: completed
priority: high
tags:
- frontend
- backend
- editor
- qled
session: conversation://23d9961a-73cc-490d-9a09-b0c7743584e9
---

# 聚焦态卡片双击编辑（优先 qled 协议，回退系统默认打开）

## 任务目标与背景
聚焦态卡片支持双击被编辑。优先尝试使用 qled:// 协议打开对应 Markdown 文件，若 qled 未安装或打开失败，则回退使用系统默认应用打开该文件。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1

## 变更概述
1. **卡片双击编辑机制**：
   - 在 `frontend/src/UICard.svelte` 中针对聚焦态（`isFocused === true`）卡片绑定 `on:dblclick` 事件处理。
   - 优化聚焦态下的单击行为：聚焦态下单击卡片内容不会误触退出聚焦（通过外部 backdrop 或 Escape 退出聚焦），确保双击手势及卡片内部交互顺畅生效。
   - 增加时间门禁防误触机制（进入聚焦态 250ms 内不触发双击动作），防止从分散态快速双击直接拉起外部编辑器。

2. **跨平台编辑器唤起与协议回退（Go 后端）**：
   - 在 `app_search_cmd.go` 中新增 `OpenCardInEditor(cardID string) error`。
   - 自动解析卡片对应的真实 Markdown 文件路径（支持 `cardID`、ULID 映射、`GlobalWatcher` 缓存、`Scattering` 目录以及临时卡片自动提升为本地卡片）。
   - 默认优先构建 `qled://open?path=<url_encoded_path>` 协议并尝试调起 Qled 编辑器。
   - 若本地未注册 `qled` 协议或调起失败，自动回退调用系统默认文件打开工具（macOS 下 `open <filepath>`，Linux 下 `xdg-open`，Windows 下 `start`）。

3. **前后端接口绑定与数据模型补全**：
   - 在 `storage.go` 的 `LoadLocalCards` 中显式填充 `card.FilePath`。
   - 在 `frontend/src/types/card.ts` 与 `frontend/src/lib/stageDecay.ts` (`toCosmicCard`) 中补全 `filePath` 属性。
   - 在 `frontend/wailsjs/go/main/App.d.ts` 与 `App.js` 中导出 `OpenCardInEditor` 绑定。

## 验证结论
- [x] 后端单元测试通过：`go test -v -run "TestOpenCardInEditor" .`
- [x] 前端 TypeScript / Svelte 诊断检查通过：`npm run check` 0 errors, 0 warnings
- [x] macOS 下 `qled://` 协议调起与参数解析验证成功
