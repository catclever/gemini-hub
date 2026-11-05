# Task: orb_button_clicks
优化下方能量球中央小按钮（`SettingsButton` in `Sources/TaiChi/Components.swift`）的点击逻辑。

## 需求说明
当前 `SettingsButton` 内部通过时间差实现了单击和双击的区别。
现在的目标是：
1. **左键单击**：保持现状（打开图标上显示的 app 或者设置）。
2. **左键双击**：**默认打开设置**（无视当前图标显示什么，直接调用 `openSettings()`）。
3. **右键单击**：执行**旧版代码里的双击逻辑**（即：打开图标上没有显示的内容。如果显示的是 App 就打开设置；如果显示的是太极就打开 App）。

## 架构蓝图
1. **引入右键捕获视图**:
   在 `Components.swift` 底部新建一个跨平台的右键捕获组件，利用 `NSViewRepresentable`：
   ```swift
   struct RightClickCatcherView: NSViewRepresentable {
       var onRightClick: () -> Void
       func makeNSView(context: Context) -> RightClickNSView {
           let view = RightClickNSView()
           view.onRightClick = onRightClick
           return view
       }
       func updateNSView(_ nsView: RightClickNSView, context: Context) {}
   }

   class RightClickNSView: NSView {
       var onRightClick: (() -> Void)?
       override func rightMouseUp(with event: NSEvent) {
           onRightClick?()
       }
   }
   ```

2. **改造 `SettingsButton` 视图结构**:
   在 `SettingsButton` 的根 `Button` 或者最外层 `ZStack` 后面追加 `.background(RightClickCatcherView { ... })` 来捕获右键。
   
   右键闭包里的逻辑完全照搬旧版的双击逻辑：
   ```swift
   if shouldShowApp {
       openSettings()
   } else {
       if let app = lastApp {
           onOpenApp?(app)
       } else {
           openSettings()
       }
   }
   ```

3. **改造左键双击逻辑**:
   将 `Button` action 中 `isDoubleClick == true` 分支里的逻辑，全部删掉，直接替换为极简的：
   ```swift
   clickTask?.cancel()
   openSettings()
   ```

   单击 (`isDoubleClick == false`) 的延迟逻辑保持不变。
