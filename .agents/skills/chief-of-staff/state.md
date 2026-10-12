# Chief of staff state

Owned by the [chief-of-staff](SKILL.md) skill. Public: no secrets, credentials, source code, or nonpublic employer/customer details. Keep only live operational obligations; repos own work details.

## Coordination

- Current CoS: [Chief of Staff Model Routing](t3-thread://v1/b826766b-7e34-4c9d-bc2d-d3199e4744f6), Opus 5.5 high. All live leaders report here.
- Leaders run on Opus 5.5 high. Delegated execution and review run on Pi Sol 6.1 at thinking high; bounded research runs on Haiku 5.5 high. Policy lives in dotfiles `agents/AGENTS.md`.
- Omarchy is the only workstation; serv01 stays NixOS; the old disk is cold storage. No production deployments are authorized.
- Windows VM: agents drive it with `win-vm` ([note](../../../software/omarchy-windows-vm.md)). Orderready's nightly/staging Windows tests run there.

## Teams

Operating model (Tobias, 2026-10-12): disposable teams, one per GitHub issue, in parallel worktrees, ended at merge; GitHub issues are the backlog and handoff. See SKILL.md Delegate and Track performance.

### Running

- [OpenCode v2 fix](t3-thread://v1/mcp:13512743-3f02-497b-9b17-78c6af701869) (dotfiles): the team installed 1.19.0 (`opencode-ai`); v2 is `@opencode/cli`. It backs up the OpenCode DB, swaps the package, checks the login, gets T3 to re-probe, and runs a smoke test. It ends when it reports.

### Winding down (convert open work to issues, then end)

Each long-lived lead files `ready` issues for all its open and next work (in-flight branches linked), moves any standing rule it holds into repo docs, finishes only a PR already merge-ready, settles its children, reports, and ends. I then dispatch fresh per-issue teams.

- [P2](t3-thread://v1/mcp:99ab7733-ab01-4241-bfc9-7f7b5f33c579) (orderready, 364 runs). Open work to file: case wall-clock implementation, B4 mailbox, backend-response gate, archive entry digest, notes-tip scrub, the rmut consumer, closing PR #37, pairing approval. The nightly's 06:00 thread check becomes a GitHub issue opened on failure.
- [GPUI](t3-thread://v1/mcp:58780b90-ecc1-4e53-9eaa-4156ab15afcf) (orderready, 317 runs). Workbench PR at review round 6: apply the review rule (merge if no correctness blocker; the rest becomes issues). Remaining `docs/rewrite-plan.md` slices become issues with dependencies. The standing rules move into repo docs: spike worktree and receipts preserved, no `--no-verify` without a CoS go, black-box tests, stdio-only driver.
- [Agent-context research](t3-thread://v1/mcp:d7502e10-2088-42ce-9c31-6ff118b57931) (pi-workspace-view): finishes the scout batch in flight; each untried mechanism becomes an issue; then it ends. Fast-loop rule and scout limits: subscription only, at most 4 concurrent, no global Pi config changes, a 12-run confirm needs a CoS go.
- [Dotfiles](t3-thread://v1/mcp:87e88c75-f093-4c7a-9817-97a135c52fe5): NAS mount, the T3 backup and Hermes removal from main become issues.
- [rmut](t3-thread://v1/mcp:2cc5f9ae-2f26-4443-9fc2-7617e9ce3e4b): done. Future producer bugs become rust-mutants issues.

### Repo-wide standing rules (until each repo documents them)

- Orderready: `tools/or test --full` is the gate (local, no hosted CI); `tools/or test --repeat N` for repeat proofs; never hand-edit the verdict cache or `~/.cache/orderready/verdicts`; no binary fixtures in Git; the pre-publication `filter-repo` purge needs Tobias's go. Parity: exact React parity until cutover, quirks as rows in `docs/parity-record.md`.

## Needs Tobias

- Decision-log review: entries marked **[review]**.

## Watch and hypotheses

- 200K Opus compaction: kept. Prompt per request fell 48% for 4.2M of compaction overhead (`~/.cache/claude-usage-20261012/report.md`; the result is in `agents/coding-models.md`). Re-measure only if quota burn or rework complaints rise.
- Retro 2026-10-11 (`~/.cache/cos-retro-20261011/`):
  - Admission false blocks and blind polling cost more than RAM did.
  - RAM versus serv01 is inconclusive.
  - The dotfiles VM receipt predates the final concurrency fixes and didn't exercise a fresh bootstrap or a disconnected-session handoff.
- Starting an idle turn may kill detached work from an earlier agent scope, so keep long jobs in independent user units. This is still a single-incident hypothesis.
- StepKit geometry team is settled at `d114b6f`, with PR42 parked. Any future qualification needs a new brief.
- Weekly task `cos-agent-context-weekly-1` (Mondays 09:00) predates the issue model; retire or retarget it once agent-context research runs from issues.
- The T3 nightly timer updates the service, not the desktop package. Don't restart T3 during live work.
