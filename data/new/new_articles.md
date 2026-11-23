# 新着記事ダイジェスト 2026-11-23

候補 4件。Daily Brief の生成は Claude Code で `/morning-brief` を実行する。

## Google Announces Agent Compute Engine for Secure AI Agent Execution

- URL: https://www.infoq.com/news/2026/11/google-agent-compute-engine
- 発行元: InfoQ(種別: secondary)
- 公開日: 2026-11-22
- トピック: ai_coding, sier_business
- 総合スコア: 3.65

Google recently announced Agent Compute Engine, a managed service that runs AI agents in isolated microVMs, with checkpointing capabilities to suspend and resume execution environments. The design keeps credentials, API keys, and OAuth refresh tokens outside the agent sandbox, using an external Agent Gateway to authenticate requests and inject the required secrets. By Renato Losio

## Claude Code Has Been Leaking Secrets through its "Don't Ask Again" Feature

- URL: https://www.infoq.com/news/2026/11/claude-code-leaking-secrets
- 発行元: InfoQ(種別: secondary)
- 公開日: 2026-11-22
- トピック: ai_coding
- 総合スコア: 3.6

Agentic security firm Apiiro found that Claude Code has been exposing secrets in public repositories due to how it stores them in local file on developers' machines to implement "Don't Ask Again". The company identified 1,122 secrets in claude/settings.local.json files and another 1,160 in git history, in the shared settings.json, and in agent chat transcripts stored in repos. By Sergio De Simone

## AWS Lambda Now Runs GPU Inference with 48 Concurrent Invocations Sharing One Model per GPU

- URL: https://www.infoq.com/news/2026/11/aws-lambda-gpu-managed-instances
- 発行元: InfoQ(種別: secondary)
- 公開日: 2026-11-22
- トピック: ai_coding
- 総合スコア: 3.6

AWS Lambda now runs Event Functions on EC2 G-series GPU instances through Lambda Managed Instances, with up to 48 concurrent invocations sharing one model per GPU, vLLM and SGLang base images that need no handler code, and 90-minute asynchronous timeouts. Billing is the instance price plus a 9.75 percent fee; first hands-on tests report an eight-minute publish and no response streaming. By Steef-Jan Wiggers

## Perplexity and Intelligence

- URL: https://openai.com/index/perplexity-and-intelligence
- 発行元: OpenAI News(種別: primary)
- 公開日: 2026-11-22
- トピック: uncategorized
- 総合スコア: 3.05

How perplexity measures progress in AI models, and why it could help developers establish a shared approach to evaluating emerging capabilities.
