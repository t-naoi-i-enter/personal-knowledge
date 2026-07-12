"""build_site.py のテスト: レポート解析・フィードバック紐付け・HTML生成"""

from datetime import date

from scripts.build_site import (
    build_index_page,
    build_report_page,
    match_feedback,
    parse_report,
    parse_yaml_doc,
    render_markdown_body,
    rewrite_relative_links,
)


class TestParseReport:
    def test_daily_report(self, tmp_path):
        p = tmp_path / "2026-07-12.md"
        p.write_text("# Daily Brief 2026-07-12\n\n本文", encoding="utf-8")
        r = parse_report(p, "daily")
        assert r["title"] == "Daily Brief 2026-07-12"
        assert r["date"] == "2026-07-12"
        assert r["type"] == "daily"
        assert r["stem"] == "2026-07-12"
        assert "本文" in r["body_md"]

    def test_deep_dive_date_from_filename_prefix(self, tmp_path):
        p = tmp_path / "2026-07-12-ai-native-sier.md"
        p.write_text("# Deep Dive: AI-native", encoding="utf-8")
        r = parse_report(p, "deep-dive")
        assert r["date"] == "2026-07-12"
        assert r["stem"] == "2026-07-12-ai-native-sier"

    def test_title_falls_back_to_stem(self, tmp_path):
        p = tmp_path / "2026-07-13.md"
        p.write_text("見出しなし本文", encoding="utf-8")
        r = parse_report(p, "daily")
        assert r["title"] == "2026-07-13"


class TestMatchFeedback:
    def test_matches_by_type_and_date_normalizing_yaml_dates(self):
        report = {"type": "daily", "date": "2026-07-12"}
        fbs = [
            {"feedback_id": "FB-1", "report_type": "daily", "report_date": date(2026, 7, 12)},
            {"feedback_id": "FB-2", "report_type": "deep-dive", "report_date": date(2026, 7, 12)},
            {"feedback_id": "FB-3", "report_type": "daily", "report_date": "2026-07-11"},
        ]
        out = match_feedback(report, fbs)
        assert [f["feedback_id"] for f in out] == ["FB-1"]


class TestParseYamlDoc:
    def test_strips_code_fences(self):
        text = "```yaml\nhypothesis_id: HYP-1\nstatus: active\n```\n"
        d = parse_yaml_doc(text)
        assert d["hypothesis_id"] == "HYP-1"
        assert d["status"] == "active"

    def test_plain_yaml_without_fences(self):
        assert parse_yaml_doc("action_id: ACT-1\n")["action_id"] == "ACT-1"

    def test_invalid_returns_none(self):
        assert parse_yaml_doc("# ただのMarkdown\n\n- 箇条書き") is None


class TestRenderMarkdownBody:
    def test_headings_and_tables(self):
        html = render_markdown_body("## 見出し\n\n| a | b |\n|---|---|\n| 1 | 2 |")
        assert "<h2" in html
        assert "<table>" in html

    def test_links_rendered(self):
        html = render_markdown_body("[リンク](https://example.com)")
        assert '<a href="https://example.com">リンク</a>' in html


class TestRewriteRelativeLinks:
    def test_report_md_links_become_html(self):
        html = '<a href="../deep-dive/2026-07-12-x.md">x</a>'
        assert 'href="../deep-dive/2026-07-12-x.html"' in rewrite_relative_links(html)

    def test_repo_root_links_go_to_github(self):
        html = '<a href="../../self/current-focus.md">f</a>'
        out = rewrite_relative_links(html)
        assert (
            'href="https://github.com/t-naoi-i-enter/personal-knowledge/blob/main/self/current-focus.md"'
            in out
        )

    def test_external_links_untouched(self):
        html = '<a href="https://example.com/a.md">x</a>'
        assert rewrite_relative_links(html) == html


class TestBuildReportPage:
    def _report(self):
        return {
            "type": "daily",
            "date": "2026-07-12",
            "title": "Daily Brief 2026-07-12",
            "stem": "2026-07-12",
            "body_md": "# Daily Brief 2026-07-12\n\n本文です。",
        }

    def test_includes_body_and_feedback(self):
        fbs = [
            {
                "feedback_id": "FB-20260712-001",
                "report_type": "daily",
                "report_date": "2026-07-12",
                "user_comment": "有益だった",
                "labels": ["important"],
                "section_id": "DB-20260712-03",
            }
        ]
        html = build_report_page(self._report(), fbs)
        assert "本文です。" in html
        assert "有益だった" in html
        assert "FB-20260712-001" in html
        assert "important" in html

    def test_no_feedback_shows_placeholder(self):
        html = build_report_page(self._report(), [])
        assert "フィードバックはまだありません" in html


class TestBuildIndexPage:
    def test_lists_reports_with_links_and_extras(self):
        reports = [
            {
                "type": "daily",
                "date": "2026-07-12",
                "title": "Daily Brief 2026-07-12",
                "stem": "2026-07-12",
                "feedback_count": 2,
            }
        ]
        extras = {
            "hypotheses": [
                {"hypothesis_id": "HYP-20260712-01", "status": "active", "statement": "仮説文"}
            ],
            "actions": [
                {"action_id": "ACT-20260712-01", "status": "proposed",
                 "proposal": {"title": "真のFDE成果実績を1事例つくる"}}
            ],
            "decisions": [
                {"decision_id": "DEC-20260712-01", "status": "pending",
                 "title": "層Aをどこまでやり切るか"}
            ],
        }
        html = build_index_page(reports, extras)
        assert 'href="reports/daily/2026-07-12.html"' in html
        assert "Daily Brief 2026-07-12" in html
        assert "HYP-20260712-01" in html
        assert "真のFDE成果実績を1事例つくる" in html
        assert "層Aをどこまでやり切るか" in html
