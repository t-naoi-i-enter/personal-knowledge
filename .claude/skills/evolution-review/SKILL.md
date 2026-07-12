---
name: evolution-review
description: Knowledge OS自体の改善点を月次で分析する(情報源・テーマ・Skills・品質指標)。システムを本人の変化に追随させる。
---

# Evolution Review

Knowledge OS 自体の改善分析(設計書16.15)。本人ではなく**システム**を見直す。

## 読み込むもの

1. `feedback/metrics/` の最新集計(なければ先に `.venv\Scripts\python -m scripts.aggregate_feedback` を実行)
2. `feedback/summaries/` の当月分
3. `data/raw/` 直近数日分の failures(取得に失敗し続けている情報源)
4. `config/topics.yaml` / `config/sources.yaml` / `sources/preferences.yaml`
5. 当月の Daily/Weekly レポートの掲載傾向(ファイル名一覧と件数で十分。全文は読まない)

## 分析と提案

1. **レポート品質指標の確認**(設計書11章) — Useful Item Rate / Noise Rate / Action Conversion Rate は metrics の数値を使う。Source Compliance Rate は Phase 1 では自動集計されないため、当月レポート数件をサンプリングして source-validator のチェックリストで目視確認する(Phase 2 で自動化)。目標: useful↑ noise↓ action↑ compliance=100%
2. **不要な情報源の特定** — 掲載されない・不要評価が続く・取得失敗が続くソース。削減候補を出す(完全除外は本人承認必須)
3. **新しいテーマ・人物・情報源の提案** — 本人の関心変化(monthly-self-review の結果)に対応するもの
4. **topics.yaml の重み変更案** — 根拠となるフィードバック件数・期間を明示(feedback-rules.yaml のしきい値を満たすもののみ)
5. **Skills・プロンプトの改善案** — レポート生成で毎回手直ししている点があれば SKILL.md の修正案を出す

## 出力

- 提案はすべて `evolution/proposed/EV-YYYYMMDD-NN.yaml` に保存(profile-updater と同形式)
- 自動反映してよいのは feedback-rules.yaml の immediate_updates に列挙された項目のみ(→ /preference-updater)
- 分析サマリは `reports/monthly/YYYY-MM-evolution.md` に保存する
