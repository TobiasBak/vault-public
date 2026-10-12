# Chief of staff state

Owned by the [chief-of-staff](SKILL.md) skill. Public: no secrets, credentials, source code, or nonpublic employer/customer details. Keep only live operational obligations; repos own work details.

## Coordination

- Current CoS: [Chief of Staff Model Routing](t3-thread://v1/b826766b-7e34-4c9d-bc2d-d3199e4744f6), Opus 5.5 high. All live leaders report here.
- Leaders run on Opus 5.5 high. Delegated execution and review run on Pi Sol 6.1 at thinking high; bounded research runs on Haiku 5.5 high. Policy lives in dotfiles `agents/AGENTS.md`.
- Omarchy is the only workstation; serv01 stays NixOS; the old disk is cold storage. No production deployments are authorized.
- Windows VM: agents drive it with `win-vm` ([note](../../../software/omarchy-windows-vm.md)). Orderready's nightly/staging Windows tests run there.

## Teams

### GPUI rewrite (orderready)

[Lead](t3-thread://v1/mcp:58780b90-ecc1-4e53-9eaa-4156ab15afcf). Rewriting the Import GUI from Tauri/React to pure-Rust GPUI (Tobias, 2026-10-11). The design is the lead's: ADR 0011, `docs/gui-testing.md` and `docs/rewrite-plan.md`, merged in PR #7 `7cebf236`.

- Slices: Foundation, Wire types (`ports::wire`), Host, Driver, Draft model, Grid, Draft editor, Recovery (SQLite), Drawing viewer, Screens, Fleet (Windows VM), Cutover. At most three building workers. Merged: Host phase 1 (PR #10 `ce4afe18`), Foundation (PR #12 `c827167b`), Host (PR #14 `c4f16093`; its GUI cases follow the Driver), Grid (PR #17 `ad827689`). Draft model (PR #21 `49c1762d`). OCCT RUNPATH (PR #22 `4f670c7b`). Optional `--frontend-dir` (PR #24 `d158b8d1`; `docs/parity-record.md` holds the frozen hashes and the post-freeze api table). Drawing viewer (PR #26 `c761baf0`, with an out-of-process PDF worker capped at 4 GiB). Driver: the AT-SPI failure isn't llvmpipe (it was refuted); it's being diagnosed in the runner's bus/namespace environment. Runner-contract fixes go to P2.
- Tobias's ADR calls: SQLite wherever it's the better store, vendored patches stay local, exact user-visible parity, machines without a GPU must work but their performance doesn't matter.
- Clean rewrite (Tobias): Tauri/React frozen, no Tauri adaptations; parity is an end gate against the frozen build.
- Tests are black-box only (theodore). The driver speaks stdio only. The Windows corpus runner runs inside the guest; there is no `--listen` and no `win-vm forward`.
- No binary fixtures or evidence in Git; drawings are referenced by hash from P2's fixture store. Further `--no-verify` commits need a CoS go.
- Preserve the spike worktree `/home/tb/.t3/worktrees/orderready/spike-gpui-import-gui` and its index, plus the receipts under `~/.local/share/orderready/gpui-spike/`.

### Orderready P2 migration

[Owner](t3-thread://v1/mcp:99ab7733-ab01-4241-bfc9-7f7b5f33c579). Owns the `tools/or` gate, the corpus runner, the test shape and the theodore rules. Local `tools/or test --full` is the gate; there is no hosted CI. Nothing is deployed.

- Merged today: AUTH consumer (PR3), C4C workflows (PR2), cache-aware admission (PR4), Q1/Q2 (PR5), own-cgroup admission fix (PR6 `a3e61272`).
- Merged: the Windows lanes on ephemeral win-vm (PR #23 `3880fd3c`), with the clone code and vm-slot lock deleted. Nightly live (PR #25 `cafd356a`): `orderready-nightly.timer` runs at 01:00, verdicts go to `$ORDERREADY_DATA/nightly/<stamp>/nightly.json`, and a 06:00 check in P2's thread reports failures. The first run failed on old Windows clippy errors; the fix in `p2/windows-clippy` adds Windows clippy to the `--full` gate.
- Merged: the corpus race fix (PR #15 `c2358ac8`), which unblocks GPUI's Grid and Draft model.
- Critical path cleared on main `58b022b2`: the await bound (#18), the identity case fix (#19) and runner throughput (#20; mailbox/first-order solo median 6.99 s → 3.55 s).
- Running: case pressure, the rmut consumer on pin `7ef780a`, the fixtures (merge to main plus 7 held rows), and the Windows lanes PR on `win-vm run --ephemeral`.
- Queued, in order of the owner's choosing:
  - the fixture migration: synthetic inputs by default, a hashed local store only for real files, zero tracked binaries, a rule in AGENTS.md.
- rmut `--cpus` is merged (`37be8a2`). The command-case consumer (`3a5fff12`) waits for corpus throughput; C3 r3d and C4B r2 follow it.
- Later: pairing approval inside the Import GUI.

### rmut

[Lead](t3-thread://v1/mcp:2cc5f9ae-2f26-4443-9fc2-7617e9ce3e4b), Opus, started 2026-10-12 from `~/code/rust-mutants/.git/agent-handoffs/lead-handoff.md`. The temporary Pi lead `mcp:45897a0c` is retired.

- Done: nested-cgroup teardown (PR #5 `bc588fa`). The qualified pin `~/.cache/rmut/qualified/7ef780a…/` supersedes `e7f0730`, and P2 has it. The lead is settled until P2's consumer turns up a producer bug.

### Dotfiles

[Team](t3-thread://v1/mcp:87e88c75-f093-4c7a-9817-97a135c52fe5). Works on main.

- Done: the restic backup to serv01 (`cad8707`, nightly at 04:00, tags `t3`/`orderready`, restore verified).
- Done: `win-vm run --ephemeral` (`564ec00`, receipt `~/.cache/win-vm/ephemeral-20261012/`); P2 has it.
- Done: reboot-residue recovery (`9ff2c91`), and the restic password is in place.
- serv01 is on generation 33 (`fb31679`): declarative Omarchy key only, Samba allows the LAN, Hermes and SearXNG are gone; failed units, restic and the LAN check are all clean. Hermes is being removed from main (Tobias), with its state on serv01 kept. The old snapshots are kept and documented (`6acb92c`).
- Later: NAS mount and the T3 backup.

### Agent-context research

[Standing owner](t3-thread://v1/mcp:d7502e10-2088-42ce-9c31-6ff118b57931), pi-workspace-view. Never settle it.

- Pi workspace-view v3 is disabled (dotfiles PR7). Checkpoint trial: case 004 never reached 128k (`f21bcb1`). The census (`69c0806`) shows 38% of Pi sessions cross 128k and 46% of Pi spend falls at or above it. No case in history crosses 128k on Sol medium (`c514c09`). CoS approved screening cases 002 and 003, 2 runs each, after the harness is generalised per case and reviewed. If neither crosses in both runs, stop for good with the verdict "not exercised". Otherwise run the trial on the qualifying case. All within the remaining 18 executions of `f1b384c`. Judge by cost per passing task, not by cache hit rate.
- Weekly task `cos-agent-context-weekly-1` runs Mondays at 09:00; the next run is 2026-10-12.

## Needs Tobias

- Delete Hermes's leftover data on serv01? That's `/var/lib/hermes` (1.2G) and the stopped `hermes-agent` container (553 MB).
- Decision-log review: entries marked **[review]**.

## Watch and hypotheses

- 200K Opus compaction: kept. Prompt per request fell 48% for 4.2M of compaction overhead (`~/.cache/claude-usage-20261012/report.md`; the result is in `agents/coding-models.md`). Re-measure only if quota burn or rework complaints rise.
- Retro 2026-10-11 (`~/.cache/cos-retro-20261011/`):
  - Admission false blocks and blind polling cost more than RAM did.
  - RAM versus serv01 is inconclusive.
  - The dotfiles VM receipt predates the final concurrency fixes and didn't exercise a fresh bootstrap or a disconnected-session handoff.
- Starting an idle turn may kill detached work from an earlier agent scope, so keep long jobs in independent user units. This is still a single-incident hypothesis.
- StepKit geometry team is settled at `d114b6f`, with PR42 parked. Any future qualification needs a new brief.
- The T3 nightly timer updates the service, not the desktop package. Don't restart T3 during live work.
