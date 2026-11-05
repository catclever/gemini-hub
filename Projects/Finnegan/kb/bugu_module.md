# Bugu (不孤) - The Global Consciousness Stream Radar

## 1. 模块定位
**Bugu (不孤)** 是 Finnegan 生态系统下的一个核心信息侦察模块。
它并非一个常规的搜索引擎，而是一个基于大模型（LLM）意图解析与高并发无头浏览器结合的“多语种暗网/极客圈信号捕捉器”。它能够打破语言屏障，将用户的搜索意图（Intent）转化为多国语言，并精准潜入全球特定社区（如俄罗斯黑客论坛、德国混沌计算机俱乐部等）抓取最硬核的一手观点，最终剥离出纯净的 Markdown 喂给系统。

## 2. 核心架构与依赖
Bugu 作为一个标准模块，通过 `init()` 注册进入 Finnegan Core，并暴露给 Wails 前端使用。

### 底层技术栈
1. **智能路由 (LLM Router)**：默认依赖 `gemini-3.8-flash`，使用 `google/generative-ai-go/genai` 官方 SDK。负责将自然语言意图转译为多语种的精准搜索词（Structured JSON Output）。
2. **侦察天线 (SearxNG Fetcher)**：并发请求私有部署的 SearxNG 引擎（要求开启 JSON format），实现免验证码的特定网站 (`site:`) 深网检索。
3. **内容剥壳机 (Jina Reader API)**：并发调用 `r.jina.ai`，剥离目标网页的复杂 HTML/SPA 渲染，提取最高信噪比的纯文本 Markdown。

## 3. 使用方法与 Wails 接口
前端 Svelte 可以直接调用 Bugu 暴露在全局对象上的方法：

### `window.go.bugu.BuguBinding.RunRadar(intent string) RadarResponse`
- **入参**：自然语言意图（例如："我想了解全球极客对 LLM 数据隐私的反制手段"）。
- **出参**：`RadarResponse` 包含 `status` 和 `results`。`results` 是一个字符串数组，每个元素是一篇抓取完成的纯 Markdown 正文。
- **执行流**：意图分析 -> 并发 SearxNG 搜索 -> 提取链接 -> 并发 Jina 解析 -> 聚合返回。

### `window.go.bugu.BuguBinding.GetRadarTargets() []models.Target`
- **功能**：读取并返回当前加载的靶标矩阵列表（共计 530+ 个精选源）。

## 4. 四层配置结构 (4-Tier Config)
Bugu 严格遵守 Finnegan 的配置注入规范。
在运行时，它的配置按照以下优先级（4为最低，1为最高）覆盖生效：

1. **全局主配置 (Tier 1)**: `~/Library/Application Support/Finnegan/finnegan.yml` (或由其 `override_config` 指向的 `<home>/.finnegan/config.yml`，Finnegan Core 解析注入)
2. **模块私有配置 (Tier 2)**: 模块目录下的 `bugu.yml`
3. **环境变量 (Tier 3)**: 运行时的环境注入 (`GEMINI_API_KEY`, `JINA_API_KEY`, `SEARXNG_URL`)
4. **代码硬编码默认值 (Tier 4)**: 兜底数据

### 推荐的全局配置示例 (`~/Library/Application Support/Finnegan/finnegan.yml`)
Core 支持单大模型声明（`llm:`）或多模型矩阵（`llms:`），并已在底层对 YAML 命名风格（`api_key`, `apiKey`, `key` 等）做了自适应反序列化：

```yaml
# 方式 A：单模型简洁配置
llm:
  provider: "gemini"
  api_key: "AIzaSy..."             # 给 LLM Router 解析意图使用
  default_model: "gemini-3.8-flash"

# 或 方式 B：多模型配置
llms:
  default:
    provider: "gemini"
    api_key: "AIzaSy..."
    default_model: "gemini-3.8-flash"

bugu:
  searxng_url: "https://searx.cathouse.host"  # 您私有部署的 SearxNG 地址
  max_concurrency: 10                         # 针对 Jina 和 SearxNG 的高并发阈值
  target_language: "Chinese"                  # 巴别塔卡片提纯的目标语言
  llm_id: "default"                           # 绑定 llms 中的模型 ID
  jina_api_key: "jina_xxx..."                 # 可选：解锁 Jina Reader 的高并发商用额度
```

### 隐藏的环境变量配置
如果在极端高并发下受到限流或未在配置文件中明文写 key，可在系统级别额外注入：
- `export GEMINI_API_KEY="AIzaSy..."`
- `export JINA_API_KEY="jina_..."`
- `export SEARXNG_URL="http://..."`

## 5. 靶标矩阵数据 (radar_targets.yml)
Bugu 依赖于项目目录下的 `modules/bugu/radar_targets.yml`（代码已自适应检索 `modules/bugu/`、`bugu/` 与根目录）。
该文件按照 `id`, `name`, `type`, `languages`, `value` 等维度，静态定义了全球极客、科技、安全、深度小众等 530 余个高价值信息源。这是 Bugu 的“雷达字典”，不可或缺。

## 6. 前端专属雷达与光纤网络 (Bugu Ray Network & Beacon)
遵循“零污染”的模块化前端原则，所有雷达与光线相关的代码 100% 收敛于 `frontend/src/modules/bugu/` 目录：
- `theme.ts`: 琥珀金（`#F59E0B`）霓虹主题常量与衰减时间参数。
- `types.ts`: `BuguSession` 会话契约（`sourceCardId`, `targetCardIds`, `status`）。
- `BuguRadarBeacon.svelte`: 空间雷达发射源，在母卡下方以同心圆弧向深空发射雷达脉冲波。
- `BuguRayNetwork.svelte`: 3D 激光光纤层，在母卡与新发现的巴别塔卡片之间实时绘制带发光滤镜和光子流动的有机三阶贝塞尔光纤。
- **插槽挂载**：在 `CosmicStage.svelte` 内部通过 `{#if buguSession}` 纯条件插槽按需挂载。平时为 0 DOM、0 渲染开销。会话结束后 25 秒自动平滑退火隐入深空。
