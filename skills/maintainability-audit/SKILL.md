---
name: maintainability-audit
description: Audit source design for self-explanatory code that fresh coding agents can understand, change, and verify. Use for source maintainability reviews, not reviews of agents operating the product or general bug hunts.
---

# Agent-native source maintainability audit

How easily can a fresh coding agent make realistic changes here, with no private project memory? Tobias develops entirely through agents, so nobody repairs locally convenient choices later. This is about agents developing the source, not operating the product.

## Follow realistic changes

Choose representative changes from actual consumers, recurring work, or stated product direction. Search for the apparent owner as an agent would, then inspect the real callers, runtime wiring, edit sites, and behavioral checks.

Look for concrete friction:
- competing sources of truth, or one decision owned in several places
- misleading names or boundaries, lying abstractions, needless indirection
- coherent changes that require scattered edits
- exceptions piling up beside an uncorrected model
- tests that pin internals and block redesign

Distinguish accidental duplication from separate responsibilities and real compatibility obligations. Ground each finding in source and show how it complicates a realistic change. File size, churn, and style alone are not problems.

## Code before prose

Prefer code that explains itself through names, cohesive ownership, truthful types, explicit effects, and behavioral tests. Commands belong in manifests. When a feature needs explaining, first try renaming the misleading thing, consolidating the decision, or making the dependency explicit. Don't compensate for structural confusion with AGENTS rules or file inventories. Keep the rationale, external contracts, and domain facts that code can't carry.

## Report and fix

For each finding, give the locations, the difficulty it causes, and the simpler design when it's worth it, with material tradeoffs. Recommend no change where the structure already works. Aim for the simplest resulting system, not the smallest diff; when fixing, stay at the affected boundary.

## Verification

Verify changed behavior through the public interface or a representative real-use flow; compilation and implementation-detail tests aren't enough. Revisit the representative change to confirm the owner is easier to find and the edits are coherent. Report what was checked.
