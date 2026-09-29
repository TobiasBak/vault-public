# Working with GPT-6 Astra

Tobias chose Astra for daily interactive Codex work on 2026-09-05 and prefers Codex CLI's native tooling over custom workers and model-routing policies. This preference does not call for an added instruction encouraging delegation.

This preference concerns interactive work. [[Choosing and steering coding models]] covers current OpenAI and Anthropic alternatives without changing that preference.

## Context and instructions

OpenAI's [Astra guidance](https://developers.openai.com/api/docs/guides/latest-model#prompting-best-practices), checked 2026-09-26, describes strong long-task coherence and instruction-following, with sensitivity to ambiguous or conflicting skills and AGENTS.md instructions. It also identifies tendencies toward extra clarification, detailed formatting, and excessive testing on small changes.

Keep Tobias's non-obvious engineering preferences and authorization boundaries explicit. Remove obsolete model-routing procedures and duplicated generic coaching. Judge a local instruction by what it adds beyond the active Codex instructions and expected model behavior. Verification can remain part of good work without a local rule telling Astra to verify; a useful principle does not automatically belong in AGENTS.md.

Give Astra the original evidence needed for a decision. Do not route evidence through a cheaper model solely to reduce the parent's context. [[Agent context engineering]] governs relevance, retrievable originals, and durable state; [[Concise AGENTS.md for capable coding agents]] governs instruction placement. Judge further removals against actual work, rather than assuming either the old setup or an instruction-free setup is best.

## Native context management

Codex's experimental context management keeps notes across context windows and lets Astra search earlier messages and tool outputs. It provides an alternative to repeatedly compressing accumulated context into one summary. [[Agent context engineering]] distinguishes this native continuation mechanism from manual checkpoints and authoritative project state.

The [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference) documents `features.context_management.experimental_mode`, off by default and requiring ChatGPT sign-in on Plus, Pro, or Pro Lite. The [Codex 0.153.0 release notes](https://learn.chatgpt.com/docs/changelog) exclude API-key sessions, custom providers, and temporary structured threads. A fresh local CLI 0.153.4 configuration check on 2026-09-05 reported `context_management=false` and `token_budget=false`; account eligibility and recovery across a window transition were not tested.

This feature concerns continuity within a task. Native cross-session memories are a separate recall feature; vault-local Codex configuration disables them, which does not affect experimental context management.

## Async work and steering

Astra's Responses API supports [async tool calls](https://developers.openai.com/api/docs/guides/async-tool-calling), allowing model progress while the application executes a tool. This differs from background response generation. [Mid-turn steering](https://developers.openai.com/api/docs/guides/steering) over WebSockets queues new instructions; acceptance does not undo output or cancel tools already started.

These capabilities allow single-agent concurrency, not just delegated work. Codex supplies its own tool lifecycle and, when available, asynchronous user questions. Selecting Astra in a different host does not automatically supply those tools. [[Prompting tool-using agents]] owns the general dependency and side-effect boundaries. [[Programmatic tool calling]] distinguishes native Codex code mode from the raw Responses API protocol.

## Reasoning effort and API integration

In standard single-agent Astra API conversations, [`configuration_update`](https://developers.openai.com/api/docs/guides/reasoning#change-reasoning-mid-conversation) can change reasoning effort between responses while preserving the original request-level effort and cached prompt prefix. This does not establish automatic effort adaptation in Codex or justify changing Tobias's configured effort.

For direct API integrations, the [migration guide](https://developers.openai.com/api/docs/guides/latest-model#migration-quickstart) requires Responses for tool calling. Astra does not support `none` or `minimal` effort, `temperature`, `top_p`, or `logprobs`. These are integration constraints, not global agent instructions.

## Provider interruptions

An interruption may come from provider monitoring rather than a local skill, permission rule, or clarification habit. OpenAI's [monitoring guide](https://developers.openai.com/api/docs/guides/safety-checks/misalignment-monitoring) describes asynchronous checks that can flag legitimate activity. Automatic API stopping depends on the endpoint and preserved conversation context; a stop does not roll back completed actions. An API `misalignment_policy_violation` is not an ordinary transient error to retry or bypass. Editing AGENTS.md cannot remove provider enforcement.

## Native delegation

Codex's [subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents), checked 2026-09-05, lists built-in default, worker, and explorer agents. Without model or effort overrides, subagents inherit the parent's settings. Custom agent files can override those settings, so removing routing prose alone does not remove a custom model route.

Dotfiles owns the active Codex configuration and global AGENTS.md. [[Projects]] provides the repository route. [[Subagent delegation]] owns general task boundaries, shared-state coordination, and validation.
