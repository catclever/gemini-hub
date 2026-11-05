# 卡片长文本渲染设计 (Card Overflow & Expansion)

## 1. 痛点
在“一切皆卡片”的 3D 散落态（Scattering）宇宙中，如果一张卡片是一篇 3000 字的长文，或者大模型提取的原文过长，直接渲染撑开会导致卡片像一根极长的面条，严重破坏空间排版和视觉美感。

## 2. 状态分级设计 (Scattered vs Focused)

我们需要根据卡片当前的**聚焦状态**，动态改变它的高度限制和文本裁切策略。

### 2.1 散落态 / 悬浮态 (Scattered & Hovered)
- **视觉目标**：像实体卡片一样，保持大致均匀的尺寸，维持 3D 视野的秩序感。
- **技术实现**：
  - 为卡片正文容器（`.card-content`）设置 `max-height`（如 `200px`）。
  - 使用 CSS 的 `-webkit-line-clamp: 6` 进行多行文本截断。
  - 末尾自动显示省略号 `...`，暗示还有更多内容。
  - 隐藏滚动条（`overflow: hidden`）。

### 2.2 聚焦态 (Focused)
- **视觉目标**：当用户点击卡片，卡片通过 Svelte Spring 被拉近到镜头前（`translateZ(200px)`）时，卡片应该解除束缚，允许用户阅读全部内容。
- **技术实现**：
  - 解除行数限制（`-webkit-line-clamp: unset`）。
  - 卡片高度根据内容自适应展开，但设置一个极值 `max-height: 80vh`（不超过屏幕高度的 80%）。
  - 出现优雅的垂直滚动条（`overflow-y: auto`），允许用户在聚焦的卡片内部上下滚动阅读长文。

## 3. CSS 核心代码预览

```css
/* 默认散落态：最多显示 6 行 */
.card-content {
  display: -webkit-box;
  -webkit-line-clamp: 6;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  transition: all 0.3s ease;
}

/* 聚焦态：解除限制，支持滚动 */
.card.is-focused .card-content {
  -webkit-line-clamp: unset;
  overflow-y: auto;
  max-height: 60vh;
  padding-right: 8px; /* 留出滚动条空间 */
}
```
