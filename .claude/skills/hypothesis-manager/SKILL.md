---
name: hypothesis-manager
description: 仮説の登録・更新・検証結果の記録を行う。新しい考えが生まれたとき、観察により考えが変わったときに起動する。
---

# Hypothesis Manager

仮説管理(設計書16.12・6.5)。自分が現在持っている考えを仮説として管理する。

## 状態と保存先

| 状態 | 意味 | 保存先 |
|---|---|---|
| active | 検証中の現役仮説 | hypotheses/active/ |
| under_review | 新しい観察により見直し中 | hypotheses/active/(status欄で表現) |
| validated | 検証済み・支持された | hypotheses/validated/ |
| rejected | 反証された | hypotheses/rejected/ |
| revised | 修正されて新版に置き換わった | hypotheses/revised/(旧版)+ active/(新版) |

## 記録形式

`hypotheses/active/HYP-YYYYMMDD-NN.md`:

```yaml
hypothesis_id: HYP-20260712-01
created: 2026-07-12
status: active
statement: 下位層の役割は、単純実装者からAIオペレーターへ変化する
background: AI時代は下位エンジニアの役割が減少するという初期仮説から修正
observations:
  - date: 2026-07-01
    note: 下位層が不要になるのではなく、AIへの指示と検証能力が重要になっている
supersedes: null       # 修正元の仮説ID
evidence: []           # 関連する記事ID・レポート・意思決定
review_date: 2026-10-01
```

## ルール

- 仮説を修正するときは旧版を削除せず revised/ へ移し、新版に `supersedes` を付ける(設計書22.1)
- 観察・根拠には出典(記事ID・レポートファイル・本人の発言日)を付ける
- レポート生成時に関連仮説があれば、支持/反証する情報を observations に追記提案する(勝手に確定しない)
