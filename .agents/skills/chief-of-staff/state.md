# Chief of staff state

Owned by the [chief-of-staff](SKILL.md) skill. Public: no secrets, credentials, source code, or nonpublic employer/customer details. Keep only live operational obligations; repos own work details.

## Coordination

- Current CoS: [Chief of Staff Model Routing](t3-thread://v1/b826766b-7e34-4c9d-bc2d-d3199e4744f6), Opus 5.5 high. All live leaders report here.
- Team leads run on Pi Sol 6.1 high behind CoS gates (trial, Tobias 2026-10-12): plan go before code, CoS merges, ≤3 children, ≤2 review rounds. All subagents run on Pi Sol 6.1 high; Space Bunny is retired (Tobias 2026-10-13; dotfiles#20 merged as 0d14a26 and live, and the routing hook denies it). Metrics use `subagents:` instead of `space_bunny:`. Opus is the CoS only; Haiku is retired. Policy lives in dotfiles `agents/AGENTS.md`.
- Omarchy is the only workstation; serv01 stays NixOS; the old disk is cold storage. No production deployments are authorized.
- Windows VM: agents drive it with `win-vm` ([note](../../../software/omarchy-windows-vm.md)). Orderready's nightly/staging Windows tests run there.

## Teams

Operating model (Tobias, 2026-10-12): disposable teams, one per GitHub issue, in parallel worktrees, ended at merge; GitHub issues are the backlog and handoff. See SKILL.md Delegate and Track performance.

### Sol-lead trial (Tobias, 2026-10-12)

Read each plan and diff before go and merge. Orderready product work comes after #87 and #44. Design-heavy issues wait.

Running:
- [orderready#44 feedback loop](t3-thread://v1/mcp:f62510ba-20e4-4fd1-8aba-541c33547610) in worktree `issue-44-latency`: continuing with corrected evidence labels; closure counts redone on Sol (all 112 jobs / 30 cases). #87 merged (PR #101, b67004b0); told to take in main, take a fresh baseline, then post the plan gate. Follow-ups: #102 renames `test_git`; #103 phase/cohort receipts; #104 validation jobs (128.7s); #105 unclassified test time (98.2s). Now: GUI probe, then batching after a verified GUI restore, then a screen on 1–2 GLOBAL workloads. The capture-cost study is read-only research, and any runtime change needs a new go.
- [Secret-leak prevention](t3-thread://v1/mcp:b808f31b-b1b8-40a2-9d2e-652bbfd41461): resumed; gitleaks now comes from mise (the pkexec unit is stopped). Done: GitHub secret scanning and push protection on all 22 public repos; vault rule 794763b. Built and reviewed (round 2 clean) but uncommitted in `~/.cache/agent-tmp/dotfiles-secret-guard`: the global hook, with passthrough for all other hooks. History audit complete (22/22): 9 exact fingerprints (4 synthetic, 5 from JHotDraw, risk accepted); t3code is upstream-owned. Round 3 is running on the full batch (mise, staged-diff pre-commit, upstream-aware pre-push), then acceptance, `./verify`, PR. The hook is Omarchy-only. Activation = CoS merge plus immediate ff of ~/code/dotfiles at a quiet moment; roll back by revert plus pull. Handoff: `~/.cache/secret-audit/paused-team-handoff-20261013.json`.
- pwv done: #5 (PR #10), #6 (swe-benchmarking#1 871ed477 + pwv#14 54b790bb; case 011 peaks 220–255k), #8 DO NOT PROMOTE, #1 and #3 dead, #2+#4 closed (results PR #15 6e07641e; harness PR swe-benchmarking#2 closed unmerged, branch kept). feat/context-scouts has 12 inherited pytest failures (not green); file and fix them before the next experiment. Threads settled. #9 is parked with no go. Scout cap: 8 total; never bypass `launch.sh`; Sol or the lead launches subject runs.
- dotfiles#12 restic: merged (0d58829d), applied with daemon-reload only, closed. dotfiles#11 NAS: merged; applying needs Tobias.

Dead and superseded team threads are settled; a cleanup child settles finished subagent threads.

### Wound down (2026-10-12)

The P2, GPUI and old-lead threads are settled. P2 filed #88–#99 and pushed `p2/case-wall-clock`. The B4 worktree `$ORDERREADY_DATA/wt/mailbox-corpus` holds an uncommitted mid-merge state; preserve it (#91). GPUI filed #92 and pushed `gpui/workbench-lifecycle-final` (53873a35), which waits on the 35s-vs-15s qualification budget decision. orderready#86/#94/#95 are merged. New per-issue teams start from these issues.

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
- Pi 1.2.0 (Tobias: update when it makes sense): run `mise up pi` only when `pgrep -f "installs/pi/"` is empty and no pwv experiment is running, because live Sol RPC processes read assets through the `latest` symlink. The T3 extension's `before_agent_start` only touches systemPrompt, so it works on 1.2.0. Then spot-check one Sol child.
- The T3 nightly timer updates the service, not the desktop package. Don't restart T3 during live work.
