"""ルールベース評価: config/scoring.yaml に基づく基礎スコアリング(設計書19章・14.2)

AIを使わない足切り用の機械的評価。Claudeによる重要度の最終判断は
/morning-brief 実行時に行う(設計書3.2)。
"""

from __future__ import annotations

import sys
from datetime import date

from scripts.common import load_json, load_yaml, save_json, today_stamp


def _clamp(value: int) -> int:
    return max(1, min(5, value))


def _score_by_table(value: float, table: list[dict], key: str, fallback: int) -> int:
    for row in table:
        if key == "min_weight" and value >= row[key]:
            return row["score"]
        if key == "max_days" and value <= row[key]:
            return row["score"]
    return fallback


def _relevance(article: dict, cfg: dict) -> int:
    base = cfg["relevance_by_priority"].get(article.get("priority", "medium"), 3)
    if article.get("topics") == ["uncategorized"]:
        return _clamp(base - 1)
    return _clamp(base + 1)


def _impact(article: dict, cfg: dict, topics_cfg: dict) -> int:
    topics = [t for t in article.get("topics", []) if t != "uncategorized"]
    if not topics:
        return cfg["uncategorized_impact"]
    max_weight = max(
        topics_cfg["topics"].get(t, {}).get("weight", 0) for t in topics
    )
    return _score_by_table(max_weight, cfg["impact_by_topic_weight"], "min_weight", 2)


def _novelty(article: dict, cfg: dict, today: date) -> int:
    published = article.get("published_at")
    if not published:
        return cfg["stale_novelty"]
    age_days = (today - date.fromisoformat(published)).days
    if age_days < 0:
        age_days = 0
    return _score_by_table(age_days, cfg["novelty_by_age_days"], "max_days", cfg["stale_novelty"])


def _actionability(text: str, cfg: dict) -> int:
    base = cfg["actionability_base"]
    if any(kw.lower() in text for kw in cfg["actionability_keywords"]):
        return _clamp(base + 1)
    return _clamp(base)


def _purpose_alignment(article: dict, cfg: dict) -> int:
    by_topic = cfg["purpose_alignment_by_topic"]
    matched = [by_topic[t] for t in article.get("topics", []) if t in by_topic]
    return max(matched) if matched else cfg["default_purpose_alignment"]


def _preference_fit(article: dict, cfg: dict, preferences: dict) -> int:
    pref = (preferences or {}).get(article.get("publisher", ""), {})
    score = pref.get("usefulness_score")
    return _clamp(score) if score else cfg["default_preference_fit"]


def score_article(
    article: dict,
    scoring_cfg: dict,
    topics_cfg: dict,
    preferences: dict | None = None,
    today: date | None = None,
) -> dict:
    today = today or date.today()
    text = f"{article.get('title', '')} {article.get('summary', '')}".lower()
    scores = {
        "relevance": _relevance(article, scoring_cfg),
        "impact": _impact(article, scoring_cfg, topics_cfg),
        "novelty": _novelty(article, scoring_cfg, today),
        "reliability": scoring_cfg["reliability_by_source_type"].get(
            article.get("source_type", "unknown"), 1
        ),
        "actionability": _actionability(text, scoring_cfg),
        "purpose_alignment": _purpose_alignment(article, scoring_cfg),
        "preference_fit": _preference_fit(article, scoring_cfg, preferences or {}),
    }
    weights = scoring_cfg["weights"]
    article["scores"] = scores
    article["total_score"] = round(sum(scores[k] * weights[k] for k in weights), 2)
    article["must_include"] = any(
        kw.lower() in text for kw in scoring_cfg["must_include_keywords"]
    )
    return article


def main() -> int:
    stamp = today_stamp()
    data = load_json(f"data/processed/classified-{stamp}.json")
    if data is None:
        print(f"data/processed/classified-{stamp}.json がありません。先に classify.py を実行してください。")
        return 1
    scoring_cfg = load_yaml("config/scoring.yaml")
    topics_cfg = load_yaml("config/topics.yaml")
    preferences = (load_yaml("sources/preferences.yaml") or {}).get("source_preferences") or {}
    articles = [
        score_article(a, scoring_cfg, topics_cfg, preferences)
        for a in data.get("articles", [])
    ]
    path = save_json(f"data/processed/scored-{stamp}.json", {"articles": articles})
    above = sum(1 for a in articles if a["total_score"] >= scoring_cfg["publish_threshold"])
    print(f"{len(articles)} 件を評価(しきい値以上 {above} 件)→ {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
