---
title: Align code with new storage layout (Scattering / Weaving / pointer config)
status: completed
priority: high
tags:
- storage
- config
- watcher
- refactor
session: conversation://b53a4c3a-bcdb-4588-84df-df4ccc750fae
depends_on: task_global_event_bus
id: storage_layout_004
---
# 将代码对齐到新的数据目录结构

## 设计依据（必读，以设计文档为准）
- 元数据目录 `~/.gemini/Projects/Finnegan/design/tentative/2026-10-11_card_storage_model.md`
- 元数据目录 `~/.gemini/Projects/Finnegan/design/tentative/2026-10-11_data_directory_layout.md`
（远端 agent 若无法访问上述文件，以本任务文件下方的规格为准。）

## 硬边界
- 不要动 `atproto/` 目录下的任何文件（用户所有）。
- 不要重新设计前端卡片 UI / 动画。
- 不要修改任务元数据文件。
- 使用草稿后缀（draft suffixing）。

## 当前代码坐标（Watcher 已合并）
- `core/config/config.go`：`Config{WatchDirs, InboxDir, DebounceMs, BuguMaxConcurrency}`，从仓库根目录的 `finnegan.yml` 加载。
- `app.go`：
  - `NewApp()` 打开当前工作目录下的 `finnegan.db`（L34）
  - `startup()` 加载 `finnegan.yml`（L63），`watcher.GetWatcher().Initialize(cfg.WatchDirs, ...)`（L73）
  - `CaptureThought()`（L111）按 `InboxDir` → `WatchDirs[0]` 的顺序选择写入目录
  - `PromoteTempCard()`（L227）调用 `CardManager.PromoteToLocal`
- `cards.go`：`CardManager.PromoteToLocal` 目前写入 SQLite（`BulkSaveDocs("cards", ...)`）
- `core/markdown/markdown.go`：从头部解析 `id`（L70）
- `core/watcher/watcher.go`：全局 watcher，提供 `WriteFile(path, content, origin)`

## 规格

### S1. 指针配置
- 路径：`~/Library/Application Support/Finnegan/finnegan.yml`，内容只有 `home: <path>`（支持 `~`）。默认值 `~/Finnegan`。
- 启动时：指针文件不存在 → 写入默认值；主目录不存在 → 创建骨架 `Scattering/`、`Weaving/`、`.finnegan/`、`.finnegan/bases/`。
- 删除仓库根目录的 `finnegan.yml`（在报告中注明）。

### S2. 自管配置 `<home>/.finnegan/config.yml`
```yaml
external_projects: []      # 绝对路径或 ~ 路径
debounce_ms: 300
bugu_max_concurrency: 1
```
- 不存在则用默认值创建。从 `Config` 中移除 `WatchDirs` / `InboxDir`。

### S3. 监听目录推导
- `watch = [<home>/Scattering, <home>/Weaving] + 存在且包含 .finnegan-project 的 external_projects`
- 永不监听 `<home>/.finnegan/`。
- 对于 external_projects 下的文件：头部**没有** `id` 的 `.md` 文件一律忽略（不入库、不修改）。

### S4. `CaptureThought(text)`
- 写入 `<home>/Scattering/`。
- 生成 ULID 作为 `id`（可引入 `github.com/oklog/ulid/v2`）。
- 文件名：`YYYYMMDD-HHMM-<slug>.md`；slug 取正文前若干字符（安全地保留中文，去掉路径非法字符，截断到约 20 个字符）；冲突时追加 `-2`、`-3`。
- 头部字段：`id`、`created`、`updated`（RFC3339 带时区）、`source: local`、`tags: []`、`publish: false`。
- 继续通过 `watcher.WriteFile(..., "capture")` 写入，并发布 `EventThoughtCaptured`（保留现有行为）。

### S5. `PromoteTempCard(id)`
- 不再写 SQLite。改为在 `<home>/Scattering/` 生成 Markdown 文件，规则同 S4，另加 `source: bugu`、`source_url`，以及（如有）`echo_of`。用 `watcher.WriteFile(..., "promote")` 写入，然后从 `tempCards` 中移除。
- 给 `Card` 增加可选字段 `EchoOf`（json `echoOf`）。
- 增加 Wails 绑定 `ClearTempCards()`。

### S6. 缓存迁移
- SQLite 缓存改到 `<home>/.finnegan/cache.db`（`NewApp` 需要在主目录解析之后再打开数据库，必要时把数据库初始化移到 `startup`）。

### S7. 以 id 为身份（修复 Watcher 遗留问题）
- Watcher 维护 `path → docID` 映射，保证删除 / 重命名带有自定义 `id` 的文件时，能正确删除或更新对应的数据库记录。
- 重复 id：两个不同路径出现同一个 id 时，保留先发现的那个，记录 warning，并发出 Wails 事件 `card:id_conflict {id, paths}`。**绝不静默覆盖。**

### S8. 不在本任务范围
- `atproto.yml` 对齐（另开任务）、嵌入解析、写时复制分支、base 快照、项目登记 UI。

## 验证
- 在临时副本中把草稿替换进去后执行：`go build ./...`、`go vet ./...`、`go test -race -count=3 ./core/...`
- 新增测试：指针配置默认值与骨架创建；监听目录推导（排除 `.finnegan/`，external 项目必须有标记文件）；忽略没有 id 的外部文件；CaptureThought 的文件名 / 头部 / ULID；带自定义 id 的文件被删除时能删除数据库记录；重复 id 的冲突处理。
- 测试中用临时目录模拟 HOME / Application Support，**不得触碰真实的用户目录**。
- 前端绑定有变化时：`cd frontend && npm install && npx tsc --noEmit`。
- 清理临时目录。

## 最终报告必须包含
- 新增 / 修改 / 删除的文件（附原文件对照）。
- 测试结果摘要（含 `-race -count=3`）。
- 未达成的项及原因。

## 完成后（主代理负责）
- 更新 `kb/knowledge.md`，并把两份 tentative 设计中的规格提炼进 kb。
