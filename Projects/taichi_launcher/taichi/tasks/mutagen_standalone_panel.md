# Task: mutagen_standalone_panel
实现一个完全独立的 Mutagen 专属配置与操作面板。

## 需求说明
1. 不要在原有的 `SettingsView` (TaiChi 系统设置) 中堆砌 Mutagen 的具体任务配置。
2. 灵动岛 Mutagen 面板里的 ⚙️ 齿轮按钮，点击后应当弹出一个**全新且独立**的窗口/面板，专用于 Mutagen 参数修改。
3. 这个独立面板需要展示：
   - 任务列表。
   - 选中任务的当前 Ignore 列表（支持增删）。
   - 【保存并热重启】按钮，利用解析出的完整参数，先 `terminate` 任务，再用携带了新 Ignore 参数的 `create` 命令重新启动它。

## 详细架构蓝图
1. **数据模型深度扩充 (`MutagenSession`)**:
   修改 `MutagenManager.swift` 中的 `MutagenSession` 结构体，完整映射 `mutagen sync list --template '{{json .}}'` 的核心字典字段：
   - `alpha` 字典 (包含 protocol, path, host 等)
   - `beta` 字典
   - `ignore` 字典 (包含 paths 数组)
   - `mode` 字符串 (可选，默认为 "two-way-safe")
   提供一个辅助方法 `generateCreateCommand(newIgnores: [String]) -> String`，用于拼凑完整的 CLI 重启命令。

2. **独立窗口管理器 (`MutagenWindowManager`)**:
   仿照 `SettingsWindowManager`，新建 `MutagenWindowManager.swift`，管理一个常规的 `NSWindow` 或 `NSPanel`，其根视图为 `MutagenConfigView`。

3. **专享配置界面 (`MutagenConfigView`)**:
   设计独立的 SwiftUI 视图。左侧是任务 List 导航，右侧是具体的 Ignore 规则列表编辑区。底部是“热重启”按钮，点击后通过 `Process` 依次执行终止和重启。

4. **入口修正**:
   将 `MutagenPanelView.swift` 中的 `SettingsWindowManager.shared.show()` 改为 `MutagenWindowManager.shared.show()`。
