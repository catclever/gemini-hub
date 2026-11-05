---
title: "Finnegan UI/UX 核心视觉规范"
date: 2026-10-10
status: active
---

# UI / UX 核心视觉规范 (The Cyber-Memex Interface)

## 1. 窗口材质 (The Canvas)
- **拒绝全透明 / 拒绝不透明**：采用 macOS 原生的 **高透明度毛玻璃 (Frosted Glass / Vibrant Material)**。
- **技术实现**：Wails `Mac.WindowIsTranslucent = true` + CSS `backdrop-filter: blur()`. 既能透出桌面壁纸保持呼吸感，又能保证文字的绝对可读性。

## 2. 卡片姿态 (The Scattering)
- **动态倾斜 (Dynamic Tilt)**：在处于“散落待机态”时，允许卡片拥有极具视觉冲击力的狂野倾斜（可达 `±15° ~ ±30°`），营造极致的混沌与艺术感。但在“交互聚焦态”（鼠标悬停或点击）时，卡片会伴随丝滑的动画瞬间**旋转回正（0°）并放大**，完美兼顾视觉震撼与阅读体验。
- **Z 轴景深 (Depth of Field)**：利用层级关系营造 3D 空间感。位于最上层（聚焦中）的卡片保持 100% 实心纯白；而被压在底层、靠后的卡片，随着 Z-index 的降低，颜色逐渐泛灰，并带有一定比例的透明度（Opacity）和极其轻微的模糊。
- **重叠与截断**：卡片允许 Z 轴部分重叠；内容过长时使用 CSS 渐隐截断，不强制撑开卡片，保持整体错落有致。

## 3. 中枢布局 (The Nucleus)
- **绝对居中**：操作框 (Omnibar) 悬浮于屏幕正中央。
- **引力交互**：搜索、点击标签时，相关卡片向中心输入框聚拢，无关卡片向四周渐隐退散。
