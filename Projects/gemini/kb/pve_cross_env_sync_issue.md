# 跨端协同架构已知问题：远端会话隐身与路由抢夺

**Status**: 已探明底牌 (Architectural Constraint Reached)
**Tag**: PVE, Mutagen, Distributed-State, Backend-Routing

## 第一阶段：会话隐身与“孤儿”问题 (已解决)
在通过 Mutagen 双向同步 `.gemini` 数据目录后，最初 PVE 的 Web UI 完全看不到 Mac 上的任何会话。

### 根因与破解：
1. **绝对路径绑定校验 (已绕过)**：底层数据库的 `workspace_uris` 硬编码了 Mac 的绝对路径 `/Users/kael/...`。我们在 PVE 上通过创建 `ln -s` 软链接骗过了操作系统的路径校验。
2. **隐藏分区隔离 (Hex Patching 破解)**：最大的元凶是 Linux 版的 `agy` 二进制文件硬编码了 `app_data_dir = 'antigravity-cli'`，而 Mac 版是 `antigravity`。导致它们在读取同一个 SQLite 数据库时，互相过滤掉了对方的会话。
   - **终极黑魔法**：我们使用 16 进制热修补（Hex Patching）了 PVE 的二进制文件，利用 Unix 多斜杠合并特性，把 `antigravity-cli` 改成了 `antigravity////`。PVE 瞬间突破次元壁，完美读取了 Mac 的所有 40 个历史会话！

---

## 第二阶段：Project ID 路由抢夺战争 (The "Night Shift" Paradox)

当我们成功让 PVE 和 Mac 完全共享同一个 SQLite 命名空间后，触及到了 Antigravity 架构最底层的“物理定律”：

### 现象描述：
当 Mac 和 PVE **同时在线**时，只要其中一方连上网页端，另一方的 `gemini` 项目就会瞬间消失（或者双双掉线闪烁）。它们不是在抢身份 ID，而是在抢 **Project ID 的后端路由权**。

### 核心根因：
1. 由于 Mutagen 完美同步了 `~/.gemini/config/projects/` 目录，Mac 和 PVE 向 Google 后端上报了**完全一模一样的 Project ID**。
2. Google 的 WebChannel 信令服务器为了防止“脑裂（Split-brain）”，实行**严格的一夫一妻制**：一个 Project ID 同一时刻只能被分配（Route）给唯一的一台物理节点执行。
3. 当 PVE 声明所有权时，Mac 瞬间被架空（项目在网页端被隐藏）；当 Mac 重新发送心跳包时，PVE 瞬间出局。

---

## 终局结论与工作流抉择

基于 Google 后端的路由定律（且我们无法绕过 Google 后端自建信令服务器），我们必须在以下两种工作流中做出抉择：

### 路线 A：接力模式（Night Shift）—— “王座只有一个”
* **运作方式**：维持共享 Project ID 的现状。
* **代价**：两台机器**绝对不能同时在线**。离开工位时必须合上 Mac（或杀掉进程），让 PVE 接管王座；回来时唤醒 Mac，PVE 被挤掉。
* **优势**：聊天记录 100% 连贯，可以在 PVE 节点里接着 Mac 的未完会话继续聊，真正实现无缝接力。

### 路线 B：双持模式（Dual Wield）—— “兵分两路派发”
* **运作方式**：给 PVE 颁发一个新的独立 Project ID（如 `gemini-算力节点`），指向同一个底层代码库。
* **代价**：两个节点的**聊天记录互相独立**。PVE 无法续聊 Mac 的旧会话。
* **优势**：两个节点**永远同时在线**且在网页端并排显示！遇到重度计算或跑脚本任务，直接点开 PVE 的项目下达指令。Mutagen 会将 PVE 改写的代码毫秒级同步回 Mac 工作区，实现完美的“任务派发”。
