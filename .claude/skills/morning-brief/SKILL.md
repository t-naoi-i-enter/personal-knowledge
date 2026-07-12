---
name: morning-brief
description: data/new/new_articles.json から出典付き Daily Brief を生成する。毎朝、収集パイプライン実行後に本人が起動する。
---

# Morning Brief

新着情報から Daily Brief(毎朝5分で読めるレポート)を生成する(設計書7.1)。

## 読み込むもの(これ以外は読まない — トークン削減、設計書14.4)

1. `data/new/new_articles.json` — 本日の候補記事(パイプラインで足切り済み)
2. `self/current-focus.md` — 現在の重点・問い・温度感
3. `config/output-preferences.yaml` — 出力形式の設定(長さ・見出し構成など)
4. `config/feedback-rules.yaml` の `temporary_focus` — 期間限定の優先度変更
5. `feedback/summaries/` の最新1ファイル(あれば) — 直近のフィードバック傾向

## 手順

1. ファイルがない・記事が0件なら「本日は掲載なし」とだけ報告して終了する。無理に件数を増やさない
2. 候補記事を読み、**5〜10件以内**に選別する。判断基準:
   - current-focus の重点・問いへの寄与
   - `must_include: true`(重大セキュリティ・法制度)は原則掲載する。ただしキーワード誤検出(セキュリティ勧告ではない解説記事等)と判断した場合は、除外理由をレポート末尾に1行残して除外してよい
   - temporary_focus の increase/decrease を反映
   - 直近フィードバックで「不要」とされた類の記事は除外
3. 各記事を [technology-analyst](../technology-analyst/SKILL.md) / [mba-analyst](../mba-analyst/SKILL.md) / [business-analyst](../business-analyst/SKILL.md) の観点で分析し、[chief-of-staff](../chief-of-staff/SKILL.md) の観点で優先順位と意思決定への翻訳を行う
4. [editor](../editor/SKILL.md) の基準で構成を整える
5. **保存前に [source-validator](../source-validator/SKILL.md) のチェックリストを必ず実行する**。満たさない場合は完成扱いにしない
6. `reports/daily/YYYY-MM-DD.md` に保存する

## レポート形式

冒頭: `# Daily Brief YYYY-MM-DD` と「今日重要な変化」の3行以内の要約。

各記事は記事ID `DB-YYYYMMDD-NN` を付け、次の構成(設計書8.3):

```markdown
## DB-20260711-01 記事タイトル

### 確認された事実
(出典で直接確認できる内容のみ。解釈を混ぜない)

### なぜ重要か
### 自分の業務への示唆
### MBA視点での示唆(該当する場合のみ)
### 推奨アクション(試す価値がある場合のみ)

### 出典
- [発行元:記事タイトル](URL)
  - 発行元:◯◯ / 公開日:YYYY-MM-DD / 種別:一次情報 or 二次情報
```

末尾に必ず付ける:

1. `# Sources` — 出典一覧(重複掲載しない、設計書8.4)
2. `# Feedback` — フィードバック欄(設計書9.6):最も有益だった項目 / 不要だった項目 / もっと深掘りしたいテーマ / 説明が長すぎた箇所 / 次回重点的に見たいテーマ / 実行したいアクション / 情報源への評価 / その他コメント

## 禁止事項

- 出典のない外部情報を書かない(設計書3.4)
- 事実とClaudeの解釈を混同しない(設計書8.2)
- summary にない内容を「確認された事実」に書かない。必要なら WebFetch で原文を確認するか、推測である旨を明示する
