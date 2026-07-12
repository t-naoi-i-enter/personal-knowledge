"""normalize.py のテスト: URL正規化・日付ISO化・本文クリーニング・ハッシュ・記事正規化"""

from scripts.normalize import (
    clean_text,
    content_hash,
    normalize_articles,
    normalize_url,
    parse_date,
)


class TestNormalizeUrl:
    def test_strips_tracking_params_and_fragment(self):
        url = "https://Example.com/Post?utm_source=x&utm_medium=y&id=3#section"
        assert normalize_url(url) == "https://example.com/Post?id=3"

    def test_removes_trailing_slash(self):
        assert normalize_url("https://example.com/a/b/") == "https://example.com/a/b"

    def test_keeps_root_slash(self):
        assert normalize_url("https://example.com/") == "https://example.com/"

    def test_plain_url_unchanged(self):
        assert normalize_url("https://example.com/a?id=3") == "https://example.com/a?id=3"


class TestParseDate:
    def test_rfc822(self):
        assert parse_date("Thu, 10 Jul 2026 12:00:00 GMT") == "2026-07-10"

    def test_iso8601(self):
        assert parse_date("2026-07-10T09:30:00+09:00") == "2026-07-10"

    def test_none_and_invalid(self):
        assert parse_date(None) is None
        assert parse_date("") is None
        assert parse_date("not a date") is None


class TestCleanText:
    def test_strips_html_and_unescapes(self):
        assert clean_text("<p>Hello <b>world</b> &amp; more</p>") == "Hello world & more"

    def test_collapses_whitespace(self):
        assert clean_text("a\n\n  b\t c") == "a b c"


class TestContentHash:
    def test_stable_and_whitespace_insensitive(self):
        h1 = content_hash("Title", "Summary  text")
        h2 = content_hash("Title", "Summary text")
        assert h1 == h2
        assert h1.startswith("sha256:")

    def test_differs_for_different_content(self):
        assert content_hash("Title A", "s") != content_hash("Title B", "s")


class TestNormalizeArticles:
    def _raw(self, **overrides):
        raw = {
            "title": "T1",
            "url": "https://example.com/a?utm_source=x",
            "summary": "<p>S1</p>",
            "published": "2026-07-10",
            "publisher": "Pub",
            "source_type": "primary",
            "language": "en",
            "category": "ai_coding",
            "priority": "high",
        }
        raw.update(overrides)
        return raw

    def test_assigns_sequential_source_ids(self):
        out = normalize_articles(
            [self._raw(), self._raw(url="https://example.com/b")],
            collected_at="2026-07-12T06:00:00+09:00",
            date_stamp="20260712",
        )
        assert out[0]["source_id"] == "src_20260712_001"
        assert out[1]["source_id"] == "src_20260712_002"

    def test_normalizes_fields(self):
        out = normalize_articles(
            [self._raw()], collected_at="2026-07-12T06:00:00+09:00", date_stamp="20260712"
        )
        a = out[0]
        assert a["url"] == "https://example.com/a"
        assert a["published_at"] == "2026-07-10"
        assert a["summary"] == "S1"
        assert a["content_hash"].startswith("sha256:")
        assert a["collected_at"] == "2026-07-12T06:00:00+09:00"
        assert a["retrieval_status"] == "success"
        assert a["publisher"] == "Pub"
        assert a["priority"] == "high"

    def test_defaults_for_missing_metadata(self):
        out = normalize_articles(
            [{"title": "T", "url": "https://example.com/x", "summary": "", "published": None}],
            collected_at="2026-07-12T06:00:00+09:00",
            date_stamp="20260712",
        )
        a = out[0]
        assert a["published_at"] is None
        assert a["source_type"] == "unknown"
        assert a["language"] == "unknown"
        assert a["priority"] == "medium"
        assert a["topics"] == []
        assert a["must_include"] is False

    def test_truncates_long_summary(self):
        out = normalize_articles(
            [self._raw(summary="x" * 2000)],
            collected_at="2026-07-12T06:00:00+09:00",
            date_stamp="20260712",
        )
        assert len(out[0]["summary"]) <= 500

    def test_skips_articles_without_url_or_title(self):
        out = normalize_articles(
            [
                {"title": "", "url": "https://example.com/x", "summary": "", "published": None},
                {"title": "T", "url": "", "summary": "", "published": None},
                {"title": "OK", "url": "https://example.com/ok", "summary": "", "published": None},
            ],
            collected_at="2026-07-12T06:00:00+09:00",
            date_stamp="20260712",
        )
        assert [a["title"] for a in out] == ["OK"]
