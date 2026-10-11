# Chief of staff state

Owned by the [chief-of-staff](SKILL.md) skill. Public: no secrets, credentials, source code, or nonpublic employer or customer details.

## Teams

Census 2026-10-11: every unsettled top-level thread.

- [Optimize Agent Workflows for Orderready](t3-thread://v1/7a790d6e-5034-4970-ba3c-56be1bc8e3a9) (orderready): runner fixes merged; five backend cases running across two agents.
- [Developer-Focused Conversation Context](t3-thread://v1/0035fcfe-aea0-4c3e-a978-cc7d54ca50d7) (pi-workspace-view): v3 snapshot view merged (30ae786), replay +1.8% input cost over native. Told to run the 12-run live benchmark (~$2.30, ~45 min) and report whether v3 cuts rereads and cost.

- [Omarchy support: reproduce the setup, proven in a VM](t3-thread://v1/mcp:5cc035fb-ec59-4838-91b4-2f4bf1ade1e1) (dotfiles, worktree `omarchy-support`). Decided by Tobias 2026-10-11: ~1.4T shared ext4 data plus ~400G Omarchy on the 2 TB disk (nvme1n1, …9170A9), contents disposable. CoS: shrink p1 instead of wiping, so the UUID and the teams' worktrees survive, after deleting the disposable bulk from NixOS once the census clears it; unattended boot to a reachable T3 (LUKS + TPM2, falling back to no LUKS); downtime approved. Scope: Home Manager standalone, bootstrap, `prepare-disk.sh`, the window runbook, `migrate-home.sh` for cut-over (~/.t3, agent state, ~/code), and the Tailscale identity. All VM-proven, nothing real. Census running of unpushed and dirty work on the 2 TB disk; the Orderready team must save its work before the window.

## Needs Tobias

None.

## Hypotheses

None open. Missing merge authority was resolved by a standing rule (2026-10-11).

## Watch

- PC has an unapplied dotfiles delta: the T3 slice module (d83df7f) and the upstream Windows VM package bump. The next pc rebuild applies them; afterwards clear the superseded `set-property` overrides per `nixos/hosts/pc/workloads.md`. A rebuild needs Tobias's go: bundle it with the Omarchy window.
- Pi failed to start a turn once (2026-10-11); a second failure triggers a diagnosis.
- stepkit mutation runs: budget kills are flaky under load, 1 in 44. Parked by the rust-mutants team (thread settled after PR #39 merged as e9d093e). The fix is either kill confirmation, which diverges from rebuild-per-mutant, or dropping per-case wall budgets during mutation runs. Raise it to Tobias only if it starts to bite.
