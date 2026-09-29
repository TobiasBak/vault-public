# DeepSeek V4.1 Flash in Codex

DeepSeek V4.1 Flash works through Codex using an OpenCode Go subscription. The agent harness and model supplier are separate choices: T3 Code → Codex → OpenCode Go → DeepSeek. Installing the OpenCode CLI does not mean DeepSeek must run in the OpenCode harness.

Tobias added this as an option for testing on 2026-09-10, not as a replacement for his daily [[Working with GPT-6 Astra|Astra]] setup.

## Installed T3 option

- Provider: **Codex · DeepSeek Go**, instance ID `codex_deepseek_go`.
- Model: **DeepSeek V4.1 Flash**, API ID `deepseek-flash`.
- Reasoning: **High** by default, with Low and Max also selectable.
- Independent Codex home: `/home/tobias/.codex-deepseek-go`. Its `config.toml` owns the endpoint and default reasoning; `models.json` owns model metadata. Global `AGENTS.md` and skills link to the existing Codex setup.
- Endpoint: `https://opencode.ai/zen/go/v1`, using the Responses protocol. The credential helper reads the existing OpenCode Go login without copying its key into the configuration.
- T3's live provider registration is in `~/.t3/userdata/settings.json`. Follow [[Projects#T3 Code|T3 Code's operational route]] before service changes.

The OpenCode provider remains available separately, where the same model's ID is `opencode-go/deepseek-flash`. Existing OpenAI Codex settings and the default model were left unchanged.

A real T3 thread on 2026-09-10 verified Codex 0.154.0, `deepseek-flash`, and persisted High effort through Go. A shell-tool call returned `391` for `17 * 23`, and the model completed the turn successfully with no file changes. This establishes connection and tool round-trip compatibility, not comparative coding quality or long-context reliability.

## DeepSeek's Codex integration

DeepSeek explicitly documents native Responses API support and Codex-specific adaptation. Its [Codex integration guide](https://api-docs.deepseek.com/quick_start/agent_integrations/codex/) supplies a model catalog with reasoning levels, tool formats, context limits, and instructions. The installed option uses that catalog's Flash entry, with an explicit V4.1 display name and context capped at OpenCode Go's advertised 1,000,000 tokens rather than the direct DeepSeek catalog's 1,048,576. [OpenCode Go documentation](https://opencode.ai/docs/go/) owns subscription access; the installed model metadata supplied the Go context limit.

Go's documentation lists Chat Completions for DeepSeek, but the authenticated Codex test succeeded through Responses. Do not infer that Codex cannot use Go's DeepSeek model from that endpoint table alone.

DeepSeek's [release notes](https://api-docs.deepseek.com/updates/) recommend Low for simple tasks, High for daily agent work, and Max for more complex work. These are effort settings, not fixed token budgets or guaranteed quality gains. In the separate OpenCode harness, **Build** selects the coding agent and tool access, not reasoning effort.

Codex compatibility and adaptation do not establish training inside Codex. No official confirmation of V4.1 training in that harness was found. Earlier V4 benchmark notes name DeepSeek Harness minimal mode for evaluation; evaluation setup is not training provenance.

## Model discovery

T3 can retain a provider model list captured before an external login. After adding OpenCode Go credentials, **Settings → Providers → Refresh provider status** reloads available models and their reasoning controls. A stale picker can label a working model unavailable.
