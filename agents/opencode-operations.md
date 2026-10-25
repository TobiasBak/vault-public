# OpenCode

v2 install, update and data-policy mechanics. Model capability in [coding models](coding-models.md); T3 thread mechanics in [T3 Code operations](../software/t3-code-operations.md).

recheck-after: 2026-11-24

Tobias wants v2 in T3, not v1. Verified 2026-10-03: nightly `0.0.46-nightly.20261003.2610` supports [2.0.18+](https://github.com/pingdotgg/t3code/releases/tag/v0.0.46-nightly.20261003.2610).

- **Binary:** T3 `opencode` uses `~/.local/share/pnpm/bin/opencode`, `@opencode/cli` 2.0.22; dotfiles bootstrap owns installs/updates. Removed separate `~/.local/share/t3code-opencode` v1; don't recreate.
- **Updater failure:** T3 installed v2 without required postinstall: `opencode --version` exited "postinstall script was not run". Repair with [pnpm build permission](https://opencode.ai/v2/docs). On pnpm 11.13.1, persist `allowBuilds: {"@opencode/cli": true}` in `~/.local/share/pnpm/global/v11/pnpm-workspace.yaml`, not global `config.yaml`; verified normal global installs run postinstall without extra flag. Refresh T3 provider afterward: the live snapshot caches failures even after executable repair.
- **Migration:** v1/v2 share database; never run side by side. Snapshot before first v2 startup; credentials/supported config carry over. ([guide](https://opencode.ai/v2/docs/migrate-v1/))
- **OpenCode access (Tobias, 2026-10-22):** paid OpenCode models are allowed. Tobias has a Go subscription and wants to use it through Pi.
- **Go DeepSeek privacy, checked 2026-10-24:** Go serves DeepSeek V4.1 Flash and V4 Pro from DeepSeek (requires the Global region in workspace privacy settings) under a monthly-renewed ZDR agreement, stated valid through 2026-10-31; Go lists no training and 0-day retention. DeepSeek's own API trains on prompts. Recheck after the agreement date.
- **Free models:** rotate weekly; retention and training terms differ per model, see below.
- **Free-model data policies, checked 2026-10-12:** [OpenCode's current model docs](https://github.com/anomalyco/opencode/blob/c57c448d31c390880e06493f81b91a2c92536ad9/services/www/src/docs/content/console/models.mdx#privacy) state the following. These are provider claims, not an independent audit. Models not named below are stated as explicit zero retention and no training use. `opencode models --verbose` is unsupported in v2; checked `opencode models` and the [live Zen catalog](https://opencode.ai/zen/v1/models) for model IDs.
  - **Big Pickle, Exo, MiMo-V2.6/V2.5 Flash, Ling 3.1/3.0 Flash Fin:** exceptions — collected data may improve the model during the free period; no retention duration given.
  - **Nemotron 3 Ultra Free, Nemotron 3.5 Lightning Free:** NVIDIA trial endpoints log use for security and product/service improvement; improvement session data is not linked to identity or a persistent identifier. Do not submit personal or confidential data. No retention duration is given.
  - **Muse Spark 1.3 Contributor Free:** permission to train future Meta models on prompts and completions in exchange for discounted pricing; no retention duration is given.
  - **Muse Spark 1.2 Contributor Free:** listed in the live Zen catalog but not separately covered in the current model docs. [OpenCode's Go privacy table](https://github.com/anomalyco/opencode/blob/c57c448d31c390880e06493f81b91a2c92536ad9/services/www/src/docs/content/console/go.mdx#privacy) says the 1.2 Contributor model uses data for training and is not ZDR; it does not separately state Zen-free terms.
  - **Jev 1.13 Free:** listed in the current docs and live catalog. The current docs state a general zero-retention/no-training policy without a Jev exception, but [v2 Zen's privacy section](https://github.com/anomalyco/opencode/blob/4617210822bdbb31e5749751afbfb4584ccedac8/packages/web/src/content/docs/zen.mdx#privacy) says Jev inputs are not used for training and data is retained under TypeSafe AI's privacy policy. The docs disagree on retention; do not claim unqualified ZDR for Jev.
- **`opencode run` can exit 1 after a clean finish** (cancelled web search); judge by the check, not the exit code.

## Retired: Codex → OpenCode Go → DeepSeek

Don't recreate it. Removed 2026-10-03: `codex_deepseek_go` T3 provider, separate Codex config, model catalog, credential helper. Standard Codex/native OpenCode remain independent. The original session archive is unavailable on this host (checked 2026-10-20).
