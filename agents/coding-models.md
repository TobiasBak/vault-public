# Coding models

OpenAI checked 2026-09-29, Anthropic 2026-09-26. Roles below reflect provider guidance, not local measurements.

## Current choice

Since 2026-10-04, Tobias talks to **Claude Opus 5.5** in T3 Code as the orchestrator. It delegates the work to **GPT-6.1 Sol** children in Pi; see [subagent delegation](subagent-delegation.md#compute-routing). Sol was chosen over Astra on 2026-09-29 for capability per task cost. No measurement yet shows Opus-orchestrates-Sol beats plain Sol on cost per finished task. Compare Opus parent usage with Pi child costs (see [Pi specifics](#pi-specifics)) before treating it as settled. Recording a preference doesn't change installed config or effort; dotfiles owns those.

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

Checked 2026-10-08: for the same supported model, Codex Fast consumes included subscription allowance at **2.5x** Standard, but purchased credits and Enterprise pay-as-you-go at **2x**. API-key billing follows API tier pricing instead. Hold reasoning effort fixed when comparing speed tiers; these are billing multipliers, not speedups. Sources: [speed](https://developers.openai.com/codex/agent-configuration/speed), [pricing](https://learn.chatgpt.com/docs/pricing).

## Choosing a setup

- Compare model, effort, instructions, tools, and host together. An API capability doesn't establish support in T3, Codex, Claude Code, or Pi.
- Measure correctness, architectural fit, corrective turns, time, and cost per successful task. See [benchmark trust](benchmark-trust.md).
- Effort labels aren't equivalent across models. Task length isn't difficulty: a big mechanical edit and a short open design question need different effort.
- Verbosity is visible detail, not reasoning depth. A short answer that drops a consequential qualifier is a failure.

## Local harness comparison, 2026-10-03

Built-in Pi codemode looked useful for latency and cost, without improving fully correct task count. This single pass does not establish a harness ranking or change the daily-provider choice.

- SWE Benchmarking: eight tasks, one run per Codex/Pi/Pi-codemode arm, all GPT-6.1 Sol medium Standard; GPT-6.1 Sol high judge. Pi used the established seven-tool benchmark suite, not its four-tool upstream default. Codex CLI 0.160.0; Pi 1.0.0.
- All arms fully passed 3/7 hidden-check tasks. Five cases were scored in every arm; mean quality was Codex 106.6, Pi 110.0, codemode 114.8 out of 125.
- On the three tasks correct in all arms, median paired elapsed ratios were Pi/Codex 1.284, codemode/Codex 0.841, codemode/Pi 0.787. Agent API-equivalent costs across all eight attempts were $2.5239/$2.4874/$1.6263, respectively.
- Codemode was used in all enabled runs. Shared host/account contention and five visible-validation failures limit the comparison. Coordinator delays were excluded from agent latency.
- Evidence: `/home/tobias/code/swe-benchmarking/setup/results/sol61-harness-20261003/REPORT.md` and `operator-analysis.json`.

## Model and host specifics

- **Sol:** tool calling needs Responses (Chat Completions works without tools). 1.05M context, US and EU residency, no Fast mode with EU residency. Supports the beta Responses [multi-agent orchestration](https://developers.openai.com/api/docs/guides/responses-multi-agent), which is separate from Codex host tools.
- **Opus 5.5:** use the effort setting rather than "think harder" prompts. A progress report can end the turn mid-work, so judge completion against evidence. Adaptive thinking is always on, and between-tool updates arrive in thinking blocks that clients must request and render. Thinking depends on prior turns, so change instructions and tools append-only. ([API notes](https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5))
- **Fable 5.1:** at low effort it searches less, so make retrieval explicit when answers depend on current facts.

### Astra specifics

- Per OpenAI's [guidance](https://developers.openai.com/api/docs/guides/latest-model#prompting-best-practices), Astra follows instructions closely and is sensitive to conflicting skills and AGENTS.md. It tends toward extra clarification, heavy formatting, and over-testing small changes. Remove conflicting coaching before adding more. Feed it original evidence, not cheaper-model summaries.
- **API:** tool calling requires Responses. No `none`/`minimal` effort, `temperature`, `top_p`, or `logprobs`. [`configuration_update`](https://developers.openai.com/api/docs/guides/reasoning#change-reasoning-mid-conversation) changes effort mid-conversation while preserving the cache. [Async tool calls](https://developers.openai.com/api/docs/guides/async-tool-calling) and WebSocket [steering](https://developers.openai.com/api/docs/guides/steering) need host support; steering doesn't cancel tools already started.
- **Interruptions:** provider [misalignment monitoring](https://developers.openai.com/api/docs/guides/safety-checks/misalignment-monitoring) can flag legitimate work. `misalignment_policy_violation` is not a transient error to retry, and AGENTS.md edits can't remove it.

### Codex specifics

- **Usage comparison:** the [TypeScript SDK](https://github.com/openai/codex/blob/main/sdk/typescript/src/events.ts) exposes token counts on `turn.completed`, not a billed dollar amount. [App-server](https://learn.chatgpt.com/docs/app-server) adds `thread/tokenUsage/updated`, account-wide quota snapshots via `account/rateLimits/read`, and aggregate token activity via `account/usage/read`. Record model, effort, requested speed tier, and usage per turn yourself; account snapshots cannot attribute consumption among concurrent clients. Subscription quota is not reconstructible from API-equivalent cost. Checked 2026-10-08: app-server's [`RateLimitWindow`](https://github.com/openai/codex/blob/main/codex-rs/app-server-protocol/src/protocol/v2/account.rs) rounds core floating-point `used_percent` to an integer, so before/after quota deltas have nearly ±1 percentage point of rounding uncertainty, even before delayed updates or concurrent usage. It is only useful for sufficiently large aggregate comparisons, not exact per-turn charges. Protocol fields vary by installed version.
- **Context management:** `features.context_management.experimental_mode` is off by default and needs a ChatGPT sign-in on Plus, Pro, or Pro Lite. It doesn't work with API keys, custom providers, or temporary structured threads ([config](https://learn.chatgpt.com/docs/config-file/config-reference), [changelog](https://learn.chatgpt.com/docs/changelog)). Local CLI 0.153.4 showed it disabled on 2026-09-05. Native cross-session memories are a separate feature, disabled in this vault's `.codex/config.toml`.
- **Subagents** ([docs](https://learn.chatgpt.com/docs/agent-configuration/subagents)): built-in default, worker, and explorer agents inherit the parent's model and effort unless custom agent files override them.
- **pnpm updates:** `pnpm add -g <package>@latest` can silently keep the previous version because of pnpm 11's release-age gate. Compare with `pnpm view <package> dist-tags.latest` and verify the executable afterward. An explicit version request installs that release and, unless strict gating is enabled, pnpm records a version-scoped `minimumReleaseAgeExclude` in its global workspace. Preserve each tool's install-script policy from dotfiles.
- **CLI backend:** a managed app-server daemon has its own installed package. Updating the CLI does not update that pinned backend; a newer CLI can still show the old backend's model picker. Compare both with `codex app-server daemon version`, not just `codex --version`. To align the backend with the installed CLI, use `codex app-server daemon update --from-cli --yes`. This pins the CLI package and restarts the daemon, potentially interrupting its sessions. `codex app-server daemon update` returns to production updates. Dotfiles owns installation policy.

### Pi specifics

Verified in installed Pi 1.0.0, 2026-10-03. Dotfiles owns `configs/pi/settings.json` and the shared `APPEND_SYSTEM.md`.

- **Response length:** the `openai-codex-responses` adapter sends `text.verbosity: "low"` by default. There is no documented general verbosity setting in Pi's settings schema; don't copy Codex's `model_verbosity` key into it.
- **Thinking display:** `hideThinkingBlock` hides reasoning from the terminal transcript, not from execution or billing. Keep response verbosity separate from reasoning effort.
- **Tool coordination:** built-in [codemode](orchestration.md#programmatic-tool-calling) filters intermediate tool results before they enter context. Keep direct tools available alongside it.
- **T3 usage gap:** nightly `0.0.46-nightly.20261003.2610` runs Pi but its Usage scanner/contract/charts omit Pi. Pi's OpenAI-backed work does not enter Codex CLI transcript totals. Pi JSONL sessions under `~/.pi/agent/sessions/` retain assistant `message.usage` token categories and `cost.total`; these can be summed per session and across delegated children. Costs are estimates, not a verified bill. Native Pi `/session` shows per-session usage/cost. See [T3 Usage](https://github.com/pingdotgg/t3code/blob/8ed276c246b6/docs/user/usage.md) and [Pi terminal usage](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/usage.md).

#### Measuring Pi throughput

Tibo's [2026-10-05 announcement](https://x.com/thsottiaux/status/2107158998495748264), posted 19:20 CEST, claims ~50% faster **default subscription** speed for GPT-6 Astra and GPT-6.1 Sol across Sign in With ChatGPT products and partners, explicitly including Pi and OpenCode. It says no changes are needed and users should feel it within two hours. His [follow-up](https://x.com/thsottiaux/status/2107159119107146237) says "Reaching 50 TPS instead of 30TPS". This is not a paid API or Fast-toggle claim; the posts do not define the TPS measurement method or percentile. Compare local subscription requests, not API benchmark figures, when checking it.

Pi JSONL can measure **effective request TPS**, not pure decode TPS: divide `message.usage.output` by the seconds between `message.timestamp` and the enclosing entry's `timestamp`. Verified in Pi 1.0.0 and 1.0.3: the adapter stamps the message before sending; the session stamps the entry on `message_end`. This includes queue/prefill, reasoning, transport retries, and generation, but excludes preceding tool execution. `usage.output` already includes `usage.reasoning`; never add it again. Total input is `input + cacheRead + cacheWrite`. First-token times and explicit backend service tiers are absent from these sessions; estimated cost can suggest a tier but cannot prove it.

On 2026-10-05, 16,270 successful Sol requests from October 3–5 showed a new 40–50.6 effective TPS upper tail across 15 sessions starting around 18:00 UTC. Earlier requests topped out near 33. This is consistent with the reported 50% faster rollout reaching some requests, not proof of its cause or a universal speedup. Evidence and scripts stay outside Git at `~/.local/state/sol-tps/2026-10-05/`.

On 2026-10-06 through 18:19 CEST, 6,017 successful Sol requests across 160 local Pi sessions had median effective TPS 26.52, p10–p90 13.55–38.97, and max 64.77. Fourteen errors and three aborts were excluded. No explicit service tiers were recorded, so these logs cannot separate Fast from Standard. The local Codex, Claude, and OpenCode stores contained no additional Sol usage records that day. Frozen metadata, source spotchecks, and the interactive chart are at `~/.local/state/sol-tps/2026-10-06/`; workload differences prevent a causal speedup claim.

### Claude Code specifics

Checked on Claude Code 2.1.287, 2026-10-02 ([settings](https://code.claude.com/docs/en/settings-reference)). Dotfiles keeps Claude, Codex, and Pi on one shared global AGENTS.md and the `~/.agents/skills` set.

- **Response length:** `verbose` and `viewMode` only change how much tool output the transcript shows. Claude has no `model_verbosity` equivalent; the built-in `Concise` output style shortens responses without reducing work.
- **Attribution:** commits get `Co-Authored-By` and PRs get a footer by default. `attribution: false` (2.1.281+) removes both.
- **Effort:** Opus 5.5 defaults to `medium` and ignores a top-level `effortLevel` in user settings; set it per model under `modelSettings` or with `/effort`.
- **Context budget:** Tobias wants Claude parents and subagents at 200K in Claude Code and T3, relying on native automatic compaction at default thresholds. `CLAUDE_CODE_DISABLE_1M_CONTEXT=1` enforces a 200K window across all Claude models. Dotfiles sets it in Claude's user settings alongside `autoCompactEnabled: true`, and in T3's service environment. T3's live `claudeAgent` provider environment also sets the cap. T3's context selector alone only adds or removes `[1m]`, which doesn't cap native-1M models. A real parent/subagent run on Claude Code 2.1.288 confirmed both at 200K, including an explicit `[1m]` child, on 2026-10-03. ([Context docs](https://code.claude.com/docs/en/model-config#extended-context), [subagent compaction](https://code.claude.com/docs/en/sub-agents#auto-compaction))
- **Discovery:** Claude reads `~/.claude/CLAUDE.md` and `~/.claude/skills`, not `~/.agents/skills`. It reads a project's AGENTS.md only when no CLAUDE.md exists there. T3 Code loads user, project, and local settings.
- **Auto memory** is on by default and builds a second, unreviewed store under `~/.claude/projects`. It's off so the vault stays the only knowledge store.

### OpenCode specifics

Tobias wants OpenCode v2 in T3 Code, not v1. Verified 2026-10-03: the installed nightly `0.0.46-nightly.20261003.2610` supports [OpenCode 2.0.18+](https://github.com/pingdotgg/t3code/releases/tag/v0.0.46-nightly.20261003.2610).

- **Active binary:** T3's `opencode` instance uses `~/.local/share/pnpm/bin/opencode`, installed as `@opencode/cli` 2.0.22. Dotfiles' bootstrap owns installation and updates. The separate `~/.local/share/t3code-opencode` v1 install was removed; do not recreate it.
- **Updater failure:** T3's provider updater installed v2 without running its required postinstall, leaving `opencode --version` to exit with "postinstall script was not run". Repair with OpenCode's [documented pnpm build permission](https://opencode.ai/v2/docs). On pnpm 11.13.1, persist `allowBuilds: {"@opencode/cli": true}` in `~/.local/share/pnpm/global/v11/pnpm-workspace.yaml`, not global `config.yaml`; verified a normal global install then runs postinstall without the extra flag. Refresh the provider through T3 afterward; the live snapshot caches failures even after the executable is repaired.
- **Migration:** v1 and v2 share OpenCode's database. Do not run them side by side. Snapshot the database before the first v2 startup; existing credentials and supported config carry over. See [the migration guide](https://opencode.ai/v2/docs/migrate-v1/).

## Retired DeepSeek Codex experiment

Tobias no longer wants the Codex → OpenCode Go → DeepSeek route. Removed 2026-10-03: the custom `codex_deepseek_go` T3 provider, separate Codex configuration, model catalog, and credential helper. Do not recreate it. Standard Codex and native OpenCode remain independent; the old test sessions are archived under `~/.local/state/codex-archives/deepseek-go-2026-10-03`.
