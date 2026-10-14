# Chief of staff state

Owned by the [chief-of-staff](SKILL.md) skill. Public: no secrets, credentials, source code, or nonpublic employer/customer details. Keep only live operational obligations; repos and decisions.md hold the history.

## Coordination

- Current CoS: thread ID in [scripts/cos-thread](scripts/cos-thread), Opus 5.5 high. Took over from b826766b on 2026-10-14. Handover procedure: SKILL.md working section.
- Routing: leads and children on Pi Sol 6.1 high; UI leads on Opus 5.5 high (studio, orderready#79). Policy lives in dotfiles `agents/AGENTS.md`.
- No dedicated Monitor/AX/mailbox test environments (Tobias, 2026-10-14): nightlies run on fakes and target staging; Tobias deploys staging by hand and tests real environments on weekends.
- Delivery model (Tobias, 2026-10-14, permanent): PR→main on fast check + touched tests + no new failures vs main; full suite nightly on main→staging; green nightlies auto-promote main to staging; only Tobias touches production; infra runs beside product; product gates get the heavy slot first.
- Private repos may hold customer names and customer-derived content (Tobias, 2026-10-14). Public repos and the vault may not.
- Census heartbeat: `scheduled-task:command:mcp:534c308f-ba1f-4c9e-a41d-995dceb4e574:schedule-task:cos-census-heartbeat-d41aa0f0`, every 30 min, bound to the CoS thread. A successor recreates it bound to itself and deletes the old one.
- Windows VM: agents drive it with `win-vm` ([note](../../../software/omarchy-windows-vm.md)).

## Live teams

Brief messages to leads with `cos.py brief --short`. Merge per the working section (orderready: `pr-merge`; others: `gh pr merge --match-head-commit`), then `link_pull_request`.

### orderready (T3 project mcp:e9b15f49-8281-4ab3-97fd-958e235a97e6, private)

- [#138 PR gate + nightly](t3-thread://v1/mcp:2d4cc779-09d9-4a10-887c-d4f16c0ff94e), Sol. Second one-shot timed out at 120 s (cold SDK installs inside the case). GO'd fixture-only fix: SDKs prepared once outside the timed case and digest-verified, no budget change, then one fresh one-shot (fails → STOP). Fixture fix passed (one-shot 96 s < 120 s). Exact-head review blocked on R1 (ancestral Fail transferred without checking current-main case key) and R2 (prefix-matching dispatch selects sibling cases); GO'd both fixes with one regression check each, re-check-only review, then four serialized once-only GUI attempts after #79's gate. The GUI deadline blocks (0–2 ms overruns under load, also on main and #79) are pre-existing and don't block; #62 owns the fix. Design: one real main-bootstrap case plus once-built baseline fixture; nightly issues name raw failing case IDs only. The sticky-test timeout is pre-existing (#139). On merge-ready: verify, `pr-merge`; then delete scheduled task `scheduled-task:command:mcp:158a57f6-2737-40e7-a61c-261fa4faf1ae:schedule-task:p2-nightly-verdict-check-1` (Opus nightly check, superseded) and have the lead live-check the first real product PR.
- [#91 mailbox corpus](t3-thread://v1/mcp:20df8d60-5189-443a-8817-7c997e32b8b5), Sol, preserved worktree `$ORDERREADY_DATA/wt/mailbox-corpus`. Migrating cases with original input bytes (binary fixtures go to the local fixture store by SHA; repo bans binary files in Git). 188/189/190 keep exact sources; export-proof receipts are findings only. Then two local hooked merges, push the real branch with full ancestry, PR handoff. All 306 migrations done. GO'd (2026-10-14) the B1 fix: 10 cases get an explicit email_body.txt and one expected-upload entry (20 fixture files), so the effective workload stays identical. Next: B1 re-check only, merges, PR to me. #142 follows it.
- [#79 mailbox enroll + machines page](t3-thread://v1/mcp:0f802e97-362a-4272-a6e0-737155243f6f), Opus (UI). GO'd: migrate 8 corpus cases + Windows lane to pairing, delete old stdin tests and platform `machine create`, ports admin seam + 4 admin routes, GPUI machines page mounted when #53 lands. GO'd (2026-10-14) api-parity allowlist `docs/api/orderready-only-operations.json` for the 4 rewrite-only admin routes (no stale/shadow entries, OIP target stays frozen). Selection gap (api-parity not selected on route change) gets fixed in scope or as a follow-up. GO'd first-order budget 8000→13000 (five real pairings, inherent 1 s poll, same headroom); other budgets restored; kill-loop-rate-1 fixed by changing the case, not the budget. Both commits reviewed (PR1 head eb3b8ccf); PR3/PR4 rebased and reviewed. GO'd (2026-10-14) `tools/or invalidate` of the #139 sticky test:xtask Fail for PR1/PR3/PR4 (that test only, xtask/src untouched), plus `tools/or gate` on PR1 after the main nightly `--full` exits, ahead of the infra slot queue. Next: PR1 merge-ready, then PR3, PR4.
- [#62 case wall clock](t3-thread://v1/mcp:8b9600ac-d941-4c7f-bc30-ce49689b5c1d), Sol, `wt/case-wall-clock`. CPU rule GO'd (schedstat run_delay); then one fresh eight-observation W7, gate, PR; yields the heavy slot to product. Integrated and checked. GO'd (2026-10-14) one synthetic dry run of unchanged c802be8d (the guard needs a receipt matching the script SHA), then W7 once. Prepared and frozen at 4cfec779 (2026-10-14), idle until granted. Heavy-slot queue: #67 counter run (holding) → #62. Grant it after #67 releases, unless an orderready gate (#79 PR1, #138 GUI attempts) is running.
- AX domain knowledge lives in orderready `docs/ax-knowledge.md` (PR #143, 8abbd2a1). #141 (Rust-only Invalid URL advice: find the debtor, check its URL/Email contact rows, recorded as intended divergence from Python) plus #69/#72 rescope comments: Sol child `node:delegated-task:command%3Amcp%3A7356da3c-9a02-4a0c-bb9c-11121d1369fd%3Adelegate-task%3Acos-141-invalid-url-advice-and-69-rescope-1`, PR to me.
- #144 AX GUI→server calls: 25-step map and passive Trace Parser plan for Tobias's weekend sessions (T01 Journal promotion, T04 sales-linked production creation, T05 backward scheduling first). Tobias can't create/deploy TT-style services (2026-10-14), so .NET BC on existing classes is the primary route, the TT owner is an optional later ask, and GUI is the fallback #144 updated: (a) 6, (c) BC 12, (d) 7. Later Tobias choice: printing. No team until traces exist.
- Queued team: #142 runner replay cases (18 attempts from 8–14 Oct; offline stages plus AX/Graph fakes). Start a Sol lead when #91 lands.
- Repo rules: `tools/or test --full` is the full gate; never hand-edit `~/.cache/orderready/verdicts`; no binary fixtures in Git; `cos-approved` label is CoS-only.

### stepkit-geometry (T3 project mcp:da4aca75-407d-45f6-a717-1826c232b90c)

- #75 merged as PR #77 (0d8011aa, 2026-10-14). Lead is fast-forwarding the primary main and running `tools/sg nightly install`; settle after it reports the timer.
- [#67 large-file stalls](t3-thread://v1/mcp:4be01f9a-8d50-4169-a811-5f19b87b48bb), Sol, branch `issue-67-remaining-stalls` at 299a85fe. Stack probe done, slot released: time goes to serial ribbon-separation certification (plane_boundary.rs:378-379) before triangulation. Source analysis can't separate the hypotheses. GO'd one counter-only ≤90 s observation (scratch only); holds the heavy slot since 2026-10-14 (then #62 is next). Fix candidate (per-segment root-ribbon reuse) waits on the counts.
- Open, no team: #73 nested parity CLI, #76 spline rounding bound (from studio #20), #63 mesh40/point-jet, #65 release freshness, #58 generator supplement; #60/#61 need a value check before any go.

### stepkit-studio (T3 project mcp:49a07e59-1f64-44c2-9649-5dd070ed4cba, private)

- [#1 v1 viewer lead](t3-thread://v1/mcp:7ceb210a-d7b1-41bd-9ebd-51026526c1e7), Opus (UI). Merged 2026-10-14: #15, #17 (pin 299a85fe), #18 (#12), #21 (#13), #23 (#11, cdd2f14b), #25 (#16, ea43570f), #28 (#8, c2b6f449), #29 (#22, 1f87c1c0; Windows branch unrun until nightly), #30 (#10 reversed-Z, ca945954). Running: #9 (parked on load-stall diagnosis). Follow-ups #19, #20 (upstream = geometry #76), #24, #26, #27.

## CoS children in flight

- `cos-runner-bc-readiness-check-1` (Sol): read-only runner check for the BC DLL, AX versions and trace groups, plus one data-neutral BC logon (Tobias authorized 2026-10-14).

- #141 child (see orderready section).




## Needs Tobias

- Nothing open.

## Watch

- Pi leads started before dotfiles b6fd8d9 (orderready #138, #91, #62; geometry #75, #67) were pinned to the old CoS thread b826766b. As of 2026-10-14 that thread is no longer readable, and #138, #67, #62, #79 and studio report straight here. If a lead goes quiet past its expected report, ask it for its status directly.
- Weekly pi-workspace-view task `scheduled-task:command:mcp:b44bca5c-af0c-40b2-8d4a-be9117fa0414:schedule-task:cos-workspace-view-weekly-omarchy-1` (Mondays 09:00, bound to thread 4d49b702) failed its last run; check why before 2026-10-19.

- Re-measure CoS answer latency on 2026-10-20 with `cos.py metrics` (baseline: median 29 s, p90 12 min).
- `mise up pi` to 1.2.0 only when `pgrep -f "installs/pi/"` is empty; then spot-check one Sol child.
- T3 restarts kill every live run: run `cos.py restart-check` first. The T3 nightly timer updates the service, not the desktop app.
- Orderready admission can false-block on reclaimable cgroup cache; the workaround is `memory.reclaim` on app-t3code.slice.
- Trim the SKILL working section toward rules only; decisions.md has 120+ unreviewed entries, so put a log review in front of Tobias when he has time.
