# AgentK 架构方案：相对中心点物理引擎 (Relative Center-Anchor Physics)

**模块：** `@agent-k/core`, `@agent-k/tentacles`, `@agent-k/shoggoth`  
**核心概念：** 废弃传统左上角绝对坐标，全面采用基于中心点与父级锚定的弹性物理坐标系。

---

## 1. 核心 Schema 规范 (`CanvasPropsSchema`)
每个组件在画布上的物理属性定义于 `canvas` 字段：
- `cx?: number`: 目标中心点 X 轴坐标（相对锚点或画布）。
- `cy?: number`: 目标中心点 Y 轴坐标（相对锚点或画布）。
- `anchor?: string`: 关联锚定组件 ID。未定义时默认相对于画布全局坐标。
- `width?: number | string`: 宽度。
- `height?: number | string`: 高度。
- `rotation?: number`: 绕中心点的旋转角度。

---

## 2. 运行时坐标解析 (`resolveAbsoluteLayout`)
在 `@agent-k/core/src/framework/LayoutResolver.ts` 中实现：
1. **拓扑解析**：递归解析 `anchorId` 指向的父级中心点 `(anchor_abs_cx, anchor_abs_cy)`。
2. **绝对中心点公式**：
   $$\text{abs\_cx} = \text{anchor\_abs\_cx} + cx$$
   $$\text{abs\_cy} = \text{anchor\_abs\_cy} + cy$$
3. **DOM 渲染坐标转换**：
   $$x = \text{abs\_cx} - \frac{\text{width}}{2}$$
   $$y = \text{abs\_cy} - \frac{\text{height}}{2}$$
4. **环路安全**：自动检测循环锚定（Circular anchor dependency），降级保底防止栈溢出死循环。

---

## 3. 编辑器反向逆解 (`inverseKinematics`)
当用户在前端画布上拖拽锚定组件至新屏幕绝对位置 $(\text{new\_abs\_x}, \text{new\_abs\_y})$ 时：
1. 计算新屏幕中心点：
   $$\text{new\_abs\_cx} = \text{new\_abs\_x} + \frac{\text{width}}{2}$$
   $$\text{new\_abs\_cy} = \text{new\_abs\_y} + \frac{\text{height}}{2}$$
2. 计算写回 JSON 的相对偏移量：
   $$cx = \text{new\_abs\_cx} - \text{anchor\_abs\_cx}$$
   $$cy = \text{new\_abs\_cy} - \text{anchor\_abs\_cy}$$
3. 确保组件在父组件移动时自然联动跟随。

---

## 4. 状态同步铁律 (State Sync Rule)
在消费端应用（如 `shoggoth/src/App.tsx`）的 `handleUpdate` 中：
当应用 `{ cx, cy }` 等更新时，必须同时深层同步 `c.canvas = { ...c.canvas, ...updates }`，确保 React State、AST 树与序列化文件无断层同步。
