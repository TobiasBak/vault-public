# Projects

Routes to repositories. Each repository owns its implementation detail; read its `AGENTS.md` before acting. A nearby copy, generated file, nested checkout, or evaluation patch is not authoritative; follow the owning repository.

## Dotfiles

Machine and dev-environment config for Windows, NixOS WSL, NixOS servers, and Arch.

- `/home/tobias/code/dotfiles`, <https://github.com/TobiasBak/dotfiles>, branch `main`
- Start with root `AGENTS.md`; for NixOS hosts and remote rebuilds, `nixos/README.md`.
- Get explicit approval before running installers or rebuild entrypoints. A file under the checkout is active only if its home or host target is a verified symlink or junction.
- Owns the installed T3 Code service (`AGENTS.md`, section "Installed T3 Code service"), the active Codex config, and the global `AGENTS.md`.
- PC OOM prevention (2026-10-05): live T3 limits are 12 GiB high / 16 GiB max / 1 GiB swap, reserving the 8 GiB VM and 6 GiB desktop budget. A timed-out scratch type-check orphaned a `tsgolint` grandchild that reached 14.4 GiB and caused global OOM. Tool/Python subprocess timeouts do not prove descendant cleanup. Host policy and `pc-workload` cancellation caveats live in dotfiles' `nixos/hosts/pc/workloads.md`.
- Windows test VM lab ownership belongs here: `oip-windows-vm`, the single shared VM limit, and workload isolation are host policy. Keep its persisted home `~/.local/share/oip-windows-vm`. Product repositories own guest qualification; frozen misc snapshots are not maintained tooling. Activated on PC by Tobias on 2026-10-04; PATH resolves `/run/current-system/sw/bin/oip-windows-vm`. Use the maintained command, not the archive. A stopped clone still belongs to its current task: wait for explicit slot release before lifecycle actions. The lifecycle lock serializes mutations; it does not grant ownership. For live lifecycle investigation, resolve the installed command's source rather than assuming the dotfiles checkout matches it. On 2026-10-05, the checkout lacked the activated base-image and desktop-readiness modules.
- Agent skills live in this vault under `skills/` (see [AGENTS.md](AGENTS.md#skills)); `scripts/bootstrap-developer-tools.sh` links them. Some agent files are generated; check guidance before editing.
- Taildrop on the `pc` device: `taildrop-receiver.service` drains incoming files to `~/Phone/Inbox`, with numbered suffixes on collisions. A manual `tailscale file get` therefore shows `0/0 files`. Configured in `nixos/home/tobias/desktop.nix`.

## T3 Code

Tobias's daily interactive coding-agent environment: Claude Opus 5.5 orchestrates and delegates to GPT-6.1 Sol in Pi (see [coding models](agents/coding-models.md#current-choice)). [Orchestrator V2](https://github.com/pingdotgg/t3code/releases/tag/v0.0.46-nightly.20261003.2610) added Pi support in the nightly released 2026-10-03.

- `/home/tobias/code/t3code`, <https://github.com/pingdotgg/t3code>
- Source work follows the checkout's `AGENTS.md`; the installed service and updates follow dotfiles. Restarting the service can kill running agent sessions.
- Direction (confirmed 2026-07-30): provider-native agents are engines. T3 owns the collaborative workspace around them (shared task state, policy, evidence, provider integration), not a generic agent loop. See [AI-era durability](software/ai-era-durability.md).
- Live provider registration: `~/.t3/userdata/settings.json`.
- Cross-project notifications: thread MCP calls are project-scoped. When Tobias explicitly asks to notify another project's existing thread, use the normal web UI if MCP rejects it. The installed runtime's `t3 pair --ttl=2m --label=...` supplies a short-lived pairing link for a fresh Playwright session; keep the link's origin throughout, never expose its token, and revoke only that temporary labeled session with `t3 auth session revoke` afterward. Verify the message appeared in the intended thread. Do not create a new conversation just to relay it.
