"""validate_links.py のテスト: MarkdownからのURL抽出(HTTP確認はCI実行時のみ)"""

from scripts.validate_links import extract_urls

MD = """
# Report

- [Anthropic発表](https://example.com/post?id=1)
- 出典: https://example.com/bare-url.
- 重複: [同じ](https://example.com/post?id=1)

```
コード内 https://example.com/in-code は対象外にしない(単純化のため抽出してよい)
```
"""


class TestExtractUrls:
    def test_extracts_and_dedupes(self):
        urls = extract_urls(MD)
        assert urls.count("https://example.com/post?id=1") == 1

    def test_strips_trailing_punctuation(self):
        urls = extract_urls(MD)
        assert "https://example.com/bare-url" in urls
        assert "https://example.com/bare-url." not in urls

    def test_markdown_link_paren_not_included(self):
        urls = extract_urls("[a](https://example.com/x)")
        assert urls == ["https://example.com/x"]

    def test_empty_text(self):
        assert extract_urls("") == []
