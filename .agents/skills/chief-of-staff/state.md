# Chief of staff state

Owned by the [chief-of-staff](SKILL.md) skill. Public: no secrets, credentials, source code, or nonpublic employer/customer details. Keep only live operational obligations; repos hold the history.

## Coordination

- Current CoS: thread ID in [scripts/cos-thread](scripts/cos-thread), Opus 5.5 high. Took over from b826766b on 2026-10-14. Handover procedure: SKILL.md working section.
- Routing: leads and children on Pi Sol 6.1 high; UI leads on Opus 5.5 high (studio, orderready#79). Policy lives in dotfiles `agents/AGENTS.md`.
- No dedicated Monitor/AX/mailbox test environments (Tobias, 2026-10-14): nightlies run on fakes and target staging; Tobias deploys staging by hand and tests real environments on weekends.
- Delivery model (Tobias, 2026-10-14, permanent): PR→main on fast check + touched tests + no new failures vs main; full suite nightly on main→staging; green nightlies auto-promote main to staging; only Tobias touches production; infra runs beside product; product gates get the heavy slot first.
- Private repos may hold customer names and customer-derived content (Tobias, 2026-10-14). Public repos and the vault may not. Orderready will never be public (Tobias, 2026-10-17); #99/#81 closed.
- Census heartbeat: `scheduled-task:command:mcp:534c308f-ba1f-4c9e-a41d-995dceb4e574:schedule-task:cos-census-heartbeat-d41aa0f0`, every 30 min, bound to the CoS thread. A successor recreates it bound to itself and deletes the old one.
- Tobias 2026-10-17: Opus UI teams: two while every quota window <40%, one while <60%, none at ≥60%; one Opus child per team. Geometry #50 backend switch approved (parity remains the technical gate). Orderready #137 OCR closed, no more OCR work.
- Windows VM: agents drive it with `win-vm` ([note](../../../software/omarchy-windows-vm.md)).

## Live teams
- Opus UI [Import page lead](t3-thread://v1/mcp:3e1d2a97-defe-49a9-bbdf-4df41204173b) (only live Opus team): Tobias 21:02 full Import REDESIGN "way better" w/ old-app features (#276 inventory, design+slicing there), real Gemini on RP2XL OK; #270 folded in; slice 1 #287 merged 575509f (#270); slice 2 #299 merged 7c010ae (#290); slice 3 = #300, impl child finishing → WIP push, then PARKED: Opus stop seven_day 60% until 10-22T18Z (wake then); routing: Tobias 21:59 no applies-to filter (customer route = all parts); renumber ALL ops sequentially 10/20/30 (no pinned numbers) unless Sol finds evidence numbers must be kept; blocked only if unplaceable. Renumber GO 22:11 (A–E, F pre-approved by rule).
- Infra lead settled (#265/#268/#283 done). Ready: dotfiles#44 pr-merge merge-base fix (launch Sol when convenient).

Brief messages to leads with `cos.py brief --short`. Merge per the working section (orderready: `pr-merge`; others: `gh pr merge --match-head-commit`). Never `link_pull_request` (Tobias, 2026-10-17).

### orderready (T3 project mcp:e9b15f49-8281-4ab3-97fd-958e235a97e6, private)

- Sol product leads: [#235 route timeout](t3-thread://v1/mcp:b0cbadaa-8c14-47e3-85ba-4b747656d28e) (parked). GUI queue after Import redesign: #218/#221/#225/#228/#234/#238/#239/#242/#244. Census ready count includes blocked issues.
- Infra lead [#265 GUI case spurious blocks](t3-thread://v1/mcp:195068c7-d2e9-4a30-8f48-71c385be892a), Sol, brief r: fix the /proc parser first, then attribute application-shell; budget/case changes need a go. Only orderready infra team. Next: #268 xtask memory admission false-blocks on reclaimable cache (Tobias: make sure it gets fixed), queued to this lead 20:42.
- #138: [lead](t3-thread://v1/mcp:2d4cc779-09d9-4a10-887c-d4f16c0ff94e) still owes closure reply and forwarding 4537dd47 to #62; settle after reply. Follow-ups #140 qualification, #145 wording. #91 criterion 7 remains parked in #62/#63, though both are later recorded closed; disposition unclear.
- [Windows GUI qualification #185→#77/#83](t3-thread://v1/mcp:a999a9cd-5c95-4d7f-887f-8c30e8b14f11): use promotion qualification's Windows obligations, not retired nightly.rs. Close obsolete #80 as superseded; old nightly budget is void, new budget needs an ask. GO'd cfg(windows)-only xtask→windows-interop leaf edge and safe Job/keyboard/session wrappers; close via pid-verified UIA WindowPattern.Close.
- [Close-flow #162/#165/#161](t3-thread://v1/mcp:9bf20638-ba45-4d99-b9fe-ac568d6b3838): team closing out after #219. Re-scope #220/#221 against parity rule, judge #242 in-app leave guard separately; closure status unclear. #218 Shift+Tab follow-up restores #161 steps.
- #202 GUI flow cost waits for Windows GUI team to land; both touch the corpus GUI runner. Then fresh #103 attribution before #103–#105 work. #90 needs disposition of old pressure-cohort findings.
- #144: Tobias tests Business Connector with the CoS on 2026-10-18; no team before that. Weekend traces T01/T04/T05 still pending; real-data authorization stays Tobias's. BC is usable for reads; facts belong in repo docs/ax-knowledge.md.
- Open follow-ups: #148, #149, platform#7, #171; #147 oracle regeneration; #154 status watcher startup; #199 Windows runtime/AX/junction qualification; #180, #183, #186–#188, #190, #192 import performance; #181 Windows measurement blocked on #77; #250 Windows warnings; #236–#239, #243, #244, #248; #158, #159, #163. #242 remains unstarted.
- Repo rules: `tools/or test --full` is the full gate; never hand-edit `~/.cache/orderready/verdicts`; no binary fixtures in Git.

### stepkit-geometry (T3 project mcp:da4aca75-407d-45f6-a717-1826c232b90c)

- #81 parked under infra freeze; old lead settled. Open without teams: #73 nested parity CLI, #63 mesh40/point-jet, #65 release freshness, #58 generator supplement; #60 needs value checks; #61 decided 2026-10-17 (versioned dedup format), ready. #90/#78 remain in start-later list; #87 policy is decided.
- Follow-ups #83/#85 from #68; #93 wall time on 5 faces. #89 decided 2026-10-17 (literal faces get budget priority); ready. #76 trial hardening/rerun obligation is under CoS children.
- #75: check first nightly result; no result recorded here. Theodore verification-tracing contract: pilot in one repo beside product work still pending.

### stepkit-studio (T3 project mcp:49a07e59-1f64-44c2-9649-5dd070ed4cba, private)

- Tobias 2026-10-17: v1 is done after #190; park #113, #183, #188, #191–#193, #124 (open, no team); stop and settle the team after #190 merges.
- Studio v1 DONE 20:59 (#196 merged b3ec7ae; #1 outcome posted; rest parked, no team). Lead settled.
- #124 remains open until a failing nightly files a report; #188 cold-cache `--try` gap is low priority. Resize-delta fidelity gap and widget-id shift/480 px-space follow-up still need disposition; no issue numbers recorded.

## CoS children in flight

- Disk cleanup done 22:40: 83%→52% (895G free). Log ~/.cache/disk-cleanup-20261017/. 80 dirty old worktrees left (mostly ~/.local/share/orderready/wt/case-clock-* probes); later: CoS-delegated triage, not a Tobias ask. Tell Tobias in morning.
- `cos-76-ab-hardening-1`: 3 issues, report_to_cos readiness check and 2 brief bullets; status not updated after "running". Analysis: ~/.cache/agent-tmp/76-compare/analysis.md. Then optional pair 2 / hardened Sol rerun. Follow-ups geometry #78/#79 remain without recorded closure; #80 is closed.
- [Heavy-lease scheduler](t3-thread://v1/mcp:2cb5489d-5432-41df-af57-599340a69529): core and pass_fds/nested-weight fixes merged; lead settlement not recorded. Follow-ups orderready #255 and #260 remain; #253 and #252 are closed.
- dotfiles#40 pool size PARKED 19:38: reviewed harness tree 2ee6b19d ready; the efficiency weight-4 lease never got admitted in 3600 s under product load (intended). Pool stays 4. Relaunch only in an idle window (heavy-lease shows no waiters, e.g. overnight); resume note in the issue. Lead settled; relaunch fresh from the issue resume note.
- Hardware-deals thread mcp:f562cb73 is a settle candidate; result already relayed, no work remains.

## Holds

- Test GUI stopped (Tobias OK 22:37; already exited). Relaunch for him 2026-10-18 signed in + real Gemini. Rule: his test runs always signed in + real Gemini (key ~/.keys/gemini.env); launcher = #272.
- #278: #285 merged 5a01b95 (00:29Z): unsigned (#279); runbook docs/distribution.md (prod publish = Tobias). #292 decided 10-18: isolated new Firestore registry + tolerant readers (ignore unknown fields); Sol lead mcp:467b7b12. #301 = delete legacy registry, Tobias only. Tobias OK agent apply; platform#10 merged 42840e8 + #302 merged 1ee6ae8 (10-18); applied 4 add/0/0 OK; effective-IAM APIs off → accepted direct-binding evidence, check at deploy; closing #292.

- Start later: orderready #202 after Windows lands, then fresh #103 attribution and #90 disposition; geometry #90/#78 and #25 consumer preview. Host lazy-mise-wrapper follow-up: Windows lead still owes an issue for 16 wrappers hanging under systemd.
- CoS tooling: delegated writer to put the in-turn wait rule into `cos.py brief`; SKILL already has it, brief-text update not recorded done.
- orderready #224: tell native-screens lead to keep reload-on-mount and decide caching once across screens; no implementation work. Native-screens team is done; delivery of this message not recorded.

## Needs Tobias
- Delegation rewrite landed 10-18: dotfiles 4624f50, vault 67a37c1 (lead rules in scripts/brief.md). Asked Tobias: platform staging→prod deploy pipeline issue + team?

- 2026-10-18: run through .NET Business Connector with Tobias for orderready #144; record findings in #144 and docs/ax-knowledge.md.

## Watch

- Watch for Tobias reporting fast Codex credit burn; CoS cannot read the balance.
- Old CoS thread b826766b is unreadable. If a lead goes quiet past its expected report, ask directly; most named old leads are now settled or replaced.
- Re-measure CoS answer latency on 2026-10-20 with `cos.py metrics` (baseline: median 29 s, p90 12 min).
- `mise up pi` to 1.2.0 only when `pgrep -f "installs/pi/"` is empty; then spot-check one Sol child.
- T3 restarts kill every live run: run `cos.py restart-check` first. The T3 nightly timer updates the service; Tobias has no desktop app (removed 2026-10-17).
