# Coding models

OpenAI checked 2026-09-29, Anthropic 2026-09-26. Effort guidance is the provider's own; Tobias's [compute routing](compute-routing.md) owns the choices, and no local number here outranks it. Host mechanics — version pins, compaction windows, updater gaps — live in [harness operations](harness-operations.md).

recheck-after: 2026-11-24

## Current choice

Follow Tobias's [compute routing](compute-routing.md) for model roles, targets, and effort. Tobias chose Sol over Astra on 2026-09-29 for capability per task cost. Include [Pi child costs](pi-operations.md#pi). [Dotfiles](../projects.md#dotfiles) owns installed config.

Tobias, 2026-10-14: Sol 6.1 is a much stronger non-UI reviewer than Opus 5.5; Opus is the better designer and planner. His hypothetical preference, "with unlimited usage, Opus 5.5 for everything and Sol 6.1 as the reviewer", is a capability judgment, not a routing exception. Follow the [compute routing](compute-routing.md) for permitted roles. Harden lead tooling and skills so Sol leads close the gap through mechanisms, not reminders.

## Effort guidance

| Model | Effort guidance |
|---|---|
| [GPT-6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol) | `medium`–`xhigh`; API default `medium`, no `none`/`minimal` |
| [GPT-6 Astra](https://developers.openai.com/api/docs/guides/latest-model) | no `none`/`minimal` |
| [GPT-6 Sol](https://developers.openai.com/api/docs/models/gpt-6-sol) | default `medium` |
| [GPT-6 Luna](https://developers.openai.com/api/docs/guides/latest-model) | below `xhigh`, silently drops work ([local test](#haiku-55-specifics)); judge whole-task cost including retries |
| [Claude Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5) | provider recommends `medium` first, `high`/`xhigh` for demonstrated gains |
| [Claude Fable 5.1](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1) | start at `high` |
| Claude Haiku 5.5 | API default `medium`; see [Haiku specifics](#haiku-55-specifics) |

## Sol vs Astra cost

Per million tokens, Standard with ≤272K input: Sol $2 input / $0.10 cached / $10 output; Astra $10 / $1 / $50. Codex credits: 50/2.5/250 vs 250/25/1,250. ([pricing](https://developers.openai.com/api/docs/pricing), [credits](https://learn.chatgpt.com/docs/pricing#token-rates))

[Artificial Analysis](https://artificialanalysis.ai/models?cost=intelligence-vs-cost-per-task#price-cost), 2026-09-29: cost per Intelligence Index task / index score.

| Comparison | Astra | Sol | Ratio |
|---|---|---|---|
| both `xhigh` | $2.309 / 52.4 | $0.393 / 51.0 | 5.9x |
| both `max` | $3.258 / 52.7 | $0.724 / 51.8 | 4.5x |

Trust price ratios, not public-index capability gaps ([benchmark trust](benchmark-trust.md)). Compare model-plus-effort configurations; credit rates don't determine subscription limits.

Checked 2026-10-24: Codex Fast consumes included subscription allowance at 2.5x Standard and purchased credits at 2x; Ultrafast (Astra and Sol, Pro $500) at 8x and 6x. Hold effort fixed: billing multipliers aren't speedups. ([speed](https://developers.openai.com/codex/agent-configuration/speed), [pricing](https://learn.chatgpt.com/docs/pricing))

## Choosing a setup

- Compare model, effort, instructions, tools, and host together; see [host vs API capabilities](orchestration.md#programmatic-tool-calling) and [benchmark trust](benchmark-trust.md). Measure correctness, architectural fit, corrective turns, time, and cost per successful task.
- Tobias rejected `low` for skipped searches, checks, and work, and `max` for costing far more than `xhigh` with little gain (2026-10-10). The [compute routing](compute-routing.md) owns effort choices, not provider defaults or benchmark arms.
- Judge a cheap or free arm by whole-task cost, never by token price: in a free-tier trial about 40% of tasks came back wrong, and the lead's rework outweighed the tokens saved. Passing checks never established equivalence to the reference fix ([feedback](learning-from-feedback.md)).
- Effort labels differ across models. Length isn't difficulty: large mechanical edits and short open design questions need different effort.
- Verbosity is visible detail, not reasoning depth. Dropping a consequential qualifier fails even in a short answer.

## Local harness comparison, 2026-10-03

One 8-task pass, one run per arm on GPT-6.1 Sol `medium`: built-in Pi codemode was ~21% faster and ~35% cheaper than Pi's own tool suite ($1.63 vs $2.49); Codex was slower at the same cost. Single pass with shared-host contention, and the artifacts are gone. Directional only — not a harness ranking, not a reason to change the daily provider.

## Model specifics

API constraints and known failure modes. Vendor positioning copy is not repeated here; it changed no decision.

- **Sol:** tools require Responses; Chat Completions works without tools. 1.05M context, US/EU residency including Fast and Ultrafast (checked 2026-10-24). Beta Responses [multi-agent orchestration](https://developers.openai.com/api/docs/guides/responses-multi-agent) is separate from Codex host tools.
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
- No request exceeded 100K. Haiku prompts reached 97K at `xhigh`; Claude Code base prompt ~23K vs Pi ~6K. Three reps per cell on synthetic tasks of unknown representativeness: trust direction, not decimals.
- **Haiku `high` findings:** it bought reliability and half Luna `xhigh`'s latency for 1.4x its cost. The benchmark arms are experiments, not approved delegation roles; follow Tobias's [compute routing](compute-routing.md). Luna's 272K tier is more forgiving; no tested task approached it.
- **Base prompts must be far below 100K.** A T3/OpenCode setup's 100K Haiku cap with ~163K base prompt compacted every step, never finished ([issue](https://github.com/SpyrosPsarras/epaflix/issues/1739)). Haiku 5.5's tokenizer counts ~30% more tokens than 4.5's. Anthropic positions it for "summaries, compactions, or database queries" ([@ClaudeDevs](https://x.com/ClaudeDevs/status/2107895955144208813)).
- **API:** adaptive thinking only; effort `low`–`max`, default `medium`. Anthropic warns of early stopping at `low` in long agent prompts, skipped verification at `low`/`medium`, occasional empty replies at `xhigh`. Claude Code harness prompt is ~17–25K before the task.
- **Routing:** retired from delegation (Tobias, 2026-10-12); see the [compute routing](compute-routing.md).

### Astra specifics

- [OpenAI guidance](https://developers.openai.com/api/docs/guides/latest-model#prompting-best-practices): follows instructions closely, sensitive to conflicting skills/AGENTS.md. Tends toward extra clarification, heavy formatting, over-testing small changes. Remove conflicting coaching before adding more; give original evidence, not cheaper-model summaries.
- **API:** tools require Responses. No `none`/`minimal` effort, `temperature`, `top_p`, `logprobs`. [`configuration_update`](https://developers.openai.com/api/docs/guides/reasoning#change-reasoning-mid-conversation) changes effort while preserving cache. [Async tools](https://developers.openai.com/api/docs/guides/async-tool-calling)/WebSocket [steering](https://developers.openai.com/api/docs/guides/steering) require host support; steering doesn't cancel started tools.
- **Interruptions:** [misalignment monitoring](https://developers.openai.com/api/docs/guides/safety-checks/misalignment-monitoring) can flag legitimate work. Don't retry `misalignment_policy_violation` as transient; AGENTS.md edits cannot remove it.

## Free-model trials

Kept to avoid re-running what already failed, not as a ranking. One `opencode run` per model, two small public dotfiles fixes with a test check, six concurrent, 20-minute cap; diffs read against the merged fix. One pass each on tasks nobody has checked for representativeness, and the transcripts are gone (checked 2026-10-20) — treat every result below as a recollection, not data.

- **Initial results, not current routing:** Muse Spark 1.3 (fastest, 54/112 s; overstated manual coverage), Big Pickle (122/137 s; invented a fact in docs), MiMo-V2.6-Flash (slower, sound research).
- **Avoid:** Nemotron 3.5 Lightning (failed both, littered debug files, claimed success), Nemotron 3 Ultra (hardcoded, timed out flailing), Step 5 Preview (passed, then spent 10 minutes repairing its own throwaway harness). Ling 3.1 Flash works but is slow and hit upstream 429s. Exo Free was already deprecated.
- **None matched the reference fix.** Every model passed the checks yet missed edge cases the reference handled (`~` paths, concurrent-edit refusal, preserving `-` directives). Passing checks and a confident report did not establish equivalence to the reference. This historical trial grants no routing or review-policy exception.
