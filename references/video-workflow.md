# GitHub Trending 短视频制作

## 模板选择

在选模板前读取场景索引。以下命令会优先使用 `~/Documents/SourceHub/CommonHub/kvs-video-template`，首次缺失时从 [GitHub 模板库](https://github.com/hongye007/kvs-video-template) 克隆到该目录，再输出目录索引。新建工程时也会自动执行同样的检查。使用 `KVS_VIDEO_TEMPLATE_DIR` 可指定已有的其他检出目录。

```bash
python3 <SKILL_DIR>/scripts/scaffold_episode.py --catalog
```

- GitHub Trending 周榜用 `github-trending-weekly`，GitHub Hot 单项目用 `github-hot-project`，官网功能导览用 `website-tour`，产品介绍用 `product-introduction`，技术趋势观点用 `technical-opinion`。
- 用户指定模板时，用场景内对应的 ID；指定版本时固定该版本。否则用场景默认模板的稳定版本。
- 场景暂无已登记模板时，按已选制作模式处理该期。可为新场景登记适用的现有模板，再通过脚手架复用。

```bash
python3 <SKILL_DIR>/scripts/scaffold_episode.py <slug> \
  --workspace <workspace-root> --scene github-trending-weekly --language zh
```

英文用 `--language en` 建独立工程；按需传入 `--template <id>` 或 `--version <version>`。脚手架从模板版本对应的 Git commit 复制源码，并在本期 `meta.json` 写入 `templateType`、`templateScene`、`templateId`、`templateVersion` 与完整 `templateCommit`。交付时保留这份记录。以下制作步骤适用于当前的浅蓝工程榜单，首次构建前在工程目录执行 `npm install`。

## 制作顺序

1. 锁定 `episode.json` 的正式项目、事实、口播和风险说明。
2. 为每个项目获取官方素材及 Logo，通常选 1–3 份，记录来源。先保证真实性，再考虑视觉丰富度。
3. 使用 `$kvs-continuous-tts` 生成一条连续口播。默认 ElevenLabs 最新稳定模型和 timestamped endpoint；用户指定豆包时才切换。保留原生速度，除非用户明确要求后期 tempo。
4. 保存最终 MP3、服务端时间戳 JSON 和 SRT。Audio Tags 不得进入显示字幕或锚点文本。
5. 根据项目名首次出现位置生成 `timeline.json` 的页面边界，全部向前对齐到 30fps 的前一帧；不要按总时长等比分配。
6. 创建 `motion-plan.json`。每个项目记录素材切换和 3-5 个短亮点卡的 SRT 原文锚点；结尾记录方向矩阵、问句、CTA 和结束语锚点。
7. 先运行 `python3 validate_project.py .`，再运行 `node build-composition.mjs`。验证器和构建器必须在锚点缺失、锚点越界、媒体数量不匹配或亮点短语超过中文 6 字 / 英文 24 字符时失败。
8. 启动预览前检查端口；已有服务可复用，冲突时换端口，不中断无关服务。
9. 执行 HyperFrames strict 检查，抽查总览每次落位、各详情页素材切换/卡片入场/归档落位、所有边界和结尾最后一帧。
10. 用户确认预览后才渲染最终成片。

## `motion-plan.json`

```json
{
  "template_version": "v3",
  "projects": {
    "owner/repo": {
      "media": [
        {
          "anchor": "口播中的原文片段",
          "label": "OFFICIAL DEMO",
          "scale": 1.04,
          "x": 0,
          "y": 0
        }
      ],
      "highlights": [
        {"anchor": "口播中的原文片段", "title": "六字以内"}
      ]
    }
  },
  "outro": {
    "direction_anchors": [{"anchor": "方向总结开头"}],
    "question_anchor": "互动问句",
    "cta_anchor": "点赞关注",
    "finish_anchor": "下期见"
  }
}
```

锚点必须是最终 SRT 中唯一且稳定的原文片段。若重复，选更长的上下文片段；不得用近似匹配掩盖文案和音频版本不一致。

## 动效语法

- 总览：最后一名到第一名逆序建立；右侧进入首位、短暂停顿、下移归位；提供音效时配 whoosh/click。
- 详情基础层：页面轻移入，标题、下划线、中文定位、Star 行、素材舞台和仓库名依次建立。
- 素材：按 SRT 锚点交接，克制推近或平移；真实 Demo 始终是主视觉。
- 亮点：按口播依次落入舞台下方，以彩色短语保留。配置 ding 时在落位处触发。英文交付保留彩色短语，默认不烧录逐句字幕。
- 转场：前页轻向左淡出，后页小距离从右进入。
- 结尾：方向矩阵按口播建立，CTA 在对应 SRT 锚点出现，音频后保留约 0.7 秒尾帧。

## 原生 2K 渲染

HTML composition、预览、快照和最终成片都必须直接使用 1440x1920。渲染原生 2K Master：

```bash
npx --yes hyperframes@<locked-version> render \
  --quality high \
  --output renders/<slug>-final-2k-master.mp4
```

需要平台交付副本时，从原生 2K Master 仅做封装或编码规格转换，保持 1440x1920，不做二次缩放：

```bash
ffmpeg -i renders/<slug>-final-2k-master.mp4 \
  -c:v libx264 -profile:v high -pix_fmt yuv420p -crf 17 -preset slow \
  -c:a aac -b:a 192k -ar 48000 -ac 2 \
  renders/<slug>-final-2k.mp4
```

使用 `ffprobe` 验证两个文件都真实解码为 1440x1920，并检查帧率、时长、编码和音轨；再执行黑帧、关键帧、场景边界和尾帧检查。只有平台或用户明确要求时才额外生成较小分辨率副本，且不得反向作为 Master。

## 发布文案

`VIDEO_COPY.md` 至少包含一版可直接复制的清单：`序号. owner/repo：一句具体中文用途`。项目数量、大小写和顺序必须与视频一致；限制说明不能为了精简而删除。
