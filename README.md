# Personal Knowledge OS

AIを活用した自分専用の Chief of Staff(戦略参謀)。

世界で起きている変化と、自分自身の関心・役割・価値観・問題意識の変化を継続的に取り込み、「今の自分は、何を考え、何を意思決定し、何を行動すべきか」を導き出す。

- 設計書: [docs/design.md](docs/design.md)
- 運用ガイド(Claude Code向け): [CLAUDE.md](CLAUDE.md)

## セットアップ

[uv](https://docs.astral.sh/uv/) を使用する(Python 3.13)。

```powershell
uv venv
uv pip install -r requirements.txt
.venv\Scripts\python -m pytest   # テスト実行
```

## 毎日の流れ(Phase 1 MVP)

1. GitHub Actions が毎朝 RSS を収集し `data/new/new_articles.json` を生成・コミット(手動実行も可、下記)
2. Claude Code を起動し `/morning-brief` → 出典付き Daily Brief が `reports/daily/` に生成される
3. 読後に `/report-feedback` でコメント・評価を記録 → 次回以降のレポートへ反映

手動でパイプラインを実行する場合:

```powershell
.venv\Scripts\python -m scripts.collect
.venv\Scripts\python -m scripts.normalize
.venv\Scripts\python -m scripts.deduplicate
.venv\Scripts\python -m scripts.classify
.venv\Scripts\python -m scripts.score
.venv\Scripts\python -m scripts.export
```

## アーキテクチャ

```
外部情報源(RSS・公式ブログ・GitHub Releases)
    ↓ Python Collector(取得・正規化・重複除去・分類・ルールベース評価)
data/new/new_articles.json
    ↓ Claude Code Skills(分析・統合・意思決定支援 — 本人が手動実行)
出典付きレポート(Daily / Weekly / Monthly / Deep Dive)
    ↓ 本人のコメント・評価・行動判断
Feedback Analyzer → 本人承認 → 次回へ反映
```

## ロードマップ

- **Phase 1(現在)**: GitHub Actions + Python + Claude Code 手動実行。API は使わない
- **Phase 2**: SQLite による知識蓄積、Monthly Self Review、アクション追跡の本格化
- **Phase 3**: MCP による業務接続(GitHub / Slack / 社内文書)
- **Phase 4**: 専用UI(Next.js)
- **Phase 5**: 価値が確認できた場合のみ完全自動化(本人承認型は維持)
