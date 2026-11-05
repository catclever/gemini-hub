---
title: Mutagen 监控面板紧凑 UI 重构与任务归档机制
status: completed
priority: high
tags:
  - mutagen
  - ui
  - persistence
---

# Task: mutagen_ui_and_archive

实现 Mutagen 监控卡片的高密度单行布局、无缝点击操作栏热替换，以及任务停止后的持久化归档机制。

## 需求说明
1. **监控卡片 UI 重构 (`MutagenPanelView.swift`)**：
   - 将现有卡片的垂直多行布局改为**紧凑单行水平布局**。
   - 左侧为标题文字，字体加粗放大（如 `.headline` 或 `.system(size: 14, weight: .bold)`），限制最大宽度，超过截断（`.lineLimit(1)`）。
   - 右侧默认展示状态文本（右对齐，保持 caption 尺寸和颜色）。
2. **点击热替换操作栏 (Hot-Swap Action Bar)**：
   - 维持单行高度不变。
   - 点击某张卡片时，右侧的状态文本**原位替换**为三个图标操作按钮：
     - **暂停/继续**：根据当前 `paused` 状态显示 `pause.fill` 或 `play.fill`。
     - **停止**：红色的 `stop.fill` 图标。
     - **配置**：灰色的 `gearshape.fill` 图标，点击直接打开独立设置面板并选中该任务。
   - 点击其他卡片时，原来的卡片恢复显示状态文本。
3. **停止任务的归档与生命周期 (`MutagenManager.swift`)**：
   - 新增持久化属性 `archivedSessions: [MutagenSession]`，存放在 `~/Library/Services/taichi/mutagen_archived_sessions.json`。
   - 当在 UI 点击**停止**按钮时，触发 `terminateAndArchive(session:)`：先将 session 深拷贝并存入 `archivedSessions`，持久化至磁盘，再执行 CLI `mutagen sync terminate <id>`，并刷新活跃列表。
   - *（注：如果用户在终端使用命令停止，由于未使用 TaiChi 的停止按钮，任务不会进入 `archivedSessions`，而是从监控面板自然消失，符合直觉的隔离机制。）*
4. **独立设置面板适配 (`MutagenConfigView.swift`)**：
   - 左侧侧边栏分为两组（利用 `Section`）：**活跃任务** 和 **已停止任务**。
   - 对于选中的已停止任务，右侧面板不提供 Ignore 编辑功能，仅展示任务信息及两大操作按钮：
     - **重新开始**：从 `archivedSessions` 移除并执行对应启动命令（如是 LinkedProject，使用 `mutagen project start -f <path>`，否则使用 `mutagen sync create ...`），并刷新活跃列表。
     - **永久删除**：从 `archivedSessions` 彻底删除。

## 详细实现规范

### 1. `MutagenManager.swift` 更新
- 引入 `@Published var archivedSessions: [MutagenSession] = []`。
- 增加 `loadArchivedSessions()` 与 `saveArchivedSessions()`。在 `init()` 时加载。
- 增加方法：
  - `togglePause(session: MutagenSession)`: 执行 `mutagen sync pause <id>` 或 `mutagen sync resume <id>`。
  - `terminateAndArchive(session: MutagenSession)`:
    1. append 到 `archivedSessions`，调用 `saveArchivedSessions()`。
    2. 异步执行 `mutagen sync terminate <session.id>`。
    3. 等待完成后调用 `fetchSessions()`。
  - `resumeArchivedSession(id: String)`:
    1. 找到对应的 session。
    2. 根据其 `sessionType`，若为 `linkedProject`，提取 `configPath` 执行 `mutagen project start -f <configPath>`；若为其他，执行 `session.generateCreateCommand(...)`。
    3. 执行后，从 `archivedSessions` 中移除并保存，最后刷新。
  - `deleteArchivedSession(id: String)`: 直接移除并保存。
- 为 `MutagenWindowManager` 的 `show()` 方法增加可选参数 `for sessionId: String? = nil`，使其打开时能直接选中对应的 Session。

### 2. `MutagenPanelView.swift` 更新
- 使用 `@State private var activeActionSessionId: String? = nil`。
- 修改 `ForEach` 中的卡片布局：
  - `HStack` 包含左侧 `Text` 和 右侧 `Spacer()` + 判定区。
  - 判定区：`if activeActionSessionId == session.id { HStack { 3个控制按钮 } } else { HStack { 状态文本 } }`。
  - 整个 `HStack` 添加 `.onTapGesture { activeActionSessionId = (activeActionSessionId == session.id) ? nil : session.id }` 增加原位热替换交互。
- 按钮实现：
  - 暂停/继续：调用 `mutagenManager.togglePause(session: session)`。
  - 停止：调用 `mutagenManager.terminateAndArchive(session: session)`；随后将 `activeActionSessionId` 设为 `nil`。
  - 配置：调用 `MutagenWindowManager.shared.show(for: session.id)`。

### 3. `MutagenConfigView.swift` 更新
- 将原来的简单 `List` 改为支持 Section 的结构：
  ```swift
  List(selection: $selectedSessionId) {
      Section(header: Text("活跃任务")) {
          ForEach(manager.sessions) { ... }
      }
      if !manager.archivedSessions.isEmpty {
          Section(header: Text("已停止任务")) {
              ForEach(manager.archivedSessions) { ... }
          }
      }
  }
  ```
- 右侧内容判定：
  - 优先在活跃 `sessions` 中寻找。如果找到，展示常规/绑定 UI。
  - 如果在活跃中找不到，但在 `archivedSessions` 中找到：
    - 右侧顶部展示 "已停止任务: \(session.name)"。
    - 下方展示“重新开始” (Resume) 与“永久删除” (Delete) 的大按钮区。
    - 不展示复杂的 Ignore 编辑与虚线框（或者只读展示）。
