# Codex

CLI and app-server mechanics: version pins, quota accounting, context management, subagent inheritance. [Dotfiles](../projects.md#dotfiles) owns installation policy; model capability in [coding models](coding-models.md).

Checked 2026-09-05 through 2026-10-08, as noted inline.

recheck-after: 2026-11-24

- **Usage:** [TypeScript SDK](https://github.com/openai/codex/blob/main/sdk/typescript/src/events.ts) reports tokens on `turn.completed`, not billed dollars. [App-server](https://learn.chatgpt.com/docs/app-server): `thread/tokenUsage/updated`, account-wide `account/rateLimits/read`, aggregate `account/usage/read`. Record model, effort, requested speed tier, per-turn usage; account snapshots can't attribute concurrent clients, nor API-equivalent costs reconstruct subscription quota. Checked 2026-10-08: [`RateLimitWindow`](https://github.com/openai/codex/blob/main/codex-rs/app-server-protocol/src/protocol/v2/account.rs) rounds core float `used_percent` to integer. Before/after quota uncertainty is nearly ±1 percentage point, before delayed/concurrent updates. Use only large aggregate comparisons, not exact turn charges. Fields vary by version.
- **Context:** `features.context_management.experimental_mode` defaults off; requires ChatGPT Plus/Pro/Pro Lite sign-in, not API keys, custom providers, temporary structured threads ([config](https://learn.chatgpt.com/docs/config-file/config-reference), [changelog](https://learn.chatgpt.com/docs/changelog)). Local CLI 0.153.4 had it disabled, 2026-09-05. Separate native cross-session memories are disabled in vault `.codex/config.toml`.
- **Subagent host behavior:** [default/worker/explorer](https://learn.chatgpt.com/docs/agent-configuration/subagents) inherit parent model/effort unless custom agent files override. Configure workers under Tobias's [routing policy](compute-routing.md); inheritance is not model selection.
- **Backend:** managed app-server daemon has its own pinned package; CLI updates don't update it, so newer CLIs can show old model pickers. Check `codex app-server daemon version`, not only `codex --version`. `codex app-server daemon update --from-cli --yes` pins installed CLI package and restarts daemon, potentially interrupting sessions. `codex app-server daemon update` restores production updates. [Dotfiles](../projects.md#dotfiles) owns installation policy.
