# Coding models

OpenAI checked 2026-09-29, Anthropic 2026-09-26. The table reflects provider guidance, not Tobias's [team-routing policy](subagent-delegation.md#compute-routing) or local measurements.

## Current choice

Follow Tobias's [team-routing policy](subagent-delegation.md#compute-routing) for model roles, targets, and effort. Tobias chose Sol over Astra on 2026-09-29 for capability per task cost. No measurement shows the current team split beats plain Sol on cost per finished task; include [Pi child costs](#pi-specifics). [Dotfiles](../projects.md#dotfiles) owns installed config.

## Provider guidance

| Model | Provider positioning | Provider effort guidance |
|---|---|---|
| [GPT-6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol) | Near-Astra coding, computer use, professional work for less | `medium`–`xhigh`; API default `medium`, no `none`/`minimal` |
| [GPT-6 Astra](https://developers.openai.com/api/docs/guides/latest-model) | Hardest coding, investigation, multi-tool research | No `none` |
| [GPT-6 Sol](https://developers.openai.com/api/docs/models/gpt-6-sol) | Complex coding, different cost and latency | Default `medium` |
| [GPT-6 Luna](https://developers.openai.com/api/docs/guides/latest-model) | Efficient work at scale | Below `xhigh`, silently drops work ([local test](#haiku-55-specifics)); judge whole-task cost, including retries |
| [Claude Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5) | Coding, knowledge work, long repo tasks | Provider recommends `medium` first, `high`/`xhigh` for demonstrated gains |
| [Claude Fable 5.1](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1) | Demanding reasoning, long agent runs | Start at `high` default |
| Claude Haiku 5.5 | Summaries, compactions, database queries | API default `medium`; see [local findings](#haiku-55-specifics) |

## Sol vs Astra cost

Per million tokens, Standard with ≤272K input: Sol $2 input / $0.10 cached / $10 output; Astra $10 / $1 / $50. Codex credits: 50/2.5/250 vs 250/25/1,250. ([pricing](https://developers.openai.com/api/docs/pricing), [credits](https://learn.chatgpt.com/docs/pricing#token-rates))

[Artificial Analysis](https://artificialanalysis.ai/models?cost=intelligence-vs-cost-per-task#price-cost), 2026-09-29: cost per Intelligence Index task / index score.

| Comparison | Astra | Sol | Ratio |
|---|---|---|---|
| both `xhigh` | $2.309 / 52.4 | $0.393 / 51.0 | 5.9x |
| both `max` | $3.258 / 52.7 | $0.724 / 51.8 | 4.5x |
| Astra `max`, Sol `low` | $3.258 / 52.7 | $0.131 / 42.1 | 24.9x, lower capability |

Trust price ratios, not public-index capability gaps ([benchmark trust](benchmark-trust.md)). Compare model-plus-effort configurations; credit rates don't determine subscription limits.

Checked 2026-10-08: on the same supported model, Codex Fast consumes included subscription allowance at 2.5x Standard, purchased credits and Enterprise pay-as-you-go at 2x. API keys follow API tier pricing. Hold effort fixed: billing multipliers aren't speedups. ([speed](https://developers.openai.com/codex/agent-configuration/speed), [pricing](https://learn.chatgpt.com/docs/pricing))

## Choosing a setup

- Compare model, effort, instructions, tools, and host together; see [host vs API capabilities](orchestration.md#programmatic-tool-calling) and [benchmark trust](benchmark-trust.md). Measure correctness, architectural fit, corrective turns, time, and cost per successful task.
- Tobias rejected `low` for skipped searches, checks, and work, and `max` for costing far more than `xhigh` with little gain (2026-10-10). The [current routing policy](subagent-delegation.md#compute-routing) owns effort choices, not provider defaults or benchmark arms.
- Effort labels differ across models. Length isn't difficulty: large mechanical edits and short open design questions need different effort.
- Verbosity is visible detail, not reasoning depth. Dropping a consequential qualifier fails even in a short answer.

## Local harness comparison, 2026-10-03

Built-in Pi codemode looked useful for latency and cost, not fully correct task count. One pass establishes neither harness ranking nor a new daily provider.

- SWE Benchmarking: eight tasks, one run per Codex/Pi/Pi-codemode arm; GPT-6.1 Sol medium Standard, Sol high judge. Pi used the established seven-tool suite, not its four-tool upstream default. Codex CLI 0.160.0; Pi 1.0.0.
- All arms fully passed 3/7 hidden-check tasks. Five cases scored in every arm: mean quality 106.6/110.0/114.8 out of 125, respectively.
- Three tasks correct across arms: median paired elapsed ratios Pi/Codex 1.284, codemode/Codex 0.841, codemode/Pi 0.787. Agent API-equivalent costs over eight attempts: $2.5239/$2.4874/$1.6263.
- Codemode appeared in every enabled run. Shared host/account contention and five visible-validation failures limit comparison. Agent latency excludes coordinator delays.
- Evidence: `/home/tobias/code/swe-benchmarking/setup/results/sol61-harness-20261003/REPORT.md`, `operator-analysis.json`.

## Model specifics

- **Sol:** tools require Responses; Chat Completions works without tools. 1.05M context, US/EU residency, no Fast with EU residency. Beta Responses [multi-agent orchestration](https://developers.openai.com/api/docs/guides/responses-multi-agent) is separate from Codex host tools.
- **Opus 5.5:** set effort, don't prompt "think harder". Progress reports can end turns mid-work; verify completion. Adaptive thinking is always on; clients must request/render between-tool updates in thinking blocks. Prior turns affect thinking, so change instructions/tools append-only. ([API notes](https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5))
- **Fable 5.1:** low effort searches less; explicitly require retrieval for current facts.

### Haiku 5.5 specifics

Checked 2026-10-10, Claude Code 2.1.296. ([AA review](https://artificialanalysis.ai/articles/claude-haiku-5-5), [100K rule](https://dev.to/akaranjkar08/claude-haiku-55-pricing-the-100k-token-rule-for-agents-cgi))

- **Pricing per MTok:** ≤100K prompt, $0.10 input / $0.50 output; above, $0.50 / $2.50. Whole-request tier includes cache reads; cached input is 0.1x tier rate. Tier-1 Haiku is 20x cheaper per token than Sol's $2 / $10. Luna shares short rates through 272K input, then $0.20 / $0.02 / $0.75 ([pricing](https://developers.openai.com/api/docs/pricing)).
- **No harness enforces 100K.** Claude Code checks `modelSettings.<model>.autoCompactWindow` (minimum 100000) between turns; parallel reads can exceed it, and compaction sends full pre-compaction context. Haiku `medium` reading four large files jumped 23K→130K. A 100K window reduced over-100K requests 2→1 but added compaction and cost $0.21 vs $0.18. Use targeted searches/ranged reads. Don't globally set `CLAUDE_CODE_AUTO_COMPACT_WINDOW`: it overrides every model.
- **Local test, 2026-10-10, t3code repo:**
  - Easy: call-site census with distractor, env-var inventory, unnamed-concept search, synthetic 5.5K-line CI-log triage, doc Q&A.
  - Hard, truth hidden from models: symptom bug two call hops down; 183-line diff with 3 defects; transitive importers (24 files); null/format audit at 9 sites; parameter addition at 9 sites requiring site-specific in-scope values.

Haiku used `claude -p`; Luna/Sol `pi -p`. Hard set: 3 reps, Sol 2; API-rate mean cost/run and mean wall time over 5 tasks.

| Arm | Fully correct | Mean cost | Mean wall time |
|---|---|---|---|
| Haiku `medium` | 14/15 | $0.009 | 34s |
| Haiku `high` | 15/15 | $0.011 | 45s |
| Haiku `xhigh` | 15/15 | $0.018 | 73s |
| Luna `medium` | 11/15 | $0.004 | 27s |
| Luna `high` | 12/15 | $0.005 | 46s |
| Luna `xhigh` | 15/15 | $0.008 | 86s |
| Sol 6.1 `medium` | 10/10 | $0.081 | 46s |

- Easy set: all perfect; Haiku `low` through `xhigh`, Luna `medium`.
- Haiku's `medium` miss: changed 7/9 sites, claimed "all seven". Luna below `xhigh`: import closure stopped at 3–5/24 files, empty review, bug line 6 lines off, required format broken twice.
- No request exceeded 100K. Haiku prompts reached 97K at `xhigh`; Claude Code base prompt ~23K vs Pi ~6K. Small samples, 3 reps/cell: trust direction, not decimals.
- **Haiku `high` findings:** it bought reliability and half Luna `xhigh`'s latency for 1.4x its cost. The benchmark arms are experiments, not approved delegation roles; follow Tobias's [team-routing policy](subagent-delegation.md#compute-routing). Luna's 272K tier is more forgiving; no tested task approached it.
- **Base prompts must be far below 100K.** A T3/OpenCode setup's 100K Haiku cap with ~163K base prompt compacted every step, never finished ([issue](https://github.com/SpyrosPsarras/epaflix/issues/1739)). Haiku 5.5's tokenizer counts ~30% more tokens than 4.5's. Anthropic positions it for "summaries, compactions, or database queries" ([@ClaudeDevs](https://x.com/ClaudeDevs/status/2107895955144208813)).
- **API:** adaptive thinking only; effort `low`–`max`, default `medium`. Anthropic warns of early stopping at `low` in long agent prompts, skipped verification at `low`/`medium`, occasional empty replies at `xhigh`. Claude Code harness prompt is ~17–25K before the task.
- **T3 host:** Pi has no Haiku. Its provider target lives in the [team-routing policy](subagent-delegation.md#compute-routing).

### Astra specifics

- [OpenAI guidance](https://developers.openai.com/api/docs/guides/latest-model#prompting-best-practices): follows instructions closely, sensitive to conflicting skills/AGENTS.md. Tends toward extra clarification, heavy formatting, over-testing small changes. Remove conflicting coaching before adding more; give original evidence, not cheaper-model summaries.
- **API:** tools require Responses. No `none`/`minimal` effort, `temperature`, `top_p`, `logprobs`. [`configuration_update`](https://developers.openai.com/api/docs/guides/reasoning#change-reasoning-mid-conversation) changes effort while preserving cache. [Async tools](https://developers.openai.com/api/docs/guides/async-tool-calling)/WebSocket [steering](https://developers.openai.com/api/docs/guides/steering) require host support; steering doesn't cancel started tools.
- **Interruptions:** [misalignment monitoring](https://developers.openai.com/api/docs/guides/safety-checks/misalignment-monitoring) can flag legitimate work. Don't retry `misalignment_policy_violation` as transient; AGENTS.md edits cannot remove it.

## Host specifics

### Codex specifics

- **Usage:** [TypeScript SDK](https://github.com/openai/codex/blob/main/sdk/typescript/src/events.ts) reports tokens on `turn.completed`, not billed dollars. [App-server](https://learn.chatgpt.com/docs/app-server): `thread/tokenUsage/updated`, account-wide `account/rateLimits/read`, aggregate `account/usage/read`. Record model, effort, requested speed tier, per-turn usage; account snapshots can't attribute concurrent clients, nor API-equivalent costs reconstruct subscription quota. Checked 2026-10-08: [`RateLimitWindow`](https://github.com/openai/codex/blob/main/codex-rs/app-server-protocol/src/protocol/v2/account.rs) rounds core float `used_percent` to integer. Before/after quota uncertainty is nearly ±1 percentage point, before delayed/concurrent updates. Use only large aggregate comparisons, not exact turn charges. Fields vary by version.
- **Context:** `features.context_management.experimental_mode` defaults off; requires ChatGPT Plus/Pro/Pro Lite sign-in, not API keys, custom providers, temporary structured threads ([config](https://learn.chatgpt.com/docs/config-file/config-reference), [changelog](https://learn.chatgpt.com/docs/changelog)). Local CLI 0.153.4 had it disabled, 2026-09-05. Separate native cross-session memories are disabled in vault `.codex/config.toml`.
- **Subagent host behavior:** [default/worker/explorer](https://learn.chatgpt.com/docs/agent-configuration/subagents) inherit parent model/effort unless custom agent files override. Configure workers under Tobias's [routing policy](subagent-delegation.md#compute-routing); inheritance is not model selection.
- **pnpm 11 updates:** `pnpm add -g <package>@latest` can silently retain old releases due to release-age gating. Compare `pnpm view <package> dist-tags.latest`; verify executable afterward. Explicit versions install that release; unless strict gating, pnpm records version-scoped `minimumReleaseAgeExclude` globally. Preserve dotfiles' per-tool install-script policy.
- **Backend:** managed app-server daemon has its own pinned package; CLI updates don't update it, so newer CLIs can show old model pickers. Check `codex app-server daemon version`, not only `codex --version`. `codex app-server daemon update --from-cli --yes` pins installed CLI package and restarts daemon, potentially interrupting sessions. `codex app-server daemon update` restores production updates. [Dotfiles](../projects.md#dotfiles) owns installation policy.

### Pi specifics

Verified Pi 1.0.0, 2026-10-03. Config files: `configs/pi/settings.json`, shared `APPEND_SYSTEM.md` in [dotfiles](../projects.md#dotfiles).

- **Verbosity:** `openai-codex-responses` defaults to `text.verbosity: "low"`; no documented general Pi verbosity setting. Don't copy Codex's `model_verbosity`. `hideThinkingBlock` hides terminal reasoning, not execution/billing. Response verbosity and effort are separate.
- [Codemode coordination](orchestration.md#programmatic-tool-calling).
- **T3 usage gap:** nightly `0.0.46-nightly.20261003.2610` runs Pi but Usage scanner/contract/charts omit it; OpenAI-backed Pi work isn't Codex CLI transcript usage. Sum assistant `message.usage` categories and `cost.total` in `~/.pi/agent/sessions/` JSONL per session/across children. Costs are estimates, not verified bills. Native `/session` shows session usage/cost. ([T3 Usage](https://github.com/pingdotgg/t3code/blob/8ed276c246b6/docs/user/usage.md), [Pi usage](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/usage.md))

- [Pi throughput](pi-throughput.md): effective-TPS measurement, subscription rollout claims, local observations.

### Claude Code specifics

Checked 2.1.287, 2026-10-02 ([settings](https://code.claude.com/docs/en/settings-reference)). [Dotfiles](../projects.md#dotfiles) shares global AGENTS.md and `~/.agents/skills` across Claude, Codex, and Pi.

- **Response length:** `verbose`/`viewMode` affect transcript tool output only. No `model_verbosity`; built-in `Concise` output style shortens responses without reducing work.
- **Attribution:** default commit `Co-Authored-By` and PR footer; `attribution: false` (2.1.281+) removes both.
- **Effort:** Opus 5.5's host default is `medium`, not Tobias's routing choice. It ignores top-level user `effortLevel`; set per-model `modelSettings` or `/effort` according to the [team-routing policy](subagent-delegation.md#compute-routing).
- **Context:** Tobias, 2026-10-11: advertise native 1M context to avoid premature wrap-up, but bound compaction per model to cap spend. Dotfiles sets `modelSettings.<model>.autoCompactWindow` by canonical name, matching dated and `[1m]` spellings: Haiku 5.5 100K minimum, triggering ~67–74K; Opus 5.5 433K, triggering ~400K. Sonnet has no override. Set windows ~33K above the intended trigger: 20K output reserve plus ~13K buffer. Haiku compacted mid-turn too. `CLAUDE_CODE_DISABLE_1M_CONTEXT=1` caps all Claude models and larger compaction windows at 200K; dotfiles removed it, but an existing T3 service retains it until restart. Uncapped Opus, Sonnet, and Haiku 5.5 report `contextWindow: 1000000`; the context selector merely toggles `[1m]`. Native children resolve their own model settings; T3 children read the same user settings in separate sessions. Approved roles come from the [team-routing policy](subagent-delegation.md#compute-routing), not these host mechanics. Verified 2.1.296, 2026-10-11. ([context](https://code.claude.com/docs/en/model-config#extended-context), [subagent compaction](https://code.claude.com/docs/en/sub-agents#auto-compaction))
- **Discovery:** reads `~/.claude/CLAUDE.md`, `~/.claude/skills`, not `~/.agents/skills`; project AGENTS.md only without CLAUDE.md. T3 loads user/project/local settings.
- **Auto memory:** defaults on, creates unreviewed `~/.claude/projects` store; disabled to keep vault the sole knowledge store.

### OpenCode specifics

Tobias wants v2 in T3, not v1. Verified 2026-10-03: nightly `0.0.46-nightly.20261003.2610` supports [2.0.18+](https://github.com/pingdotgg/t3code/releases/tag/v0.0.46-nightly.20261003.2610).

- **Binary:** T3 `opencode` uses `~/.local/share/pnpm/bin/opencode`, `@opencode/cli` 2.0.22; dotfiles bootstrap owns installs/updates. Removed separate `~/.local/share/t3code-opencode` v1; don't recreate.
- **Updater failure:** T3 installed v2 without required postinstall: `opencode --version` exited "postinstall script was not run". Repair with [pnpm build permission](https://opencode.ai/v2/docs). On pnpm 11.13.1, persist `allowBuilds: {"@opencode/cli": true}` in `~/.local/share/pnpm/global/v11/pnpm-workspace.yaml`, not global `config.yaml`; verified normal global installs run postinstall without extra flag. Refresh T3 provider afterward: the live snapshot caches failures even after executable repair.
- **Migration:** v1/v2 share database; never run side by side. Snapshot before first v2 startup; credentials/supported config carry over. ([guide](https://opencode.ai/v2/docs/migrate-v1/))

## Retired DeepSeek Codex experiment

Don't recreate Codex → OpenCode Go → DeepSeek. Removed 2026-10-03: `codex_deepseek_go` T3 provider, separate Codex config, model catalog, credential helper. Standard Codex/native OpenCode remain independent. Old sessions: `~/.local/state/codex-archives/deepseek-go-2026-10-03`.
