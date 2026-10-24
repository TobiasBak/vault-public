# Verification in under one minute

Tobias's goal: an agent can verify a meaningful edit in **under 60 seconds**, including static checks, compilation and the necessary behavioral tests. Optimize time to a trustworthy verdict for both a single agent and agents sharing limited hardware. Higher fleet throughput alone is not success.

Faster staging and production qualification is also a goal. Measure those complete paths separately; a fast development verdict does not satisfy missing release obligations. The [delivery policy](../tobias/preferences.md#delivery-and-releases) still governs which checks run at each boundary. This is a target, not an achieved result or a decision to build a particular architecture.

recheck-after: 2027-01-24

## Measure the whole wait

- Time verification request to returned verdict, including launcher preparation, admission, local locks, static checks, compile/link, test setup, execution and evidence publication. Also record last relevant edit to verdict availability so watchers and precomputation cannot hide work outside the timer.
- Use real source-content changes under the normal warm-workspace workflow. Separate source edits, unchanged-tree cache hits and cold toolchain/dependency changes. A cached green response or mtime-only rebuild does not establish edit-loop speed.
- Report workload, input identity, cache state, concurrency, process boundary and executed obligations. Compare solo latency with representative multiagent load; include tail latency and failure-detection latency, not just averages or successful runs.
- Follow the critical path. Summed parallel job time is neither wall time nor a saving. Moving a wait into another queue or preparation step does not shorten verification.
- Preserve checks and independent expectations. The minute is a performance goal, not a timeout that turns incomplete work into success. A complete, wrong result should fail promptly; genuinely pending work still needs its completion evidence.

## Build on shared warm state

Build on gah's copy-on-write workspaces, inherited build outputs and stable source paths rather than creating another workspace provisioner or target copier. The repository owns incremental builds and product verification; the kernel shares host CPU and memory, with no host admission (Tobias, 2026-10-23). See the [feedback optimization loop](../skills/theodore-kaczynski-nullifier/references/manifest.md) for established mechanisms and [remote execution boundaries](../hardware/agent-era-dev-machine.md#make-extra-machines-execute-work).

Share immutable preparation, compatible artifacts and exact-input proofs; join identical in-flight work. Keep each execution's mutable state isolated. Evaluate sharing by how much sooner an individual agent gets its verdict under load, not how many jobs can be admitted. More agents should not imply proportionally more compiler processes, test environments or copies of the same work.

Do not build a verification runner framework in every repository. Share execution and evidence mechanics; keep product-specific checks, required-test selection, fixtures and oracles at their product owner. Whether the shared implementation belongs in gah or a separate tool is an architectural choice, not a reason to duplicate it.

Prefer Linux scheduling runnable work over adding userspace capacity queues. Exact-key duplicate suppression and one writer per mutable build state are correctness constraints, not CPU scheduling. Do not bake existing slot counts, weights or memory estimates into a new verifier as necessities. Measure their effect and any memory-safety need before retaining, changing or removing them at the host owner. Hardware limits are not an explanation for uninvestigated waits or wasted compute.

## Parked: Rust UI development like a game engine

Tobias does not want to explore live Rust UI development as the route to the verification-latency goal. UI testing and browser automation are not established critical-path bottlenecks for this effort. Retain this research as background, not work to start; required behavioral tests still follow the changed contract and delivery policy.

The idea is to keep the native application and an interesting UI scenario alive while delivering changed Rust code at explicit reload boundaries. Preserve or reconstruct valid state instead of rebuilding, relaunching and navigating back after every edit. This is actual code hot-patching, not necessarily a new presentation language.

[Dioxus Subsecond and ThinLink](https://github.com/DioxusLabs/dioxus/blob/main/packages/subsecond/subsecond/src/lib.rs) provide a concrete precedent: changed code, object-file differences, dynamic dependency linking and jump-table dispatch. The source inspected on 2026-10-21 documents tip-crate-only patching, thread-local restrictions and incompatible struct layouts requiring state reconstruction. Do not assume arbitrary workspace edits, live callbacks or native handles survive a patch safely.

Any future pilot must measure a real UI change reaching its behavioral and rendered verdict, not merely the patch loading. Preserve ordinary exact-build and native-platform qualification.

## Research directions for shared verification

These are hypotheses to test against the latency goal, not an implementation mandate:

- **Share execution across different candidate patches.** [AccMut](https://github.com/wangbo15/accmut) and [variational execution](https://www.cs.cmu.edu/~ckaestne/pdf/oopsla18.pdf) share compatible computations across program variants. Explore a family of actual agent patches together, separating work where implementations or values differ and retaining individual verdicts. Conditional-state overhead and early divergence can erase the benefit; ordinary caching and a combined executable do not provide this sharing by themselves.
- **Defer native code generation.** [Sulong](https://www.graalvm.org/latest/reference-manual/llvm/) interprets LLVM bitcode before compiling hot regions; [LLVM ORC](https://llvm.org/docs/ORCv2.html#laziness) supports lazy native materialization. A tiered development runtime could return evidence before compiling every candidate body. Rust frontend work, versioned types and native interoperability remain constraints.
- **Version executable knowledge.** [Unison](https://www.unison-lang.org/docs/the-big-idea/) identifies definitions and dependencies by content; [Julia world ages](https://docs.julialang.org/en/v1/manual/worldage/) give running tasks a defined view of code versions. These suggest shared compiler knowledge with explicit execution-world identities, rather than silently replacing code underneath live callers.
- **Branch scenarios, not whole test campaigns.** [Antithesis](https://antithesis.com/docs/product/debugging/advanced_multiverse_debugging/moment_branch/) explores alternate futures from recorded moments. [FoundationDB](https://apple.github.io/foundationdb/testing.html) runs production implementation in a deterministic simulated environment. Reuse a scenario prefix only when changed code could not have affected it. Virtual time skips waiting, not CPU work; simulation does not establish native input, rendering or platform behavior it excludes.

Use the [scout-first experiment loop](autoresearch.md#fast-loops-first-tobias-2026-10-12). First show that a proposed mechanism removes measured work on a real edit while preserving its verdict. Broader compiler/runtime changes need Tobias's architectural decision. Keep project measurements, designs and implementation plans in their owning repositories, not this note.
