# Design principles

These govern changes to Theodore. Keep one sentence per principle, with operational contracts in the linked references. Update the owning principle when a durable correction changes it; do not append session history.

- Theodore should shrink as shared tools absorb its procedures, leaving judgment and product-specific contracts rather than a second agent operating environment.
- Fix recurring mechanics once at their owner; repositories [integrate shared infrastructure](../SKILL.md#ownership) instead of rebuilding it.
- Optimize the named product [edit-to-main loop](../SKILL.md#the-loop), including model turns, coordination, and shared-tool waits, rather than an isolated command benchmark.
- Adopt a capability to remove a measured cost or repair a broken contract, never merely because this skill describes it.
- Preserve the product's [observable contract](black-box-tests.md#the-box) when changing implementation or verification machinery.
- Preserve a check's guarantee when its execution model changes by validating the [actual landing candidate](enforcement.md#check-targets), not assuming a staging area or hook exists.
- Warm artifacts save execution, while [verdicts certify matching inputs and qualified environments](manifest.md#3-cache-verdicts), so inherited state is never behavioral proof.
- Share evidence by its inputs, but bind [live source-reading services](control-cli.md#runs) to the workspace and namespace they actually serve.
- Required metadata and rationale must [survive composition](enforcement.md#landing-metadata), including child integration and squash, through tool contracts rather than agent memory.
- Give each policy one authority and [link to its owner](agent-context.md#owners) instead of copying mechanics that will drift.
