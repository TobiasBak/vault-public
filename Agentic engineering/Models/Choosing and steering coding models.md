# Choosing and steering coding models

OpenAI capabilities and pricing checked 2026-09-29; Anthropic guidance checked 2026-09-26. [[Tobias's developer preferences]] owns the daily interactive Codex choice. The roles below describe provider guidance, not a measured local winner or an automatic routing policy.

## Current choices

| Model | Relevant role | Effort guidance |
| --- | --- | --- |
| [GPT-6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol) | Tobias's chosen daily model. OpenAI describes near-Astra performance for complex coding, computer use, and professional work at lower cost. | Preserve the chosen effort. The API defaults to `medium` and supports `low`, `medium`, `high`, `xhigh`, and `max`, not `none` or `minimal`. |
| [GPT-6 Astra](https://developers.openai.com/api/docs/guides/latest-model) | Difficult coding, investigation, research, and work spanning several tools. No longer Tobias's daily default. | Keep the chosen setting unless a task or comparison justifies changing it. `none` is not supported. |
| [GPT-6 Sol](https://developers.openai.com/api/docs/models/gpt-6-sol) | Complex coding and agent workflows with a different cost and latency tradeoff. | The API defaults to `medium`; compare effort levels on the actual workload. |
| [GPT-6 Luna](https://developers.openai.com/api/docs/guides/latest-model) | Efficient, repeatable work at scale. | Judge the complete task, including retries and review, before moving work to it. |
| [Claude Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5) | Coding and knowledge work, including long repository tasks. | Start at `medium`. Reserve `xhigh` and `max` for demonstrated quality gains. |
| [Claude Fable 5.1](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1) | Demanding reasoning and long-running agent work. | Start at its `high` default and adjust from task results. |

## Sol's cost advantage

At Standard speed with up to 272K input tokens, GPT-6.1 Sol costs $2 input, $0.10 cached input, and $10 output per million tokens. Astra costs $10, $1, and $50 respectively. Sol is therefore 5x cheaper for uncached input and output, and 10x cheaper for cached input. Codex credit rates have the same ratios: Sol is 50/2.5/250 credits versus Astra's 250/25/1,250. [API pricing](https://developers.openai.com/api/docs/pricing), [Codex credit rates](https://learn.chatgpt.com/docs/pricing#token-rates)

Token-price ratios do not bound the saving per task. Artificial Analysis measures weighted average cost per Intelligence Index task using each model's actual input, cache, reasoning, and answer tokens. Its 2026-09-29 comparison supports Sol's capability-to-task-cost advantage:

| Comparison | Astra cost per task / index | Sol cost per task / index | Cost ratio |
| --- | --- | --- | --- |
| Both at `xhigh` | $2.309 / 52.4 | $0.393 / 51.0 | 5.9x |
| Both at `max` | $3.258 / 52.7 | $0.724 / 51.8 | 4.5x |
| Astra `max`, Sol `low` | $3.258 / 52.7 | $0.131 / 42.1 | 24.9x, with lower capability |

Compare model-and-effort configurations, not model names alone. Larger cross-effort savings can come with lower capability. AA's metric counts benchmark tasks, not only successful outcomes; local cost also includes retries and review. Tobias's choice is based on capability for the task cost, not merely the price of a fixed number of tokens. [Artificial Analysis comparison](https://artificialanalysis.ai/models?cost=intelligence-vs-cost-per-task#price-cost)

Credit rates do not determine included subscription limits. OpenAI's near-Astra claim and AA's benchmark comparison are not local quality measurements.

## Sol integration

GPT-6.1 Sol uses Responses for tool calling; Chat Completions supports it without tools. It supports a 1,050,000-token context window and US and EU data residency, though Fast mode is unavailable with EU residency. [Model documentation](https://developers.openai.com/api/docs/models/gpt-6.1-sol)

Sol supports the Responses API's beta multi-agent orchestration. This is a provider-managed API capability, distinct from Codex's host tools and the managed Agents API. [[Subagent delegation]] owns whether delegation is useful; API support does not call for a new routing policy. [Responses multi-agent](https://developers.openai.com/api/docs/guides/responses-multi-agent)

## Choose the complete working setup

Compare model, effort, instructions, tools, and host together. An API capability does not establish support in T3, Codex, Claude Code, or Pi. Native continuation, progress reporting, permissions, and verification can change how much supervision the same model needs.

Measure correctness, architectural fit, corrective user turns, elapsed time, and total cost per successful task. Token price and launch benchmarks cannot decide the choice alone. [[Coding-agent benchmark trust]] owns fair comparisons; [[Subagent delegation]] owns whether splitting the work is justified.

Effort labels are not equal amounts of reasoning across models. Task length is also not reasoning difficulty: a large mechanical edit and a short unresolved design question need different kinds of work. More reasoning earns its cost when it improves the result. Recording a model preference does not itself change installed model or effort settings.

## Steer observed behavior

For Astra, make intended autonomy, material decision boundaries, writing style, and proportionate verification clear where the active instructions leave a gap. Remove conflicting or redundant skill instructions before adding more coaching. [[Working with GPT-6 Astra]] holds the model-specific details.

For Opus 5.5, use the effort setting before adding generic instructions to think harder. In interactive chat, such instructions can add delay without improving the answer. A progress report can end a turn while work remains; completion needs evidence against the requested outcome, not merely an end-of-turn signal. These are observed provider behaviors, not reasons to install a universal continuation loop. [Opus guidance](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5)

At low effort, Fable 5.1 may retrieve or search less often. Make source retrieval explicit when the answer depends on current or external evidence. [Fable guidance](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1)

Verbosity concerns visible detail, not reasoning depth. Ask for enough explanation to judge the result; a short answer that drops a consequential qualification is a failure. [[Prompting tool-using agents]] owns the general task contract, evidence, and acceptance guidance.

## Integration details that can resemble model failures

Opus 5.5 always uses adaptive thinking. Its between-tool progress updates arrive in thinking blocks and can be invisible at the default display setting. A client must request and render updates; prompting alone cannot fix discarded output. Its thinking blocks also depend on the preceding conversation, so use supported append-only instruction and tool changes rather than rewriting earlier turns. [Opus API behavior](https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5)

GPT-6 supports asynchronous tool work, mid-turn steering, and effort changes that preserve the cached prefix. The host must implement those protocols; choosing the model does not supply them automatically. [[Working with GPT-6 Astra]] records Astra's integration boundaries.
