# Chief of staff state

Owned by the [chief-of-staff](SKILL.md) skill. Public: no secrets, credentials, source code, or nonpublic employer or customer details.

## Teams

Census 2026-10-11: every unsettled top-level thread.

- [Optimize Agent Workflows for Orderready](t3-thread://v1/7a790d6e-5034-4970-ba3c-56be1bc8e3a9) (orderready): runner fixes merged; five backend cases running across two agents.
- [Developer-Focused Conversation Context](t3-thread://v1/0035fcfe-aea0-4c3e-a978-cc7d54ca50d7) (pi-workspace-view): the standing owner, per Tobias 2026-10-11. Never settle this thread. A Monday 09:00 schedule (`cos-workspace-view-weekly-1`) wakes me to send the audit request. Audit 1 had too little data for a rollback verdict (7 of 20 sessions). It found that v3 sees only 40 of 925 real file reads, because codemode hides the rest, so the benchmark's −15% doesn't carry over to real use. I approved the NEXT.md experiment: an uninstalled codemode-aware prototype, 18 Luna runs, capped at $10. If it gets killed and v3 is also within 5% of baseline, the team reverts 7973c61 itself. Installing the prototype is Tobias's call, after the numbers.

- [Omarchy support](t3-thread://v1/mcp:5cc035fb-ec59-4838-91b4-2f4bf1ade1e1) (dotfiles). Tobias 2026-10-11: Omarchy takes the whole 2 TB disk (nvme1n1, …9170A9) in Full disk mode, installed live, with the Pi CLI on Omarchy fixing breakage and NixOS as the fallback. Wrap-up is on dotfiles main at 870df05: `omarchy/README.md` runbook, `bootstrap.sh`, `migrate-home.sh`, `orderready.rsync-filter`, and the pc mount drop. Builds pass; nothing has been activated on the host. Untested: HM activation onward, TPM2 (`--tpm2`), `migrate-home.sh`. **Window started 2026-10-11, git first** (Tobias corrected the copy plan). Omarchy starts fresh: clone from remotes, log in again, T3 with no history, new teams started from repo handoffs and this file. The NixOS disk stays as cold storage (mount it `ro,noload`).
  1. Done: Orderready (paused) pushed all 18 worktrees clean and wrote its handoff, `docs/p2-omarchy-handoff-report.md` (e60b8ab7). Its 6 open questions for Tobias are in that file; bring them to him after the move. Done: pi-workspace-view now has a private remote, TobiasBak/pi-workspace-view (main e5fcd2a with HANDOFF.md). The codemode prototype needs its review fixes reviewed and the v3 replay check before the 18 runs; $0 spent. swe-benchmarking is pushed. Leftover: the rust-mutants local `twin` branch.
  2. Omarchy team: park only the non-git Orderready data (`evidence/`, `briefs/`, artifacts) to `~/orderready-park/` as cold storage, delete `migrate-home.sh`, rewrite first boot (Pi, dotfiles, bootstrap, Tailscale, T3, gh, vault, `/chief-of-staff`), and apply the review fixes (TPM2 mapping for `/dev/mapper/root`, `ro,noload`, mise fallback).
  3. The census is done: 85 of 100 checkouts have local-only state, all on the NixOS disk, which survives. A Sol sweep is pushing Tobias's own repos as WIP refs and creating private remotes for the 4 repos with none (`cos-omarchy-git-sweep-1`). Skipped: the JoergenDahl OIP checkouts (see Needs Tobias), the t3code spike, CanineArchive, csbetting, and /tmp.
  4. The ISO is on Tobias's Ventoy stick (sda, verified). Next: Tobias reboots, boots the stick, installs.
  - **Restart on Omarchy:** relaunch Orderready from its handoff; workspace-view (its experiment is interrupted by the reboot, so it reruns from the repo, and the Monday schedule needs re-creating); recreate the `cos-workspace-view-weekly-1` schedule. Then apply the bundled restart items: the askpass env (`SSH_ASKPASS_REQUIRE=never`) and the T3 env without DISABLE_1M, both via dotfiles.

## Needs Tobias

- OIP (`JoergenDahl/order-integration-platform`, someone else's repo): about 10 T3 worktrees with dirty state (up to 482 files) and 7 stashes, local only. Recommendation: leave them on the NixOS disk as cold storage, and push `wip/` branches only if you want that work on Omarchy. Waiting on it: nothing, the move doesn't depend on it.

## Hypotheses

None open. Missing merge authority was resolved by a standing rule (2026-10-11).

## Watch

- Claude per-model compaction is done (dotfiles 76f82b2, vault a4f6956). T3 still runs with the old env (`CLAUDE_CODE_DISABLE_1M_CONTEXT=1`), which caps Opus at 200K. It clears at the T3 restart bundled with the Omarchy switch-over: `systemctl --user daemon-reload && systemctl --user restart t3code.service`.
- A GUI ssh password prompt (x11-ssh-askpass) popped on Tobias's desktop from the Omarchy team's VM ssh (2026-10-11). Candidate fix at the owner: `SSH_ASKPASS_REQUIRE=never` in the T3 service environment (dotfiles `service.conf`). It takes effect on the next T3 restart; bundle it with the Omarchy window.
- PC has an unapplied dotfiles delta: the T3 slice module (d83df7f) and the upstream Windows VM package bump. The next pc rebuild applies them; afterwards clear the superseded `set-property` overrides per `nixos/hosts/pc/workloads.md`. A rebuild needs Tobias's go: bundle it with the Omarchy window.
- Pi failed to start a turn once (2026-10-11); a second failure triggers a diagnosis.
- stepkit mutation runs: budget kills are flaky under load, 1 in 44. Parked by the rust-mutants team (thread settled after PR #39 merged as e9d093e). The fix is either kill confirmation, which diverges from rebuild-per-mutant, or dropping per-case wall budgets during mutation runs. Raise it to Tobias only if it starts to bite.
