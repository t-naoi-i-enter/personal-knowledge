"""score.py のテスト: ルールベース評価(設計書19章)"""

from datetime import date

from scripts.score import score_article

SCORING = {
    "weights": {
        "relevance": 0.25,
        "impact": 0.20,
        "novelty": 0.10,
        "reliability": 0.15,
        "actionability": 0.15,
        "purpose_alignment": 0.05,
        "preference_fit": 0.10,
    },
    "publish_threshold": 3.0,
    "relevance_by_priority": {"high": 4, "medium": 3, "low": 2},
    "impact_by_topic_weight": [
        {"min_weight": 25, "score": 5},
        {"min_weight": 20, "score": 4},
        {"min_weight": 15, "score": 3},
        {"min_weight": 0, "score": 2},
    ],
    "uncategorized_impact": 1,
    "novelty_by_age_days": [
        {"max_days": 1, "score": 5},
        {"max_days": 3, "score": 4},
        {"max_days": 7, "score": 3},
        {"max_days": 30, "score": 2},
    ],
    "stale_novelty": 1,
    "reliability_by_source_type": {
        "primary": 5,
        "research": 4,
        "secondary": 3,
        "opinion": 2,
        "social": 1,
        "unknown": 1,
    },
    "actionability_base": 3,
    "actionability_keywords": ["release", "発表"],
    "purpose_alignment_by_topic": {"public_policy": 4, "personal_purpose": 5},
    "default_purpose_alignment": 2,
    "default_preference_fit": 3,
    "must_include_keywords": ["vulnerability", "脆弱性"],
}

TOPICS = {
    "topics": {
        "ai_coding": {"weight": 20},
        "engineering_management": {"weight": 25},
        "public_policy": {"weight": 10},
    }
}

TODAY = date(2026, 7, 12)


def _article(**overrides):
    a = {
        "title": "Claude Code release",
        "summary": "",
        "url": "https://example.com/a",
        "publisher": "Example",
        "published_at": "2026-07-11",
        "source_type": "primary",
        "priority": "high",
        "topics": ["ai_coding"],
    }
    a.update(overrides)
    return a


class TestScoreArticle:
    def test_full_weighted_total(self):
        a = score_article(_article(), SCORING, TOPICS, preferences={}, today=TODAY)
        assert a["scores"] == {
            "relevance": 5,  # priority high(4) + トピック該当(+1)
            "impact": 4,  # ai_coding weight 20
            "novelty": 5,  # 1日前
            "reliability": 5,  # primary
            "actionability": 4,  # base 3 + "release"
            "purpose_alignment": 2,
            "preference_fit": 3,
        }
        assert a["total_score"] == 4.3
        assert a["must_include"] is False

    def test_uncategorized_gets_low_scores(self):
        a = score_article(
            _article(topics=["uncategorized"], priority="medium", title="Gardening"),
            SCORING,
            TOPICS,
            preferences={},
            today=TODAY,
        )
        assert a["scores"]["relevance"] == 2  # 3 - 1
        assert a["scores"]["impact"] == 1

    def test_novelty_stale_when_old_or_unknown(self):
        old = score_article(_article(published_at="2026-01-01"), SCORING, TOPICS, {}, TODAY)
        unknown = score_article(_article(published_at=None), SCORING, TOPICS, {}, TODAY)
        assert old["scores"]["novelty"] == 1
        assert unknown["scores"]["novelty"] == 1

    def test_purpose_alignment_by_topic(self):
        a = score_article(
            _article(topics=["public_policy"], title="行政DXの話"),
            SCORING,
            TOPICS,
            {},
            TODAY,
        )
        assert a["scores"]["purpose_alignment"] == 4

    def test_must_include_keyword_in_title(self):
        a = score_article(
            _article(title="重大な脆弱性が発見された", topics=["uncategorized"], priority="low"),
            SCORING,
            TOPICS,
            {},
            TODAY,
        )
        assert a["must_include"] is True

    def test_preference_fit_from_source_preferences(self):
        prefs = {"Example": {"usefulness_score": 5}}
        a = score_article(_article(), SCORING, TOPICS, preferences=prefs, today=TODAY)
        assert a["scores"]["preference_fit"] == 5

    def test_scores_clamped_to_1_5(self):
        a = score_article(
            _article(priority="low", topics=["uncategorized"], title="zzz"),
            SCORING,
            TOPICS,
            {},
            TODAY,
        )
        assert all(1 <= v <= 5 for v in a["scores"].values())
