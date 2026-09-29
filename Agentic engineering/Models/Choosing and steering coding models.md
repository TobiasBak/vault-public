# Choosing and steering coding models

Provider guidance checked 2026-09-26. [[Working with GPT-6 Astra]] owns Tobias's daily interactive Codex preference. The alternatives below describe current provider guidance, not a measured local winner or an automatic routing policy.

## Current choices

| Model | Relevant role | Effort guidance |
| --- | --- | --- |
| [GPT-6 Astra](https://developers.openai.com/api/docs/guides/latest-model) | Difficult coding, investigation, research, and work spanning several tools. Tobias's current daily choice. | Keep the chosen setting unless a task or comparison justifies changing it. `none` is not supported. |
| [GPT-6 Sol](https://developers.openai.com/api/docs/models/gpt-6-sol) | Complex coding and agent workflows with a different cost and latency tradeoff. | The API defaults to `medium`; compare effort levels on the actual workload. |
| [GPT-6 Luna](https://developers.openai.com/api/docs/guides/latest-model) | Efficient, repeatable work at scale. | Judge the complete task, including retries and review, before moving work to it. |
| [Claude Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5) | Coding and knowledge work, including long repository tasks. | Start at `medium`. Reserve `xhigh` and `max` for demonstrated quality gains. |
| [Claude Fable 5.1](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1) | Demanding reasoning and long-running agent work. | Start at its `high` default and adjust from task results. |

## Choose the complete working setup

Compare model, effort, instructions, tools, and host together. An API capability does not establish support in T3, Codex, Claude Code, or Pi. Native continuation, progress reporting, permissions, and verification can change how much supervision the same model needs.

Measure correctness, architectural fit, corrective user turns, elapsed time, and total cost per successful task. Token price and launch benchmarks cannot decide the choice alone. [[Coding-agent benchmark trust]] owns fair comparisons; [[Subagent delegation]] owns whether splitting the work is justified.

Effort labels are not equal amounts of reasoning across models. Task length is also not reasoning difficulty: a large mechanical edit and a short unresolved design question need different kinds of work. More reasoning earns its cost when it improves the result. Neither a model release nor this note authorizes changing Tobias's configured model or effort.

## Steer observed behavior

For Astra, make intended autonomy, material decision boundaries, writing style, and proportionate verification clear where the active instructions leave a gap. Remove conflicting or redundant skill instructions before adding more coaching. [[Working with GPT-6 Astra]] holds the model-specific details.

For Opus 5.5, use the effort setting before adding generic instructions to think harder. In interactive chat, such instructions can add delay without improving the answer. A progress report can end a turn while work remains; completion needs evidence against the requested outcome, not merely an end-of-turn signal. These are observed provider behaviors, not reasons to install a universal continuation loop. [Opus guidance](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5)

At low effort, Fable 5.1 may retrieve or search less often. Make source retrieval explicit when the answer depends on current or external evidence. [Fable guidance](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1)

Verbosity concerns visible detail, not reasoning depth. Ask for enough explanation to judge the result; a short answer that drops a consequential qualification is a failure. [[Prompting tool-using agents]] owns the general task contract, evidence, and acceptance guidance.

## Integration details that can resemble model failures

Opus 5.5 always uses adaptive thinking. Its between-tool progress updates arrive in thinking blocks and can be invisible at the default display setting. A client must request and render updates; prompting alone cannot fix discarded output. Its thinking blocks also depend on the preceding conversation, so use supported append-only instruction and tool changes rather than rewriting earlier turns. [Opus API behavior](https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5)

GPT-6 supports asynchronous tool work, mid-turn steering, and effort changes that preserve the cached prefix. The host must implement those protocols; choosing the model does not supply them automatically. [[Working with GPT-6 Astra]] records the boundaries and current local preference.
