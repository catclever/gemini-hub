# 浮动模态弹窗 1:1 全景壁纸视口切片映射与防跳跃规范

## 1. 核心问题与物理机理 (The Root Causes)

在 Antigravity 这种基于 Electron/Chromium 的 SPA 架构中，使悬浮模态弹窗（如设置面板 Settings Modal）呈现出**与底层全屏幕壁纸绝对同轴、1:1 无缩放取景**的高级毛玻璃质感，面临三大底层陷阱：

### 陷阱 A：W3C Transform 包含块陷阱（为什么 fixed 会退化并缩放）
- **现象**：在弹窗上简单设置 `background-attachment: fixed; background-size: cover;` 时，背景并未直通 Viewport，而是被等比缩小成一张完整的缩略图塞在弹窗内。
- **底层原因**：现代前端模态弹窗（如 Radix UI / Shadcn Dialog）在居中或入场时带有 `transform`（如 `translate(-50%, -50%)` 或 `scale(0.95)`）。根据 W3C CSS Transforms 规范，**任何带有非 `none` 的 `transform` 祖先元素都会成为新的绝对包含块**，强制导致子孙元素的 `background-attachment: fixed` 退化为相对于该弹窗的局部 `scroll`。`background-size: cover` 遂把整张壁纸等比压缩进几百像素的弹窗内。

### 陷阱 B：宽泛选择器误伤陷阱（为什么次级侧边栏会变黑）
- 曾尝试通过全局选择器清空导航包装层背景（如 `[class*="border-sidebar-border"]`），但由于 Tailwind 的类名复用，Subagents、Background Tasks 等抽屉侧边栏也带有该类名，导致全局背景被误伤剥离、变成纯黑。
- **铁律**：选择器必须严格限定作用域（如 `:has(button[data-testid^="settings-nav-item-"])`），严禁跨界消杀。

### 陷阱 C：入场缩放动画坐标抖动陷阱（为什么会“小跳跃”）
- **现象**：弹窗刚唤出时坐标有微小偏差，随后突然瞬移跳回正常位置。
- **底层原因**：弹窗入场带有缩放动画（`scale(0.95) -> scale(1.0)`）。在动画播放期间读取 `getBoundingClientRect()`，左上角因被缩小而向内缩了约 20 像素。若使用延迟计时器（`setTimeout`）在动画收敛后再更新坐标，就会触发一次肉眼可见的“二次瞬移”。

---

## 2. 解决方案：取景框数学切片映射 (Windowing Slicing)

放弃浏览器在 transform 下失效的 `fixed`，转为**直接使用数学精确推导并反向投射**：

### 算法实现：
1. **探测原图物理分辨率**：通过内存中常驻的 `Image` 对象获取壁纸真实 `naturalWidth` 和 `naturalHeight`；
2. **推导全局 Cover 物理尺寸与中心裁切量**：
   ```javascript
   const aspectWin = W / H;
   const aspectImg = bgNaturalWidth / bgNaturalHeight;
   if (aspectWin > aspectImg) {
       renderW = W;
       renderH = W / aspectImg;
       originX = 0;
       originY = (H - renderH) / 2;
   } else {
       renderW = H * aspectImg;
       renderH = H;
       originX = (W - renderW) / 2;
       originY = 0;
   }
   ```
3. **几何中心不变性 (Invariant Center Math) 杜绝跳跃**：
   利用无论弹窗如何缩放、几何中心点永恒不变的物理特性，在第 0 毫秒直接算得静止态真实坐标：
   ```javascript
   const layoutW = (target.offsetWidth && target.offsetWidth > 100) ? target.offsetWidth : rect.width;
   const layoutH = (target.offsetHeight && target.offsetHeight > 100) ? target.offsetHeight : rect.height;
   const centerX = rect.left + rect.width / 2;
   const centerY = rect.top + rect.height / 2;
   const restingLeft = Math.round(centerX - layoutW / 2);
   const restingTop = Math.round(centerY - layoutH / 2);

   const posX = Math.round(originX - restingLeft);
   const posY = Math.round(originY - restingTop);
   ```
4. **CSS 注入与定格**：
   ```css
   .leviosa-settings-dialog-card,
   #root div:has(> div[style*="container-type: size"] button[data-testid^="settings-nav-item-"]),
   #root [role="dialog"]:has(button[data-testid^="settings-nav-item-"]),
   #root div[style*="container-type: size"]:has(button[data-testid^="settings-nav-item-"]) {
       background-image: var(--antigravity-bg) !important;
       background-size: var(--settings-bg-size, 100vw 100vh) !important;
       background-position: var(--settings-bg-pos, center center) !important;
       background-repeat: no-repeat !important;
       background-attachment: scroll !important;
       overflow: hidden !important;
       animation: none !important;
       transition: background-position 0s, background-size 0s !important;
   }
   ```
5. **移除延迟定时器**：仅在挂载时同步计算一次，并跟随单次 `requestAnimationFrame` 保证布局闭环，彻底实现零延迟、零跳变。
