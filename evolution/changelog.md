# Evolution Changelog

Knowledge OS(profile / topics / values / sources 等)への承認済み変更の記録。
過去を削除せず、before / after / reason / date / source を必ず残す(設計書22.1)。

---

## 2026-07-13

- **レポート生成に独立レビュー(裏取り+校閲)工程を追加**(EV-20260713-01)。
  - before: 品質保証は source-validator の自己チェックリスト1段のみ(形式チェック中心)。
  - after: 執筆 → source-validator(形式) → 独立レビュー(執筆者と別 Agent による事実の裏取り+校閲) → 修正 → 保存。レポート末尾に `# Review` 節を残す。
  - 適用: deep-dive / weekly-brief / monthly-self-review は必須。morning-brief は外部数値・二次情報を含む日に起動(3件以下かつ全て一次情報の日は免除)。校閲も含める。
  - reason: FB-20260713-002「内容の裏取りはレビュワー/校閲者を設けてしっかりレビューして欲しい」。
  - source: feedback/structured/FB-20260713-002.yaml / evolution/proposed/2026-07-13-report-review-process.md
  - 反映ファイル: .claude/skills/{morning-brief,deep-dive,weekly-brief,monthly-self-review,source-validator}/SKILL.md

## 2026-07-12

- 初期構築(Phase 1 MVP)。設計書v1.2に基づく初期設定を投入。
