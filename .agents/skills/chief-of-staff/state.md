# Chief of staff state

Owned by the [chief-of-staff](SKILL.md) skill. Public: no secrets, credentials, source code, or nonpublic employer/customer details. Keep only live operational obligations; repos own work details.

## Coordination

- Current CoS: [Take Over Chief of Staff](t3-thread://v1/4d49b702-82f7-4931-a5f2-4e785676067d). Former `ccd17c32-b147-491a-bb29-189a3b19af51` is archived. All six team leaders have the new report target. Handover: `~/.cache/cos-takeover-20261011/handover.md`; no live former-CoS children.
- Teams own workers, reviews, gates, commits and integration. Report only completed workstreams/agreed milestones, unowned cross-team/authority blockers and material Tobias decisions. Questions use numbered **Your decisions**; informational calls use **Decided by me**.
- Claude quota is still unconfirmed. Recorded reset was 2026-10-11 18:40 CEST, not an availability guarantee. Current Sol leaders are temporary recovery. Opus 5.5 owns TOP-LEVEL leadership/design/decisions, NEVER subagents; execution/implementation/code-review delegates explicitly target Pi Sol 6.1. Bounded Haiku non-coding research remains allowed, but no Claude calls while quota is exhausted.
- Model policy is merged/live-file verified in dotfiles PR8 `a16284f`, reviewed `6aab6ec`, identical tree `51ba40d`, 14-test/static gates and three canonical instruction-link hashes. Existing hook defaults explicitly select Pi/Sol. Active leaders received a steer; fresh sessions adopt persisted instructions. Vault notes aligned at `b4d88f9`; writers/verifiers settled. No provider/quota test or restart.
- Omarchy is the only workstation, Nix-free; serv01 remains NixOS. Old disk is cold storage. Windows VM is Tobias's staging tool: agents never provision/start/run it. No production deployments or T3 restart authorized.

## Teams

### GPUI pure-Rust Linux/Windows compile proof

[Team](t3-thread://v1/mcp:58780b90-ecc1-4e53-9eaa-4156ab15afcf), orderready. Tobias wants BOTH builds on Linux: native Linux ELF and cross-compiled Windows PE, no Windows-host compilation/CI/VM-build fallback. No API/Tokio bridge or Orderready integration/rewrite plan. A Windows .exe is compile proof, not Windows runtime proof; runtime checks remain Tobias's staging responsibility.

- FINAL independently reviewed proof COMPLETE for unmodified Longbridge gpui-pre/platform0.3.8: ALL builds on Linux, actual nativeLinuxELF and cross-compiledWindowsDEBUGPE, both cleanCargo0. WindowsRELEASEcrossbuild FAILS actualCargo101: Windows-host-gated FXC shader generation leaves missing shaders_bytes.rs/emptyOUT_DIR. DebugPE depends on source shaderpaths, NOTportable/distributable/runtime-qualified. No Windowsnativefallback/CI/VM/fork/patch/pipelinechange. Receipts/reviews/binaries `~/.cache/gpui-dual-compile-20261011/{result.md,review/round2-terminal-release-report.md}`, owningMarkdown `04ba2d4` in `/home/tb/.local/share/orderready/wt/gpui-dual-compile-proof/docs/gpui-dual-compile-proof.md`. CoS final artifact verification COMPLETE: ELF/PE bytes rehashed/headerschecked, clean input/package/command provenance and0/0/101 exits/budget/terminalunits align. No mismatch blocks closure; team/verifier settled. Original buildproof complete, no Windowsrelease/runtime claim.
- All compileunits terminal/emptyControlGroup; solecompileowner/two independentSol-high reviews completed/noqueuedwork. Budget298.928367/3600sadmitted; one-slot/6GiB/CPUQuota200%/twojobs/globalcaps preserved. Unmodifiedproof closed; approvedlocalfix phase uses remaining3301.071633sof original3600 admittedbudget, one2-job/6GiB/200% shared-slot compiler. No Windowsruntime/VMoperation authorized.
- Previous raw ancestor `MemoryHigh - MemoryCurrent` guard blocked on inactive file cache despite available host RAM. CoS overengineered admission; superseded replay prerequisite with real host availability and one bounded job. No generic admission framework, cache clearing, cap increase or killing other work. Diagnosis: `~/.cache/cos-gpui-memory-20261011.md`.
- Approvedlocal shaderfix is TOOL-BLOCKED: bounded inventory foundnoWine/authenticMSFXC/nativeD3DCompilerDLL; existingxwinonlyheaders/importlibs. Newmaterialroute asksTobias: Linuxbuild-timeWine + officialSDKx64FXC/matchingnativeDLL, conditionalofficiallicense review beforeacceptance/execution. Publicdocs/terms/metadata audit active (`cos-gpui-official-fxc-license-info-20261011-r1`), NOpackage/dialog/payloaddownload started; version/hash/terms notestablished. Localbuild.rs-only targetgatepatch prepared at `fxc-cross-patch/`, SHA854082bc36f83849ea11409f95aa25a1e9cf504bbb946f0b3dea369ac2329bf8; independentSol-high patchreviewrunning. NoCargo/newbudget;3301.071633sremaining, slotsfree/noconflict/notreservedwhiletoolgap. Registry/originalproof/studyindex untouched. Target-driven generation preserves HLSL/FXCbytecode/rendererse mantics, explicitLinux-side shadercompiler/tool/runner provenance; newcompiler/renderer/fork/pipeline/licensing choice mustreturn. Goal actualLinux-crossRELEASEPE with embeddedshaders/no registry-source dependency, independentreview and exactpatch/artifact proof. No upstreamcontact/publication orproductionrewrite authorized. Windowsruntime remainsuntested.
- Preserve `/home/tb/.t3/worktrees/orderready/spike-gpui-import-gui` AND its Git index: eleven original source/lock files remain staged/uncommitted under accepted static blockage. Original report `151e8b3` is an unqualified study, not platform-impossibility proof. Preserve `~/.local/share/orderready/gpui-spike/` receipts. No VM operation, production rewrite or deployment.

### Orderready P2 migration

[Owner](t3-thread://v1/mcp:99ab7733-ab01-4241-bfc9-7f7b5f33c579). Foundation/RF and platform AUTH merged; no deployment. Local `tools/or test --full` is the gate, no hosted CI.

- AUTH consumer resumed after Tobias approved ONLY five mechanical required-environment updates in frozen constructors/wire fixtures. Preserve every business assertion and migration obligation; no suite deletion, optional fallback or assertion relaxation. P2 owns patch, independent review, exact-head green and integration. Prior `93cd645` was reviewed but not aggregate-green; repo evidence `omarchy-notes/evidence/p2-platform/auth-consumer/`.
- C4C eight public recovery/lifecycle workflows and scoped OIP fixes MERGED PR2/main `67af023`. CoS spot-check VERIFIED merged/reviewed tree `2c3259d73ace`, exact-source review, all24 retained outputs byte-identical, reviewed/full and merged/cached gates; no substantive mismatch, verifier settled. PARTIAL migration: all36mutation obligations/tenhistoricalC3rows retained, premerge56kills NOT finalhead counts. Evidence notes `1c5d9df`, `omarchy-notes/evidence/p2-backend/c4c-r3-resume/`.
- INF `5d26489` integration HELD for reviewed P1: nearest agents24.5GiBhigh ignores tighter outer16.8GiBhigh/21.4GiBmax. CoS AUTHORIZED safety correction: each governing ancestor's finitehigh/max and OWNcurrent/headroom, retain existingrawcache/slots/reserve/caps. P2 owns patch/regressioncase/independentreview/exact-headgate/integration; historicalmanualoutergreen isn't changed-selector qualification. C4B qualification/consumerbundleproof still depend onINF; C3 positive implementation/review active.
- Historical C3 `9f670af` remains unqualified: old37-file argv unrecoverable, 58 routed executable obligations retained. Approved NEW source-grounded scope includes successful adapter/dependency owners; fresh exact-head inventory/control/final counts, no fabricated replay/dead-code waivers or higher budgets. Eleven positives split times/catalogue; current73-path preparation is not qualification.
- Immutable upstream command bundle delivered and consumer hash verified; consumer parity/integration is pending behind INF. Keep old harness until proof passes. Private bundle details remain in owning handoffs.
- Approved follow-on: pairing approval inside Import GUI, replacing operator `machine create` after shipping. Windows VM remains out of scope.
- Shared three-slot admission remains; GPUI compileunits are terminal, its temporary priorityreservation may release after ownercoordination. P2 supplied checkpoint `evidence/p2-capacity/checkpoint.md`:1819716/9fbe0cfd belongs oldGPUIOrderreadywatch;2028624/4bb9473c Stepkittoolswatch;2298200C4Bwatch;2038653gone/nohistoricalcheckpoint recovered. Verifier now finds only2298200stilllive/C4Bconfirmed;1819716/2028624gone, their mappings historical;2038653stillgone/nohistoricproof. Revalidate PIDs at actualrestart, notglobalclearance; no kills or newproof inferred.

### Agent-context research

[Standing owner](t3-thread://v1/mcp:d7502e10-2088-42ce-9c31-6ff118b57931), pi-workspace-view. NEVER settle owner. Tobias approved disabling v3 while continuing context-construction experiments.

- V3 config/persistence disable and fresh SDK behavior are complete: dotfiles PR7 `bf2ca78`; live extensions=[]; stock native/nested reads reach context unmodified. Fresh proof `~/.cache/pwv-disable-proof/receipt.json` uses deterministic provider responses, zero provider requests, NOT performance evidence. Existing sessions untouched; prototype uninstalled; repo/package retained.
- Reviewed proposal at `f1b384c`, `results/context-checkpoint-proposal-2026-10-11.md`: stock Pi vs one default-format checkpoint at128k projected context, preserving stock reserve/output/tail/recovery. **HOLD for top-level Opus design after confirmed quota recovery. Neither readiness implementation nor trial authorized.**
- Proposed ceiling20 subscription executions, 004/009 ×2 arms ×5 reps; first004 pair conditional, initially serial/resource-admitted. Must establish failing controls/passing oracles, full004 UI behavior and correctness-only evaluation without normal judge. Existing compaction observations don't prove full-task payback; prefix churn unmeasured and real sample not stock baseline.
- Measure all failed-attempt, summary, warming, cached/uncached/output and retry costs per objectively passing task; separate warm-up/steady runs and compaction recovery. No fixed97% cache target, paid API spend or new global installation.
- Weekly `cos-agent-context-weekly-1` remains bound here, Monday09:00 CEST; next2026-10-12. No v3 re-enable or immediate old-experiment rerun.

### Dotfiles restoration owner

[Team](t3-thread://v1/mcp:87e88c75-f093-4c7a-9817-97a135c52fe5). Overhaul, v3 disable and model-policy tasks complete with independently aligned receipts. Desktop/freerdp/Stremio/Taildrop applied; serv01 source unchanged. No broad task active.

- Completion indices under `~/.cache/agent-tmp/`: `overhaul-completed-receipt.json`, `pi-v3-disable-receipt.json`, `opus-top-level-receipt.json`. Source/gates/live facts checked; not cryptographic execution attestations.
- Remaining: T3 environment adoption, serv01 SSH authorization, restic restoration; then NAS mount/T3 backup restoration. Resume existing owner only for a necessary authorized step. No duplicate dialogs or secrets in chat.

## Needs Tobias

- GPUI shaderfix: approve Linuxbuild-timeWine + authenticofficialMicrosoftSDKFXC/nativeD3DCompilerDLL, conditionallicense review beforeacceptance/execution? Recommendyes, preservingexistingshaderformat; noapplicationruntime/WindowsVM/nativehost/fork changes. SDKversion/hash/terms stillbeingresearched; noinstall/download authorized yet. GPUIteam waits ontoolroute, patchreviewcancontinue.


- T3 restart authorization AFTER CoS establishes cross-team checkpoint/readiness. Service still predates TMPDIR/askpass environment; completion of dotfiles alone isn't safety. GPUI compileunits are now terminal; other hosted work still needs ownership/recovery confirmation.
- Serv01 SSH authorization and private restic password restoration. Use private secret-entry tools, never chat. NAS/T3 backup restoration waits on these prerequisites.
- Decision-log review: seven entries marked **[review]**; unmarked entries clear as right calls unless Tobias objects. Distill lessons and delete reviewed entries.

## Watch and hypotheses

- Don't resurrect admission theory before this isolated GPUI compile. General cache-aware scheduling safety remains unproven. Three historical OOM counters don't establish three separate new incidents; another confirmed OOM needs machine-level scheduling diagnosis.
- Geometry team is settled at `d114b6f`; PR42 parked. Approved source-faithful StepKit B still lacks generic material-validity proof and atomic extraction. Future qualification needs a new brief from repo contract/ADR0005 and `~/.cache/sg-b-qualification/qualification.md`; no native adapter/boundary authorized.
- T3 nightly timer updates service, not desktop AUR package. Desktop updates through dotfiles bootstrap with app/agents stopped or working Omarchy update; tell Tobias when app lags. No restart during live work.
- Agent TMPDIR is configured on disk but needs T3 restart. Workspace owner holds post-round pnpm-store cleanup; confirm no tmp workspaces before removing `/tmp/.pnpm-store`. Global limits are MemoryHigh55%/MemoryMax70%.
- Compaction settings verified on disk: Opus433K, Haiku100K, no Sonnet override. Loaded-session behavior/cache effect unproven; no Claude quota test now.
- Old CoS failures were context-handoff guards, not demonstrated Pi startup defects. Fresh bounded handover solved this; prior isolated Pi start failure remains isolated.
- Starting an idle turn may kill prior agent-scope detached work: keep long jobs in independent immutable user units. That earlier workspace incident remains a hypothesis; don't start housekeeping turns over live detached jobs.
- Bare chromium uses Tobias's real profile; playwright-cli is safe. Expected test aborts need LimitCORE=1 to suppress crash toasts; another test-tool incident should be fixed at agent-slice owner, not repeatedly per tool.
- Claude usage accounting was independently verified: `~/.cache/claude-usage-20261011/`. Large coordinator histories/request counts, not cache-miss storm; subscription quota attribution unknowable. Retain Opus leadership/Sol implementation-review; reduce coordination/context waste instead.
