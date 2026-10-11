# Chief of staff state

Owned by the [chief-of-staff](SKILL.md) skill. Public: no secrets, credentials, source code, or nonpublic employer or customer details.

## Teams

Census 2026-10-11: every unsettled top-level thread.

- [Optimize Agent Workflows for Orderready](t3-thread://v1/7a790d6e-5034-4970-ba3c-56be1bc8e3a9) (orderready): runner fixes merged; five backend cases running across two agents.
- [Developer-Focused Conversation Context](t3-thread://v1/0035fcfe-aea0-4c3e-a978-cc7d54ca50d7) (pi-workspace-view): the standing owner, per Tobias 2026-10-11. Weekly audit of v3 on real sessions: rollback check, failure-mode mining, bug fixes, and it reverts 7973c61 itself if the threshold trips. It also writes `NEXT.md`, the v4 direction; that's an architecture call for Tobias via me, and v4 isn't built before he decides. A Monday 09:00 schedule (`cos-workspace-view-weekly-1`) wakes me to send the audit request. Never settle this thread.

- [Omarchy support: reproduce the setup, proven in a VM](t3-thread://v1/mcp:5cc035fb-ec59-4838-91b4-2f4bf1ade1e1) (dotfiles, worktree `omarchy-support`). Tobias 2026-10-11: Omarchy takes the whole 2 TB disk (nvme1n1, …9170A9) in the installer's Full disk mode; no shared partition, `prepare-disk.sh` dropped. Unattended boot to a reachable T3 (LUKS + TPM2, falling back to no LUKS); downtime approved. VM-proven so far: installer, Limine boot, HM build, pc/wsl closures unchanged; TPM2 and bootstrap in progress. Still owed: proof the Full disk install leaves the NixOS disk untouched, removal of the NixOS `/mnt/data-2tb` mount, `migrate-home.sh`, the Tailscale identity, the runbook, and `du` of `orderready/`. Window order: Orderready pushes local-only branches and WIP (CoS coordinates), pause, park `orderready/` on the NixOS disk, install, migrate back to the same absolute path `/mnt/data-2tb/orderready` so T3's worktree paths hold.
- [Claude: 1M advertised window, compaction at 200K](t3-thread://v1/mcp:259dab12-ad03-4b7e-b656-f27780f209ad) (dotfiles): landed as dotfiles 08e517f and vault 8d9f2da, both checked. Claude Code compacts ~33K below the setting (20K output reserve plus a ~13K buffer). Last step: raise Opus to 433K so it really compacts at ~400K, keeping Haiku 100K (real ~70K, under the price tier) and Sonnet 200K. T3 still runs with DISABLE_1M=1, which caps Opus at 200K, until the restart bundled with the Omarchy switch-over (`systemctl --user daemon-reload && systemctl --user restart t3code.service`).

## Needs Tobias

None.

## Hypotheses

None open. Missing merge authority was resolved by a standing rule (2026-10-11).

## Watch

- A GUI ssh password prompt (x11-ssh-askpass) popped on Tobias's desktop from the Omarchy team's VM ssh (2026-10-11). Candidate fix at the owner: `SSH_ASKPASS_REQUIRE=never` in the T3 service environment (dotfiles `service.conf`). It takes effect on the next T3 restart; bundle it with the Omarchy window.
- PC has an unapplied dotfiles delta: the T3 slice module (d83df7f) and the upstream Windows VM package bump. The next pc rebuild applies them; afterwards clear the superseded `set-property` overrides per `nixos/hosts/pc/workloads.md`. A rebuild needs Tobias's go: bundle it with the Omarchy window.
- Pi failed to start a turn once (2026-10-11); a second failure triggers a diagnosis.
- stepkit mutation runs: budget kills are flaky under load, 1 in 44. Parked by the rust-mutants team (thread settled after PR #39 merged as e9d093e). The fix is either kill confirmation, which diverges from rebuild-per-mutant, or dropping per-case wall budgets during mutation runs. Raise it to Tobias only if it starts to bite.
