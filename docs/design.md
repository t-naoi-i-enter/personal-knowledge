# Personal Knowledge OS 設計書 v1.2

## 1. 目的

AIを活用した、自分専用の Chief of Staff(戦略参謀)を構築する。

目的は、ニュースを大量に読むことではない。世界で起きている変化と、自分自身の関心・役割・価値観・問題意識の変化を継続的に取り込み、「今の自分は、何を考え、何を意思決定し、何を行動すべきか」を導き出すことを目的とする。

## 2. コンセプト

このシステムは、単なるニュース収集システムではない。Personal Knowledge Operating System(個人向け知識OS)として、自分の思考・判断・学習・行動を支援し、蓄積していく。

外部情報を収集するだけでなく、以下まで一貫して扱う。

- 世界で何が変わったか
- 自分の業務にどう影響するか
- MBAの理論とどうつながるか
- 自分の関心や問題意識がどう変化したか
- 過去にどのような意思決定をしたか
- 実行した結果、何を学んだか
- どの情報が実際に有益だったか
- どの提案が行動につながったか
- 次に何を意思決定すべきか

最終的には、「世の中がどう変化したか」「自分自身がどう変化したか」「その両方を踏まえて、次に何をすべきか」を考えられる、自分専用の戦略参謀へ育てていく。

## 3. 基本思想

### 3.1 情報収集ではなく意思決定支援

収集した記事やニュースの件数を成果としない。成果とするものは以下である。

- 新しい意思決定につながった
- 業務改善のアクションが生まれた
- 組織課題への理解が深まった
- 技術検証の優先順位が明確になった
- 事業機会やリスクを発見した
- 自分の考えの変化に気づいた
- 過去の判断を振り返ることができた
- 実行した結果から学びを得た
- 不要な情報が減った
- レポートの有用性が継続的に高まった

### 3.2 AIは最後に使う

情報の取得・整理・重複除去など、機械的に処理できる部分にはAIを使わない。Claudeは、以下のような人間に近い判断が必要な部分だけで使用する。

- 重要度の最終判断
- 業務への意味付け
- MBA理論との接続
- 複数情報の統合
- 意思決定への翻訳
- 自分自身の変化の分析
- アクションの提案
- フィードバック傾向の分析
- Knowledge OSの改善提案

### 3.3 自己進化は本人承認型にする

Claudeが勝手にプロフィール、価値観、志、判断基準を変更しない。Claudeは更新候補を提示し、本人が承認した内容だけを正式に反映する。

```
変化の検出 → 更新案の提示 → 本人による確認・承認 → 正式反映
```

一方で、レポートの長さや表示順など、重要性の低い出力設定については、自動反映可能な範囲を別途定義できるものとする。

### 3.4 出典のない外部情報は掲載しない

外部情報を根拠にした記述には、必ず出典を付ける。

- すべての主要トピックに出典リンクを付ける
- 可能な限り一次情報を優先する
- 事実とClaudeの解釈を分ける
- 出典を確認できない情報は断定しない
- 推測や将来予測は、その旨を明示する
- 出典の内容とレポート本文が一致しているか検証する

### 3.5 本人の反応を次回に活かす

レポートに対する本人のコメントや評価を、単なる感想として終わらせない。次回以降の以下へ反映する。

掲載テーマ / 情報源 / 優先順位 / レポートの長さ / 分析の深さ / MBA視点の強さ / 業務との関連付け方 / 推奨アクションの粒度 / 文体 / 不要情報の除外 / 長期的な関心や判断基準の更新候補

## 4. 支援してほしい意思決定

### 4.1 現在の業務

AI駆動開発の推進 / Claude Code・生成AIの組織展開 / AI開発標準・開発ハーネスの整備 / エンジニア生産性向上 / テックリード制度 / 組織設計 / 人材育成 / 教育制度 / 評価制度 / 技術戦略 / 開発プロセス改善 / AI時代の役割設計 / AI活用に伴う組織変革 / マネージャー・テックリード・エンジニアの役割再定義

### 4.2 技術判断

Claude Code / Anthropic / OpenAI / GitHub Copilot / Cursor / Gemini / AWS / Amazon Bedrock / MCP / AI Agent / Terraform / Next.js / Platform Engineering / Developer Experience / AIガバナンス / AIセキュリティ / 開発ハーネス / Agentic Coding / AIを活用した品質保証

### 4.3 事業判断

SIerのビジネスモデル変革 / FDE / Palantir型ビジネス / AIコンサルティング / AI導入支援 / 内製化支援 / マネージドサービス / 垂直統合 / 業務特化型AI / Platform Business / 人月モデルからの転換 / AI時代の受託開発 / 技術と業務知識を組み合わせたサービス / 継続収益型ビジネス / 顧客接点の上流化

### 4.4 キャリア・志

デジタルデバイド解消 / 地方DX / 行政DX / 公共DX / AI政策 / 社会課題の解決 / 技術と経営の両輪 / AI時代のリーダーシップ / 組織や事業を通じた社会的価値の創出 / 自分が今後どのような立場で価値を発揮するか / 肩書きではなく、何を実現したいか

## 5. 情報収集テーマ

### 5.1 AI・ソフトウェア開発

対象例: Claude Code / Anthropic / OpenAI / Gemini / GitHub Copilot / Cursor / MCP / AI Agent / Agentic Coding / AWS / Amazon Bedrock / Platform Engineering / Developer Experience / DORA / SPACE / AI駆動開発 / 開発ハーネス / ソフトウェア開発の自動化 / AIガバナンス / AIセキュリティ / コーディングエージェント / AIレビュー / AIテスト / AIによる要件定義支援

重視する観点: 何が変わったか / 従来と何が違うか / 開発現場で使えるか / 組織展開できるか / コストやライセンスへの影響 / セキュリティや統制への影響 / エンジニアの役割がどう変わるか / 既存の開発標準へどう組み込めるか / 試す価値があるか / 継続監視だけでよいか

### 5.2 エンジニアリングマネジメント

対象例: エンジニア生産性 / 評価制度 / テックリード / Engineering Manager / Product Manager / AI時代の組織 / 採用 / 育成 / 標準化 / 品質管理 / 1on1 / スキルマネジメント / Developer Experience / Platform Engineering / 組織設計 / 心理的安全性 / チェンジマネジメント / 権限移譲 / マネージャーのスパン / キャリアラダー / 技術戦略 / 組織能力

重視する観点: 現在の組織課題に適用できるか / 制度に組み込めるか / 評価や育成に活用できるか / マネージャーやテックリードの役割に影響するか / AI導入時の抵抗や変革にどう対応するか / 組織の生産性をどう評価するか / 個人比較ではなく役割ごとの価値をどう測るか / 現場で実行可能か / 管理負荷を増やさないか

### 5.3 SIer・ビジネスモデル

対象例: SIer / FDE / AIコンサルティング / SaaS / Palantir / LayerX / AIサービス / 垂直統合 / 内製化支援 / モダナイゼーション / Managed Service / 業務特化型AI / 人月ビジネス / プロフェッショナルサービス / AI時代の受託開発 / 継続課金 / ソリューションビジネス / プラットフォーム戦略 / データビジネス

重視する観点: 売上構造がどう変わるか / 人月モデルにどのような影響があるか / 顧客との関係がどう変化するか / 新しいサービスとして成立するか / 自社が提供できる価値は何か / 技術と業務知識をどう統合するか / 顧客業務へどこまで入り込むべきか / 再利用可能な資産をどう作るか / プロダクトと受託をどう組み合わせるか

### 5.4 公共・社会課題

対象例: デジタル庁 / 行政DX / 公共DX / 地方創生 / AI政策 / 国産AI / ガバメントクラウド / サイバー安全保障 / デジタルデバイド / 教育DX / 医療DX / 介護DX / 地方企業のAI活用 / デジタル公共財 / 中小企業DX / 地域産業 / 公共サービスのアクセシビリティ

重視する観点: デジタルデバイド解消につながるか / 地方と都市の格差に影響するか / 自社や自分が関われる余地があるか / 将来の事業テーマになり得るか / 社会課題と技術をどう接続できるか / 利用者側の使いやすさが考慮されているか / 技術を使える人と使えない人の格差を広げないか

### 5.5 MBA・経営

MBA関連は、ニュースではなく経営知見の収集として扱う。

- 戦略: Porter / Christensen / Dynamic Capability / Competitive Advantage / Blue Ocean Strategy / Platform Strategy / Ecosystem / Resource-Based View / Corporate Strategy / Business Model / Vertical Integration / Core Competence / Strategic Positioning
- 組織・人材: Leadership / Change Management / Organizational Behavior / HRM / Psychological Safety / Motivation / Culture / Talent Management / Organization Design / Learning Organization / Power and Influence / Team Effectiveness / Succession Planning
- マーケティング: Jobs to be Done / Customer Insight / B2B Marketing / Branding / Customer Experience / Value Proposition / Segmentation / Positioning / Go-to-Market
- 財務・会計: ROIC / 投資判断 / バリュエーション / SaaS指標 / Unit Economics / Management Accounting / Capital Allocation / Cash Flow / Business Case / Portfolio Management
- イノベーション: Lean Startup / Design Thinking / Product Management / Ambidextrous Organization / Disruptive Innovation / Open Innovation / Corporate Venture / Innovation Portfolio
- オペレーション: Lean / Six Sigma / BPM / SCM / Theory of Constraints / Service Operations / Process Design / Capacity Management / Quality Management

主な情報源候補: Harvard Business Review / MIT Sloan Management Review / Stanford Insights / INSEAD Knowledge / Wharton Knowledge / London Business School / McKinsey / BCG / Bain / Deloitte / PwC / Accenture / NRI

MBA関連の記事は、以下まで分析する: どの経営理論と関係するか / 既存理論を補強するのか、否定するのか / AI時代に何が変わったのか / 自分の組織にどう適用できるか / 実務で試せるアクションは何か / 卒業後の実務経験とどう接続できるか / 経営者視点で何を考えるべきか

### 5.6 人物ウォッチ

候補: 平将明 / 堀義人 / Sam Altman / Dario Amodei / Satya Nadella / Jensen Huang / Alex Karp / Andrew Ng / Ethan Mollick / Ben Thompson

収集対象: 公式ブログ / 講演 / インタビュー / Podcast / YouTube / 書籍 / 論文 / 政府資料 / 国会発言 / 企業発表

人物ウォッチでは、単なる最新発言だけでなく以下を分析する: 以前の主張と何が変わったか / 一貫している考えは何か / 新しく重視し始めたテーマは何か / 自分の業務やキャリアにどう関係するか / 発言と実際の行動に一貫性があるか

## 6. 自分自身から取り込む情報

### 6.1 関心の変化

関心の強弱を時系列で記録し、収集テーマの優先度に反映する。(例: Claude Codeの使い方 → AIの組織展開 → FDEやSIerのビジネスモデルへ関心が拡大)

### 6.2 役割の変化

担当業務、役職、責任範囲が変われば、必要な情報も変わる。

```yaml
roles:
  - title: Webアプリユニットマネージャー
    start_date: 2025-04
    priorities:
      - organization
      - talent_development
      - productivity
      - ai_adoption
```

役割が変わった場合は、記事評価基準やDaily Briefの観点も更新する。

### 6.3 意思決定

重要な意思決定と、その理由を記録する。記録項目: 何を決めたか / どの選択肢があったか / なぜその判断をしたか / 判断時点の前提 / 想定したリスク / いつ見直すか / 実行後の結果

### 6.4 価値観・志

価値観や志は上書きせず、履歴として残す。

```yaml
values_history:
  - date: 2026-06
    theme: career
    statement: 技術と経営の両輪で組織を牽引したい
  - date: 2026-07
    theme: purpose
    statement: 社会課題の解決の一端を担いたい
```

相反する価値観があっても、一つに決めつけない。矛盾として排除せず、同時に存在するものとして管理する。

### 6.5 仮説

自分が現在持っている考えを、仮説として管理する。仮説の状態: active / under_review / validated / rejected / revised

### 6.6 行動と結果

提案や意思決定を実行した結果も記録する(提案 → 実行 → 結果 → 学び)。これにより、一般論ではなく、自分の実績に基づいた助言が可能になる。

### 6.7 レポートへの反応

レポートを読んだ際のコメントも、自己理解の材料として保存する。短期的なレポート改善と、長期的な関心変化の両方に利用する。

## 7. アウトプット

### 7.1 Daily Brief

毎朝5分程度で読めるレポート。想定内容:

1. 今日重要な変化 / 2. 確認された事実 / 3. なぜ重要か / 4. 自分の業務との関係 / 5. MBA視点での示唆 / 6. 試す価値 / 7. 推奨アクション / 8. 出典

掲載件数は原則5〜10件以内とする。情報が少ない日は、無理に件数を増やさない。

### 7.2 Weekly CEO Brief

毎週1回生成する戦略レポート。想定内容:

1. 今週最も重要だった変化 / 2. 複数情報から見える共通トレンド / 3. 技術への影響 / 4. 組織への影響 / 5. 事業への影響 / 6. MBA視点での考察 / 7. 自分の関心の変化 / 8. 今週の重要な意思決定 / 9. 来週考えるべきこと / 10. 推奨アクション / 11. 出典一覧

### 7.3 Monthly Self Review

月に1回、自分自身の変化を分析する。想定内容:

1. 今月関心が強まったテーマ / 2. 関心が弱まったテーマ / 3. 新しく生まれた問題意識 / 4. 変化した考え方 / 5. 重要な意思決定 / 6. 意思決定の結果 / 7. 現在の仮説 / 8. 修正された仮説 / 9. 過去の自分との違い / 10. レポートへのフィードバック傾向 / 11. profile.mdの更新候補 / 12. topics.yamlの重み変更候補 / 13. 情報源の追加・削減候補 / 14. 来月重点的に追う情報

自分自身の発言や記録を出典として使う場合は、対象ファイルや記録日を示す。

### 7.4 Deep Dive

必要なときだけ実行する。日常的に自動生成せず、本人が必要と判断した場合のみ実行する。すべての主要な主張に出典を付ける。

### 7.5 Action Proposal

価値の高い情報は、具体的な行動へ変換する。候補: GitHub Issue / 技術検証タスク / チームへの共有 / 上司への報告 / 勉強会テーマ / 制度変更案 / 新規事業仮説 / MBA理論の再学習テーマ / ブログや登壇テーマ

提案には以下を含める: 何をするか / なぜ行うか / 根拠となる情報 / 期待効果 / 必要な工数 / リスク / 完了条件

## 8. 出典管理

### 8.1 基本ルール

- 各トピックに最低1件以上の出典リンクを付ける
- 可能な限り一次情報を優先する
- 二次情報を利用した場合は一次情報と区別する
- 発行元、記事タイトル、公開日、URLを記録する
- 公開日と出来事の発生日が異なる場合は両方を記録する
- 出典を確認できない情報は断定しない
- Claudeの推測や解釈は事実と分ける
- リンク切れや取得失敗を明示する
- 同じ発表を複数メディアが扱っている場合は、公式発表を代表出典とする

### 8.2 情報の区分

レポート内の記述を次の4種類に分け、混同しない。

1. **確認された事実** — 出典によって直接確認できる情報
2. **出典に基づく要約** — 出典内容を短く整理したもの
3. **Knowledge OSによる解釈** — 事実をもとに、自分の業務・組織・事業への意味を分析したもの
4. **推奨アクション** — 解釈をもとに提案する行動

### 8.3 各トピックの表示形式

```markdown
## DB-20260711-01 Claude Codeの新機能

### 確認された事実
AnthropicがClaude Codeに新しい機能を追加した。

### なぜ重要か
開発工程内の自動処理を、従来より細かく制御できる可能性がある。

### 自分の業務への示唆
AI開発標準や開発ハーネスにおける、テスト・Lint・レビュー工程の自動化に活用できる可能性がある。

### 推奨アクション
検証環境で既存の開発フローとの接続可否を確認する。

### 出典
- [Anthropic公式発表:記事タイトル](https://example.com)
  - 発行元:Anthropic
  - 公開日:2026-07-10
  - 種別:一次情報
```

### 8.4 レポート末尾の出典一覧

```markdown
# Sources

1. Anthropic, "記事タイトル", 2026-07-10
   https://example.com
2. MIT Sloan Management Review, "記事タイトル", 2026-07-09
   https://example.com
```

同じ出典を複数項目で利用した場合は、重複掲載しない。

### 8.5 出典データモデル

```json
{
  "source_id": "src_20260711_001",
  "title": "Article title",
  "url": "https://example.com",
  "publisher": "Anthropic",
  "author": "Author Name",
  "published_at": "2026-07-10",
  "event_date": "2026-07-09",
  "collected_at": "2026-07-11T06:00:00+09:00",
  "source_type": "primary",
  "language": "en",
  "content_hash": "sha256...",
  "retrieval_status": "success"
}
```

source_type: primary / secondary / research / opinion / social / unknown

### 8.6 出典の信頼性評価

- **高**: 企業や組織の公式発表 / 公式ドキュメント / 政府資料 / 査読論文 / 原著論文 / 決算資料 / 法令 / 公的統計
- **中**: 信頼性の高い報道機関 / ビジネススクールの解説 / 大手コンサルティング会社のレポート / 専門家による詳細な分析
- **低または要確認**: 出典不明の記事 / 個人ブログ / SNS投稿 / まとめ記事 / 根拠が示されていない予測 / 宣伝目的のコンテンツ

信頼性が低い情報を掲載する場合は、その旨を明示する。

## 9. フィードバック学習

### 9.1 目的

レポートに対する本人の反応を記録し、次回以降へ反映する: 掲載するテーマ / テーマの優先順位 / 情報源の選択 / 分析の深さ / レポートの長さ / 文体 / MBA視点の強さ / 業務への関連付け方 / 推奨アクションの粒度 / 不要な情報の除外 / 関心の変化 / 判断基準の変化

### 9.2 入力方法

レポート確認後に `/report-feedback` を実行するか、自然言語でコメントする。

### 9.3 フィードバックの種類

- トピック評価: important / useful / interesting / not_relevant / already_known / too_detailed / too_shallow
- 分析評価: insightful / generic / actionable / not_actionable / well_connected / weakly_connected
- 出力評価: too_long / too_short / easy_to_read / hard_to_read / too_many_items / too_few_items
- 情報源評価: trustworthy / useful / promotional / low_quality / too_repetitive
- アクション評価: will_do / consider_later / already_doing / not_worth_it / needs_more_research

### 9.4 フィードバックデータモデル

```yaml
feedback_id: FB-20260711-001
report_type: daily
report_date: 2026-07-11
section_id: DB-20260711-03

user_comment: >
  テックリード制度との関連は有益だった。
  AIツール単体の機能説明はもっと短くてよい。

ratings:
  relevance: 5
  usefulness: 4
  depth: 3
  readability: 4
  actionability: 4

labels:
  - important
  - well_connected
  - too_detailed

topic:
  primary: engineering_management
  secondary:
    - ai_coding

source_feedback:
  source_id: src_20260711_003
  rating: trustworthy

action_feedback:
  status: consider_later

created_at: 2026-07-11T08:30:00+09:00
```

### 9.5 フィードバックの反映先

- **即時反映**(次回からすぐ変更可): レポートの長さ / 1記事あたりの要約量 / リンクの表示位置 / 推奨アクションの形式 / MBA説明の長さ / 見出し構成
- **一時的な重み付け**(期間限定でテーマ優先度を変更):

```yaml
temporary_focus:
  start_date: 2026-07-11
  end_date: 2026-08-31
  increase:
    - engineering_management
    - sier_business
  decrease:
    - model_benchmarks
```

- **長期設定の更新候補**: 複数回同じ傾向が確認された場合、変更案を作る(例: 3回連続で「重要ではない」→ topics.yamlの重み引き下げ提案)
- **情報源評価**: 情報源ごとの信頼性・有用性を更新する(sources/preferences.yaml)
- **個人の変化として反映**: 長期的な関心変化が見つかった場合は、自己進化候補(evolution/proposed/)として扱う

### 9.6 レポート末尾のフィードバック欄

```markdown
# Feedback

- 最も有益だった項目:
- 不要だった項目:
- もっと深掘りしたいテーマ:
- 説明が長すぎた箇所:
- 次回重点的に見たいテーマ:
- 実行したいアクション:
- 情報源への評価:
- その他コメント:
```

各記事には一意のIDを付ける(例: DB-20260711-03)。

## 10. アクション追跡

レポートで提案されたアクションについて、本人の判断と結果を記録する。

```yaml
action_id: ACT-20260711-002
source_report: daily-2026-07-11
source_section: DB-20260711-03

proposal:
  title: AI開発標準への適用可能性を検証する

status: in_progress

user_response:
  decision: will_do
  comment: 小規模なチームで試したい

result:
  completed_at:
  outcome:
  learning:
```

状態: proposed / accepted / in_progress / completed / rejected / deferred

## 11. レポート品質指標

月次で以下を集計する: レポート掲載件数 / 有益と評価された件数 / 不要と評価された件数 / 既知情報だった件数 / 実際の行動につながった件数 / 深掘りされた件数 / 情報源別の有用性 / テーマ別の有用性 / フィードバック回答率 / 推奨アクションの採用率 / 出典不備件数

主要KPI:

- Action Conversion Rate = 行動につながった提案件数 ÷ 全提案件数
- Useful Item Rate = 有益と評価された項目数 ÷ 掲載項目数
- Noise Rate = 不要・既知と評価された項目数 ÷ 掲載項目数
- Source Compliance Rate = 出典要件を満たした項目数 ÷ 全掲載項目数

目標は掲載件数を増やすことではなく、Useful Item Rateを高め、Noise Rateを下げ、Action Conversion Rateを高め、Source Compliance Rateを100%にすること。

## 12. 全体アーキテクチャ

```
外部情報源(RSS / 公式ブログ / GitHub Releases / MBA・経営記事 / 論文 / 政府・公共情報 / 人物の発信)
    ↓
Python Collector(取得 / 正規化 / 日付判定 / 重複除去 / キーワード分類 / ルールベース評価 / 出典メタデータ保存)
    ↓
JSON / Markdown / SQLite
    ↓
Claude Code(Technology Analyst / MBA Analyst / Business Analyst / Self Reflection / Chief of Staff / Editor / Source Validator)
    ↓
出典付きアウトプット(Daily Brief / Weekly CEO Brief / Monthly Self Review / Deep Dive / GitHub Issue / Knowledge OS更新提案)
    ↓
本人が読む → コメント・評価・行動判断
    ↓
Feedback Analyzer(即時改善 / 一時的な優先度変更 / 情報源評価 / 長期的な傾向分析 / 自己進化候補)
    ↓
本人承認 → 次回の収集・分析・出力へ反映
```

## 13. 使用ツール

- **GitHub**: リポジトリ・設定・レポート・意思決定履歴・仮説・フィードバック履歴・アクション追跡の管理
- **GitHub Actions**: 毎日の情報収集 / 定期的なPython実行 / JSONやMarkdownの生成 / 収集結果のコミット / リンク確認 / データ整合性チェック。MVPではClaude CodeをGitHub Actionsから自動実行しない
- **Python**: RSS取得 / Web取得 / GitHub Release取得 / HTML本文抽出 / 正規化 / 日付判定 / URL正規化 / 重複除去 / ハッシュ生成 / ルールベース評価 / JSON生成 / Markdown生成 / SQLite保存 / リンク確認 / 出典メタデータ管理 / フィードバック集計。利用候補: feedparser / httpx / BeautifulSoup / trafilatura / PyYAML / Pydantic / sqlite3 / rapidfuzz / python-dateutil
- **Claude Code**: 情報の最終選別 / 要約 / 意味付け / 業務との関連分析 / MBA理論との接続 / 事業への影響分析 / 複数記事の統合 / 意思決定支援 / 自分自身の変化の分析 / レポート生成 / GitHub Issue候補生成 / Knowledge OS更新案の生成 / フィードバックの構造化・傾向分析 / 出典と記述の整合性確認
- **SQLite**(Phase 2以降): 記事履歴 / 分析済み管理 / URL・ハッシュ・スコア管理 / 意思決定・仮説・フィードバック履歴 / 情報源評価 / アクション履歴 / 出典とレポートの関連管理
- **MCP**(Phase 3以降): GitHub / Slack / SharePoint / Google Drive / Notion / 社内システム / 独自検索基盤。大量の定期取得には使わず、Claudeが必要なときに外部サービスを検索・操作する用途で使用する

## 14. コスト最適化方針

### 14.1 基本方針

Claudeは、考える必要がある情報だけを読む。

```
1000件取得 → Pythonで重複・古い情報を除外 → 300件
  → ルールベースで関連度を判定 → 20件
  → Claudeで分析 → 5〜10件をDaily Briefへ掲載
```

### 14.2 AIを使わない処理

RSS取得 / HTML取得 / GitHub API取得 / 日付比較 / URL正規化 / 重複除去 / キーワード分類 / タイトル類似判定 / 既読判定 / 分析済み判定 / 基礎スコアリング / リンク確認 / 出典メタデータ保存 / フィードバック件数集計

### 14.3 Claudeを使う処理

要約 / 新規性の判定 / 自分への関連度 / 組織への影響 / 事業への影響 / MBA理論との接続 / 複数記事の統合 / アクション提案 / 自分自身の変化の分析 / フィードバックコメントの解釈 / 長期的な傾向の抽出 / 出典内容と解釈の整合性確認

### 14.4 トークン削減策

記事全文を原則送らない / タイトル・概要・重要部分だけを渡す / 新規記事だけを分析する / 分析済み記事を再分析しない / URLと本文ハッシュで重複判定する / Daily Briefの件数を制限する / MBA関連は週次中心 / 人物ウォッチは週次中心 / Deep Diveは必要時のみ / profile.mdを肥大化させない / current-focus.mdだけを日常分析に使う / 毎回すべての過去レポートを読ませない / 必要な期間・テーマだけを渡す / フィードバックも対象記事に紐づくものだけを渡す / 月次分析時のみ長期履歴を参照する

## 15. Claude Code運用方針

### 15.1 MVPではAPIを利用しない

初期構成では、Anthropic APIやAmazon Bedrockを使った自動実行は行わない。Claude Codeのサブスクリプション範囲で、本人が手動実行する。

```
GitHub Actions → Pythonで情報収集 → new_articles.json生成
  → 本人がClaude Codeを起動 → /morning-brief → 出典付きDaily Brief生成
  → /report-feedback → フィードバック保存
```

これにより、API料金を抑え、AIを動かす前に内容を確認でき、不要な日は実行しなくてよく、低コストで価値検証できる。価値が十分確認できた段階で、APIによる完全自動化を検討する。

### 15.2 実行頻度

- 毎日: Pythonによる情報収集 / 必要に応じて /morning-brief、/reflection / レポート確認後に /report-feedback
- 毎週: /weekly-brief / /feedback-analyzer / 情報収集テーマの確認 / 未処理アクションの確認 / 情報源評価の確認
- 毎月: /monthly-self-review / /evolution-review / profileやtopicsの更新候補確認 / 仮説と意思決定結果の振り返り / レポート品質指標の確認

## 16. Claude Code Skills

18スキル: morning-brief / weekly-brief / deep-dive / technology-analyst / mba-analyst / business-analyst / chief-of-staff / editor / source-validator / reflection / decision-capture / hypothesis-manager / profile-updater / monthly-self-review / evolution-review / report-feedback / feedback-analyzer / preference-updater

各スキルの役割は `.claude/skills/<name>/SKILL.md` を参照(設計書16章の内容を各SKILL.mdに反映済み)。

## 17. リポジトリ構成

```
knowledge-os/
├── .claude/skills/          # 18スキル
├── config/                  # topics / people / sources / scoring / schedules / feedback-rules
├── self/                    # profile / current-focus / values / roles / interests / decision-principles
├── journal/                 # daily / weekly / monthly
├── decisions/               # pending / decided / outcomes
├── hypotheses/              # active / validated / rejected / revised
├── evolution/               # proposed / approved / changelog.md
├── feedback/                # raw / structured / summaries / metrics
├── actions/                 # proposed / active / completed / rejected / deferred
├── sources/                 # registry.yaml / preferences.yaml / blocked.yaml
├── scripts/                 # collect / normalize / deduplicate / classify / score / export / validate_links / aggregate_feedback
├── data/                    # raw / processed / new / history
├── reports/                 # daily / weekly / monthly / deep-dive
├── .github/workflows/       # collect.yml / validate-links.yml
├── tests/
├── requirements.txt
├── README.md
└── .gitignore
```

## 18. 主な設定ファイル

### 18.1 topics.yaml

```yaml
topics:
  ai_coding:            {weight: 20, frequency: daily}
  engineering_management: {weight: 25, frequency: daily}
  sier_business:        {weight: 20, frequency: weekly}
  mba:                  {weight: 15, frequency: weekly}
  public_policy:        {weight: 10, frequency: weekly}
  personal_purpose:     {weight: 10, frequency: monthly}
```

重みはClaudeが変更案を出すが、自動変更しない。

### 18.2 sources.yaml / 18.3 people.yaml

情報源はname / type / category / priority / source_type / urlを持つ。人物はname / priority / topicsを持つ。

### 18.4 feedback-rules.yaml

```yaml
feedback_rules:
  immediate_updates:
    - report_length
    - section_order
    - summary_length
    - action_format
  approval_required:
    - topic_weight
    - long_term_interest
    - value_statement
    - career_goal
    - decision_principle
    - blocked_source
  trend_thresholds:
    repeated_negative_feedback: 3
    repeated_positive_feedback: 3
    minimum_observation_period_days: 14
```

## 19. 情報評価

各記事を5段階で評価する: 関連度 / 影響度 / 新規性 / 信頼性 / 実行可能性 / 志との関連 / 過去のフィードバックとの適合度

```
総合スコア = 関連度×0.25 + 影響度×0.20 + 新規性×0.10 + 信頼性×0.15
           + 実行可能性×0.15 + 志との関連×0.05 + フィードバック適合度×0.10
```

一定スコア未満の記事はDaily Briefに掲載しない。ただし、重大なセキュリティ情報や法制度変更などは、スコアに関係なく掲載対象とする。

## 20. レポート生成時の必須チェック

保存前に source-validator を実行する。

- [ ] すべての外部情報に出典リンクがある
- [ ] 出典タイトルが記載されている
- [ ] 発行元が記載されている
- [ ] 公開日が記載されている
- [ ] 一次情報と二次情報を区別している
- [ ] 出典の内容と要約が一致している
- [ ] Claudeの解釈を事実として記載していない
- [ ] リンク切れがない
- [ ] 同じ出典が不要に重複していない
- [ ] レポート末尾にSources一覧がある
- [ ] 各記事に記事IDが付いている
- [ ] フィードバック欄がある
- [ ] 過去のフィードバックが適切に反映されている

必須項目を満たさない場合は、レポートを完成扱いにしない。

## 21. 自己進化フロー

```
会話・日記・意思決定・行動結果・フィードバック
  → Claudeが変化候補を抽出 → 事実と推測を分ける
  → evolution/proposed/へ保存 → 本人が確認 → 承認・修正・却下
  → approvedへ移動 → profile / topics / values / sourcesへ反映
  → changelogへ記録
```

更新候補はproposal_id / target / change / reason / evidence / statusを持つ。

## 22. 自己進化におけるルール

1. **過去を削除しない** — before / after / reason / date / source を必ず残す
2. **事実と推測を分ける**
3. **一度の発言だけで恒久更新しない** — 本人の明示的な依頼、複数回の同傾向、実際の行動への反映、一定期間の継続を重視する
4. **矛盾を無理に統合しない**
5. **重要項目は本人承認を必須とする** — 価値観 / 志 / キャリア目標 / 重要な判断原則 / 重点テーマ / 人物評価 / 長期的な関心 / 情報源の完全除外

## 23. ロードマップ

- **Phase 1: MVP** — GitHub / GitHub Actions / Python / Claude Code / JSON / Markdown。外部情報の自動収集、出典メタデータ保存、重複排除、new_articles.json生成、手動で出典付きDaily Brief生成、Reflection記録、意思決定の保存、Weekly Brief生成、レポートフィードバック保存、次回レポートへの軽微な改善反映
- **Phase 2: 知識蓄積** — SQLite、分析済み管理、差分分析、仮説管理、意思決定結果管理、Monthly Self Review、profile更新提案、topics重み変更提案、情報源評価、フィードバック指標、アクション追跡
- **Phase 3: 業務接続** — GitHub MCP / Slack / SharePoint / Google Drive / 社内文書・検索基盤。社内外情報の統合、チーム共有、GitHub Issue作成、業務文書との関連分析
- **Phase 4: 専用UI** — Next.js。検索 / タイムライン / テーマ別・人物別表示 / 意思決定履歴 / 仮説一覧 / Knowledge Graph / フィードバックボタン / ダッシュボード / 出典一覧
- **Phase 5: 完全自動化** — 価値が確認できた場合のみ。Anthropic API / Amazon Bedrock / Claude Code GitHub Actions / Slack自動通知。完全自動化後も、プロフィール・価値観・志・長期設定の更新は本人承認型を維持する

## 24. 最終ビジョン

このシステムはニュース要約ツールではない。半年から数年をかけて、自分の考え・関心の変化・価値観・志・役割・意思決定・行動と結果・仮説と修正履歴・レポートへの反応・有益/不要だった情報・信頼する情報源・行動につながった提案・組織運営の知見・MBA理論・AI/ソフトウェア開発の進化・SIer/IT業界の変化・世界の技術・経営・社会の変化を蓄積し続ける。

最終的には、「世界で何が変わったのか」「自分はどう変わったのか」「過去に何を考え、何を決めたのか」「その結果、何を学んだのか」「どの情報が本当に有益だったのか」「今の自分は、次に何を意思決定すべきか」を継続的に考えられる、自分専用の Chief of Staff AI を実現する。

Knowledge OS自体も固定された仕組みではなく、本人の変化とフィードバックに合わせて、収集テーマ・情報源・分析観点・出力形式・判断基準・レポートの粒度・推奨アクションの出し方を更新し続ける。

ただし、**システムが本人を決めつけるのではなく、本人が自分自身の変化を理解し、選択するための補助線として機能することを最も重要な原則とする。**
