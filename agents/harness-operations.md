# Harness operations

Where each agent harness's mechanics live, plus the install traps that hit all of them. Model capability and price in [coding models](coding-models.md); Tobias's role routing in the [team-routing policy](subagent-delegation.md#compute-routing). [Dotfiles](../projects.md#dotfiles) owns installed config and shares global AGENTS.md and `~/.agents/skills` across Claude, Codex, and Pi.

recheck-after: 2026-11-24

- [Codex](codex-operations.md): app-server daemon pin, quota fields, context management, subagent inheritance
- [Claude Code](claude-code-operations.md): attribution, effort defaults, compaction windows, discovery, auto memory
- [Pi](pi-operations.md): verbosity, session usage, print-mode stdin, OpenRouter model overrides
- [OpenCode](opencode-operations.md): v2 install and update failure, migration, Go/Zen data policies

## Global CLI installs

- **pnpm 11 updates:** `pnpm add -g <package>@latest` can silently retain old releases due to release-age gating. Compare `pnpm view <package> dist-tags.latest`; verify executable afterward. Explicit versions install that release; unless strict gating, pnpm records version-scoped `minimumReleaseAgeExclude` globally. Preserve dotfiles' per-tool install-script policy.
- **Check the binary itself after any install or version change**, not the install command's exit. Provider and daemon failures outlive the repair ([OpenCode](opencode-operations.md), [Codex](codex-operations.md)).
