# Chief of staff state

Owned by the [chief-of-staff](SKILL.md) skill. Public: no secrets, credentials, source code, or nonpublic employer or customer details.

## Teams

Census 2026-10-11: every unsettled top-level thread.

- [Optimize Agent Workflows for Orderready](t3-thread://v1/7a790d6e-5034-4970-ba3c-56be1bc8e3a9) (orderready): runner fixes merged; five backend cases running across two agents.
- [Developer-Focused Conversation Context](t3-thread://v1/0035fcfe-aea0-4c3e-a978-cc7d54ca50d7) (pi-workspace-view): the standing owner, per Tobias 2026-10-11. Never settle this thread. A Monday 09:00 schedule (`cos-workspace-view-weekly-1`) wakes me to send the audit request. Audit 1 had too little data for a rollback verdict (7 of 20 sessions). It found that v3 sees only 40 of 925 real file reads, because codemode hides the rest, so the benchmark's −15% doesn't carry over to real use. I approved the NEXT.md experiment: an uninstalled codemode-aware prototype, 18 Luna runs, capped at $10. If it gets killed and v3 is also within 5% of baseline, the team reverts 7973c61 itself. Installing the prototype is Tobias's call, after the numbers.

- [Omarchy support](t3-thread://v1/mcp:5cc035fb-ec59-4838-91b4-2f4bf1ade1e1) (dotfiles). Tobias 2026-10-11: Omarchy takes the whole 2 TB disk (nvme1n1, …9170A9) in Full disk mode, installed live, with the Pi CLI on Omarchy fixing breakage and NixOS as the fallback. Wrap-up is on dotfiles main at 870df05: `omarchy/README.md` runbook, `bootstrap.sh`, `migrate-home.sh`, `orderready.rsync-filter`, and the pc mount drop. Builds pass; nothing has been activated on the host. Untested: HM activation onward, TPM2 (`--tpm2`), `migrate-home.sh`. A Sol-high data-loss review is running (task `cos-omarchy-runbook-review-1`); the window waits for it to come back clean. **Window started 2026-10-11** (Tobias: "you do stuff, tell me when to reboot"). Agents have no sudo, so Orderready parks at `/home/tobias/orderready-park/` with no root, and the pre-window pc rebuild is dropped (the mount is `nofail`). Order:
  1. Orderready "pause for Omarchy" sent; waiting for "quiet".
  2. Omarchy team adapts `migrate-home.sh` and the runbook, and copies the ISO to `~/Downloads`.
  3. On "quiet", I send "go: quiet"; the team parks and verifies.
  4. Review clean.
  5. Tobias plugs in a USB stick and runs `sudo dd`, his one root step, then reboots into the installer.

## Needs Tobias

None.

## Hypotheses

None open. Missing merge authority was resolved by a standing rule (2026-10-11).

## Watch

- Claude per-model compaction is done (dotfiles 76f82b2, vault a4f6956). T3 still runs with the old env (`CLAUDE_CODE_DISABLE_1M_CONTEXT=1`), which caps Opus at 200K. It clears at the T3 restart bundled with the Omarchy switch-over: `systemctl --user daemon-reload && systemctl --user restart t3code.service`.
- A GUI ssh password prompt (x11-ssh-askpass) popped on Tobias's desktop from the Omarchy team's VM ssh (2026-10-11). Candidate fix at the owner: `SSH_ASKPASS_REQUIRE=never` in the T3 service environment (dotfiles `service.conf`). It takes effect on the next T3 restart; bundle it with the Omarchy window.
- PC has an unapplied dotfiles delta: the T3 slice module (d83df7f) and the upstream Windows VM package bump. The next pc rebuild applies them; afterwards clear the superseded `set-property` overrides per `nixos/hosts/pc/workloads.md`. A rebuild needs Tobias's go: bundle it with the Omarchy window.
- Pi failed to start a turn once (2026-10-11); a second failure triggers a diagnosis.
- stepkit mutation runs: budget kills are flaky under load, 1 in 44. Parked by the rust-mutants team (thread settled after PR #39 merged as e9d093e). The fix is either kill confirmation, which diverges from rebuild-per-mutant, or dropping per-case wall budgets during mutation runs. Raise it to Tobias only if it starts to bite.
