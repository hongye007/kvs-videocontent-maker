# 共享内容源

视频、X 配图和发布文案均以工程根目录的 `episode.json` 为事实源。动画语义另存 `motion-plan.json`，场景边界另存 `timeline.json`；不要把项目事实硬编码进构建器。

## `episode.json`

```json
{
  "episode": "EP.019",
  "slug": "github-trending-developer-ep019",
  "week_label": "第 45 周 · 2026",
  "query_date": "2026-11-05",
  "trending_sources": [
    "https://github.com/trending?since=daily",
    "https://github.com/trending?since=weekly",
    "https://github.com/trending?since=monthly"
  ],
  "overview_title": "本期热门项目",
  "overview_subtitle": "GITHUB TRENDING · AI CURATED",
  "intro_voice": "锁定的开场口播",
  "projects": [
    {
      "rank": 1,
      "repo": "owner/name",
      "url": "https://github.com/owner/name",
      "display_name": "NAME",
      "slug": "name",
      "tagline_zh": "一行具体中文定位",
      "category": "developer-productivity",
      "language": "TypeScript",
      "stars": 12345,
      "stars_this_period": 1234,
      "period": "weekly",
      "display_delta": "周 +1.2K",
      "license": "MIT",
      "what_it_is_zh": "它是什么",
      "what_it_does_zh": "它解决什么问题",
      "core_highlight_zh": "最核心差异",
      "narration_zh": "最终项目口播",
      "risk_zh": "必要限制",
      "logo": {
        "path": "assets/logos/name.svg",
        "row_path": "assets/logos/name-row.svg",
        "detail_path": "assets/logos/name-detail.svg",
        "alt": "官方标识",
        "kind": "official-logo",
        "official": true,
        "source_url": "https://..."
      },
      "media": [
        {
          "path": "assets/images/name-demo.png",
          "type": "image",
          "alt": "官方 Demo",
          "source_url": "https://...",
          "fit": "contain"
        }
      ],
      "sources": ["https://github.com/owner/name"]
    }
  ],
  "outro_visual": "本期五个技术方向",
  "outro_directions": [
    {"rank": "01", "zh": "方向名称", "en": "DIRECTION"}
  ],
  "outro_question": "你想先试哪个？",
  "outro_cta": "点赞 · 关注 · 下期见",
  "outro_voice": "最终结尾口播"
}
```

## 字段要求

- `repo` 保留真实大小写；底部显示完整 `owner/repo`。
- `period` 与 `display_delta` 必须一致，事实文件保留原始整数增量。
- `license` 未知时为 `null`，不得猜测。特殊许可证的限制写入 `risk_zh`。
- `media` 顺序必须与 `motion-plan.json` 对应项目的 `media` 顺序一致。
- `fit` 默认 `contain`；只有已验证不会遮掉关键信息时使用 `cover`。
- `logo` 找不到官方素材时使用 `text-placeholder`、`official: false`、`source_url: null`。
- 每项目恰好一个主要 category；不要用 `other` 逃避分类。

## `motion-plan.json`

`projects` 以完整 `owner/repo` 为键。每个 `media` 动作包含最终 SRT 中的锚点、标签和轻微镜头参数；`highlights` 包含锚点及不超过 6 个汉字的短文案。`outro.direction_anchors` 数量必须等于 `episode.outro_directions` 数量。

构建器应验证：项目计划存在、媒体数量一致、锚点存在且位于当前场景、卡片长度合规、结尾锚点齐全。

## 来源文件

- `assets/logos/sources.json`：Logo 来源、官方性、哈希和修改说明。
- `assets/images/sources.json` 或同等素材清单：官方 Demo 来源、获取时间、哈希和修改说明。
- `assets/audio/sfx/sources.json`：whoosh、click、ding 的来源或生成方式。
- `audio_meta.json`：provider、模型、音色、速度、音频路径、SRT、时间戳、时长和请求标识；不存 API key。

中英文各有一份 `episode.json`，以 `language`（`zh` / `en`）标记。沿用原结构的 `tagline_zh` 等字段名，填入本版语言的显示文案。
