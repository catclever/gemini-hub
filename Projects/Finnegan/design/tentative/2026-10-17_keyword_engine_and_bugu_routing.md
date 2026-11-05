---
date: 2026-10-17
title: Built-in 多维关键词认知引擎与 Bugu 谱系驱动路由架构设计
status: tentative
---

# Built-in 多维关键词认知引擎 (`keywords`) 与 Bugu 谱系路由架构

## 1. 核心设计哲学

1. **认知与执行彻底解耦**：
   - **关键词模块 (`keywords`)** 是“认知官/理解者”：只在本地卡片（永久 `.md` 文件）生成时触发，负责理解卡片内容、门控筛选适用的维度，并按各维度专属逻辑提取结构化关键词，持久化写入 Markdown 的 YAML Frontmatter。
   - **Bugu 模块 (`bugu`)** 是“执行者/猎手”：不再直接生啃卡片长文猜意图，而是读取卡片 Frontmatter 中涌现出的 `keywords` 谱系，根据不同关键词类型的组合，动态决定去哪些类型的网站（Target Tags）、用什么句式搜索（Query Style）、以及要求什么级别的时效性（`time_range`）。
2. **反死板分类，由关键词谱系自然涌现卡片性格**：
   - 卡片不设 `category` 字段。一张卡片长出了哪些维度的关键词（如 `entity + symptom` vs `emotion + metaphor`），自然就定义了它此刻的灵魂切片。
3. **维度百花齐放 + 用户自由开关 + LLM 严格门控**：
   - 系统内置丰富的关键词维度库（10+ 种），用户可在配置中自由激活/关闭任意维度。
   - 对单张卡片，LLM 执行 **Salience Gating（显著度门控）**：哪怕用户开启了 10 个维度，一张纯技术报错卡也只会点亮 2 个相关维度，绝不无脑硬凑。

---

## 2. 内置关键词维度全景词典（10 大可选维度）

| 维度 ID | 维度名称 | 门控触发条件 (When to Activate) | 专属提取逻辑 (How to Extract) | Bugu 站点偏好 & 时效策略 (`time_range`) |
| :--- | :--- | :--- | :--- | :--- |
| **`entity`** *(默认开)* | **专用名词 / 实体** | 出现特定技术栈、协议、软件、学术概念、特定流派或专有黑话 | **原教旨高保真**：保留精确术语、版本号、原名（如 `WebKitGTK 4.1`），严禁上位词泛化 | 技术文档、Wiki、GitHub、垂直社区 \| **时效：`year`** |
| **`event`** *(默认开)* | **事件 / 动态** | 提及正在发生的行业动态、版本发布、社会/圈层事件或具体变动 | **主体+动态锚定**：提取“谁/什么 + 发生了什么变化”的紧凑短语 | 新闻源、HN、Reddit、V2EX、Telegram \| **时效：`month` / `week`** |
| **`judgment`** *(默认开)* | **判断 / 命题** | 蕴含鲜明的观点、价值判断、批判、或者二元对立的思考张力 | **张力命题化**：转化为可激发深度辩论的思辨命题或反常识切口（如 `Local-First 的同步悖论`） | 独立博客、Substack、LessWrong、少数派、豆瓣长评 \| **时效：`all` 或 `year`** |
| **`emotion`** *(默认开)* | **情绪 / 心境** | 流露出明显的情感基调、生存境遇体验、深夜独白或心境状态 | **去临床化切片**：禁用“焦虑/抑郁”等医学词，提取具象生活与心境短语（如 `深夜独自排错的宁静感`） | 豆瓣小组/日记、Reddit 人文版块、IndieWeb 随笔 \| **时效：`all`（永恒共鸣）** |
| **`question`** *(默认开)* | **待解问题 / 求索** | 存在明确的困惑、悬而未决的疑问、方案选型纠结或求助意图 | **How/Why 问题重构**：提炼为社区高信息密度的提问式短语 | StackOverflow、Reddit、V2EX 问与答、知乎/Quora \| **时效：`year`** |
| **`metaphor`** *(默认开)* | **隐喻 / 意象** | 包含独特的文学修辞、通感、哲学意象、梦境碎片或美学符号 | **意象结晶**：保留核心隐喻体与美学意象组合（如 `数字废墟中的苔藓`、`赛博招魂`） | 文学/艺术社区、豆瓣、独立博客、哲学板块 \| **时效：`all`** |
| **`symptom`** *(可选开)* | **异常 / 踩坑现象** | 描述具体的 Bug 表现、诡异报错、性能劣化或反常物理/系统现象 | **高区分度特征**：提取核心错误特征码、环境条件与异常表现 | GitHub Issues、论坛踩坑帖、Arch/Debian 社区 \| **时效：`year` / `month`** |
| **`methodology`** *(可选开)* | **方法论 / 范式** | 探讨工作流、思维模型、架构模式、效率实践或做事法则 | **范式提炼**：提取为“X 驱动的 Y”、“Z 工作流/原则”结构 | 极客博客、PKM 社区、Obsidian/Roam 论坛、少数派 \| **时效：`year` / `all`** |
| **`counter_intuitive`** *(可选开)* | **反直觉 / 悖论** | 揭示某种常识背后的荒谬、事与愿违的规律或讽刺现象 | **悖论对比式**：提取出“表面 A 实则 B”的核心冲突词 | LessWrong、HN 深度串、哲学/社科评论 \| **时效：`all`** |
| **`person_work`** *(可选开)* | **人物 / 作品坐标** | 提及特定作者、思想家、导演、书籍、论文、电影、播客或开源作品 | **精确书名/人名对齐**：提取标准译名与原名对 | 豆瓣书影音、Goodreads、ArXiv、学术/文化评论 \| **时效：`all`** |

---

## 3. 数据流与生命周期设计

### 3.1 触发时机：仅在本地永久 `.md` 卡片生成时触发
1. **统一监听入口**：
   - 无论通过 `CaptureThought`、`CaptureThoughtWithImages`、`CaptureChatLogWithImages` 还是将临时卡 `PromoteToLocal` 转为本地卡，最终都会在 `<home>/Scattering/`（或 `Weaving/`）生成永久 `.md` 文件，并由 `GlobalWatcher` 或 Capture 流程发出事件。
   - 关键词引擎监听本地卡片创建事件（排除 `origin == "keywords"` 以防循环，且忽略纯内存临时卡 `tempCards`）。
2. **LLM 门控提取与 Frontmatter 回写**：
   - 关键词引擎读取卡片正文，结合用户当前开启的 `enabled_dimensions`，调用 Gemini 进行一次性门控识别与提取。
   - 提取完成后，使用 `GlobalWatcher.WriteFile(filePath, updatedContent, "keywords")` 将 `keywords` 字典无损合并写入该 `.md` 文件的 YAML Frontmatter：
     ```yaml
     ---
     id: 01J...
     type: thought
     created: 2026-10-17T14:50:00+08:00
     keywords:
       entity:
         - SearxNG
         - PageRank
       judgment:
         - 默认权重排序导致搜索引擎无法发现最新社区讨论
       question:
         - 元搜索引擎如何平衡内容时效性与讨论深度
     ---
     ```
   - 同时在 EventBus 上广播 `EventKeywordsExtracted` 事件（携带 `DocID`, `Keywords`, `Body`），通知前端刷新卡片元数据并触发下游模块（如自动或手动等待的 Bugu）。

### 3.2 Bugu 消费关键词谱系的全新工作流
当对某张本地卡片执行 `/bugu`（或自动触发雷达）时：
1. **读取关键词谱系**：
   - 优先直接读取卡片 YAML Frontmatter 中的 `keywords` 字段（零重复提取开销）。
   - *兜底机制*：如果是历史遗留老卡片（Frontmatter 中尚无 `keywords`），则先实时调用一次 `KeywordEngine.ExtractAndSave(docID)`，拿到谱系后再继续。
2. **谱系驱动的多支线搜索规划 (`GenerateFacetSearchPlan`)**：
   - Bugu 将卡片的 `keywords` 谱系（例如含有 `event` + `judgment`）连同 `radar_targets.yml` 传给路由规划器：
   - **差异化站点选型**：根据存在的关键词维度，匹配对应调性的站点（如 `event` 匹配新闻/即时论坛，`judgment` 匹配深度博客/人文站）。
   - **差异化多语言 Query 转化**：
     - 针对 `entity` / `symptom`：转化为精准原生术语组合；
     - 针对 `judgment` / `question`：转化为社区母语的探讨句式/争论焦点的表达；
     - 针对 `emotion` / `metaphor`：转化为母语文化圈下的共鸣表达。
   - **差异化时效注入 (`time_range`)**：
     - 在生成的每个子搜索任务（SearchTask）上附带 `time_range` 属性（`"week"` | `"month"` | `"year"` | `""`）。
     - `SearxNGClient.Search(query, target, timeRange)` 在请求 URL 中动态拼接 `&time_range=month` 或 `&time_range=year`，彻底解决“搜不回最新内容”的顽疾，同时又不误伤需要跨时间沉淀的“情绪/判断/隐喻”类搜索！
