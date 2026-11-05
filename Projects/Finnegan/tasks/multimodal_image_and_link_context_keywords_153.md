---
id: multimodal_image_and_link_context_keywords_153
title: Upgrade Keyword Engine with Multimodal Image Recognition and In-Card URL Context
  Perception
status: in_review
priority: high
tags:
- backend
- keywords
- multimodal
- jina
session: 76a131c7-7c91-4893-befe-a4882d5f46df
---

## 任务目标与背景
升级 Finnegan 卡片认知与实心锚点提取引擎（core/keywords），支持多模态图片理解与卡片内嵌网页链接感知：
1. 当卡片包含附图（images: [...]）时，从 <home>/assets/ 读取图片流传入 Gemini 3.8 Flash，融合图文提取 4 维实心锚点，并生成 visual_summary 写入 frontmatter（为本地搜索与布谷离线预索引，彻底避免运行时识别开销）；
2. 当卡片正文包含 URL 时，通过内置 Jina Reader 或 HTTP 轻量拉取前 1500 字符纯净正文摘要（限时 3s），作为背景参考传入 Gemini，提炼精准技术/主题锚点；
3. 将 finnegan.yml 中的 default LLM 临时切换为正常返回的 satan_gemini key（AIzaSy...），使后台异步提取恢复工作；
4. 对 gemini是懂梗的~（带2图）与 super_agent（带GitHub链接）两张历史卡片执行回填验证。

## 涉及核心文件
- ~/Library/Application Support/Finnegan/finnegan.yml: 更新 default key
- core/keywords/types.go: 扩展数据结构（如 ImageData、VisualSummary 等）
- core/keywords/engine.go: 升级 GeminiLLMClient 支持 genai.ImageData 多模态输入，构建融合 Prompt 与单次输出解析
- core/keywords/fetcher.go (或 link.go): 嗅探正文 URL，3s 软超时轻量获取 Jina/网页 Markdown
- core/keywords/frontmatter.go: 无损回写 visual_summary 与 keywords 到 YAML Frontmatter
- app_capture.go / app_events.go: 确保传递卡片图片与完整路径
- 单元测试与卡片回填验证脚本

## 交付验收清单
- [ ] finnegan.yml 切换 default key 并验证 generateContent 正常响应
- [ ] core/keywords 多模态图片读取与 Prompt 组装通过自动化测试
- [ ] core/keywords 网页 URL 嗅探与 3s 软超时摘要抓取通过自动化测试
- [ ] gemini是懂梗的~ 回填验证：成功提炼图文融合实心锚点并生成 visual_summary
- [ ] super_agent 既然提到了存算分离 回填验证：成功读取 Dalembert 仓库背景并提炼精准实心锚点
