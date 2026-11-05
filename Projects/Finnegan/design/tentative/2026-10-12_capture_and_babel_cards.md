# Card Capture & Bugu Babel Integration

## 1. 目标
打通“用户输入 -> 生成实体卡片 -> 触发 Bugu -> 生成巴别塔临时卡片”的完整数据流，并区分卡片类型体系。

## 2. 需求拆解

### 2.1 清理测试卡片
- 前端和后端移除所有用于早期排版的 Mock 卡片和硬编码数据。
- 确保界面启动时，只有真实读取的实体卡片。

### 2.2 基础卡片入库 (碎碎念卡片 / Thought Card)
- **前端**：在顶部的 Omnibar 输入框中输入文字，按回车或点击确认按钮，触发后端的入库逻辑。
- **后端**：复用并调整现有的 `CaptureThought` 方法。
  - 写入的 Markdown 文件头部增加 `type: thought`。
  - 卡片模型 (`Card` struct) 增加 `Type` 字段映射。
- **暂缓**：前端的输入框暂不触发实时的“检索”匹配逻辑，仅作纯粹的入库收集器。

### 2.3 触发 Bugu 与异步流
- 当 `CaptureThought` 成功落盘后，Go 后端异步启动 Bugu 模块（不阻塞前端入库的响应）。
- Bugu 接收到用户刚才输入的“碎碎念”文本作为 `intent`，开始执行检索流（SearxNG -> Jina）。

### 2.4 巴别塔卡片 (Babel Card) 的生成
目前的 Bugu (Jina) 会返回网页的全文 Markdown，直接做成卡片不仅难看而且信息过载。我们需要对 Bugu 的后处理环节进行大模型提纯。
- **大模型提纯 (LLM Extraction)**：Bugu 拿到网页全文后，调用 `core.LLM`，根据用户的 `intent`，从全文中提取最相关的一段话（字数受控）。
- **生成结构化数据**：
  - `original_text`: 提取出的外文原文片段。
  - `translated_text`: 对应的精准中文翻译。
  - `source_url`: 来源网站链接。
- **注入临时池**：Bugu 将上述数据封装为 `type: babel` 的临时卡片，注入到 `CardManager` 的 `tempCards` 内存池中。
- **前端展现**：前端轮询或通过事件监听到新的临时卡片，渲染出 Babel 专属的 UI 样式（双语对照 + 来源链接）。

## 3. 前后端接口规约调整
- `Card` 结构体：
  ```go
  type Card struct {
      ID      string
      Type    string // "thought" | "babel"
      Title   string
      Content string // 对于 thought 来说就是内容
      
      // 巴别塔专属字段 (存在 Frontmatter 里，或者 JSON 里)
      OriginalText   string
      TranslatedText string
      SourceURL      string
  }
  ```
