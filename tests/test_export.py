"""export.py のテスト: しきい値足切り・件数制限・new_articles 出力"""

from scripts.export import render_markdown, select_articles

CFG = {"publish_threshold": 3.0, "max_export_items": 3}


def _article(score, title="T", must_include=False, **overrides):
    a = {
        "source_id": "src_20260712_001",
        "title": title,
        "url": "https://example.com/a",
        "publisher": "Pub",
        "published_at": "2026-07-11",
        "source_type": "primary",
        "summary": "S",
        "topics": ["ai_coding"],
        "total_score": score,
        "must_include": must_include,
        "scores": {},
    }
    a.update(overrides)
    return a


class TestSelectArticles:
    def test_drops_below_threshold(self):
        out = select_articles([_article(2.9), _article(3.0)], CFG)
        assert [a["total_score"] for a in out] == [3.0]

    def test_must_include_survives_low_score(self):
        out = select_articles([_article(1.0, must_include=True)], CFG)
        assert len(out) == 1

    def test_sorted_must_include_first_then_score_desc(self):
        out = select_articles(
            [_article(3.5), _article(4.5), _article(1.0, must_include=True)], CFG
        )
        assert [a["total_score"] for a in out] == [1.0, 4.5, 3.5]

    def test_caps_at_max_items_keeping_must_include(self):
        articles = [_article(s) for s in (4.9, 4.8, 4.7, 4.6)] + [
            _article(1.0, must_include=True)
        ]
        out = select_articles(articles, CFG)
        assert len(out) == 3
        assert out[0]["must_include"] is True
        assert [a["total_score"] for a in out[1:]] == [4.9, 4.8]


class TestRenderMarkdown:
    def test_contains_metadata_and_sources(self):
        md = render_markdown([_article(4.3, title="Claude Code 2.0")], "2026-07-12")
        assert "2026-07-12" in md
        assert "Claude Code 2.0" in md
        assert "https://example.com/a" in md
        assert "Pub" in md
        assert "2026-07-11" in md

    def test_empty_day_renders_notice(self):
        md = render_markdown([], "2026-07-12")
        assert "0件" in md
