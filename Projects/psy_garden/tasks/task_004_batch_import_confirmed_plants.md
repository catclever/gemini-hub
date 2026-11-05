---
id: task_004_batch_import_confirmed_plants
title: 'Task 004: 批量入库确认的植物草稿资产'
status: backlog
priority: medium
tags: []
---
# Task 004: 批量入库确认的植物草稿资产

- **状态**: completed
- **完成时间**: 2026-10-19
- **类型**: 资产批量处理 / 自动化切片入库

## 任务背景与目标
公主在 Botanist Studio 中挑选并确认了 40 款白底/候选植物草稿图片，要求将其自动化批量入库并切片生成资产，以验证切片和通道拆解效果。

## 执行过程与技术细节
1. **数据清洗与分析**:
   - 读取 `tools/confirmed_candidates.json` 中选中的 45 个条目；
   - 发现其中 40 款为独立草稿图片，5 个为指向已有 `candidate_plant_plant_...` 文件的软链接（自动去重并安全移除）；
   - 从文件名自动解析出标准语义标识符（如 `plant_0353`）与中文别名（如 `翠錦竹芋`）。
2. **多变体管理与去重 (Variants Management & Deduplication)**:
   - 针对同种植物的多张草稿，自动按顺序生成变体编号归入同名物种目录下；
   - 经 MD5 哈希严格比对，排查发现有 5 款植物（`孔雀竹芋`、`秋水仙`、`牛至`、`牛眼馬錢`、`光果苏铁`）因历史脚本生成了包含 `candidate_plant_plant_...` 双重前缀的文件副本，与无双重前缀的图片完全一致。现已完成精简清理，剔除多余的重复变体（保留高质量 Variant 01）；
   - 而 `鵝鑾鼻燈籠草`（`plant_0071`）的两张草稿经校验确为截然不同的形态画作，正常保留变体 `01` 与 `02`。
3. **自动化切片打包 (`tools/batch_import_confirmed.py`)**:
   - 自动检测并支持白底抠图（`WHITE` 背景检测）与平滑边缘混合；
   - 自动按 RGB 权重拆解为 Red 通道（花叶/顶盖）、Green 通道（茎枝/主干）、Blue 通道（细节/点缀）；
   - 生成各图层 PNG 及 `metadata.json`；
   - 自动向 `src/styles.css` 注入各变体的 CSS 像素渲染规则；
   - 原草稿图片自动安全归档至 `tools/candidates/processed/` 避免备选池混杂，已确认清单清空闭环。
4. **Git 与环境同步**:
   - PVE 端完成全量资产、CSS 与脚本的 Git 提交：`843617a feat: batch import 40 confirmed plant candidates into asset library`；
   - Botanist Studio (端口 18087) 与 Web Preview (端口 18088) 实时刷新可用。
