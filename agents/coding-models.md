# Coding models

OpenAI checked 2026-09-29, Anthropic 2026-09-26. Roles below reflect provider guidance, not local measurements.

## Current choice

Tobias's daily model is **GPT-6.1 Sol** in Codex via T3 Code, chosen 2026-09-29 over Astra for capability per task cost. Recording a preference doesn't change installed config or effort; dotfiles owns those.

| Model | Role | Effort |
|---|---|---|
| [GPT-6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol) | Daily driver; near-Astra on coding, computer use, and professional work at lower cost | Keep the chosen setting. API default `medium`; `low`–`max`, no `none`/`minimal` |
| [GPT-6 Astra](https://developers.openai.com/api/docs/guides/latest-model) | Hardest coding, investigation, multi-tool research | No `none` |
| [GPT-6 Sol](https://developers.openai.com/api/docs/models/gpt-6-sol) | Complex coding at a different cost and latency | Default `medium` |
| [GPT-6 Luna](https://developers.openai.com/api/docs/guides/latest-model) | Efficient work at scale | Judge whole-task cost, including retries |
| [Claude Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5) | Coding and knowledge work, long repo tasks | Start `medium`; `xhigh`/`max` only on demonstrated gains |
| [Claude Fable 5.1](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1) | Demanding reasoning, long agent runs | Start at `high` default |

## Sol vs Astra cost

Per million tokens (Standard, ≤272K input), Sol is $2 input / $0.10 cached / $10 output and Astra is $10 / $1 / $50. Codex credits keep the same ratios: 50/2.5/250 vs 250/25/1,250. ([pricing](https://developers.openai.com/api/docs/pricing), [credits](https://learn.chatgpt.com/docs/pricing#token-rates))

[Artificial Analysis](https://artificialanalysis.ai/models?cost=intelligence-vs-cost-per-task#price-cost) (2026-09-29), cost per Intelligence Index task / index score:

| Comparison | Astra | Sol | Ratio |
|---|---|---|---|
| both `xhigh` | $2.309 / 52.4 | $0.393 / 51.0 | 5.9x |
| both `max` | $3.258 / 52.7 | $0.724 / 51.8 | 4.5x |
| Astra `max`, Sol `low` | $3.258 / 52.7 | $0.131 / 42.1 | 24.9x, lower capability |

Compare model-plus-effort configurations, not model names. Credit rates don't determine subscription limits.

## Choosing a setup

- Compare model, effort, instructions, tools, and host together. An API capability doesn't establish support in T3, Codex, Claude Code, or Pi.
- Measure correctness, architectural fit, corrective turns, time, and cost per successful task. See [benchmark trust](benchmark-trust.md).
- Effort labels aren't equivalent across models. Task length isn't difficulty: a big mechanical edit and a short open design question need different effort.
- Verbosity is visible detail, not reasoning depth. A short answer that drops a consequential qualifier is a failure.

## Model-specific behavior

- **Sol:** tool calling needs Responses (Chat Completions works without tools). 1.05M context, US and EU residency, no Fast mode with EU residency. Supports the beta Responses [multi-agent orchestration](https://developers.openai.com/api/docs/guides/responses-multi-agent), which is separate from Codex host tools.
- **Opus 5.5:** use the effort setting rather than "think harder" prompts. A progress report can end the turn mid-work, so judge completion against evidence. Adaptive thinking is always on, and between-tool updates arrive in thinking blocks that clients must request and render. Thinking depends on prior turns, so change instructions and tools append-only. ([API notes](https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5))
- **Fable 5.1:** at low effort it searches less, so make retrieval explicit when answers depend on current facts.

### Astra specifics

- Per OpenAI's [guidance](https://developers.openai.com/api/docs/guides/latest-model#prompting-best-practices), Astra follows instructions closely and is sensitive to conflicting skills and AGENTS.md. It tends toward extra clarification, heavy formatting, and over-testing small changes. Remove conflicting coaching before adding more. Feed it original evidence, not cheaper-model summaries.
- **Codex context management:** `features.context_management.experimental_mode` is off by default and needs a ChatGPT sign-in on Plus, Pro, or Pro Lite. It doesn't work with API keys, custom providers, or temporary structured threads ([config](https://learn.chatgpt.com/docs/config-file/config-reference), [changelog](https://learn.chatgpt.com/docs/changelog)). Local CLI 0.153.4 showed it disabled on 2026-09-05. Native cross-session memories are a separate feature, disabled in this vault's `.codex/config.toml`.
- **API:** tool calling requires Responses. No `none`/`minimal` effort, `temperature`, `top_p`, or `logprobs`. [`configuration_update`](https://developers.openai.com/api/docs/guides/reasoning#change-reasoning-mid-conversation) changes effort mid-conversation while preserving the cache. [Async tool calls](https://developers.openai.com/api/docs/guides/async-tool-calling) and WebSocket [steering](https://developers.openai.com/api/docs/guides/steering) need host support; steering doesn't cancel tools already started.
- **Interruptions:** provider [misalignment monitoring](https://developers.openai.com/api/docs/guides/safety-checks/misalignment-monitoring) can flag legitimate work. `misalignment_policy_violation` is not a transient error to retry, and AGENTS.md edits can't remove it.
- **Codex subagents** ([docs](https://learn.chatgpt.com/docs/agent-configuration/subagents)): built-in default, worker, and explorer agents inherit the parent's model and effort unless custom agent files override them.

### Claude Code specifics

Checked on Claude Code 2.1.287, 2026-10-02 ([settings](https://code.claude.com/docs/en/settings-reference)). Dotfiles keeps Claude, Codex, and Pi on one shared global AGENTS.md and the `~/.agents/skills` set.

- **Response length:** `verbose` and `viewMode` only change how much tool output the transcript shows. Claude has no `model_verbosity` equivalent; the built-in `Concise` output style shortens responses without reducing work.
- **Attribution:** commits get `Co-Authored-By` and PRs get a footer by default. `attribution: false` (2.1.281+) removes both.
- **Effort:** Opus 5.5 defaults to `medium` and ignores a top-level `effortLevel` in user settings; set it per model under `modelSettings` or with `/effort`.
- **Discovery:** Claude reads `~/.claude/CLAUDE.md` and `~/.claude/skills`, not `~/.agents/skills`. It reads a project's AGENTS.md only when no CLAUDE.md exists there. T3 Code loads user, project, and local settings.
- **Auto memory** is on by default and builds a second, unreviewed store under `~/.claude/projects`. It's off so the vault stays the only knowledge store.

## DeepSeek V4.1 Flash in Codex

A test option added 2026-09-10, not the default. The chain is T3 Code → Codex → OpenCode Go subscription → DeepSeek; the OpenCode harness isn't involved.

- **T3 provider:** "Codex · DeepSeek Go" (`codex_deepseek_go`), model `deepseek-flash`, effort High by default (Low and Max available).
- **Codex home:** separate at `~/.codex-deepseek-go`. `config.toml` holds the endpoint `https://opencode.ai/zen/go/v1` (Responses) and effort; `models.json` holds metadata. Global AGENTS.md and skills are symlinked from the main Codex setup. The credential helper reads the existing OpenCode Go login.
- **Responses works:** Go's docs list only Chat Completions for DeepSeek, but Responses worked anyway. Verified 2026-09-10 on Codex 0.154.0 with a tool round-trip; quality and long context are untested.
- **Catalog:** the model catalog comes from DeepSeek's [Codex guide](https://api-docs.deepseek.com/quick_start/agent_integrations/codex/), with context capped at Go's 1,000,000 rather than 1,048,576. DeepSeek recommends Low for simple tasks, High for daily agent work, and Max for complex work.
- **Stale model list:** T3 may show stale models after a new login. Fix with Settings → Providers → Refresh provider status.
