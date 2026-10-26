# Pi

Config files: `configs/pi/settings.json`, shared `APPEND_SYSTEM.md` in [dotfiles](../projects.md#dotfiles). [Pi throughput](pi-throughput.md) owns effective-TPS measurement; [coding models](coding-models.md) owns model choice.

Verified Pi 1.0.0, 2026-10-03 unless noted.

recheck-after: 2026-11-24

- **Verbosity:** `openai-codex-responses` defaults to `text.verbosity: "low"`; no documented general Pi verbosity setting. Don't copy Codex's `model_verbosity`. `hideThinkingBlock` hides terminal reasoning, not execution/billing. Response verbosity and effort are separate.
- [Codemode coordination](orchestration.md#programmatic-tool-calling).
- **Usage:** T3 Usage reads Pi sessions from `~/.pi/agent/sessions` or `PI_CODING_AGENT_SESSION_DIR` (checked 2026-10-24). For manual totals, sum assistant `message.usage` categories and `cost.total` in the session JSONL, including children. Costs are estimates, not verified bills. Native `/session` shows session usage/cost. ([T3 Usage](https://github.com/pingdotgg/t3code/blob/main/docs/user/usage.md), [Pi usage](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/usage.md))
- **`pi --print` blocks on open stdin.** Non-TTY stdin is read to EOF and prepended to the prompt. In agent shells stdin can be a socket that never closes, so print mode hangs silently with no output or session file. Run `pi --print ... < /dev/null` from scripts (Pi 1.4.0, 2026-10-24).
- **OpenRouter models:** change a catalog model with `providers.openrouter.modelOverrides`; a `models` entry with the same ID replaces it and drops catalog `thinkingLevelMap`, image input and compat flags (developer role, reasoning replay). `compat.openRouterRouting` is sent verbatim as `provider`; Pi sends `x-session-id` to OpenRouter by default. [OpenRouter routing](../software/openrouter.md).
