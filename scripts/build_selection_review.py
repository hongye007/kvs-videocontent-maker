#!/usr/bin/env python3
"""Build a user-facing selection gate from a scored Trending shortlist."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_SUMMARY_FIELDS = (
    "summary_zh",
    "use_case_zh",
    "core_highlight_zh",
    "risk_zh",
)


def load_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("shortlist must be a JSON object")
    return payload


def clean_table(value: object) -> str:
    return str(value or "").replace("|", "／").replace("\n", " ").strip()


def candidate_decision(repo: str, selected: set[str], backups: set[str], status: str) -> str:
    key = repo.lower()
    if key in selected:
        return "recommended"
    if key in backups:
        return "backup"
    if status == "below_threshold":
        return "below_threshold"
    return "eligible_not_selected"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--shortlist", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-markdown", type=Path, required=True)
    args = parser.parse_args()

    source = load_json(args.shortlist)
    selected = {str(row["repo"]).lower() for row in source.get("selected", [])}
    backups = {str(row["repo"]).lower() for row in source.get("backups", [])}
    previously_used: list[str] = []
    other_exclusions: list[dict] = []
    candidates: list[dict] = []

    for row in source.get("ranked", []):
        repo = str(row.get("repo", ""))
        reasons = list(row.get("exclusion_reasons", []))
        if row.get("status") == "excluded":
            if "previously_used" in reasons:
                previously_used.append(repo)
            remaining = [reason for reason in reasons if reason != "previously_used"]
            if remaining:
                other_exclusions.append({"repo": repo, "reasons": remaining})
            continue

        missing = [field for field in REQUIRED_SUMMARY_FIELDS if not str(row.get(field, "")).strip()]
        if missing:
            raise ValueError(f"{repo}: missing selection-review fields: {', '.join(missing)}")

        candidates.append({
            "repo": repo,
            "decision": candidate_decision(repo, selected, backups, str(row.get("status", ""))),
            "category": row.get("category"),
            "language": row.get("language"),
            "stars": row.get("stars"),
            "stars_this_period": row.get("stars_this_period"),
            "period": row.get("period"),
            "periods": row.get("periods", []),
            "sightings": row.get("sightings", []),
            "source_urls": row.get("source_urls", []),
            "summary_zh": row["summary_zh"],
            "use_case_zh": row["use_case_zh"],
            "core_highlight_zh": row["core_highlight_zh"],
            "risk_zh": row["risk_zh"],
            "score": row.get("score"),
            "selection_score": row.get("selection_score"),
            "score_breakdown": row.get("score_breakdown", {}),
        })

    candidates.sort(key=lambda row: (-(row.get("score") or 0), row["repo"].lower()))
    for index, row in enumerate(candidates, start=1):
        row["rank"] = index

    review = {
        "as_of": source.get("as_of"),
        "status": "awaiting_confirmation",
        "minimum_score": source.get("minimum_score"),
        "filtered": {
            "previously_used": sorted(previously_used, key=str.lower),
            "other_exclusions": sorted(other_exclusions, key=lambda row: row["repo"].lower()),
        },
        "recommended": [row["repo"] for row in source.get("selected", [])],
        "backups": [row["repo"] for row in source.get("backups", [])],
        "candidates": candidates,
        "warnings": source.get("warnings", []),
        "confirmation_prompt": "请确认按推荐名单继续，或说明要删除、替换、换序或调整到 5-7 个项目。",
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_markdown.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# GitHub Trending 选题确认",
        "",
        f"- 查询日期：{review['as_of']}",
        f"- 状态：`{review['status']}`",
        f"- 已过滤做过的项目：{len(review['filtered']['previously_used'])} 个",
        f"- 未做候选：{len(candidates)} 个",
        "",
        "| 排名 | 项目 | 榜单 | 是什么 | 用来做什么 | 核心亮点 | 风险 | 分数 | 建议 |",
        "| ---: | --- | --- | --- | --- | --- | --- | ---: | --- |",
    ]
    for row in candidates:
        lines.append(
            f"| {row['rank']} | `{clean_table(row['repo'])}` | {clean_table('/'.join(row['periods']))} | "
            f"{clean_table(row['summary_zh'])} | {clean_table(row['use_case_zh'])} | "
            f"{clean_table(row['core_highlight_zh'])} | {clean_table(row['risk_zh'])} | "
            f"{row['score']:.2f} | `{row['decision']}` |"
        )
    lines.extend([
        "",
        "## 推荐组合",
        "",
        ", ".join(f"`{repo}`" for repo in review["recommended"]) or "无",
        "",
        "## 备选",
        "",
        ", ".join(f"`{repo}`" for repo in review["backups"]) or "无",
        "",
        "## 已过滤",
        "",
        ", ".join(f"`{repo}`" for repo in review["filtered"]["previously_used"]) or "无",
        "",
        review["confirmation_prompt"],
        "",
    ])
    args.output_markdown.write_text("\n".join(lines), encoding="utf-8")
    print(f"candidates={len(candidates)} filtered_used={len(previously_used)} status=awaiting_confirmation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
