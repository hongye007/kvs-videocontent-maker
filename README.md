# KVS Video Content Maker

用于 GitHub Trending、开源项目介绍和产品口播视频制作的 Codex Skill。工作流程见 [SKILL.md](SKILL.md)。

## 安装

将本仓库克隆到 Codex 的 Skill 目录。

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/hongye007/kvs-videocontent-maker.git ~/.codex/skills/kvs-videocontent-maker
```

首次读取模板索引或新建工程时，脚手架会使用 CommonHub 中的模板库。如本地缺失，会从 [kvs-video-template](https://github.com/hongye007/kvs-video-template) 克隆到 `~/Documents/SourceHub/CommonHub/kvs-video-template`。
