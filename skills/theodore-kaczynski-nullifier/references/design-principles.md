# Design principles

These govern repository design and changes to Theodore. Operational contracts belong in the linked references. Revise the owning principle when a durable correction changes it; do not append session history.

## Aim

A fresh agent should be able to understand the system, change it correctly, establish what actually happened, and recover when reality disagrees.

## Principles

- **Trust is built into the codebase:** make the correct path obvious and known mistakes impossible or mechanically rejected through structure, types, boundaries, and checks, rather than relying on agent memory, obedience, or model strength.
- **Correctness needs independent authority:** judge existing code against the intended contract, not the intended contract against existing code; authority comes from provenance, not whether a source lives inside or outside the repository. Bad examples and tests preserving a bug do not justify more bad behavior, while real compatibility obligations need evidence from consumers or persisted data.
- **The codebase is the living documentation:** names, types, interfaces, ownership, executable checks, and behavioral cases should explain the system and how to change it.
- **The running system should be as self-explanatory as its source:** expose authoritative state and causal evidence through [inspectable outcomes, structured logs, traces, and diagnostics](runtime-outcomes.md#make-outcomes-inspectable) so another agent can establish what happened, where it went wrong, and what remains incomplete.
- **Prevent known mistakes; make unforeseen mistakes visible, contained, and repairable:** represent partial failure explicitly, bound effects, and provide [supported recovery at the effect boundary](runtime-outcomes.md#repair-at-the-effect-boundary) rather than assuming a source revert undoes them.
- **Prose must earn its place:** keep only necessary intent, external contracts, hazards, or navigation that the executable system cannot adequately express, with [one authoritative home](agent-context.md#owners) rather than a parallel description of the code.
- **Trust evidence, not completion claims:** distinguish [mechanical acceptance, observed behavior, and judgment against independent authority](black-box-tests.md#evidence-and-authority). A well-formed oracle or trailer does not prove its claim. Execution establishes what happened only for the [inputs, environment, and scope actually checked](manifest.md#3-cache-verdicts); missing or blocked verification is never success.
- **Optimize the resulting codebase, not the patch:** leave the simplest coherent system that meets the requirements, repairing ownership and removing bad examples instead of accumulating workarounds for the next agent to copy.
- **Fast feedback makes autonomy practical:** remove measured waits from the [autonomy loop](../SKILL.md#the-loop), including navigation, verification, and coordination, without weakening the guarantees that make its output trustworthy.
- **Constraints protect outcomes:** distinguish [chosen policies](../SKILL.md#repository-rules), which need Tobias's agreement to change, from mechanisms that implement them. Preserve each constraint's reason and replace a mechanism when that reason no longer holds, without losing required behavior, safety, or intent across context loss and integration.
- **A skill is a self-contained unit:** keep its instructions and required file references inside its own directory so it remains usable without the surrounding vault or other skills. Identify shared-tool and host dependencies without copying the policies they own.
- **Fix each recurring problem at its owner:** repositories [integrate shared infrastructure](../SKILL.md#ownership) instead of rebuilding it, and Theodore should shrink as tools absorb its procedures.
- **Machinery must earn adoption:** add a capability to close a demonstrated autonomy gap, remove a measured cost, or repair a broken contract, never merely because this skill describes it.
