# 交付检查

## 选题与事实

- daily、weekly、monthly 候选已合并，历史重复已过滤。
- 正式项目达到质量线并覆盖至少 3 个场景；备选完整保留但未进入成片和已使用账本。
- Star、增量、语言、License、Release 和限制均有日期与主来源。
- 特殊许可证、高权限、付费依赖、硬件门槛以及医疗/金融限制没有被宣传文案删掉。

## 模板和内容源

- `meta.json` 记录选用的类型、场景、模板 ID、版本和完整 Git commit，保留工程实际使用的值。
- `meta.json.canvas` 为 `1440x1920@30`，`template-base.txt` 与生成后的 `index.html` 都声明相同的原生 2K composition。
- `episode.json`、最终口播、SRT、`timeline.json` 和 `motion-plan.json` 属于同一版本。
- `validate_project.py` 通过后才进入预览和渲染。
- 每个项目有官方素材、Logo/占位和来源记录。
- `motion-plan.json` 的媒体数量与 `episode.json.projects[].media` 一致；亮点 3–5 条，每条中文最多 6 字、英文最多 24 字符。

## 音频与时间轴

- 连续口播使用用户确认的 provider、模型、音色和原生速度；没有静默切换或后期拉伸。
- 服务端时间戳 JSON 与 SRT 存在；Audio Tags 已从显示时间轴清除。
- 每个 SRT 锚点唯一、存在且位于对应场景；页面边界向前对齐到 30fps 前一帧。
- 口播、whoosh、click 和 ding 音量层级合理，音效不压口播、不连续堆叠。

## 视觉与动效

- 浅蓝 64px/256px 网格、深色官方素材舞台和深蓝灰文字一致。
- 首页开始时列表为空，逆序入场、首位停顿、下移归位完整；播放不会在几秒后意外重头。
- 详情顶部安全区、标题、Star 行、素材舞台、归档区和底部仓库名无重叠。
- 官方素材使用 `contain` 优先，无拉伸、严重裁切、错配、加载失败或跨幕残留。
- 彩色亮点依照 SRT 锚点逐条落位，检查短语可读性，并在配置 ding 时核对音效时点。
- 完整 `owner/repo` 底部居中、足够大、不截断。
- 结尾方向矩阵、问句、CTA 和尾帧完整。
- HyperFrames strict 为 0 errors / 0 warnings；抽查首帧、每次首页落位、每个素材切换、每次归档、全部场景边界和最后一帧。

## Master 与 2K

- HTML composition、预览快照和正式渲染均真实为 1440x1920、30fps。
- Master/Delivery 直接从原生 2K composition 渲染，使用 H.264 High、yuv420p、AAC 48kHz 双声道；不得先生成 1080 再放大。
- Master/Delivery 均通过 `ffprobe`、黑帧、边界、首尾帧和完整播放检查。
- 正式渲染清单为 `CURRENT`；如同时保留 Master 与 Delivery，两者都必须是原生 2K，只按交付用途命名。

## X 线程

- 图片共“正式项目数 + 1”张，全部 1440x1920，来自最终视频稳定帧。
- 主帖 1 张总览图；每个项目一条回复、一张对应详情图和一个 GitHub 链接。
- 文案顺序与视频一致，字符数合规，替代文本和来源完整。
- 发布前状态为 `exported_not_published`。获得授权并确认外部页面成功后，才改为 `published`。

## 导出包

- `video/` 包含原生 2K Master/Delivery、封面、最终音频、SRT/时间戳、脚本、内容源、动效计划和来源。
- `x/` 包含总览、详情图、线程文案、替代文本、事实、来源和复盘文件。
- 根目录有 `export-manifest.json`、`checksums.sha256`；同名 ZIP 可完整解压。
- 发布后额外包含 `publish/publish-receipt.json`，并重建校验和与 ZIP。

## 权限门

- 名单确认不等于允许生成外部付费语音；调用前遵循对应 provider 的授权与密钥规则。
- 预览确认不等于允许最终渲染。
- 导出完成不等于允许发布。
- 发布授权只覆盖用户指定平台和当前内容，不自动扩展到其他账号、平台或后续期数。
