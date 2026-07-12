# Personal Knowledge OS — Phase 1 MVP 実装計画

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 設計書 v1.2 の Phase 1 MVP(RSS収集→正規化→重複除去→分類→スコアリング→new_articles.json 生成、および Claude Code Skills による手動レポート生成基盤)を空リポジトリに構築する。

**Architecture:** Python スクリプト群(scripts/)がファイルベースのパイプラインを構成する(data/raw → data/processed → data/new)。AI を使わない機械的処理はすべて Python 側で行い、Claude Code Skills(.claude/skills/)が人間の起動により new_articles.json を読んで出典付きレポートを生成する。状態は JSON/Markdown/YAML のみ(SQLite は Phase 2)。

**Tech Stack:** Python 3.13(uv 管理)、feedparser、httpx、PyYAML、pydantic、rapidfuzz、python-dateutil、pytest。CI は GitHub Actions。

---

## データ契約(スクリプト間の受け渡し)

記事レコード(JSON、設計書 8.5 準拠+パイプライン拡張):

```json
{
  "source_id": "src_20260712_001",
  "title": "Article title",
  "url": "https://example.com/post",
  "publisher": "Anthropic",
  "author": null,
  "published_at": "2026-07-10",
  "event_date": null,
  "collected_at": "2026-07-12T06:00:00+09:00",
  "source_type": "primary",
  "language": "en",
  "content_hash": "sha256:...",
  "retrieval_status": "success",
  "summary": "RSS の summary/description",
  "category": "ai_coding",
  "topics": ["ai_coding"],
  "scores": {"relevance": 4, "impact": 3, "novelty": 3, "reliability": 5, "actionability": 3, "purpose_alignment": 2, "preference_fit": 3},
  "total_score": 3.4,
  "must_include": false
}
```

パイプラインの中間ファイル:

| ステージ | 入力 | 出力 |
|---|---|---|
| collect.py | config/sources.yaml | data/raw/articles-YYYYMMDD.json |
| normalize.py | data/raw/articles-YYYYMMDD.json | data/processed/normalized-YYYYMMDD.json |
| deduplicate.py | normalized + data/history/seen.json | data/processed/deduped-YYYYMMDD.json(+ seen.json 更新) |
| classify.py | deduped + config/topics.yaml | data/processed/classified-YYYYMMDD.json |
| score.py | classified + config/scoring.yaml | data/processed/scored-YYYYMMDD.json |
| export.py | scored | data/new/new_articles.json + new_articles.md |

## ファイル構成

- `CLAUDE.md`(ルート・運用ガイド)/ `.claude/skills/*/SKILL.md`(18 スキル)
- `config/`: topics.yaml, sources.yaml, people.yaml, scoring.yaml, schedules.yaml, feedback-rules.yaml
- `self/`: profile.md, current-focus.md, values.md, roles.md, interests.md, decision-principles.md
- `scripts/`: common.py, collect.py, normalize.py, deduplicate.py, classify.py, score.py, export.py, validate_links.py, aggregate_feedback.py(database.py は Phase 2 のため作らない)
- `tests/`: test_normalize.py, test_deduplicate.py, test_classify.py, test_score.py, test_export.py, test_collect.py, test_aggregate_feedback.py, fixtures/
- `journal/ decisions/ hypotheses/ evolution/ feedback/ actions/ sources/ data/ reports/` の骨格(.gitkeep)
- `.github/workflows/`: collect.yml, validate-links.yml

## タスク

### Task 1: ハーネス設定(コミット1)
- [x] 本計画書を docs/superpowers/plans/ へ保存
- [ ] CLAUDE.md(リポジトリ運用ガイド: パイプライン実行方法、Skills 運用、出典ルール、テスト実行方法)
- [ ] .gitignore(.venv, __pycache__, .pytest_cache, data/raw/ は保持方針に従い管理)
- [ ] requirements.txt / pyproject.toml(pytest 設定、pythonpath)
- [ ] README.md(セットアップ手順: uv venv → uv pip install -r requirements.txt → uv run pytest)
- [ ] `uv venv && uv pip install -r requirements.txt && uv run pytest`(0 tests, 正常終了)を確認
- [ ] コミット: `chore: 開発ハーネスを設定`

### Task 2: 設定ファイル・self・ディレクトリ骨格(コミット2)
- [ ] config/topics.yaml — 設計書 18.1 の6テーマ + keywords(分類用)
- [ ] config/sources.yaml — RSS 情報源(公式ブログ中心、source_type 付き)
- [ ] config/people.yaml — 設計書 18.3 の人物
- [ ] config/scoring.yaml — 設計書 19 の重み・しきい値・must_include キーワード
- [ ] config/schedules.yaml — daily/weekly/monthly の実行内容
- [ ] config/feedback-rules.yaml — 設計書 18.4
- [ ] self/*.md 6ファイル(設計書 4章・6章を反映したテンプレート)
- [ ] sources/registry.yaml, preferences.yaml, blocked.yaml
- [ ] journal/ decisions/ hypotheses/ evolution/ feedback/ actions/ data/ reports/ 骨格 + evolution/changelog.md
- [ ] コミット: `feat: 設定ファイルとリポジトリ骨格を追加`

### Task 3: scripts/common.py + normalize.py(TDD)
- [ ] tests/test_normalize.py: URL 正規化(utm 除去・fragment 除去・末尾スラッシュ)、日付 ISO 化、content_hash 安定性、pydantic モデル検証
- [ ] pytest 実行 → FAIL 確認
- [ ] scripts/common.py(load_yaml/load_json/save_json/now_jst)、scripts/normalize.py 実装
- [ ] pytest 実行 → PASS 確認
- [ ] コミット: `feat: 正規化処理を追加`

### Task 4: deduplicate.py(TDD)
- [ ] tests/test_deduplicate.py: URL 完全一致、content_hash 一致、rapidfuzz によるタイトル類似(>= 90)、履歴更新
- [ ] FAIL → 実装 → PASS → コミット: `feat: 重複除去を追加`

### Task 5: classify.py(TDD)
- [ ] tests/test_classify.py: キーワード→トピック付与、複数トピック、未該当は uncategorized
- [ ] FAIL → 実装 → PASS → コミット: `feat: キーワード分類を追加`

### Task 6: score.py(TDD)
- [ ] tests/test_score.py: ルールベース素点、重み付き総合スコア(設計書 19 の係数)、must_include(セキュリティ・法制度)
- [ ] FAIL → 実装 → PASS → コミット: `feat: ルールベース評価を追加`

### Task 7: export.py(TDD)
- [ ] tests/test_export.py: しきい値未満除外(must_include は残す)、スコア降順、最大件数制限、new_articles.json/md 形式
- [ ] FAIL → 実装 → PASS → コミット: `feat: new_articles 出力を追加`

### Task 8: collect.py(TDD、fixture RSS 使用・ネットワーク不要)
- [ ] tests/fixtures/sample_feed.xml + tests/test_collect.py: feedparser でのパース→記事レコード変換、source メタデータ引き継ぎ
- [ ] FAIL → 実装(httpx で取得、失敗時 retrieval_status=failed で継続)→ PASS → コミット: `feat: RSS収集を追加`

### Task 9: validate_links.py + aggregate_feedback.py(TDD)
- [ ] tests/test_aggregate_feedback.py: 設計書 11 の KPI(Useful Item Rate / Noise Rate / Action Conversion Rate / Source Compliance Rate)
- [ ] validate_links.py は Markdown から URL 抽出のみテスト(HTTP はモック不要の関数分離)
- [ ] FAIL → 実装 → PASS → コミット: `feat: リンク検証とフィードバック集計を追加`

### Task 10: Claude Code Skills(18個)
- [ ] .claude/skills/<name>/SKILL.md ×18(設計書 16 の役割 + 7 の出力形式 + 8.3 の表示形式 + 20 のチェックリストを反映)
- [ ] コミット: `feat: Claude Code Skills を追加`

### Task 11: GitHub Actions
- [ ] .github/workflows/collect.yml(毎日 21:00 UTC = JST 06:00、パイプライン実行、data/ をコミット)
- [ ] .github/workflows/validate-links.yml(週次、レポートのリンク確認)
- [ ] コミット: `ci: 収集・リンク検証ワークフローを追加`

### Task 12: 自己レビュー(最大5回)
- [ ] 各ラウンド: 全テスト実行 + 設計書との突合(Phase 1 スコープ)+ コード読み直し → 問題があれば修正コミット
- [ ] 指摘ゼロのラウンドで終了(最大5ラウンド)
