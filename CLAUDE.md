# Personal Knowledge OS

自分専用の Chief of Staff(戦略参謀)AI。ニュース要約ツールではなく、世界の変化と自分自身の変化を取り込み「次に何を意思決定すべきか」を導くための個人向け知識OS。

設計書: [docs/design.md](docs/design.md) / 実装計画: [docs/superpowers/plans/2026-07-12-knowledge-os-mvp.md](docs/superpowers/plans/2026-07-12-knowledge-os-mvp.md)

## 基本原則(必ず守る)

1. **AIは最後に使う** — 取得・正規化・重複除去・分類・基礎スコアリングは Python(scripts/)で行う。Claude は重要度の最終判断・意味付け・統合・提案のみ担当する。
2. **出典のない外部情報は掲載しない** — レポートの全トピックに出典(タイトル・発行元・公開日・URL)を付け、事実と解釈を分ける。保存前に source-validator を実行する。
3. **自己進化は本人承認型** — profile / values / topics の重み等を勝手に変更しない。変更案は `evolution/proposed/` に保存し、本人の承認後にのみ反映して `evolution/changelog.md` に記録する。
4. **過去を削除しない** — 価値観・仮説・意思決定は履歴として残す(before / after / reason / date / source)。
5. **矛盾を無理に統合しない** — 相反する価値観・志は同時に存在するものとして管理する。

## パイプライン(AIを使わない部分)

```
uv venv && uv pip install -r requirements.txt   # 初回のみ
.venv\Scripts\python scripts/collect.py         # RSS取得 → data/raw/
.venv\Scripts\python scripts/normalize.py       # 正規化 → data/processed/
.venv\Scripts\python scripts/deduplicate.py     # 重複除去(data/history/seen.json と照合)
.venv\Scripts\python scripts/classify.py        # キーワード分類(config/topics.yaml)
.venv\Scripts\python scripts/score.py           # ルールベース評価(config/scoring.yaml)
.venv\Scripts\python scripts/export.py          # → data/new/new_articles.json / .md
```

GitHub Actions(.github/workflows/collect.yml)が毎朝これを自動実行し、結果をコミットする。

## テスト

```
.venv\Scripts\python -m pytest
```

スクリプトを変更したら必ずテストを実行する。ネットワークに依存するテストは書かない(fixtureを使う)。

## Skills 運用(MVP: 手動実行のみ)

- 毎日: `/morning-brief`(data/new/new_articles.json を読んで Daily Brief 生成)→ 読後に `/report-feedback`。必要に応じ `/reflection`
- 毎週: `/weekly-brief`、`/feedback-analyzer`
- 毎月: `/monthly-self-review`、`/evolution-review`
- 随時: `/deep-dive`、`/decision-capture`、`/hypothesis-manager`

レポートは `reports/{daily,weekly,monthly,deep-dive}/` に保存する。記事IDは `DB-YYYYMMDD-NN` 形式。レポート生成時は日常分析に `self/current-focus.md` のみを使い、profile.md 全体を毎回読み込まない(トークン削減)。

## ディレクトリの役割

- `config/` — 収集テーマ・情報源・スコアリング等の設定(重み変更は本人承認制)
- `self/` — 本人のプロフィール・関心・価値観(履歴保持)
- `data/` — パイプラインの入出力(raw → processed → new、履歴は history)
- `reports/` — 生成レポート、`feedback/` — レポートへの反応、`actions/` — 提案アクションの追跡
- `decisions/` `hypotheses/` — 意思決定と仮説の履歴、`evolution/` — 自己進化の提案と承認記録

## レポート保存前チェック(設計書20章)

全項目に出典リンク・発行元・公開日がある / 一次・二次情報を区別 / 解釈を事実として書かない / 記事IDとフィードバック欄がある / 末尾に Sources 一覧がある。満たさない場合は完成扱いにしない。
