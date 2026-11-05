# Eagle Feed Channel Architecture & Specifications

## 1. Overview
`eagle_feed_channel`（📻 灵感电台）是一个专为 Eagle 4.0+ 桌面素材管理软件设计的官方规格多频道网络壁纸管理插件。
具备以下核心特性：
- **个人网络收藏夹管理（Collections）**：原生支持 Wallhaven 个人收藏夹与关键词检索，配置 Wallhaven API Key 后可一键拉取账号下的全部公开/私密收藏夹，生成对应独立频道。
- **灵感电台 / 随心看**：通过 Fisher-Yates 洗牌算法打散图片，支持单次拉取 10-100 张随机图，配合 Eagle 原生看图与瀑布流体验。
- **频道独立分级目录**：在 Eagle 中自动建立「📻 灵感电台 / <频道名>」树状隔离目录结构，并支持按 `feed:<channel_id>` 专属标签沉淀。
- **关掉即焚（Self-Destruct）**：当用户在面板停用或清空频道时，联动 Eagle `item.moveToTrash` API 瞬间粉碎清空该频道的本地下载缓存图片（频道配置安全保留在列表中随时可重新激活）；只有点击“删除此频道”才会彻底移除该频道。
- **隐私隐藏频道（Incognito）**：支持将特定频道设为隐藏频道，需输入主密码（SHA-256 哈希加密持久化校验）方可临时解锁（🔒/🔓），防止敏感图片被随意窥探。
- **API Key 凭证与配置持久化**：API Key 与频道增删改查、排序、配置偏好自动写入本地存储（`localStorage` / `eagle.storage`），重载插件不丢失。

## 2. Directory Layout
- Workspace Root: `/Users/kael/Projects/eagle_plugin`
- Plugin Directory: `eagle_feed_channel/`
  - `manifest.json`: Eagle 4.0+ 插件清单定义（ID: `com.eagle.feed.channel`）
  - `package.json`: Node.js ES module 模块配置与测试脚本
  - `src/providers/wallhaven.js`: Wallhaven REST API 适配器（集合拉取 `/collections`、集合壁纸拉取、`/search` 关键词搜索、洗牌算法、错误分类处理）
  - `src/core/channel_manager.js`: 频道状态机（CRUD、配置持久化、自定义排序、密码加密哈希与验证）
  - `src/core/eagle_bridge.js`: Eagle 资产桥接引擎（自动建树、画质分流、流式进度追踪、下载异常断点隔离、停用即焚粉碎）
  - `src/ui/`: 前端界面层（现代化暗黑原生风格）
    - `index.html`: 控制面板主体、设置中心（API Key 管理）、双模式建频模态窗
    - `styles.css`: Eagle 4.0 原生视觉暗黑样式、平滑进度条、响应式卡片、Tab 切换器
    - `app.js`: 前端控制器（事件绑定、流式同步、模态窗生命周期、密码弹窗、收藏夹拉取联动）
    - `ui_helpers.js`: 纯函数业务逻辑辅助库（表单校验、API Key 脱敏校验、画质翻译、进度计算、HTML 安全转义）
  - `tests/`: 自动化测试套件（使用 Node 22 原生 `node:test` 与 `node:assert`，零外部依赖）
    - `wallhaven.test.js`: Wallhaven 适配器、搜索与收藏夹接口测试
    - `channel_manager.test.js`: 频道管理、排序、验证、生命周期与持久化测试
    - `eagle_bridge.test.js`: 资产同步、断点容错、目录生命周期与关停即焚测试
    - `ui_helpers.test.js`: 前端纯函数、API Key 校验与状态辅助方法测试
    - `mocks/eagle_mock.js`: Eagle 插件 API 内存无头 Mock 层

## 3. Remote Development & Verification
- PVE Mirror: `/root/Projects/eagle_plugin`（双向同步：Mutagen `eagle-plugin`）
- Verification Command: `npm test`（运行 `node --test eagle_feed_channel/tests/**/*.test.js`）
- Test Metrics: **31 测试套件、120 项单元测试 100% PASS**（Mac 本地与 PVE 端均完全对齐）
