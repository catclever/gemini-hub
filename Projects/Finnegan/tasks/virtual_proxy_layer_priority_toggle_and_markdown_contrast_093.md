---
id: virtual_proxy_layer_priority_toggle_and_markdown_contrast_093
title: 虚拟卡位与聚焦卡层级动态切换与白底Markdown文字对比度修复
status: completed
priority: high
tags:
- virtual-proxy
- focus
- layer-priority
- markdown
- typography
session: 58c97e35-a614-4542-ad8d-16f08d35616c
---

# 虚拟卡位与聚焦卡层级动态切换与白底Markdown文字对比度修复

## 变更概述
完成虚拟卡位两大核心体验优化：
1. 虚拟卡位与聚焦卡层级优先级自由切换：
   - 默认进入聚焦时聚焦卡在前（z-index: 1000, translateZ: 120px），遮挡虚拟卡角落，保障主阅读区文字 0 遮挡；
   - 点击虚拟卡时，虚拟卡平滑抬升至最前端（z-index: 1005, translateZ: 125px），完整呈现虚拟母卡/子卡详情；
   - 点击聚焦卡任意位置时，瞬间让位恢复聚焦卡在前（虚拟卡回退至 z-index: 995, translateZ: 116px，依然在背景遮罩 112px 之上）；
   - 双击虚拟卡依然平滑将焦点完整切换至该卡片。
2. 修复图片卡片文字不可见与遮挡问题：
   - 根因定位：MarkdownContent 与 VirtualCardProxy 缺少深色文本继承，在 body { color: white } 的全局样式下继承了白字，与卡片白色毛玻璃背景重合导致文字隐形；
   - 修复方案：为 VirtualCardProxy 注入 --card-text-color: #1e293b 与完整深色规范，重构 MarkdownContent 的段落、标题、链接、引用块（柔和深灰与淡边框）与代码块样式；
   - 布局防撑破：对虚拟卡内图片增加 max-height: 180px 约束，开启卡内自然滚轮滚动（pointer-events: auto），确保文字与配图均完美清晰呈现。

## 验证结论
- [x] 核心逻辑已实现并通过验证
