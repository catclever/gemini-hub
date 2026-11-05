# Task: mutagen_panel
Implement the Mutagen visual interface panel in TaiChi.

## 需求说明
在灵动岛面板中增加 Mutagen 任务管理功能，具体要求：
1. 仅在系统安装了 Mutagen CLI 并且系统设置中勾选了启用时，才会展现。
2. 如果未安装，系统设置中的勾选框应置灰（不可选）。
3. 使用按需监听（Lazy Loading），只有在面板展开为 `mutagen` 模式时，才进行状态拉取。

## 详细架构蓝图
1. **TaiChiConfig & SettingsView**:
   - `TaiChiConfig` (在 `Models.swift` 中): 增加 `enableMutagen: Bool = false`。
   - `SettingsView`: 增加关于网络硬盘和 Mutagen 同步的设置。检测系统是否有 mutagen (`Process` 执行 `which mutagen` 或 `mutagen version`)，如果有则可勾选，否则置灰。

2. **IslandMode**:
   - 在 `IslandStateModel.swift` 的 `IslandMode` 增加 `.mutagen`。

3. **MutagenManager (新增文件)**:
   - 建议在 `Sources/TaiChi/Island/MutagenManager.swift`。
   - 提供方法: `checkInstallStatus() -> Bool`
   - 提供方法: `fetchSessions() -> [MutagenSession]`，执行 `mutagen sync list --template '{{json .}}'`。
   - 数据模型定义: `MutagenSession` (遵循 `Codable`)。

4. **UI 接入 (ExpandedPanelView & ModeSwitcherView)**:
   - 在右键切换中支持进入 `.mutagen` 模式。
   - 在 `ExpandedPanelView` (或新建 `MutagenPanelView`) 中展示 sessions。
   - 遵守 Lazy Loading 逻辑，利用 `.onAppear` 启动 Timer，`.onDisappear` 销毁 Timer。
