# Video mode

用于 GitHub Trending 或指定开源项目的开发者短视频。该模式吸收 `ai-blogger-video-workflow` 的制作与验收职责，但由共享 KVS 入口统一事实、选题确认和导出授权。

## Editorial shape

```text
一句核心判断
→ 真实仓库/官网证据
→ 1–3 个亮点
→ 真实 Demo 或运行结果
→ 限制、入口和结尾 CTA
```

不要把 README 改写成功能清单。口播、画面和发布正文使用同一份事实包；动态数据标注查询日期。

编写项目介绍、准备素材、调整剪辑或替换口播前，读取 [editorial-production.md](../editorial-production.md)。该参考统一专业客观的表述、素材证据、阅读节奏、版本同步与成片验收。

## Default production

- GitHub Trending 周榜使用该场景的默认模板。EP019 版式为原生 1440×1920、3:4、30fps，采用浅蓝工程网格、官方 Demo 舞台和 SRT 锚点彩色短语。
- 设计画面时读取 [视觉系统与 EP.020 动效参考](../visual-system.md#ep020-可选画面与动效参考)，按本期口播与素材密度选用。
- 先做无最终口播的结构预览，再锁口播；连续配音默认走 `$kvs-continuous-tts` 的 ElevenLabs。
- 页面、仓库和 Demo 必须是真实素材；AI 图只用于封面创意、概念视觉或明确标注的生成结果。
- HyperFrames 预览通过后仍需对最终 MP4 做黑帧、错帧、音轨、场景边界、尾帧和视觉空档检查。
- 交付保留 `BRIEF.md`、`DECISIONS.md`、`SCRIPT.md`、`STORYBOARD.md`、`assets/`、`snapshots/`、`renders/render-manifest.json` 和 QA 报告。

## Export gate

未获导出授权不渲染最终成片；未获发布授权不操作 X 或其他平台。导出清单必须区分 `exported_not_published` 与 `published`。

需要选模板时，参照 [场景模板选择与脚手架](../video-workflow.md#模板选择)。
