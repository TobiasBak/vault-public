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

- Sol product leads, briefs o/p/q: [#235 route timeout](t3-thread://v1/mcp:b0cbadaa-8c14-47e3-85ba-4b747656d28e), [#98 workcenter defaults](t3-thread://v1/mcp:e2bc18cb-7603-4d80-8ba2-39543cc66b5e), [#183 then #232](t3-thread://v1/mcp:db96fb05-07cd-4b6e-9d05-8097ee8c4817) (#183 MERGED as PR #264 → c17d4859; #232 in progress), from origin/main. GUI #218/#221/#225/#228/#234/#238/#239/#242/#244 wait for Studio #190's Opus UI turn; census ready count includes blocked issues.
- (20:06) #98 draft PR #266 blocked on GUI-case flakes (application-shell 30 ms over budget under contention; close-flow /proc '-1' counter): one more push verification authorized, else park until #265. Infra lead [#265 GUI case spurious blocks](t3-thread://v1/mcp:195068c7-d2e9-4a30-8f48-71c385be892a), Sol, brief r: fix the /proc parser first, then attribute application-shell; budget/case changes need a go. Only orderready infra team.
- #138: [lead](t3-thread://v1/mcp:2d4cc779-09d9-4a10-887c-d4f16c0ff94e) still owes closure reply and forwarding 4537dd47 to #62; settle after reply. Follow-ups #140 qualification, #145 wording. #91 criterion 7 remains parked in #62/#63, though both are later recorded closed; disposition unclear.
- [Windows GUI qualification #185→#77/#83](t3-thread://v1/mcp:a999a9cd-5c95-4d7f-887f-8c30e8b14f11): use promotion qualification's Windows obligations, not retired nightly.rs. Close obsolete #80 as superseded; old nightly budget is void, new budget needs an ask. GO'd cfg(windows)-only xtask→windows-interop leaf edge and safe Job/keyboard/session wrappers; close via pid-verified UIA WindowPattern.Close.
- [Close-flow #162/#165/#161](t3-thread://v1/mcp:9bf20638-ba45-4d99-b9fe-ac568d6b3838): team closing out after #219. Re-scope #220/#221 against parity rule, judge #242 in-app leave guard separately; closure status unclear. #218 Shift+Tab follow-up restores #161 steps.
- #202 GUI flow cost waits for Windows GUI team to land; both touch the corpus GUI runner. Then fresh #103 attribution before #103–#105 work. #90 needs disposition of old pressure-cohort findings.
- #144: no team until Tobias's weekend traces T01/T04/T05 exist; real-data authorization stays Tobias's. BC is usable for reads; facts belong in repo docs/ax-knowledge.md.
- Open follow-ups: #148, #149, platform#7, #171; #147 oracle regeneration; #154 status watcher startup; #199 Windows runtime/AX/junction qualification; #180, #183, #186–#188, #190, #192 import performance; #181 Windows measurement blocked on #77; #250 Windows warnings; #236–#239, #243, #244, #248; #158, #159, #163. #242 remains unstarted.
- Repo rules: `tools/or test --full` is the full gate; never hand-edit `~/.cache/orderready/verdicts`; no binary fixtures in Git.

### stepkit-geometry (T3 project mcp:da4aca75-407d-45f6-a717-1826c232b90c)

- [#67 ribbon reuse](t3-thread://v1/mcp:b4fa9c4d-2446-4905-80d2-5939a53773ac), Sol: `issue-67-ribbon` from `issue-67-resume` ca941ab, brief l. PR #104 MERGED 19:56 → c2d1b34d (12x faster, outputs byte-identical); the 2.6 MB/13 MB models still time out at 300 s, #67 stays open, convergence in #97/#98. Lead finalizing; settle on done.
- [#87 measure refusal](t3-thread://v1/mcp:7042feda-5d4c-4504-8646-0f1f73ac5ad7), Sol, brief m: tagged refusal on reconstructed junctions until a bound is proved. Policy revised: junctions with proved tolerance-bounded displacement are measured with per-channel error terms, otherwise refused; the two tangent-slot expectations stay at main unless one still refuses with per-case evidence; curved-cylinder-junction checks still approved.
- [#102 red main](t3-thread://v1/mcp:17072b56-c5ed-4159-b994-b17455108c0c), Sol, brief n: GO'd descriptor-loss fix at 4 case_runner sites plus byte-race fixture driver plumbing only.
- #81 parked under infra freeze; old lead settled. Open without teams: #73 nested parity CLI, #63 mesh40/point-jet, #65 release freshness, #58 generator supplement; #60/#61 need value checks. #90/#78 remain in start-later list; #87 policy is decided.
- Follow-ups #83/#85 from #68; #93 wall time on 5 faces. #89 remains under Needs Tobias. #76 trial hardening/rerun obligation is under CoS children.
- #75: check first nightly result; no result recorded here. Theodore verification-tracing contract: pilot in one repo beside product work still pending.

### stepkit-studio (T3 project mcp:49a07e59-1f64-44c2-9649-5dd070ed4cba, private)

- [UI lead](t3-thread://v1/mcp:7ceb210a-d7b1-41bd-9ebd-51026526c1e7): #190 resumed 18:15: geometry re-pinned to deffaf8f (Studio 0910ebe on main c6dd990), Opus implementer `studio-190-ui-impl-1` running; lead reviews, then merge_ready. Picks: #164 muted depth number on capped rows only; Refusals tree filter, collapsible per-type counts, eye always visible on hidden rows; defer x-ray. #194 already merged #164/#189; which picks remain is unclear.
- #124 remains open until a failing nightly files a report; #188 cold-cache `--try` gap is low priority. Resize-delta fidelity gap and widget-id shift/480 px-space follow-up still need disposition; no issue numbers recorded.

## CoS children in flight

- `cos-76-ab-hardening-1`: 3 issues, report_to_cos readiness check and 2 brief bullets; status not updated after "running". Analysis: ~/.cache/agent-tmp/76-compare/analysis.md. Then optional pair 2 / hardened Sol rerun. Follow-ups geometry #78/#79 remain without recorded closure; #80 is closed.
- [Heavy-lease scheduler](t3-thread://v1/mcp:2cb5489d-5432-41df-af57-599340a69529): core and pass_fds/nested-weight fixes merged; lead settlement not recorded. Follow-ups orderready #255 and #260 remain; #253 and #252 are closed.
- dotfiles#40 pool size PARKED 19:38: reviewed harness tree 2ee6b19d ready; the efficiency weight-4 lease never got admitted in 3600 s under product load (intended). Pool stays 4. Relaunch only in an idle window (heavy-lease shows no waiters, e.g. overnight); resume note in the issue. Lead settled; relaunch fresh from the issue resume note.
- Hardware-deals thread mcp:f562cb73 is a settle candidate; result already relayed, no work remains.

## Holds

- Start later: orderready #202 after Windows lands, then fresh #103 attribution and #90 disposition; geometry #90/#78 and #25 consumer preview. #87 is already launched. Host lazy-mise-wrapper follow-up: Windows lead still owes an issue for 16 wrappers hanging under systemd.
- CoS tooling: delegated writer to put the in-turn wait rule into `cos.py brief`; SKILL already has it, brief-text update not recorded done.
- orderready #224: tell native-screens lead to keep reload-on-mount and decide caching once across screens; no implementation work. Native-screens team is done; delivery of this message not recorded.
- Vault: delegate parity-scope rule into tobias/preferences.md. Business logic needs parity, UI incidentals may improve; completion not recorded.

## Needs Tobias

- Open for Tobias (asked 2026-10-17): allow two Opus UI teams; my recommendation is yes while five_hour < 40%, keep the 60% stop.
- Parked choices, not urgent: geometry #89 (triangle allocation order policy), geometry #61 (versioned persisted observation format), orderready #137 (OCR: measure scanned-PDF incidence first), #144 (real-data qualification authorization), orderready #99 / geometry #50 (history rewrite / backend promotion).

## Watch

- Watch for Tobias reporting fast Codex credit burn; CoS cannot read the balance.
- Old CoS thread b826766b is unreadable. If a lead goes quiet past its expected report, ask directly; most named old leads are now settled or replaced.
- Re-measure CoS answer latency on 2026-10-20 with `cos.py metrics` (baseline: median 29 s, p90 12 min).
- `mise up pi` to 1.2.0 only when `pgrep -f "installs/pi/"` is empty; then spot-check one Sol child.
- T3 restarts kill every live run: run `cos.py restart-check` first. The T3 nightly timer updates the service, not the desktop app.
- Orderready admission can false-block on reclaimable cgroup cache; workaround: `memory.reclaim` on app-t3code.slice.
