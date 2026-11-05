---
id: botanist_studio_two_phase_ai_analysis_025
title: Botanist Studio 双阶段入库流与 OpenAI 兼容植物生物学 AI 分析
status: completed
priority: high
tags:
- botanist_studio
- ai_analysis
- pipeline
- ui
session: 5d790e93-04e6-43ef-b03b-bd7f64dac343
---

# Botanist Studio 双阶段入库流与 OpenAI 兼容植物生物学 AI 分析

## 任务目标与背景
1. 配置文件: 留出 `tools/ai_config.json` (含 url, key, model，key 允许为空，支持 OpenAI 兼容直接 HTTP 请求)。
2. 后端双阶段服务:
   - 阶段 A (切图): candidate 移入资产目录并执行真彩切图 (生成 layer_red/green/blue 等及基础 metadata)。
   - 阶段 B (AI 生物体量分析): 请求 OpenAI 兼容接口，解析植物学真实高度范围、游戏映射高度范围、形态分类等，写入 metadata.json。
3. 前端交互状态演进:
   - 点击入库后，候选卡片立即移动至右侧资产区，初始呈现灰色禁用态，标注文案为【切图中】。
   - 切图完成后，更新为半可用态（支持点击卡片打开详情弹窗预览图层），状态标记为【AI分析中】。
   - AI 分析完成后，状态恢复正常并可在详情弹窗中查看 AI 生物体量与高度范围测算结果。
4. 已有资产保持现状，待新管线验证跑通后后续批量处理。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
