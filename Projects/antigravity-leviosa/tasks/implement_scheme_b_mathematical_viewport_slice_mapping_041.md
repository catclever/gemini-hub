---
id: implement_scheme_b_mathematical_viewport_slice_mapping_041
title: 实现方案B：设置面板取景框数学切片映射(1:1视口同轴无缩放)
status: completed
priority: high
tags: []
session: fba8eb14-e6fb-4b79-a186-9eb1a0f0fda6
---

# 实现方案B：设置面板取景框数学切片映射(1:1视口同轴无缩放)

## 变更概述
鉴于Chromium规范中模态弹窗的局部transform会强制破坏background-attachment: fixed并退化为局部cover缩放，落地方案B：自动探测壁纸自然宽高与窗口宽高，以数学严密推导的renderW/renderH与负坐标偏移(origin-rect)动态注入--settings-bg-size与--settings-bg-pos，使设置弹窗以取景框方式1:1无缩放呈现全局壁纸。

## 验证结论
- [x] 核心逻辑已实现并通过验证
