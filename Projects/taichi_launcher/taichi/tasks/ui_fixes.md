# Task: ui_fixes
修复 Mutagen 面板的两处 UI 问题。

## 需求说明
1. **模式切换器 (ModeSwitcherView) 上的文字被截断/看不见**。
   原因分析：`IslandView.swift` 中对 `.modeSwitcher` 状态硬编码了 `stateModel.capsuleWidth = 260`。当加入第三个 Mutagen 按钮后，260pt 的宽度不足以容纳 3 个按钮的横向排列，导致文字被挤扁。
   解决方案：根据 `TaiChiSettings.shared.enableMutagen` 的状态动态分配宽度，开启时给定更大的宽度（例如 350）。

2. **无法进入操作面板 (Settings)**。
   原因分析：`MutagenPanelView.swift` 缺乏进入系统设置的入口。
   解决方案：在 `MutagenPanelView.swift` 的顶部标题（"Mutagen Sessions"）右侧添加一个 `gearshape.fill` 齿轮按钮，点击后调用 `SettingsWindowManager.shared.show()`。

## 详细架构蓝图
1. **修改 `IslandView.swift`**:
   定位到 `case .modeSwitcher:`，将宽度逻辑修改为：
   ```swift
   case .modeSwitcher:
       stateModel.capsuleWidth = TaiChiSettings.shared.enableMutagen ? 350 : 260
       stateModel.capsuleHeight = hasPhysicalNotch ? 120 : 100
   ```

2. **修改 `MutagenPanelView.swift`**:
   将现有的 `Text("Mutagen Sessions")` 包裹进 `HStack`，并在其右侧添加 `Spacer()` 和一个齿轮 `Button`：
   ```swift
   HStack {
       Text("Mutagen Sessions")
           .font(.headline)
           .foregroundColor(.white)
       
       Spacer()
       
       Button(action: {
           SettingsWindowManager.shared.show()
       }) {
           Image(systemName: "gearshape.fill")
               .font(.system(size: 16))
               .foregroundColor(.gray)
       }
       .buttonStyle(PlainButtonStyle())
   }
   .padding(.horizontal)
   .padding(.top, 16)
   ```
