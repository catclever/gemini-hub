---
id: scattered_markdown_render_breaks_147
title: 散落态卡片支持 Markdown 紧凑换行渲染并保持列表行内流
status: completed
priority: medium
tags: []
session: 3b81dfaf-55b0-49c9-afb0-ff758080dc29
---

# 散落态卡片支持 Markdown 紧凑换行渲染并保持列表行内流

## 变更概述
在 MarkdownContent.svelte 中启用 marked breaks 配置，允许散落态卡片自然渲染段落与换行；设置紧凑段落间距并保持列表项（ul/ol/li）行内圆点流以节省卡片空间。

## 验证结论
- [x] 核心逻辑已实现并通过验证
