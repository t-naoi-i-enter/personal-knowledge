---
name: report-feedback
description: レポートへの本人のコメント・評価を受け取り、構造化して保存する。レポートを読んだ後に起動する。
---

# Report Feedback

フィードバックの取得と構造化(設計書16.16・9章)。

## 手順

1. 本人のコメントを受け取る(引数または自然言語)。対象が曖昧なら、どのレポート・どの記事ID(DB-YYYYMMDD-NN 等)かを確認する。「今日の」なら reports/daily/ の最新
2. **rawを保存**: コメント原文を `feedback/raw/YYYY-MM-DD-NN.md` に、対象レポート名と共にそのまま保存する(要約しない)
3. **構造化して保存**: 記事ごとに `feedback/structured/FB-YYYYMMDD-NNN.yaml` を作成する(下記形式)。ラベルはコメントから推定し、推定したことを本人に見せて確認する
4. 即時反映できる形式フィードバック(too_long 等)があれば `/preference-updater` の実行を提案する

## 構造化形式(設計書9.4)

```yaml
feedback_id: FB-20260711-001
report_type: daily          # daily / weekly / monthly / deep-dive
report_date: 2026-07-11
section_id: DB-20260711-03  # レポート全体へのコメントなら null

user_comment: >
  (原文のまま)

ratings:                    # 本人が明示した場合のみ。勝手に付けない
  relevance: 5
  usefulness: 4

labels:                     # 設計書9.3から選ぶ
  - important               # トピック: important/useful/interesting/not_relevant/already_known/too_detailed/too_shallow
  - well_connected          # 分析: insightful/generic/actionable/not_actionable/well_connected/weakly_connected
                            # 出力: too_long/too_short/easy_to_read/hard_to_read/too_many_items/too_few_items
topic:
  primary: engineering_management
  secondary: [ai_coding]

source_feedback:            # 情報源への言及があった場合のみ
  source_id: src_20260711_003
  rating: trustworthy       # trustworthy/useful/promotional/low_quality/too_repetitive

action_feedback:            # 推奨アクションへの反応があった場合のみ
  status: consider_later    # will_do/consider_later/already_doing/not_worth_it/needs_more_research

created_at: 2026-07-11T08:30:00+09:00
```

## ルール

- ratingsを推定で埋めない(本人が数字を言った場合のみ)
- labelsの推定は本人に確認してから保存する
- アクション評価が will_do の場合、`actions/proposed/` に該当アクションがあれば `actions/active/` への移動を提案する(設計書10章)
