---
name: monthly-self-review
description: 月に1回、自分自身の変化(関心・仮説・意思決定・フィードバック傾向)を分析するレポートを生成する。
---

# Monthly Self Review

自分自身の変化の月次分析(設計書7.3・16.14)。世界の変化ではなく**自分の変化**を扱う。

## 読み込むもの(月次のみ長期履歴を参照してよい、設計書14.4)

1. `journal/` の当月分
2. `decisions/` の当月分と、review_date が到来した過去の意思決定
3. `hypotheses/` の全active仮説
4. `feedback/structured/` の当月分と `feedback/metrics/` の最新集計(なければ先に `.venv\Scripts\python -m scripts.aggregate_feedback` を実行)
5. `self/` 全ファイル(current-focus / interests / values / roles)
6. 前月の Monthly Self Review(あれば)

## レポート構成(設計書7.3、この順で)

1. 今月関心が強まったテーマ
2. 関心が弱まったテーマ
3. 新しく生まれた問題意識
4. 変化した考え方
5. 重要な意思決定
6. 意思決定の結果(outcomes/ から)
7. 現在の仮説
8. 修正された仮説
9. 過去の自分との違い(前月レビューとの比較)
10. レポートへのフィードバック傾向(metrics の数値を引用)
11. profile.md / current-focus.md の更新候補(→ /profile-updater 形式で evolution/proposed/ へ)
12. topics.yaml の重み変更候補(→ 承認制。evolution/proposed/ へ)
13. 情報源の追加・削減候補
14. 来月重点的に追う情報

## ルール

- 自分の発言・記録を出典として使う場合は、対象ファイルと記録日を示す(設計書7.3)
- 事実(本人の記録)と推測(Claudeの解釈)を分ける
- `reports/monthly/YYYY-MM.md` に保存。記事IDは `MR-YYYYMM-NN`。末尾に # Sources(参照した自分のファイル一覧)と # Feedback
- 保存前に source-validator を実行する
