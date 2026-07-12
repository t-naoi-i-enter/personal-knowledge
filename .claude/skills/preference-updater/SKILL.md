---
name: preference-updater
description: フィードバックから出力設定・テーマ優先度・情報源評価への反映を行う。軽微な出力設定のみ自動反映し、それ以外は承認候補を作る。
---

# Preference Updater

設定への反映(設計書16.18・9.5)。**自動反映できる範囲は config/feedback-rules.yaml の immediate_updates のみ。**

## 自動反映してよいもの(immediate_updates)

`config/output-preferences.yaml` を直接更新する:

- report_length(レポート全体の長さ・掲載件数の範囲)
- summary_length(1記事あたりの要約量)
- section_order(見出し構成・表示順)
- action_format(推奨アクションの形式)

更新時は同ファイル末尾の `history:` に before / after / reason / date を追記する(過去を削除しない)。

## 承認候補を作るもの(approval_required)

以下は直接変更せず `evolution/proposed/EV-YYYYMMDD-NN.yaml` に候補を保存し、本人の承認を待つ:

- config/topics.yaml の weight(topic_weight)
- self/ 配下すべて(long_term_interest / value_statement / career_goal / decision_principle)
- sources/blocked.yaml への追加(blocked_source)

## 一時的な重み付け(temporary_focus)

config/feedback-rules.yaml の `temporary_focus` は、本人が口頭で同意すれば設定してよい。
必ず start_date / end_date を付け、期限切れのものは次回実行時に null へ戻す。

## 情報源評価

sources/preferences.yaml の trust_score / usefulness_score は、本人の明示的な情報源評価
(trustworthy / promotional 等)があった場合に更新する(score.py の preference_fit に反映される)。
更新内容は本人に見せて確認してから保存する。
