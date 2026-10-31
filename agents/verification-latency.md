# Verification in under one minute

Tobias's goal: an agent can verify a meaningful edit in **under 60 seconds**, including static checks, compilation and the necessary behavioral tests. Optimize time to a trustworthy verdict for both a single agent and agents sharing limited hardware. Those agents are independent top-level agents working their own tasks, not one task fanned out across workers ([subagent delegation](subagent-delegation.md)); higher fleet throughput alone is not success.

Faster staging and production qualification is also a goal. Measure those complete paths separately; a fast development verdict does not satisfy missing release obligations. The [delivery policy](../tobias/preferences.md#delivery-and-releases) still governs which checks run at each boundary. This is a target, not an achieved result or a decision to build a particular architecture.

recheck-after: 2027-01-24

## Measure the whole wait

- Time verification request to returned verdict, including launcher preparation, exclusive-resource locks, static checks, compile/link, test setup, execution and evidence publication. Also record last relevant edit to verdict availability so watchers and precomputation cannot hide work outside the timer.
- Use real source-content changes under the normal warm-workspace workflow. Separate source edits, unchanged-tree cache hits and cold toolchain/dependency changes. A cached green response or mtime-only rebuild does not establish edit-loop speed.
- Report workload, input identity, cache state, concurrency, process boundary and executed obligations. Compare solo latency with representative multiagent load; include tail latency and failure-detection latency, not just averages or successful runs.
- Follow the critical path. Summed parallel job time is neither wall time nor a saving. Moving a wait into another queue or preparation step does not shorten verification.
- Preserve checks and independent expectations. The minute is a performance goal, not a timeout that turns incomplete work into success. A complete, wrong result should fail promptly; genuinely pending work still needs its completion evidence.

## Explain why the hot work runs

Attribute host load to workloads and their descendants before tuning a hot function. An LLVM-heavy profile locates compiler cost; it does not establish that those compilations were necessary. Trace the operation that scheduled or invalidated the work. See the measured [Cargo context preservation case](../software/cargo-target-cache.md#measured-preservation-result) and the [benchmark checklist](../skills/benchmark-checklist/SKILL.md).

## Build on shared warm state

Build on gah's copy-on-write workspaces, inherited build outputs and stable source paths rather than creating another workspace provisioner or target copier. The repository owns incremental builds and product verification through the language's own build tool and test runner, with thin glue. The kernel shares CPU with no host admission (Tobias, 2026-10-23); memory is capped per heavy job, and nothing queues behind a host-wide lock. The [feedback speed reference](../skills/theodore-kaczynski-nullifier/references/manifest.md) owns those rules; see also [remote execution boundaries](../hardware/agent-era-dev-machine.md#make-extra-machines-execute-work).

Evaluate sharing by how much sooner an individual agent gets its verdict under load, not how many jobs can be admitted. More agents should not imply proportionally more compiler processes, test environments or copies of the same work. Exact-key duplicate suppression and one writer per mutable build state are correctness constraints, not scheduling. Hardware limits are not an explanation for uninvestigated waits or wasted compute.

## Measured: shared verification tooling did not pay (2026-10-31)

verify-at-home (vah) is a shared execution and input-keyed evidence tool: 8,750 lines and a 22-requirement spec, built 2026-10-21 to 2026-10-30. Over its first 7 days of run reports (3,816 runs, 28.5 h wall):

| Measure | Value |
|---|---:|
| Jobs executed / reused inside runs | 17,990 / 323 (1.8% reuse) |
| Work time | 24.4 h |
| Of which Orderready `xtask` tests (the verification pipeline testing itself) | 16.4 h (67%) |
| Every other job family | under 0.9 h each |
| Identity and wait overhead inside vah | 1.2 h |

Nearly every execution had a distinct key, so source edits invalidated almost everything. `vah status` lookups are not logged, so reuse that skipped a run entirely is unmeasured; the tool could not show its own saving, which is the gap a trial would have closed. The same week, a no-op cached read of all Orderready verdicts took 16.2 s, one `tools/or why` 11.8 s, and the 22–30-minute gate suite drove a 7.5-hour delegate.

Conclusion: build shared verification machinery only after a [trial](../skills/theodore-kaczynski-nullifier/references/manifest.md#optimization-loop) on a real workflow shows the saving, and count its own test suite as its cost. Method: a job counts as executed when its artifacts sit in its own run directory and as reused otherwise; work time is the trace's `work` spans. Raw data stays outside the vault.

vah was retired on 2026-10-31. Orderready (`2e2eac2f7`) now runs cargo and nextest behind a thin `tools/or`, with the slow self-test suite deleted. The dotfiles pin is removed, the repository is archived, and its 46 GB of local run state is deleted. On the same one-item edit to `core/order`, the targeted domain lint and test went from 44 s to 21 s on the first run and from 22 s to 4 s warm. A full landing check that selects all 188 jobs takes 260 s. Still open: `tools/or test --affected` after that edit selects 173 jobs and takes 444 s, because every reverse dependent and all 89 corpus cases count as affected.

[Parked verification research](verification-research-parked.md) holds ideas not to start without a new measured case.
