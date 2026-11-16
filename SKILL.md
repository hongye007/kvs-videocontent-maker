---
name: kvs-videocontent-maker
description: "Shared KVS video-production entry for GitHub Trending and specified open-source projects. Routes on demand to developer video, product/AI talking video, and release modes; keeps facts, assets, QA, and authorization in one auditable workflow. Do not auto-publish."
---

# KVS Shared Content Publisher

这是 KVS 视频内容生产的共享入口。它负责统一视频项目事实、素材来源、状态、授权和交付；具体视频能力按需路由，避免一次加载所有制作规则。图文任务使用 `$kvs-imagenote-maker`，不从本 Skill 进入。

## Mode routing (load only the selected reference)

先判断用户要交付什么，再读取对应模块：

| 用户目标 | 路由 | 读取 |
|---|---|---|
| GitHub Trending / 开源项目短视频 | `video` | [video.md](references/modes/video.md) |
| 产品、AI 工具或知识型口播视频 | `video-mpc` | [video-mpc.md](references/modes/video-mpc.md) |
| 已完成作品的跨平台分发 | `release` | 使用 `$kvs-content-release`，不要在本 Skill 内重复实现发布治理 |

默认选择：

- 未指定媒体形式但要介绍项目：如果是图文，转到 `$kvs-imagenote-maker`；如果是视频，继续在本 Skill 内选择视频模式。
- 需要可渲染视频模板时，先判断应用场景，再按 [模板库的场景索引](references/video-workflow.md#模板选择) 选择模板。[GitHub 模板库](https://github.com/hongye007/kvs-video-template) 在本地缺失时由脚手架克隆到 `~/Documents/SourceHub/CommonHub/kvs-video-template`。GitHub Trending 周榜走 `video`，场景为 `github-trending-weekly`。
- 产品或 AI 工具口播视频：用 `video-mpc`，先锁口播，再按音频生成时间轴。

## Shared fact and evidence layer

所有模式共用同一份事实包，不重复调研：

- 项目名、作者、仓库、官网、版本、License、可变数字和查询日期；
- 每个功能的来源、截图/录屏来源、AI 生成素材标记和素材授权；
- API Key、模型费用、硬件、部署门槛和已知限制；
- `draft`、`素材完成`、`待发布`、`已发布` 等状态。

动态数据不得跨日期或跨统计口径混用。无法核实的内容删除或标记待验证。真实 UI/官网/运行效果必须使用真实证据，AI 图不能冒充产品界面。

建议共享文件：`facts.json`、`sources.md`、`image-source.json`、`DECISIONS.md`。不同媒体的脚本、页面或时间轴只在选定模块中创建。

## Reusable bottom layers

内容模式按需调用底层能力，不复制实现：

- 图片生成/编辑：`$kvs-image-generation`，默认再路由到 `$atomflow-image-generation`；
- 连续口播和时间戳：`$kvs-continuous-tts`；
- 数字人/口型视频：仅在用户需要数字人时加载当前环境的数字人 Skill；
- 姿势×服饰×人物融合：按需调用 `$pose-costume-character`。

底层只返回媒体和 provenance；视频模式负责口播、镜头、QA 和视频交付，图文模式由 `$kvs-imagenote-maker` 负责。

## Shared stage gates

1. **Research**：形成事实包和来源台账。
2. **Editorial**：锁定一个核心判断和媒体模式。
3. **Production**：只加载所选模式的规则、模板和脚本。
4. **QA**：检查尺寸、事实、来源、可读性、截图真实性、授权文字和文件顺序。
5. **Export**：生成可验收的素材包，明确 `exported_not_published` 或 `published`。
6. **Publish**：只有用户明确授权后才操作外部账号；发布后保存真实 URL 和回执。

## Compatibility entries

以下旧名称保留给已有项目和脚本使用，但新任务从本 Skill 进入：

- `ai-blogger-video-workflow` → `video` 模式的历史实现/工具兼容入口；
- `kvs-image-generation` → 共享的图片生成底层；由视频或 `$kvs-imagenote-maker` 按需调用。

兼容入口不得启动第二套事实调研、发布流程或重复导出。共享 Skill 的新实现应优先使用本目录的 `references/modes/`。

## Permission boundary

默认只生成草稿、素材包和 QA 结果。创建帖子、上传文件、发送消息、登录账号或公开发布都需要用户对具体平台和内容的明确授权。
