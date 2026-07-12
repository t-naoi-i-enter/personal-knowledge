---
name: feedback-analyzer
description: 一定期間のフィードバックを分析し、一時的な感想と継続的な傾向を分けて改善案を出す。週次で起動する。
---

# Feedback Analyzer

フィードバック傾向の分析(設計書16.17・9.5)。

## 手順

1. `scripts/aggregate_feedback.py` を実行して機械集計を最新化する(件数集計はAIでやらない、設計書14.2)
2. `feedback/structured/` の直近2週間分と `feedback/metrics/` の最新を読む
3. **一時的な感想と継続的な傾向を分ける**。判定基準は `config/feedback-rules.yaml` の trend_thresholds(同傾向3回以上・観察期間14日以上)
4. 改善案をカテゴリ別に出す:
   - **即時反映可**(immediate_updates: レポート長・見出し構成・要約量・アクション形式)→ `/preference-updater` で config/output-preferences.yaml へ
   - **一時的な重み付け** → feedback-rules.yaml の temporary_focus 案(期間を必ず付ける)
   - **長期設定の更新候補**(topic_weight・情報源評価・長期的関心)→ `evolution/proposed/EV-*.yaml`(本人承認待ち)
   - **情報源評価** → sources/preferences.yaml の更新案(trust_score / usefulness_score)
5. 分析結果を `feedback/summaries/YYYY-MM-DD.md` に保存する(morning-brief が次回参照する)

## サマリ形式

```markdown
# フィードバック傾向 YYYY-MM-DD(対象: 過去14日)

## 数値(metricsから)
- Useful Item Rate / Noise Rate / Action Conversion Rate

## 継続的な傾向(しきい値を満たしたもの)
- 例: AIツール単体の機能記事に not_relevant が3回(7/1, 7/5, 7/9)→ 掲載縮小を提案

## 一時的な感想(傾向とはみなさないが記録)

## 次回レポートへの反映事項(即時反映分)

## 承認待ち提案(evolution/proposed/ へ保存したもの)
```

## ルール

- 個人の関心変化に踏み込む提案は必ず承認制(evolution/proposed/)。事実と推測を分ける(設計書9.5・22章)
