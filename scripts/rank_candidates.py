#!/usr/bin/env python3
"""Score enriched GitHub Trending candidates and choose a diverse shortlist."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
from pathlib import Path


WEIGHTS = {
    "developer_utility": 5,
    "novelty": 4,
    "evidence": 3,
    "clarity": 3,
    "audience_fit": 1,
}
MIN_SCORE = 68
PERIOD_DAYS = {
    "daily": 1.0,
    "weekly": 7.0,
    "monthly": 30.4375,
}


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def percentile(values: list[float], value: float) -> float:
    if len(values) <= 1:
        return 1.0
    below = sum(item < value for item in values)
    equal = sum(item == value for item in values)
    return (below + max(0, equal - 1) / 2) / (len(values) - 1)


def parse_time(value: str | None) -> dt.datetime | None:
    if not value:
        return None
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


def freshness_points(pushed_at: str | None, now: dt.datetime) -> float:
    pushed = parse_time(pushed_at)
    if not pushed:
        return 0
    days = max(0, (now - pushed).days)
    if days <= 7:
        return 4
    if days <= 30:
        return 3
    if days <= 90:
        return 2
    if days <= 180:
        return 1
    return 0


def weekly_gain(candidate: dict) -> float:
    gain = float(candidate.get("stars_this_period") or 0)
    days = PERIOD_DAYS.get(str(candidate.get("period") or "weekly").lower(), 7.0)
    return gain * 7.0 / days


def used_repos(payload: object) -> set[str]:
    if isinstance(payload, list):
        rows = payload
    elif isinstance(payload, dict):
        rows = payload.get("repositories", [])
    else:
        rows = []
    result: set[str] = set()
    for row in rows:
        repo = row if isinstance(row, str) else row.get("repo")
        if repo:
            result.add(str(repo).lower())
    return result


def hard_exclusion(candidate: dict, used: set[str], now: dt.datetime) -> list[str]:
    reasons: list[str] = []
    repo = str(candidate.get("repo", "")).lower()
    flags = candidate.get("flags", {})
    if repo in used and not flags.get("major_release_override"):
        return ["previously_used"]
    for key in ("archived", "disabled", "fork_only", "primary_source_missing", "unsafe"):
        if flags.get(key):
            reasons.append(key)
    pushed = parse_time(candidate.get("pushed_at"))
    if pushed and (now - pushed).days > 180 and not flags.get("major_release_override"):
        reasons.append("inactive_over_180_days")
    if not candidate.get("repo") or not candidate.get("category"):
        reasons.append("missing_identity_or_category")
    return reasons


def validate_ratings(candidate: dict) -> dict[str, float]:
    ratings = candidate.get("ratings", {})
    normalized: dict[str, float] = {}
    for key in WEIGHTS:
        entry = ratings.get(key)
        if not isinstance(entry, dict) or not str(entry.get("reason", "")).strip():
            raise ValueError(f"{candidate.get('repo')}: ratings.{key} needs score and evidence reason")
        raw = entry.get("score")
        if not isinstance(raw, (int, float)) or not 0 <= raw <= 5:
            raise ValueError(f"{candidate.get('repo')}: ratings.{key} must be 0-5")
        normalized[key] = float(raw)
    return normalized


def penalty(candidate: dict) -> tuple[float, list[str]]:
    flags = candidate.get("flags", {})
    rules = {
        "license_missing": 3,
        "paid_dependency_unclear": 5,
        "demo_unavailable": 4,
        "self_reported_metric": 3,
        "misleading_claim": 8,
        "thin_wrapper": 6,
    }
    reasons = [key for key in rules if flags.get(key)]
    return float(sum(rules[key] for key in reasons)), reasons


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--used", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--select", type=int, default=5, choices=range(5, 8), metavar="{5,6,7}")
    parser.add_argument("--backups", type=int, default=2)
    parser.add_argument("--as-of", help="UTC date YYYY-MM-DD; defaults to today")
    args = parser.parse_args()

    source = load_json(args.candidates)
    candidates = source.get("candidates", source) if isinstance(source, dict) else source
    if not isinstance(candidates, list) or not candidates:
        parser.error("candidate input must be a non-empty array or {candidates: []}")
    used = used_repos(load_json(args.used))
    today = dt.date.fromisoformat(args.as_of) if args.as_of else dt.datetime.now(dt.timezone.utc).date()
    now = dt.datetime.combine(today, dt.time.max, tzinfo=dt.timezone.utc)

    eligible = [candidate for candidate in candidates if not hard_exclusion(candidate, used, now)]
    gains = [weekly_gain(candidate) for candidate in eligible]
    velocities = [weekly_gain(candidate) / max(float(candidate.get("stars") or 0), 100.0) for candidate in eligible]

    ranked: list[dict] = []
    for candidate in candidates:
        row = dict(candidate)
        exclusions = hard_exclusion(candidate, used, now)
        if exclusions:
            row.update({"status": "excluded", "exclusion_reasons": exclusions, "score": None})
            ranked.append(row)
            continue
        ratings = validate_ratings(candidate)
        gain = weekly_gain(candidate)
        velocity = gain / max(float(candidate.get("stars") or 0), 100.0)
        momentum = round(6 * percentile(gains, gain) + 5 * percentile(velocities, velocity) + freshness_points(candidate.get("pushed_at"), now), 2)
        subjective = sum(ratings[key] * WEIGHTS[key] for key in WEIGHTS)
        deductions, deduction_reasons = penalty(candidate)
        score = round(max(0.0, min(100.0, subjective + momentum - deductions)), 2)
        row.update({
            "status": "eligible" if score >= MIN_SCORE else "below_threshold",
            "score": score,
            "score_breakdown": {
                "dimensions": {
                    key: {
                        "score": ratings[key],
                        "points": round(ratings[key] * WEIGHTS[key], 2),
                        "reason": candidate["ratings"][key]["reason"],
                    }
                    for key in WEIGHTS
                },
                "subjective": round(subjective, 2),
                "momentum": momentum,
                "weekly_gain_normalized": round(gain, 2),
                "penalty": deductions,
                "penalty_reasons": deduction_reasons,
            },
        })
        ranked.append(row)

    pool = sorted(
        (row for row in ranked if row.get("status") == "eligible"),
        key=lambda item: (-item["score"], item["repo"].lower()),
    )
    selected: list[dict] = []
    categories: dict[str, int] = {}
    owners: set[str] = set()
    languages: set[str] = set()
    while pool and len(selected) < args.select:
        choices: list[tuple[float, dict]] = []
        for item in pool:
            owner = item["repo"].split("/", 1)[0].lower()
            category = item["category"]
            if owner in owners or categories.get(category, 0) >= 2:
                continue
            diversity = (3 if category not in categories else 0) + (2 if item.get("language") and item["language"] not in languages else 0)
            choices.append((item["score"] + diversity, item))
        if not choices:
            break
        choices.sort(key=lambda pair: (-pair[0], pair[1]["repo"].lower()))
        selection_score, picked = choices[0]
        pool.remove(picked)
        picked = dict(picked)
        picked["selection_score"] = round(selection_score, 2)
        picked["status"] = "selected"
        selected.append(picked)
        owner = picked["repo"].split("/", 1)[0].lower()
        owners.add(owner)
        categories[picked["category"]] = categories.get(picked["category"], 0) + 1
        if picked.get("language"):
            languages.add(picked["language"])

    selected_names = {item["repo"].lower() for item in selected}
    remaining = [
        row for row in ranked
        if row.get("status") == "eligible" and row["repo"].lower() not in selected_names
    ]
    remaining.sort(key=lambda item: (-item["score"], item["repo"].lower()))
    backups = [dict(item, status="backup") for item in remaining[: args.backups]]

    warnings: list[str] = []
    if len(selected) != args.select:
        warnings.append(f"Only {len(selected)} candidates passed threshold and diversity constraints; do not fill slots with weak projects.")
    if len({item["category"] for item in selected}) < min(3, args.select):
        warnings.append("Selected set covers fewer than three categories; manually review the next ranked projects.")
    if len(backups) < args.backups:
        warnings.append(f"Only {len(backups)} backup candidates passed the quality threshold.")

    output = {
        "generated_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "as_of": today.isoformat(),
        "minimum_score": MIN_SCORE,
        "selected": selected,
        "backups": backups,
        "ranked": sorted(
            ranked,
            key=lambda item: (
                item.get("score") is None,
                -(item.get("score") if item.get("score") is not None else -math.inf),
                item.get("repo", "").lower(),
            ),
        ),
        "warnings": warnings,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"selected={len(selected)} backups={len(backups)} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
