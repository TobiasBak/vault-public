# Chief of staff state

Owned by the [chief-of-staff](SKILL.md) skill. Public: no secrets, credentials, source code, or nonpublic employer or customer details.

## Teams

On Omarchy since 2026-10-11 (user `tb`, host `tb-omarchy`). Nix-free (Tobias). git@ GitHub URLs are rewritten to HTTPS. The NixOS disk is cold storage.

- [Omarchy settle-in](t3-thread://v1/mcp:28a26fdb-7dbe-4a04-aacc-b21727653dff) (dotfiles): done (4f4e90b, 1ef2a79). Idle; reuse it for dotfiles work. GitHub goes over HTTPS through git insteadOf plus gh credentials (there is no SSH key). uv, vite-plus 1.1.0, go and playwright-cli come through mise. The T3 slice matches NixOS. The askpass env loads at the next service restart.
- [P2 test-suite migration (resume)](t3-thread://v1/mcp:99ab7733-ab01-4241-bfc9-7f7b5f33c579) (orderready): running. The Nix port (`p2/off-nix`, mise.toml + mise.lock) lands off-nix → p2/integrate → main. No hosted CI: the gate is `tools/or test --full` plus the Windows nightly. Q5 closed: AX SQL credentials stay in Firestore, served to employees (the AX-11 design), per Tobias. Cutting-rates 500 filed as orderready-platform#1. The `domain` census is running. Five P2 rounds are parked until the port lands. The Windows VM is parked until a release candidate; its Omarchy setup goes to dotfiles. orderready-platform gets the Nix port after.
- [Workspace view standing owner](t3-thread://v1/mcp:d7502e10-2088-42ce-9c31-6ff118b57931) (pi-workspace-view): never settle it. The 18 runs (≤$10) have run since 12:41Z on prototype `4858015` (fixes reviewed; v3 replay byte-identical). The vp version doesn't matter: 004 pins vite-plus 0.2.2 locally. Next: the numbers. Kill rule: revert v3 through a change sent to dotfiles (pre-approved). Installing the prototype is Tobias's call. Schedule `cos-workspace-view-weekly-1` (Mon 09:00, bound here) wakes me for the weekly audit.
- [rmut command-cases mode](t3-thread://v1/mcp:45897a0c-83cb-48aa-8781-99cb87131a2e) (rust-mutants, `feature/command-cases`): design approved (third mode: process per case with env vars; exit 0/1/2/3; deadline timeouts get a solo rerun). My change: pure JSON on stdout, header to stderr, stepkit consumers updated if they parse it. Merges on its own check; Orderready confirms after its Nix port.


## Needs Tobias

- Decision log review: 7 entries still marked **[review]** in `decisions.md`; the unmarked ones get cleared as right calls. Waiting: me, to distill the lessons.
- Mailbox automation auth to orderready-platform (no interactive Microsoft login): Tobias is unsure. The Orderready team is writing a brief (current machine token, weaknesses, recommendation). Waiting: me, to bring it to Tobias.

## Hypotheses

None open. Missing merge authority was resolved by a standing rule (2026-10-11).

## Watch

- Pi failed to start a turn once (2026-10-11); a second failure triggers a diagnosis.
- stepkit mutation runs: budget kills are flaky under load, 1 in 44. Parked by the rust-mutants team. The fix is either kill confirmation or dropping per-case wall budgets during mutation runs. Raise it to Tobias only if it starts to bite.
- The T3 update timer updates the service, not the desktop app. The app (AUR `t3code-nightly-bin`) needs `yay -S aur/t3code-nightly-bin` or a bootstrap rerun; tell Tobias when the app lags the service by a nightly.
- No isolated-profile `chromium` wrapper on Omarchy: an agent running bare `chromium` uses Tobias's real profile. playwright-cli is safe. Fix through dotfiles if an agent ever touches it.
