---
description: 'macOS 切屏 (Space Transition) 与焦点管理陷阱及解决方案'
---

# macOS 切屏 (Space Transition) 与焦点管理陷阱

在使用 Hammerspoon (`hs.spaces.watcher`) 或其他工具处理 macOS 多屏幕/多桌面切换时，处理不当极易引发“切屏被强行拉回”或“无限循环切屏”的严重体验问题。以下是已在 TaiChi 项目中验证的陷阱与标准解决方案。

## 核心机制与陷阱

### 1. 焦点回退 (Fallback Focus) 引发的“切屏拉回”
当你在 Space A 激活了一个应用（或悬浮窗），然后切到 Space B：
如果此时你通过代码强行 `hide()` 掉了该应用，macOS 发现当前活动窗口消失，会自动执行“焦点回退”逻辑，去历史记录中寻找下一个活跃窗口来接管焦点。
**陷阱**：如果下一个活跃窗口位于之前的 Space A，macOS 会**强行将屏幕切回 Space A**。这给用户的直观感受是“刚刚切过去，过了一会儿又被强行拽回来了”。

### 2. 跨屏 Focus 引发的“死循环”
为了解决上述的“拉回”问题，常规思路是：在 `hide()` 前，主动获取屏幕上的其他窗口并强行给予焦点，以此阻断 macOS 的自动回退。
**陷阱**：如果你使用 `hs.window.orderedWindows()` 获取所有窗口，它返回的是**全局（跨所有 Space）**的窗口。如果错误地 `focus()` 了一个属于其他 Space 的窗口，macOS 会立即切换到那个 Space。
由于切屏会再次触发 `spaceChanged`，进而再次执行这段 Focus 逻辑，最终导致在两个 Space 之间无限循环切屏（死循环）。

## 标准解决方案

为了完美平滑地处理切屏和悬浮窗的隐藏，TaiChi 采用了“Swift 端状态锁” + “Hammerspoon 严格同屏焦点锚定”的双重机制。

### 1. Swift 端：引入切屏锁 (Space Lock) 与缓冲防抖
在 `BrainManager.swift` 中，监听 `spaceChanged` 事件时：
- **立即上锁**：收到事件立刻标记 `isSpaceTransitioning = true`。这期间拦截所有可能引起焦点冲突的 UI 交互动作（如 `toggleAllFloatingApps`、`togglePin`）。
- **防抖缓冲**：等待 500ms（`Task.sleep`），让 macOS 的切换动画和事件风暴彻底平息。期间如果发生新的切屏，则取消旧 Task，让新 Task 接管倒计时，锁状态保持不断。
- **解锁后执行**：500ms 安全期过后，释放锁 `isSpaceTransitioning = false`，再真正下发 `hideAppIfOnScreen` 指令。

### 2. Hammerspoon 端：严格同屏焦点锚定 (Strict Same-Space Anchoring)
在下发隐藏指令后（`floating_action.lua`），在执行真正的 `app:hide()` 前，执行严格的锚定逻辑：

```lua
-- 1. 仅当即将被隐藏的 App 目前处于前台时，才需要锚定（因为只有隐藏前台 App 才会引起焦点回退）
if app:isFrontmost() then
    -- 2. 严格限制：只获取【当前 Space】的标准可见窗口
    local wf = hs.window.filter.new():setCurrentSpace(true)
    local windows = wf:getWindows()
    local anchored = false
    
    for _, w in ipairs(windows) do
        local s = w:screen()
        if s and s:getUUID() == screenUUID and w:application():name() ~= appName and w:isStandard() and w:isVisible() then
            w:focus()
            anchored = true
            break
        end
    end
    
    -- 3. 如果当前屏幕是纯空的（没有任何其他窗口）
    if not anchored then
        -- 绝对不能去 activate Finder（因为如果 Finder 在别的 Space 有窗口，依然会导致跨屏拉回）
        -- 最安全的做法是将焦点下沉给桌面环境 (Desktop)
        local desktop = hs.window.desktop()
        if desktop then
            desktop:focus()
        end
    end
end

-- 4. 安全隐藏
app:hide()
```

## 经验总结
- **跨屏时永远不要随意 `hide` 前台应用**，除非你已经明确将焦点转移给了当前 Space 的安全对象。
- **获取当前屏幕的窗口必须使用 `setCurrentSpace(true)` 过滤**，决不能使用 `orderedWindows()`。
- 当找不到锚定目标时，用 `hs.window.desktop():focus()` 将焦点安全下沉给桌面。
