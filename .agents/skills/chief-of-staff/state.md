# Chief of staff state

Owned by the [chief-of-staff](SKILL.md) skill. Public: no secrets, credentials, source code, or nonpublic employer or customer details.

## Teams

On Omarchy since 2026-10-11 (user `tb`, host `tb-omarchy`). Nix-free (Tobias). git@ GitHub URLs are rewritten to HTTPS. The NixOS disk is cold storage.

- [Omarchy settle-in](t3-thread://v1/mcp:28a26fdb-7dbe-4a04-aacc-b21727653dff) (dotfiles): done (4f4e90b, 1ef2a79). Idle; reuse it for dotfiles work. GitHub goes over HTTPS through git insteadOf plus gh credentials (there is no SSH key). uv, vite-plus 1.1.0, go and playwright-cli come through mise. The T3 slice matches NixOS. The askpass env loads at the next service restart.
- [P2 test-suite migration (resume)](t3-thread://v1/mcp:99ab7733-ab01-4241-bfc9-7f7b5f33c579) (orderready): Nix port merged into p2/integrate (gate green on 9995566). PR TobiasBak/orderready#1 (integrate → main, 48 commits) is in whole-diff review and merges on a pass. Running: P2-X case tokens (blocks the C4B/C4C/B4 merges), C3 r3c, AUTH-AB (env binding + audit) on the platform. Then the pairing enrollment (approved). rmut installed at ~/.local/bin from b4dacbb; update it when the GIT_DIR fix lands. No hosted CI; the gate is `tools/or test --full`. **Pending notes for its next report:** Xvfb is installed once Tobias confirms, so run the `tools/or dev` smoke. production deploys are Tobias's alone, so when (a) lands, the breaking change and the exact token-reissue steps go in the deploy-time notes or runbook; never plan or run a deploy.
- [Workspace view standing owner](t3-thread://v1/mcp:d7502e10-2088-42ce-9c31-6ff118b57931) (pi-workspace-view): never settle it. Round 1 was killed at ~13:05Z when its session restarted ($0.98 lost). The rerun is `systemd-run --user --unit=pwv-bench-r2` from 13:06Z, ~$7.3, total ~$8.3 of the $10 cap. Next: the numbers. Kill rule: revert v3 through a change sent to dotfiles (pre-approved). Installing the prototype is Tobias's call. Schedule `cos-workspace-view-weekly-1` (Mon 09:00, bound here) wakes me for the weekly audit.
- [stepkit-geometry: stock-take and next work](t3-thread://v1/mcp:4a9ba562-db85-4d69-961b-ca7c3827ccec) (stepkit-geometry): new team, per Tobias. Checks the build on Omarchy, sorts the branches into dead or live, proposes 1–3 next items, and reports before building. Hardening item: strip git env in `tools/sg_cli/gate.py`.
- [rmut command-cases mode](t3-thread://v1/mcp:45897a0c-83cb-48aa-8781-99cb87131a2e) (rust-mutants): LimitCORE=1 + an EBUSY retry are on main (`b4dacbb`). Incident: the pre-push hook's GIT_DIR leaked into fixture git commands, which pushed an engine-deleting commit; the team force-restored main. Fix branch `fix/git-env-leak` (`1ded734`) is in gate and review; command-cases is paused until it merges. Then it tells Orderready the rmut rev to pin. Census: no other repo is exposed. The vault rule is in fa82257.


## Needs Tobias

- Run `omarchy pkg add xorg-server-xvfb` (Tobias said yes; agents can't sudo). Then tell Orderready to run the `tools/or dev` smoke. Dotfiles is adding it to bootstrap.
- Decision log review: 7 entries still marked **[review]** in `decisions.md`; the unmarked ones get cleared as right calls. Waiting: me, to distill the lessons.

## Hypotheses

- My `auto` message (settle rule, ~13:05Z) started a new turn in the idle workspace-view thread, and T3 stopped the old session's scope, killing its detached benchmark. If confirmed, don't start turns in idle teams that have detached work running; long jobs use `systemd-run --user` (vault rule landed in 62e74f5).

## Watch

- Pi failed to start a turn once (2026-10-11); a second failure triggers a diagnosis.
- stepkit mutation runs: budget kills are flaky under load, 1 in 44. Parked by the rust-mutants team. The fix is either kill confirmation or dropping per-case wall budgets during mutation runs. Raise it to Tobias only if it starts to bite.
- The T3 update timer updates the service, not the desktop app. The app (AUR `t3code-nightly-bin`) updates only by rerunning `~/code/dotfiles/omarchy/bootstrap.sh` in a terminal with the app closed and agents stopped (it builds only when the AUR is newer, then restarts T3), or through `omarchy update` once Omarchy's own repo build passes it. `omarchy pkg aur add` silently does nothing here. Tell Tobias when the app lags the service by a nightly.
- No isolated-profile `chromium` wrapper on Omarchy: an agent running bare `chromium` uses Tobias's real profile. playwright-cli is safe. Fix through dotfiles if an agent ever touches it.
- Expected crashes from agent test runs trigger systemd-coredump desktop notifications (rmut mutant SIGABRT, 2026-10-11; rmut is setting LimitCORE=1 on its units; 0 still journals a "no coredump" entry that omarchy-crash-watch toasts on, while 1 makes the kernel skip the pipe helper). If a second test tool causes one, fix it once for the T3 agent slice in dotfiles with LimitCORE=1 on agent scopes, rather than per tool.
- T3 slice contention: Orderready's full-gate subagent was OOM-killed (2026-10-11) while the workspace-view benchmark and rmut runs shared the ~16.8 GiB slice. Teams check headroom and cap parallelism. A second OOM means designing machine-level scheduling for heavy jobs (the NixOS `pc-workload` had none on Omarchy).
