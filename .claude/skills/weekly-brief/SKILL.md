---
name: weekly-brief
description: 1週間分の情報を横断分析して Weekly CEO Brief を生成する。毎週1回本人が起動する。
---

# Weekly CEO Brief

1週間分の情報を横断分析する戦略レポート(設計書7.2)。

## 読み込むもの

1. `reports/daily/` の直近7日分の Daily Brief
2. `feedback/structured/` の直近7日分のフィードバック
3. `self/current-focus.md`
4. `decisions/decided/` の今週分(あれば)
5. `config/people.yaml` — 人物ウォッチ対象(週次で確認、設計書14.4)

## 手順

1. 個別記事の再掲ではなく、**複数情報から見える共通トレンド**を抽出する
2. technology-analyst / mba-analyst / business-analyst / chief-of-staff の観点を統合する
3. 人物ウォッチ: `config/people.yaml` の priority: high の人物について WebSearch で今週の発信(ブログ・講演・インタビュー等)を確認し、あれば以前の主張との差分・一貫性を分析する(設計書5.6)。取得した発信には必ず出典を付ける。見つからなければ省略してよい
4. 保存前に source-validator のチェックリストを実行する
5. `reports/weekly/YYYY-Wnn.md`(例: 2026-W28.md)に保存する

## レポート構成(この順で)

1. 今週最も重要だった変化
2. 複数情報から見える共通トレンド
3. 技術への影響
4. 組織への影響
5. 事業への影響
6. MBA視点での考察
7. 自分の関心の変化(今週のフィードバックから読み取れるもの。事実と推測を分ける)
8. 今週の重要な意思決定(decisions/ から)
9. 来週考えるべきこと
10. 推奨アクション
11. 出典一覧(# Sources)

末尾に # Feedback 欄を付ける。記事ID は `WB-YYYYMMDD-NN`。

Daily Brief を出典として使う場合は対象ファイル名を、自分の記録を使う場合はファイルと記録日を示す(設計書7.3)。
