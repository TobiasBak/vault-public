# Chief of staff state

Owned by the [chief-of-staff](SKILL.md) skill. Public: no secrets, credentials, source code, or nonpublic employer/customer details. Keep only live operational obligations; repos own work details.

## Coordination

- Current CoS: [Chief of Staff Model Routing](t3-thread://v1/b826766b-7e34-4c9d-bc2d-d3199e4744f6), Opus 5.5 high. All live leaders report here.
- Team leads run on Pi Sol 6.1 high behind CoS gates (trial, Tobias 2026-10-12): plan go before code, CoS merges, ≤3 children, ≤2 review rounds. Subagents default to Space Bunny (free OpenCode) everywhere (Tobias 2026-10-12); Sol 6.1 high does independent review, locking/cleanup/ownership work, and takes over after limit errors (rerun on first, team switches on second). Never send Space Bunny secrets. Opus is the CoS only; Haiku is retired. Policy lives in dotfiles `agents/AGENTS.md`.
- Omarchy is the only workstation; serv01 stays NixOS; the old disk is cold storage. No production deployments are authorized.
- Windows VM: agents drive it with `win-vm` ([note](../../../software/omarchy-windows-vm.md)). Orderready's nightly/staging Windows tests run there.

## Teams

Operating model (Tobias, 2026-10-12): disposable teams, one per GitHub issue, in parallel worktrees, ended at merge; GitHub issues are the backlog and handoff. See SKILL.md Delegate and Track performance.

### Sol-lead trial (Tobias, 2026-10-12)

Restart order: dotfiles and pi-workspace-view first, then orderready#44 once the first plans and diffs look sound, then the P2/GPUI wind-downs, orderready product work last. Read each plan and diff; log Space Bunny usage from the `space_bunny:` metrics lines. Design-heavy issues wait.

Running:
- [dotfiles#12 restic restore](t3-thread://v1/mcp:e4035b7a-460e-4d4f-9d7f-b4eaef4f3818): go given: one real backup in a transient unit with MemoryHigh=1G/MemoryMax=3G, restore drill with scratch deleted after; no live apply before merge.
- [dotfiles#11 NAS mount](t3-thread://v1/mcp:d7830e61-2113-4825-8f92-7cd7193ec192): PR #18 merged by CoS (2cd0b78); lead closes #11 with metrics. Applying needs Tobias (commands in omarchy/README.md § NAS mount). #13 closed.
- [orderready#44 feedback loop](t3-thread://v1/mcp:f62510ba-20e4-4fd1-8aba-541c33547610): was blocked by a hooks-test leak into the real repo (core.bare=true, test commits on main/p2/case-wall-clock, branch `side`). CoS restored from reflogs; bug filed as orderready#87. Told to hand off to worktree `issue-44-latency`, take a fresh cold baseline on 8e8095f7, then plan gate.
- [pi-workspace-view#8 epoch-pruning confirm](t3-thread://v1/mcp:aeffffc6-06e6-4007-8a73-f2c9ea117703): go given; 12-run confirm running (holds all 4 scout slots; pwv HANDOFF caps subject runs at 4 and `launch.sh` refuses a fifth).
- pi-workspace-view#5: done. PR #10 merged by CoS (3ab8cdd7); thread settled. Wall 9m, 1 review round, 0 runs, Space Bunny 1/1 accepted. Follow-up #9 (subscription protocol gate) is parked and has no go.
- [pi-workspace-view#6 long session](t3-thread://v1/mcp:516fe2e0-b4cc-446b-9747-0f062053c839), [#1+#3 output truncation](t3-thread://v1/mcp:d6ba12c8-7254-41ae-aaf6-2c2504186741), [#2+#4 compaction](t3-thread://v1/mcp:8e61b6dd-a5d2-4d60-8998-8adf9d526443): relaunched 2026-10-12 from the dead threads; all three have go. After #8 frees slots each holds ≤1, #6 first; never bypass `launch.sh`. #1 runs nothing; #3 runs only if the corrected model-free ceiling clears ≥10% (numbers to CoS first); #2+#4 runs one structured-50k scout, second only on a clear halving.

Dead and superseded team threads are settled; a cleanup child settles finished subagent threads.

### Winding down (convert open work to issues, then end; both failed on the session limit mid wind-down)

Relaunched 2026-10-12 as Sol wind-down teams behind plan gates: [P2 wind-down](t3-thread://v1/mcp:f9cca1af-7fdf-4d01-a5b4-d6dc94522b64), [GPUI wind-down](t3-thread://v1/mcp:925be72c-4cb7-4c3a-ba3d-2490ed919a16). Both have go. They settle the dead leads and their queued children. orderready#86 (standing rules) merged by CoS as 516ccd09. The workbench never reached a PR: its head is pushed to `gpui/workbench-lifecycle-final` and is waiting on the 35s-vs-15s qualification budget decision. Backend-response-gate and archive-digest PRs come to the CoS.

Each long-lived lead files `ready` issues for all its open and next work (in-flight branches linked), moves any standing rule it holds into repo docs, finishes only a PR already merge-ready, settles its children, reports, and ends. I then dispatch fresh per-issue teams.

- [P2](t3-thread://v1/mcp:99ab7733-ab01-4241-bfc9-7f7b5f33c579) (orderready, 364 runs). Open work to file: case wall-clock implementation, B4 mailbox, backend-response gate, archive entry digest, notes-tip scrub, the rmut consumer, closing PR #37, pairing approval. The nightly's 06:00 thread check becomes a GitHub issue opened on failure.
- [GPUI](t3-thread://v1/mcp:58780b90-ecc1-4e53-9eaa-4156ab15afcf) (orderready, 317 runs). Workbench PR at review round 6: apply the review rule (merge if no correctness blocker; the rest becomes issues). Remaining `docs/rewrite-plan.md` slices become issues with dependencies. The standing rules move into repo docs: spike worktree and receipts preserved, no `--no-verify` without a CoS go, black-box tests, stdio-only driver.
- Dotfiles, rmut and the agent-context owner: done and settled. Dotfiles' backlog is issues #11 (NAS mount) and #12 (T3 restic restore proof; the unit peaks at its 1G MemoryMax).

### Repo-wide standing rules (until each repo documents them)

- Orderready: `tools/or test --full` is the gate (local, no hosted CI); `tools/or test --repeat N` for repeat proofs; never hand-edit the verdict cache or `~/.cache/orderready/verdicts`; no binary fixtures in Git; the pre-publication `filter-repo` purge needs Tobias's go. Parity: exact React parity until cutover, quirks as rows in `docs/parity-record.md`.

## Needs Tobias

- dotfiles#11 NAS: apply the root units and restore `~/.config/samba/nas.credentials` (omarchy/README.md § NAS mount), then live-check reboot, read/write and outage.

- Artificial Analysis: Tobias has no API key. Either he signs up (free tier) and stores it at `~/.keys/artificial-analysis` (0600), or the tracker drops scores. The table (dotfiles #15) works without them; #16 waits.
- Decision-log review: entries marked **[review]**.

## Watch and hypotheses

- 200K Opus compaction: kept. Prompt per request fell 48% for 4.2M of compaction overhead (`~/.cache/claude-usage-20261012/report.md`; the result is in `agents/coding-models.md`). Re-measure only if quota burn or rework complaints rise.
- Retro 2026-10-11 (`~/.cache/cos-retro-20261011/`):
  - Admission false blocks and blind polling cost more than RAM did.
  - RAM versus serv01 is inconclusive.
  - The dotfiles VM receipt predates the final concurrency fixes and didn't exercise a fresh bootstrap or a disconnected-session handoff.
- Starting an idle turn may kill detached work from an earlier agent scope, so keep long jobs in independent user units. This is still a single-incident hypothesis.
- StepKit geometry team is settled at `d114b6f`, with PR42 parked. Any future qualification needs a new brief.
- The weekly pi-workspace-view audit (Mondays 09:00) now launches a fresh thread per run and reports to CoS.
- The T3 nightly timer updates the service, not the desktop package. Don't restart T3 during live work.
