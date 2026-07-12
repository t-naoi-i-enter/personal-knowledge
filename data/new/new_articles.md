# 新着記事ダイジェスト 2026-07-12

候補 20件。Daily Brief の生成は Claude Code で `/morning-brief` を実行する。

## 🚨 OpenAI Fixes 18-Year-Old GNU libunwind Bug by Treating Crash Debugging Like Epidemiology

- URL: https://www.infoq.com/news/2026/07/openai-libunwind-core-dumps
- 発行元: InfoQ(種別: secondary)
- 公開日: 2026-07-09
- トピック: ai_coding
- 総合スコア: 3.5

OpenAI found two unrelated bugs masquerading as one in ChatGPT's data infrastructure. Silent hardware corruption on one Azure host and an 18-year-old race condition in GNU libunwind's setcontext function with a one-instruction vulnerability window. The breakthrough came from switching to population-level crash analysis rather than examining individual core dumps. By Steef-Jan Wiggers

## v2.1.207

- URL: https://github.com/anthropics/claude-code/releases/tag/v2.1.207
- 発行元: Claude Code Releases(種別: primary)
- 公開日: 2026-07-11
- トピック: ai_coding
- 総合スコア: 4.15

What's changed Auto mode is now available without CLAUDE_CODE_ENABLE_AUTO_MODE opt-in on Bedrock, Vertex AI, and Foundry; disable via disableAutoMode in settings Fixed the terminal freezing and keystrokes lagging while streaming responses containing very long lists, tables, paragraphs, or code blocks Fixed remote managed settings from a non-interactive run ( claude -p , the SDK) being permanently recorded as consented without ever showing the security consent dialog Fixed spurious prompt-injecti

## v2.1.202

- URL: https://github.com/anthropics/claude-code/releases/tag/v2.1.202
- 発行元: Claude Code Releases(種別: primary)
- 公開日: 2026-07-06
- トピック: ai_coding
- 総合スコア: 4.1

What's changed Added a "Dynamic workflow size" setting in /config for controlling how large Claude generally makes dynamic workflows (small/medium/large agent counts) — an advisory guideline, not an enforced cap Added workflow.run_id and workflow.name OpenTelemetry attributes to telemetry emitted by workflow-spawned agents, so a workflow run's activity can be reconstructed from OTel data Fixed a crash in the inline Ctrl+R history search when accepting or cancelling while the search was still sca

## v2.1.206

- URL: https://github.com/anthropics/claude-code/releases/tag/v2.1.206
- 発行元: Claude Code Releases(種別: primary)
- 公開日: 2026-07-10
- トピック: ai_coding
- 総合スコア: 4.05

What's changed Added directory path suggestions to /cd , matching /add-dir behavior Added a /doctor check that proposes trimming checked-in CLAUDE.md files by cutting content Claude could derive from the codebase /commit-push-pr now auto-allows git push to the repo's configured push remote ( remote.pushDefault , or the sole remote when only one is configured) in addition to origin Gateway: /login now supports Anthropic-operated public gateway endpoints EnterWorktree now asks for confirmation bef

## How Deutsche Telekom is rewiring telecommunications with AI

- URL: https://openai.com/index/deutsche-telekom
- 発行元: OpenAI News(種別: primary)
- 公開日: 2026-07-10
- トピック: ai_coding
- 総合スコア: 4.05

How Deutsche Telekom is becoming an AI-native telco with OpenAI-transforming customer service, employee workflows, network operations, and the future of voice.

## GPT-5.6 is now the preferred model in Microsoft 365 Copilot

- URL: https://openai.com/index/gpt-5-6-preferred-model-microsoft-365-copilot
- 発行元: OpenAI News(種別: primary)
- 公開日: 2026-07-09
- トピック: ai_coding
- 総合スコア: 4.05

Learn how GPT-5.6 powers Microsoft 365 Copilot with stronger AI capabilities across Word, Excel, PowerPoint, Chat, and Cowork for faster, higher-quality work.

## GPT-5.6: Frontier intelligence that scales with your ambition

- URL: https://openai.com/index/gpt-5-6
- 発行元: OpenAI News(種別: primary)
- 公開日: 2026-07-09
- トピック: ai_coding
- 総合スコア: 4.05

More intelligence from every token, stronger performance per dollar, and more capability on demand for your hardest work.

## GPT-5.5 Bio Bug Bounty

- URL: https://openai.com/index/bio-bug-bounty
- 発行元: OpenAI News(種別: primary)
- 公開日: 2026-07-09
- トピック: ai_coding
- 総合スコア: 4.05

Details about the OpenAI Bio Bounty program

## Launching our first OpenAI Certifications courses

- URL: https://openai.com/index/openai-certificate-courses
- 発行元: OpenAI News(種別: primary)
- 公開日: 2025-12-09
- トピック: ai_coding, personal_purpose
- 総合スコア: 4.05

Learn how OpenAI’s new certifications and AI Foundations courses help people build real-world AI skills, boost career opportunities, and prepare for the future of work.

## HP Inc. launches Frontier strategic partnership with OpenAI

- URL: https://openai.com/index/hp-frontier-partnership
- 発行元: OpenAI News(種別: primary)
- 公開日: 2026-06-28
- トピック: ai_coding
- 総合スコア: 4.0

HP Inc. scales its OpenAI Frontier partnership to deploy AI across customer experiences, software development, and enterprise operations.

## Predicting model behavior before release by simulating deployment

- URL: https://openai.com/index/deployment-simulation
- 発行元: OpenAI News(種別: primary)
- 公開日: 2026-06-16
- トピック: ai_coding
- 総合スコア: 4.0

OpenAI introduces Deployment Simulation, a method to predict AI model behavior before deployment using real conversation data to improve safety and evaluation accuracy.

## Introducing the OpenAI Partner Network

- URL: https://openai.com/index/introducing-openai-partner-network
- 発行元: OpenAI News(種別: primary)
- 公開日: 2026-06-14
- トピック: ai_coding
- 総合スコア: 4.0

OpenAI launches the Partner Network, investing $150M to help global partners accelerate enterprise AI adoption, deployment, and transformation.

## How Preply combines AI and human tutors to personalize learning

- URL: https://openai.com/index/preply
- 発行元: OpenAI News(種別: primary)
- 公開日: 2026-06-12
- トピック: ai_coding
- 総合スコア: 4.0

Preply uses OpenAI to launch AI-generated lesson summaries, providing personalised feedback and language learning exercises.

## v2.1.205

- URL: https://github.com/anthropics/claude-code/releases/tag/v2.1.205
- 発行元: Claude Code Releases(種別: primary)
- 公開日: 2026-07-08
- トピック: ai_coding
- 総合スコア: 3.95

What's changed Added an auto mode rule that blocks tampering with session transcript files Fixed --json-schema silently producing unstructured output when the schema was invalid, and schemas using the format keyword being rejected Fixed a message sent while Claude was working being silently lost when the turn ended at the --max-turns limit Fixed Windows worktree removal deleting files outside the worktree when an NTFS junction or directory symlink existed inside it Fixed background agents stayin

## v2.1.203

- URL: https://github.com/anthropics/claude-code/releases/tag/v2.1.203
- 発行元: Claude Code Releases(種別: primary)
- 公開日: 2026-07-07
- トピック: ai_coding
- 総合スコア: 3.95

What's changed Added a warning when your login is about to expire, so you can re-authenticate before background sessions are interrupted Added a grey ⏸ badge to the footer when in manual permission mode, making the active mode always visible Added the session's additional working directories to MCP roots/list , with notifications/roots/list_changed sent when the set changes Fixed opening or switching background agent sessions on macOS stalling for 15–20 seconds due to a false low-memory detectio

## Our approach to government and national security partnerships

- URL: https://openai.com/index/government-national-security-partnerships
- 発行元: OpenAI News(種別: primary)
- 公開日: 2026-07-08
- トピック: ai_coding
- 総合スコア: 3.95

Learn how OpenAI approaches government and national security partnerships, with principles for responsible AI use, democratic accountability, and public safety.

## Separating signal from noise in coding evaluations

- URL: https://openai.com/index/separating-signal-from-noise-coding-evaluations
- 発行元: OpenAI News(種別: primary)
- 公開日: 2026-07-08
- トピック: ai_coding
- 総合スコア: 3.95

A new analysis from OpenAI reveals issues in SWE-Bench Pro, a popular coding benchmark, raising concerns about reliability and accuracy in evaluating AI models.

## Helping K–12 educators build practical AI skills

- URL: https://openai.com/index/k-12-educators-practical-skills
- 発行元: OpenAI News(種別: primary)
- 公開日: 2026-07-08
- トピック: ai_coding
- 総合スコア: 3.95

OpenAI Academy and the Walton Family Foundation are bringing hands-on AI Skills Jams to help K–12 educators build practical AI skills for the classroom.

## Introducing GPT-Live

- URL: https://openai.com/index/introducing-gpt-live
- 発行元: OpenAI News(種別: primary)
- 公開日: 2026-07-08
- トピック: ai_coding
- 総合スコア: 3.95

A new generation of voice models for natural human-AI interaction, now powering ChatGPT Voice.

## MUFG aims to become AI-native with OpenAI

- URL: https://openai.com/index/mufg
- 発行元: OpenAI News(種別: primary)
- 公開日: 2026-07-07
- トピック: ai_coding
- 総合スコア: 3.95

MUFG uses ChatGPT Enterprise to build an AI-native organization, improve workflows, and deliver new AI-powered financial services at scale.
