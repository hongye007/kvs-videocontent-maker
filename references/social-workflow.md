# X 图片线程

## 默认结构

默认使用 1 条主帖 + N 条项目回复：

- 主帖附 `images/00-overview.png`，概括本期项目跨度并说明下方按视频顺序给出链接。
- 每个正式项目各占一条回复，附对应 `images/NN-<project>.png`，正文包含 `N/总数`、完整 `owner/repo`、一句具体用途、必要限制和 GitHub URL。
- 最后一条回复可追加最终 CTA，但不得删除项目限制或风险提示。
- 每条只附 1 张图，项目、文案、链接和图片严格一一对应。不要为了减少帖子数量重新拼成四图宫格。

## 图片

- 总览图来自所有项目稳定落位后的榜单稳定帧。
- 项目图来自对应 DETAIL 的稳定阅读段；应显示标题、Star 行、官方素材、已归档亮点和完整仓库名。
- 全部从最终成片提取原生 1440x1920 稳定帧。`image.png` 作为总览图兼容入口，与 `images/00-overview.png` 内容一致。
- 不另外生成不同主题封面。
- `alt-text.md` 按发布顺序提供逐图替代文本；`image-source.json` 记录场景、时间和事实/素材来源。

## 文案原则

- 主帖控制在 X 加权字符限制内，不塞入全部 README 摘要。
- 项目回复保留真实仓库名及大小写；链接放在其对应回复，不集中堆在最后一条。
- Open-source 不等于数据、模型、API 或商业使用全部免费。遇到特殊许可证、高权限、硬件或非医疗等限制时必须保留。
- HashTag 最多 2 个，只有确实有发现价值时使用。

## 输出

`x/` 至少包含：

- `post.md`
- `image.png`
- `images/00-overview.png`
- `images/NN-<project>.png`
- `alt-text.md`
- `image-source.json`
- `facts.json`
- `sources.md`
- `RETRO.md`

图片数量必须等于正式项目数 + 1；`post.md` 明确每条帖子对应的图片相对路径。

## 发布状态

- 默认只生成草稿，不发布。
- 用户明确授权发布后，仍需在外部发送动作前遵循当前计算机操作确认规则。
- 成功发布必须记录主帖和每条回复的真实 URL、账号、时间、帖子数、图片数和核验方式到 `publish/publish-receipt.json`。
- 同步把 `export-manifest.json` 更新为 `published: true`、`publication_status: published`，更新 `RETRO.md`、校验和及 ZIP。页面未显示真实帖子 URL 时不得标记成功。
