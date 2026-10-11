# Chief of staff state

Owned by the [chief-of-staff](SKILL.md) skill. Public: no secrets, credentials, source code, or nonpublic employer or customer details.

## Teams

On Omarchy since 2026-10-11 (user `tb`, host `tb-omarchy`, T3 0.0.46-nightly.20261011.2967, Pi enabled live). Omarchy is Nix-free by design (Tobias). Clone over https; GitHub SSH is broken (no `~/.ssh` at all), and dotfiles is fixing it. The NixOS disk is cold storage.

- [Omarchy settle-in](t3-thread://v1/mcp:28a26fdb-7dbe-4a04-aacc-b21727653dff) (dotfiles): Pi done. Next: `uv` + `vite-plus` via mise (workspace-view is blocked on them; the team pings it directly), port the rest of `developer-cli.nix` to mise/pacman, SSH setup, the uncommitted AGENTS.md/README.md edits, `SSH_ASKPASS_REQUIRE=never`, a T3 memory slice, the update timer's coverage. Pre-approved: workspace-view's v3 revert change if its kill condition triggers. Restart, sudo and irreversible steps come back as one bundle.
- [P2 test-suite migration (resume)](t3-thread://v1/mcp:99ab7733-ab01-4241-bfc9-7f7b5f33c579) (orderready): worktrees rebuilt under `~/.local/share/orderready/wt`. Builds are blocked: the repo runs everything through `nix develop`. It owes me an estimate for moving off Nix. Running meanwhile: old-path fixes, the `domain` census, the cutting-rates 500 issue, the Q5 consistency check, and the rmut requirement for the rmut team.
- [Workspace view standing owner](t3-thread://v1/mcp:d7502e10-2088-42ce-9c31-6ff118b57931) (pi-workspace-view): never settle it. Setup OK (v3 active for `tb`). Fix review and replay check running; the 18 runs (≤$10) wait on `uv`/`vp`. Kill rule: revert v3 via a change sent to the dotfiles team. Installing the prototype is Tobias's call. Schedule `cos-workspace-view-weekly-1` (Mon 09:00, bound here) wakes me for the weekly audit.
- [rmut command-cases mode](t3-thread://v1/mcp:45897a0c-83cb-48aa-8781-99cb87131a2e) (rust-mutants, worktree `feature/command-cases`): a general rmut mode so Orderready can delete `mutants_harness.py`. Orderready sends the requirement; rmut owns the design.

## Needs Tobias

- Orderready needs Nix for every build, and Omarchy has none. Options: install Nix as a package manager only, for project dev shells (`pacman -S nix`, daemon, flakes; no Home Manager); or port Orderready's toolchain to mise. Recommend pacman Nix: about 4 sudo commands, keeps the pinned toolchain and CI parity, and P2 restarts today. Waiting on the team's off-Nix estimate as well.

## Hypotheses

None open. Missing merge authority was resolved by a standing rule (2026-10-11).

## Watch

- Pi failed to start a turn once (2026-10-11); a second failure triggers a diagnosis.
- stepkit mutation runs: budget kills are flaky under load, 1 in 44. Parked by the rust-mutants team. The fix is either kill confirmation or dropping per-case wall budgets during mutation runs. Raise it to Tobias only if it starts to bite.
