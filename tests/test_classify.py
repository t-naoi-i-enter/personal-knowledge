"""classify.py のテスト: config/topics.yaml のキーワードによるトピック分類"""

from scripts.classify import classify_article

TOPICS_CFG = {
    "topics": {
        "ai_coding": {"weight": 20, "keywords": ["claude code", "mcp", "生成ai"]},
        "engineering_management": {"weight": 25, "keywords": ["テックリード", "tech lead"]},
    }
}


def _article(title, summary=""):
    return {"title": title, "summary": summary, "topics": []}


class TestClassifyArticle:
    def test_matches_single_topic_case_insensitive(self):
        a = classify_article(_article("Claude Code 2.0 Released"), TOPICS_CFG)
        assert a["topics"] == ["ai_coding"]

    def test_matches_keyword_in_summary(self):
        a = classify_article(_article("今週のニュース", "生成AIの組織展開について"), TOPICS_CFG)
        assert a["topics"] == ["ai_coding"]

    def test_matches_multiple_topics(self):
        a = classify_article(_article("テックリードのためのMCP入門"), TOPICS_CFG)
        assert set(a["topics"]) == {"ai_coding", "engineering_management"}

    def test_no_match_becomes_uncategorized(self):
        a = classify_article(_article("全く関係ない園芸の話"), TOPICS_CFG)
        assert a["topics"] == ["uncategorized"]

    def test_word_boundary_for_short_ascii_keywords(self):
        # "mcp" が "PMCPortal" のような部分文字列に誤マッチしない
        a = classify_article(_article("PMCPortal update"), TOPICS_CFG)
        assert a["topics"] == ["uncategorized"]
