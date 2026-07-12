"""deduplicate.py のテスト: URL・ハッシュ・タイトル類似による重複除去と履歴更新"""

from scripts.deduplicate import dedupe, empty_history


def _article(url="https://example.com/a", title="Claude Code 2.0 released", chash="sha256:aaa"):
    return {"url": url, "title": title, "content_hash": chash}


class TestDedupe:
    def test_all_new_articles_pass_through(self):
        new, history = dedupe([_article()], empty_history(), today="2026-07-12")
        assert len(new) == 1

    def test_removes_url_already_seen(self):
        history = empty_history()
        history["urls"]["https://example.com/a"] = "2026-07-11"
        new, _ = dedupe([_article()], history, today="2026-07-12")
        assert new == []

    def test_removes_hash_already_seen(self):
        history = empty_history()
        history["hashes"]["sha256:aaa"] = "2026-07-11"
        new, _ = dedupe([_article(url="https://other.com/b")], history, today="2026-07-12")
        assert new == []

    def test_removes_similar_title_already_seen(self):
        history = empty_history()
        history["titles"]["claude code 2.0 released today"] = "2026-07-11"
        new, _ = dedupe(
            [_article(url="https://other.com/b", chash="sha256:bbb")],
            history,
            today="2026-07-12",
        )
        assert new == []

    def test_keeps_dissimilar_title(self):
        history = empty_history()
        history["titles"]["完全に別のニュース記事タイトル"] = "2026-07-11"
        new, _ = dedupe([_article()], history, today="2026-07-12")
        assert len(new) == 1

    def test_dedupes_within_batch(self):
        articles = [
            _article(),
            _article(url="https://mirror.com/a", chash="sha256:bbb"),  # 同一タイトル
        ]
        new, _ = dedupe(articles, empty_history(), today="2026-07-12")
        assert len(new) == 1

    def test_short_subset_title_is_not_fuzzy_matched(self):
        # token_set_ratio はトークン部分集合で100になるため、
        # 短いタイトル("OpenAI"等)が長い既出タイトルに誤マッチしないこと
        history = empty_history()
        history["titles"]["openai releases gpt-5 for enterprise customers"] = "2026-07-11"
        new, _ = dedupe(
            [_article(title="OpenAI", url="https://x.com/1", chash="sha256:x")],
            history,
            today="2026-07-12",
        )
        assert len(new) == 1

    def test_token_count_gap_is_not_fuzzy_matched(self):
        # トークン数が大きく異なるタイトル同士は類似判定しない
        history = empty_history()
        history["titles"]["weekly update"] = "2026-07-11"
        new, _ = dedupe(
            [
                _article(
                    title="Weekly update on AI coding agents and developer tools",
                    url="https://x.com/2",
                    chash="sha256:y",
                )
            ],
            history,
            today="2026-07-12",
        )
        assert len(new) == 1

    def test_duplicate_refreshes_history_date(self):
        # フィードに載り続ける記事が保持期限切れ→新着として再出現しないよう、
        # 重複検出時に履歴の日付を更新する(last_seen方式)
        history = empty_history()
        history["urls"]["https://example.com/a"] = "2026-01-01"
        _, updated = dedupe([_article()], history, today="2026-07-12")
        assert updated["urls"]["https://example.com/a"] == "2026-07-12"

    def test_prunes_history_older_than_retention(self):
        history = empty_history()
        history["urls"]["https://old.example/a"] = "2020-01-01"
        history["hashes"]["sha256:old"] = "2020-01-01"
        history["titles"]["old title long gone"] = "2020-01-01"
        history["urls"]["https://recent.example/b"] = "2026-07-01"
        _, updated = dedupe([], history, today="2026-07-12")
        assert "https://old.example/a" not in updated["urls"]
        assert "sha256:old" not in updated["hashes"]
        assert "old title long gone" not in updated["titles"]
        assert "https://recent.example/b" in updated["urls"]

    def test_updates_history_with_new_articles(self):
        _, history = dedupe([_article()], empty_history(), today="2026-07-12")
        assert history["urls"]["https://example.com/a"] == "2026-07-12"
        assert history["hashes"]["sha256:aaa"] == "2026-07-12"
        assert "claude code 2.0 released" in history["titles"]
