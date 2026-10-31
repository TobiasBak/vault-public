# Parked verification research

Do not start these. They are hypotheses kept for a future measured case, not directions for current work; the [verification latency goal](verification-latency.md) is pursued through the [feedback speed rules](../skills/theodore-kaczynski-nullifier/references/manifest.md) first.

recheck-after: 2027-01-24

## Rust UI development like a game engine

Tobias does not want to explore live Rust UI development as the route to the verification-latency goal. Retain this research as background, not work to start; required behavioral tests still follow the changed contract and delivery policy. [Renderless verification](renderless-verification.md) is a separate, measured change to the proof boundary, not hot-patching research.

The idea is to keep the native application and an interesting UI scenario alive while delivering changed Rust code at explicit reload boundaries. Preserve or reconstruct valid state instead of rebuilding, relaunching and navigating back after every edit. This is actual code hot-patching, not necessarily a new presentation language.

[Dioxus Subsecond and ThinLink](https://github.com/DioxusLabs/dioxus/blob/main/packages/subsecond/subsecond/src/lib.rs) provide a concrete precedent: changed code, object-file differences, dynamic dependency linking and jump-table dispatch. The source inspected on 2026-10-21 documents tip-crate-only patching, thread-local restrictions and incompatible struct layouts requiring state reconstruction. Do not assume arbitrary workspace edits, live callbacks or native handles survive a patch safely.

Any future pilot must measure a real UI change reaching its behavioral and rendered verdict, not merely the patch loading. Preserve ordinary exact-build and native-platform qualification.

## Research directions for shared verification

These are hypotheses to test against the latency goal, not an implementation mandate:

- **Share execution across different candidate patches.** [AccMut](https://github.com/wangbo15/accmut) and [variational execution](https://www.cs.cmu.edu/~ckaestne/pdf/oopsla18.pdf) share compatible computations across program variants. Explore a family of actual agent patches together, separating work where implementations or values differ and retaining individual verdicts. Conditional-state overhead and early divergence can erase the benefit; ordinary caching and a combined executable do not provide this sharing by themselves.
- **Defer native code generation.** [Sulong](https://www.graalvm.org/latest/reference-manual/llvm/) interprets LLVM bitcode before compiling hot regions; [LLVM ORC](https://llvm.org/docs/ORCv2.html#laziness) supports lazy native materialization. A tiered development runtime could return evidence before compiling every candidate body. Rust frontend work, versioned types and native interoperability remain constraints.
- **Version executable knowledge.** [Unison](https://www.unison-lang.org/docs/the-big-idea/) identifies definitions and dependencies by content; [Julia world ages](https://docs.julialang.org/en/v1/manual/worldage/) give running tasks a defined view of code versions. These suggest shared compiler knowledge with explicit execution-world identities, rather than silently replacing code underneath live callers.
- **Branch scenarios, not whole test campaigns.** [Antithesis](https://antithesis.com/docs/product/debugging/advanced_multiverse_debugging/moment_branch/) explores alternate futures from recorded moments. [FoundationDB](https://apple.github.io/foundationdb/testing.html) runs production implementation in a deterministic simulated environment. Reuse a scenario prefix only when changed code could not have affected it. Virtual time skips waiting, not CPU work; simulation does not establish native input, rendering or platform behavior it excludes.

Use the [scout-first experiment loop](autoresearch.md#fast-loops-first-tobias-2026-10-12). First show that a proposed mechanism removes measured work on a real edit while preserving its verdict. Keep project measurements, designs and implementation plans in their owning repositories, not this note.
