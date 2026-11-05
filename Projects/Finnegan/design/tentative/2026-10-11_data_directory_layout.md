---
title: "Finnegan 数据目录结构"
date: 2026-10-11
status: tentative   # 已与用户确认，等 Watcher 任务完成后实施；实施后提炼进 kb/
session: "conversation://b53a4c3a-bcdb-4588-84df-df4ccc750fae"
related:
  - design/tentative/2026-10-11_card_storage_model.md
  - tasks/task_global_event_bus.md
---

# Finnegan 数据目录结构

> 本文是 `2026-10-11_card_storage_model.md` 的落地篇：规定卡片文件放在哪里，以及配置如何组织。

## 1. 设计原则

1. **唯一的用户配置是"主目录在哪"**，其余一切由 Finnegan 自己管理。
2. **散落卡片完全由 Finnegan 的主目录管理。**
3. **项目可以放在主目录内，也可以放在任意外部目录。**两者格式相同，只是位置不同。
4. **主目录自包含**：整个主目录拷到另一台机器上就能直接用。
5. **数据与代码分离**：数据不放在代码仓库里（代码仓库在 PVE 上，经由 Mutagen 同步）。

## 2. 指针配置（唯一需要用户关心的配置）

固定位置：`~/Library/Application Support/Finnegan/finnegan.yml`

```yaml
home: ~/Finnegan     # Finnegan 主目录，用户可以随意修改
```

- 默认值是 `~/Finnegan`，选这个位置是为了方便用户直接用 VS Code / Finder 访问；用户也可以改成 Application Support 下的某个目录。
- 首次启动时如果文件或主目录不存在：生成默认的指针配置，并初始化主目录骨架。
- **废弃**：代码仓库根目录下的 `finnegan.yml`（原先的 `watch_dirs` / `inbox_dir` 空壳）。

## 3. 主目录结构

```
<home>/                          ← 例如 ~/Finnegan/
├── Scattering/                  ← 散落卡片：只由 Finnegan 管理，扁平存放
│   └── 20261011-1512-短标题.md
├── Weaving/                     ← 内部项目（自动发现，无需登记）
│   └── 论乔伊斯/
│       ├── .finnegan-project    ← 项目标记文件
│       └── *.md
└── .finnegan/                   ← 系统区，用户不需要碰
    ├── config.yml               ← Finnegan 自管配置
    ├── bases/<sha256>.md        ← 全局 base 快照库（内容寻址）
    └── cache.db                 ← RxDB/SQLite 缓存，删掉可以重建
```

### 3.1 `.finnegan/config.yml`（Finnegan 自己维护，用户一般不手改）

```yaml
external_projects:               # 外部项目登记表（内部项目自动发现）
  - ~/Writing/MyBook
debounce_ms: 300
bugu_max_concurrency: 1
```

## 4. 外部项目

```
~/Writing/MyBook/                ← 任意外部目录，比如一个现成的 git 仓库
├── .finnegan-project            ← 有它才算 Finnegan 项目
├── chapter-draft.md             ← 头部有 id 的才是卡片
└── README.md                    ← 没有 id 的：Finnegan 不碰
```

`.finnegan-project`：

```yaml
root: 01JB...        # 项目根卡的 id（项目本身也是一张卡）
```

- 由 Finnegan 负责登记和取消登记（通过界面操作），用户不需要手改配置。
- 内部项目挪到外部：把目录移走，再在 Finnegan 里登记即可。

## 5. 监听目录（由系统推导，不再手填）

```
实际监听 = <home>/Scattering/ + <home>/Weaving/ + external_projects
```

- `<home>/.finnegan/` 不监听。
- 外部项目目录中，只有头部带 `id` 的 `.md` 文件才会被当作卡片。

## 6. 规则

1. **身份只认 `id`**：同一个 id 无论出现在哪个目录，都是同一张卡。如果出现两个文件 id 相同（例如用户手动复制了一份），后发现的那个报冲突，**绝不静默覆盖**。
2. **没有 id 的文件一律忽略**，直到用户在界面上主动"收编"（收编时才写入头部和 id）。Finnegan 不会自动修改用户已有的文件。
3. **写入目标固定**：Omnibar 捕获的想法、Bugu 卡片转正，都写进 `<home>/Scattering/`。
4. **base 快照库是全局的**：外部项目产生的分支，其 base 快照也存在 `<home>/.finnegan/bases/`。代价是外部项目单独拷到别的机器上时，三方合并会退化成双方对比，但卡片本身不受影响。
5. **缓存位置**：`<home>/.finnegan/cache.db`。现有代码在当前工作目录下写 `finnegan.db`，需要迁移过来。

## 7. 概念更名与废弃对照

| 旧概念 | 新概念 | 说明 |
|---|---|---|
| `Inbox` / `00_Inbox` / `inbox_dir` | `Scattering/` | 保存即转正，不再有"待处理收件箱" |
| `watch_dirs`（用户手填） | 推导得出 | 由 home + Weaving + external_projects 计算 |
| 仓库根目录的 `finnegan.yml` | 指针配置 + `.finnegan/config.yml` | 指针只存 `home` |
| `finnegan.db`（当前工作目录） | `<home>/.finnegan/cache.db` | 可以重建的缓存 |
| `atproto.yml` 中的 `inbox_dir` / `notes_dir` | 待对齐 | AT Protocol 拉取的内容应写入 `Scattering/`（`source: atproto`） |

## 8. 实施顺序

1. **等待** `task_global_event_bus`（Watcher 第 3 轮）在 PVE 上完成并验收，期间不改动相关代码。
2. 接手对齐任务 `tasks/storage_layout_004.md`。
3. 完成后更新 `kb/knowledge.md`，并把本文与存储模型文档的规格提炼进 kb。
