---
title: Mutagen 项目配置文件绑定与三态交互管理
status: in_review
priority: high
tags:
  - mutagen
  - ui
  - configuration
---

# Task: mutagen_project_binding
实现 Mutagen 任务配置文件的持久化绑定与“三态模型”（普通任务、未绑定项目任务、已绑定项目任务）及拖拽交互。

## 需求说明
1. **持久化存储**：
   在 TaiChi 目录下（优先存放在 `(TaiChiSettings.shared.scriptsPath as NSString).expandingTildeInPath` 下的 `mutagen_projects.json`），将 `projectId`（来源于 Mutagen JSON 的 `labels["io.mutagen.project"]`）与配置文件的绝对路径进行键值持久化映射。
2. **三态模型定义**：
   - **普通任务 (CLI Task)**：无 `io.mutagen.project` 标签。正常编辑 Ignore，点击“保存并热重启”时执行 CLI `terminate` + `create`。
   - **未绑定项目任务 (Unlinked Project Task)**：有 `io.mutagen.project` 标签，但在 `mutagen_projects.json` 中找不到存在的配置文件路径。
     - 右侧 Ignore 详情区整体替换为**拖拽绑定交互区**（虚线框、提示文字、大图标）。
     - 支持将 `mutagen.yml` / `.yaml` 拖拽到该区域直接绑定（利用 `.onDrop`）。
     - 同时也支持点击虚线框弹出系统的 `NSOpenPanel` 浏览选择文件。
     - 绑定成功后保存到 `mutagen_projects.json`，并立即自动切换为“已绑定项目任务”状态。
   - **已绑定项目任务 (Linked Project Task)**：有 `io.mutagen.project` 标签，且绑定的配置文件在本地磁盘上存在。
     - 任务标题旁展示 📄 Project 标签以及配置文件路径。
     - 提供“在访达中显示”和“重新绑定”按钮。
     - Ignore 列表可正常增删修改。
     - 保存按钮变为“保存至配置文件并重启项目”：
       - 备份源文件为 `.bak`。
       - 修改 `mutagen.yml` 中对应任务的 `ignore.paths`。
       - 执行 `mutagen project terminate -f <path>` 并执行 `mutagen project start -f <path>` 实现重载。

## 详细实现规范

### 1. 数据模型与管理层 (`MutagenManager.swift`)
- `MutagenSession`：
  - 新增字段 `let labels: [String: String]?`。
  - 增加计算属性 `var projectId: String? { labels?["io.mutagen.project"] }`。
  - 定义三态枚举：
    ```swift
    enum SessionType: Equatable {
        case normal
        case unlinkedProject(projectId: String)
        case linkedProject(projectId: String, configPath: String)
    }
    ```
- `MutagenProjectStore` 或在 `MutagenManager` 中提供持久化：
  - 属性 `@Published var projectMappings: [String: String] = [:]`。
  - 路径：`URL(fileURLWithPath: (TaiChiSettings.shared.scriptsPath as NSString).expandingTildeInPath).appendingPathComponent("mutagen_projects.json")`。
  - 方法：
    - `loadMappings()`
    - `saveMappings()`
    - `bind(projectId: String, path: String)`
    - `unbind(projectId: String)`
    - `sessionType(for session: MutagenSession) -> SessionType`
- YAML 规则更新辅助方法：
  - 读取并安全修改 `mutagen.yml` 中指定 session 的 `ignore.paths`，保持 YAML 缩进与格式，修改前自动备份 `.bak`。

### 2. UI 界面重构 (`MutagenConfigView.swift`)
- 左侧边栏 List：
  - 为每个 session 项展示状态图标：普通任务展示终端/命令行图标，项目任务展示 📄 文件的图标（未绑定时展示黄色警示标识）。
- 右侧主区域：
  - 根据 `sessionType` 切换呈现：
    - **未绑定状态**：渲染大面积虚线圆角矩形区域（带 `doc.badge.plus` 大图标，文字“将 mutagen.yml 拖拽至此，或点击浏览文件”）。支持 `.onDrop(of: [.fileURL])` 和点击触发 `NSOpenPanel`。
    - **已绑定状态**：顶部显示配置文件路径卡片（带“在访达中显示”与“重新绑定”按钮）；下方为可编辑的 Ignore 列表；底部为“保存至配置文件并重启”按钮。
    - **普通状态**：原有可编辑 Ignore 列表及“保存并热重启”按钮。

## 验证规划
1. 编译无任何 Concurrency 与语法报错。
2. 启动测试，在没有 project 标签的 session 下展示普通任务模式。
3. 模拟或检测 project 标签任务，拖拽或选取 yml 文件后，自动持久化至 `mutagen_projects.json` 并进入已绑定状态。
