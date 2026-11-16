# Video MPC mode

用于产品介绍、AI 工具评测、知识科普和观点型口播视频。该模式把 `kvs-mpc-workflow` 作为历史制作引擎，通过共享入口统一事实、素材、授权和交付状态。

## Recipe

编写口播、绑定素材或修改已制作视频时，读取 [editorial-production.md](../editorial-production.md)，按同一套证据、节奏和版本规则执行。

```text
锁定中文口播稿
→ 生成一条连续配音和时间戳
→ 以语义段落建立 SHOTBOOK / 分镜
→ 绑定真实页面、素材和动效
→ 预览、QA、导出多平台发布包
```

- 口播稿是时间轴的上游；未锁稿不要做最终镜头排布。
- 连续配音默认使用 `$kvs-continuous-tts`；用户明确指定 provider 时才切换。
- 数字人是可选底层能力，只在用户明确需要时加载数字人 Skill；最终数字人替换不能改变已确认的圆窗几何和时间轨。
- 图片主视觉或修复按需调用 `$kvs-image-generation`，真实产品界面仍必须使用截图/录屏。
- 完成条件包括最终 MP4 视觉 QA、音画同步检查、媒体报告、发布素材包和明确状态。

新任务从 `$kvs-videocontent-maker` 进入；已有工程可继续直接使用 `$kvs-mpc-workflow` 兼容入口。
