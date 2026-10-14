# Chief of staff state

Owned by the [chief-of-staff](SKILL.md) skill. Public: no secrets, credentials, source code, or nonpublic employer/customer details. Keep only live operational obligations; repos and decisions.md hold the history.

## Coordination

- Current CoS: thread ID in [scripts/cos-thread](scripts/cos-thread), Opus 5.5 high. Took over from b826766b on 2026-10-14. Handover procedure: SKILL.md working section.
- Routing: leads and children on Pi Sol 6.1 high; UI leads on Opus 5.5 high (studio, orderready#79). Policy lives in dotfiles `agents/AGENTS.md`.
- Delivery model (Tobias, 2026-10-14, permanent): PR→main on fast check + touched tests + no new failures vs main; full suite nightly on main→staging; green nightlies auto-promote main to staging; only Tobias touches production; infra runs beside product; product gates get the heavy slot first.
- Private repos may hold customer names and customer-derived content (Tobias, 2026-10-14). Public repos and the vault may not.
- Census heartbeat: `scheduled-task:command:mcp:534c308f-ba1f-4c9e-a41d-995dceb4e574:schedule-task:cos-census-heartbeat-d41aa0f0`, every 30 min, bound to the CoS thread. A successor recreates it bound to itself and deletes the old one.
- Windows VM: agents drive it with `win-vm` ([note](../../../software/omarchy-windows-vm.md)).

## Live teams

Brief messages to leads with `cos.py brief --short`. Merge per the working section (orderready: `pr-merge`; others: `gh pr merge --match-head-commit`), then `link_pull_request`.

### orderready (T3 project mcp:e9b15f49-8281-4ab3-97fd-958e235a97e6, private)

- [#138 PR gate + nightly](t3-thread://v1/mcp:2d4cc779-09d9-4a10-887c-d4f16c0ff94e), Sol. Implementing the GO'd design: one real main-bootstrap case plus once-built baseline fixture; nightly issues name raw failing case IDs only. The sticky-test timeout is pre-existing (#139). On merge-ready: verify, `pr-merge`; then delete scheduled task `scheduled-task:command:mcp:158a57f6-2737-40e7-a61c-261fa4faf1ae:schedule-task:p2-nightly-verdict-check-1` (Opus nightly check, superseded) and have the lead live-check the first real product PR.
- [#91 mailbox corpus](t3-thread://v1/mcp:20df8d60-5189-443a-8817-7c997e32b8b5), Sol, preserved worktree `$ORDERREADY_DATA/wt/mailbox-corpus`. Migrating cases with original input bytes (binary fixtures go to the local fixture store by SHA; repo bans binary files in Git). 188/189/190 keep exact sources; export-proof receipts are findings only. Then two local hooked merges, push the real branch with full ancestry, PR handoff. No open gate.
- [#79 mailbox enroll + machines page](t3-thread://v1/mcp:0f802e97-362a-4272-a6e0-737155243f6f), Opus (UI). GO'd: migrate 8 corpus cases + Windows lane to pairing, delete old stdin tests and platform `machine create`, ports admin seam + 4 admin routes, GPUI machines page mounted when #53 lands. Census 2026-10-14 flagged it idle with a plan or question: read its last message and answer.
- [#62 case wall clock](t3-thread://v1/mcp:8b9600ac-d941-4c7f-bc30-ce49689b5c1d), Sol, `wt/case-wall-clock`. CPU rule GO'd (schedstat run_delay); then one fresh eight-observation W7, gate, PR; yields the heavy slot to product. Census 2026-10-14: last run failed; resume it.
- Repo rules: `tools/or test --full` is the full gate; never hand-edit `~/.cache/orderready/verdicts`; no binary fixtures in Git; `cos-approved` label is CoS-only.

### stepkit-geometry (T3 project mcp:da4aca75-407d-45f6-a717-1826c232b90c)

- [#75 gate team](t3-thread://v1/mcp:61b06fd3-e81c-481c-948d-0444a2a0c9da), Sol, branch `gate/fast-pr-nightly-full`. Holds the heavy slot: hooked push running, then subset demonstration, then merge-ready. On merge or slot release: tell the #67 lead it has the slot (product gates first).
- [#67 large-file stalls](t3-thread://v1/mcp:4be01f9a-8d50-4169-a811-5f19b87b48bb), Sol, branch `issue-67-remaining-stalls` at 299a85fe. Queued grant: one p0283 ordinal-15 probe under gdb (stack snapshots first, at most two 90 s windows), then STOP, report, release the slot. Waiting on the slot.
- Open, no team: #73 nested parity CLI, #76 spline rounding bound (from studio #20), #63 mesh40/point-jet, #65 release freshness, #58 generator supplement; #60/#61 need a value check before any go.

### stepkit-studio (T3 project mcp:49a07e59-1f64-44c2-9649-5dd070ed4cba, private)

- [#1 v1 viewer lead](t3-thread://v1/mcp:7ceb210a-d7b1-41bd-9ebd-51026526c1e7), Opus (UI). Merged 2026-10-14: #15, #17 (pin 299a85fe), #18 (#12), #21 (#13), #23 (#11, cdd2f14b). Running: #16 and side lane #22. Next: #8 (expects a gate; renderer pixel bands), #9, #10. Follow-ups #19, #20 (upstream = geometry #76), #24.

## CoS children in flight

- `node:delegated-task:command%3Amcp%3Ade412bf8-cff4-4245-ba58-a9ea021fcd6a%3Adelegate-task%3Acos-report-retarget-1` (Sol; owned by the old CoS thread b826766b, so its completion wakes that thread: read the result from the child thread or the dotfiles log on the census): Pi `report_to_cos` extension retargets to the latest `CoS-thread:` line, plus whether live sessions load it without restart. On result: verify the dotfiles commit; if live sessions need a reload, tell Tobias which leads stay pinned to the old thread until their issue ends.

## Needs Tobias

- Nothing pending.

## Watch

- Weekly pi-workspace-view task `scheduled-task:command:mcp:b44bca5c-af0c-40b2-8d4a-be9117fa0414:schedule-task:cos-workspace-view-weekly-omarchy-1` (Mondays 09:00, bound to thread 4d49b702) failed its last run; check why before 2026-10-19.

- Re-measure CoS answer latency on 2026-10-20 with `cos.py metrics` (baseline: median 29 s, p90 12 min).
- `mise up pi` to 1.2.0 only when `pgrep -f "installs/pi/"` is empty; then spot-check one Sol child.
- T3 restarts kill every live run: run `cos.py restart-check` first. The T3 nightly timer updates the service, not the desktop app.
- Orderready admission can false-block on reclaimable cgroup cache; the workaround is `memory.reclaim` on app-t3code.slice.
- Trim the SKILL working section toward rules only; decisions.md has 120+ unreviewed entries, so put a log review in front of Tobias when he has time.
