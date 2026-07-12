---
name: profile-updater
description: 日記・会話・意思決定・フィードバックから本人の変化を抽出し、profile/current-focusの更新候補を作る。自動更新は絶対にしない。
---

# Profile Updater

自己情報の更新候補作成(設計書16.13・21章)。**self/ 配下を直接編集してはならない。**

## 手順

1. 材料を読む: journal/(直近1か月)、decisions/decided/、feedback/summaries/、hypotheses/
2. 変化の候補を抽出し、**事実と推測を分ける**(設計書22.2):
   - 事実: 本人が明示的に言った・書いた・評価した内容(日付・ファイルを引用)
   - 推測: そこから読み取れる関心・価値観の変化の可能性
3. 恒久更新の条件を確認する(設計書22.3): 本人の明示的な依頼 / 複数回の同傾向 / 実際の行動への反映 / 一定期間の継続 — のいずれかを満たすか
4. 更新候補を `evolution/proposed/EV-YYYYMMDD-NN.yaml` に保存する
5. 本人に候補を提示し、承認されたら:
   - 対象ファイル(self/current-focus.md 等)を更新(履歴は残す: before/after/reason/date/source)
   - 候補ファイルを `evolution/approved/` へ移動
   - `evolution/changelog.md` に記録

## 候補の形式(設計書21章)

```yaml
proposal_id: EV-20260712-01
created: 2026-07-12
target:
  file: self/current-focus.md
change:
  increase_priority: [AIの組織展開, SIerのビジネスモデル]
  decrease_priority: [AIモデルの単純性能比較]
reason:
  - 最近の会話とレポート評価で、組織・事業への関心が強まっているため
evidence:
  - 本人の明示的な発言(journal/daily/2026-07-10.md)
  - 複数回のフィードバック(FB-20260708-002, FB-20260710-001)
status: pending      # pending / approved / rejected
```

## 禁止事項(設計書22章)

- 価値観・志・キャリア目標・判断原則・重点テーマ・長期的関心は本人承認なしに変更しない
- 一度の発言だけで恒久更新の候補にしない
- 過去の記述を削除しない。相反する価値観を無理に統合しない
