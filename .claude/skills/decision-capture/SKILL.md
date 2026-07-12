---
name: decision-capture
description: 重要な意思決定を構造化して記録する。何かを決めたとき・決めようとしているときに起動する。
---

# Decision Capture

意思決定の構造化記録(設計書16.11・6.3)。

## 手順

1. 本人から聞き取る(不足項目のみ質問する):
   - 何を決めたか(または決めようとしているか)
   - どの選択肢があったか
   - なぜその判断をしたか
   - 判断時点の前提
   - 想定したリスク
   - いつ見直すか
2. 決定済みなら `decisions/decided/DEC-YYYYMMDD-NN.md`、検討中なら `decisions/pending/` に保存する
3. 関連する仮説(hypotheses/)があればリンクする

## 記録形式

```yaml
decision_id: DEC-20260712-01
date: 2026-07-12
title: 完全自動化ではなく手動実行を選択
status: decided        # pending / decided
decision: APIコストを避けてClaude Codeの手動実行で開始する
options_considered:
  - Anthropic APIによる完全自動化
  - Claude Code手動実行
reasons:
  - まず価値を検証したい
  - 継続コストを抑えたい
  - 人間の確認を残したい
assumptions:
  - 毎朝5分の手動実行は継続可能
risks:
  - 実行忘れによる情報の欠落
review_date: 2026-10-01
related_hypotheses: []
outcome: null          # 実行後に decisions/outcomes/ で記録
```

## 実行後の結果記録

見直し時期が来たら、または結果が出たら `decisions/outcomes/DEC-YYYYMMDD-NN-outcome.md` に:
実行内容 / 結果 / 学び / 前提は正しかったか を記録する(設計書6.6)。
過去の記録は削除・上書きしない(設計書22.1)。
