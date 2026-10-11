# Chief of staff state

Owned by the [chief-of-staff](SKILL.md) skill. Public: no secrets, credentials, source code, or nonpublic employer or customer details.

## Teams

On Omarchy since 2026-10-11 (user `tb`, host `tb-omarchy`, T3 0.0.46-nightly.20261011.2967). Fresh T3: projects vault-public, dotfiles, pi-workspace-view, orderready (cloned over https; SSH to GitHub failed host-key verification). The NixOS disk is cold storage; old threads stayed there.

- [Omarchy settle-in](t3-thread://v1/mcp:28a26fdb-7dbe-4a04-aacc-b21727653dff) (dotfiles): enable Pi in T3 first (disabled and not on the service PATH; teams fall back to Codex Sol until then), then GitHub SSH host keys, the uncommitted AGENTS.md/README.md edits in the checkout, bootstrap gaps (`nix`/`home-manager` absent), `SSH_ASKPASS_REQUIRE=never` in the service env, a T3 memory slice, the update timer's coverage. Restart, sudo and irreversible steps come back as one bundle for Tobias.
- [P2 test-suite migration (resume)](t3-thread://v1/mcp:99ab7733-ab01-4241-bfc9-7f7b5f33c579) (orderready): resumes from `docs/p2-omarchy-handoff-report.md`. I answered handoff questions 1, 2, 4, 6; 3 and 5 are in Needs Tobias.
- [Workspace view standing owner](t3-thread://v1/mcp:d7502e10-2088-42ce-9c31-6ff118b57931) (pi-workspace-view): the standing owner; never settle it. Runs the approved codemode-aware experiment from HANDOFF.md (fix review, v3 replay check, 18 Luna runs, ≤$10). If the prototype is killed and v3 is within 5% of baseline, it reverts 7973c61 itself. Installing the prototype is Tobias's call. Schedule `cos-workspace-view-weekly-1` (Mon 09:00, bound to this thread) wakes me to send the weekly audit request.
- Vault child `cos-vault-projects-omarchy-1` (Codex Sol): `projects.md` routes to `/home/tb`, non-route bullets moved or dropped. Spot-check its diff.

## Needs Tobias

- Orderready Q5: where AX SQL credentials live (Firestore field or Secret Manager) and whether GUI users get them. Recommend Secret Manager, with GUI users never holding them directly. Blocks cutover only.
- Orderready Q3: add a "command cases" mode to rmut so Orderready can delete `mutants_harness.py`. Recommend yes: one owner for mutation runs. Needs rust-mutants work.

## Hypotheses

None open. Missing merge authority was resolved by a standing rule (2026-10-11).

## Watch

- Pi failed to start a turn once (2026-10-11); a second failure triggers a diagnosis.
- stepkit mutation runs: budget kills are flaky under load, 1 in 44. Parked by the rust-mutants team. The fix is either kill confirmation or dropping per-case wall budgets during mutation runs. Raise it to Tobias only if it starts to bite.
- Leftover from the move: the rust-mutants local `twin` branch; check it reached the remote before anyone wipes the NixOS disk.
