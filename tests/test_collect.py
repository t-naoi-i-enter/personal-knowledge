"""collect.py のテスト: フィードのパースと出典メタデータの引き継ぎ(ネットワーク不使用)"""

from pathlib import Path

from scripts.collect import is_blocked, parse_feed

FIXTURE = Path(__file__).parent / "fixtures" / "sample_feed.xml"

SOURCE = {
    "name": "Example Tech Blog",
    "type": "rss",
    "category": "ai_coding",
    "priority": "high",
    "source_type": "primary",
    "language": "en",
    "url": "https://example.com/feed",
    "enabled": True,
}


class TestParseFeed:
    def _parse(self):
        return parse_feed(FIXTURE.read_text(encoding="utf-8"), SOURCE)

    def test_extracts_entries_with_links(self):
        articles = self._parse()
        assert len(articles) == 2  # link のないエントリは除外

    def test_maps_entry_fields(self):
        first = self._parse()[0]
        assert first["title"] == "Claude Code 2.0 released"
        assert first["url"] == "https://example.com/claude-code-2?utm_source=rss"
        assert "agentic" in first["summary"]
        assert first["published"] == "Fri, 10 Jul 2026 12:00:00 GMT"

    def test_carries_source_metadata(self):
        first = self._parse()[0]
        assert first["publisher"] == "Example Tech Blog"
        assert first["category"] == "ai_coding"
        assert first["priority"] == "high"
        assert first["source_type"] == "primary"
        assert first["language"] == "en"
        assert first["retrieval_status"] == "success"

    def test_missing_date_is_none(self):
        second = self._parse()[1]
        assert second["published"] is None


class TestIsBlocked:
    def test_blocks_by_name_or_url(self):
        blocked = {"blocked": [{"name": "Bad Media", "url": "https://bad.example/feed"}]}
        assert is_blocked({"name": "Bad Media", "url": "https://other.example"}, blocked)
        assert is_blocked({"name": "Other", "url": "https://bad.example/feed"}, blocked)
        assert not is_blocked(SOURCE, blocked)

    def test_empty_blocklist(self):
        assert not is_blocked(SOURCE, {"blocked": []})
        assert not is_blocked(SOURCE, None)
