# 选题确认表

选题阶段固定生成机器可读的 `selection-review.json` 和便于阅读的 `SELECTION_REVIEW.md`。两个文件来自同一份 `shortlist.json`，状态默认为 `awaiting_confirmation`。

## JSON 结构

```json
{
  "as_of": "2026-09-19",
  "status": "awaiting_confirmation",
  "filtered": {
    "previously_used": ["owner/repo"],
    "other_exclusions": [{"repo": "owner/repo", "reasons": ["archived"]}]
  },
  "recommended": ["owner/repo"],
  "backups": ["owner/repo"],
  "candidates": [
    {
      "rank": 1,
      "repo": "owner/repo",
      "decision": "recommended",
      "summary_zh": "一句话说明是什么",
      "use_case_zh": "具体用来做什么",
      "core_highlight_zh": "核心亮点",
      "risk_zh": "限制或风险",
      "score": 88.5,
      "score_breakdown": {}
    }
  ]
}
```

`candidates` 只包含未做项目，并按总分降序排列。`filtered.previously_used` 只用于说明哪些仓库已被过滤，不参与评分或推荐。

## 用户确认

向用户展示 Markdown 表格和推荐组合，并明确等待以下任一输入：

- 按推荐名单继续。
- 删除或替换某个项目。
- 调整项目顺序。
- 在 5-7 个范围内调整数量。

确认前不得创建视频工程、生成 TTS、制作图文或写入已用项目账本。
