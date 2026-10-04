# Design for the next agent

Assume the next contributor sees only the files it opened, copies the nearest example, and takes the shortest path that compiles. Prefer the design where a change that looks right from one file is right for the whole repo.

## Design it twice

For a material shape decision, sketch at least two structurally different candidates before choosing: whole shapes, not point fixes inside one. Write the caller's usage first and derive types and signatures from it. Screen each candidate against the red flags, then prefer the one that hides more behind a smaller public surface. If implementation keeps producing the same workaround, escape-hatch types, or callers that must know internal rules, throw the sketch out and redesign from the new constraints instead of patching it.

## Red flags

Each is a reason to revise or reject a shape.

- **Shallow module:** a large interface hiding little. Callers coordinate several methods for one operation, options expose internal stages, or learning the interface doesn't spare learning the implementation. A deep module concentrates capability; a deep call chain scatters it.
- **Information leakage:** several modules depend on one internal decision, so changing it needs coordinated edits. Re-exported wire or storage types are leakage; parse external data into domain types behind the interface.
- **Temporal decomposition:** modules split by execution order (load, validate, transform, save) that repeat one representation and its invariants across boundaries. Group by the knowledge owned.
- **Pass-through method:** forwards the same arguments to the same shape, adding a layer without policy, adaptation, or abstraction. Remove it or move the responsibility.
- **Split ownership:** more than one module writes the same state or keeps its own copy. An agent editing one writer can't see the others. One owner; others read or ask.
- **Two ways to do one task:** agents copy whichever they find first, so every way keeps gaining callers. Keep one, migrate callers, delete the rest in the same change.
- **Importable internals:** whatever compiles becomes interface. Make outside imports of internals fail the build.
- **Hand-synced list:** the same items listed in several places. Derive the others from one list, or fail the build when they disagree.

Source: Lauren Tan's pstack `architect` skill and its `design-red-flags.md` (2026-10-03), after Ousterhout's *A Philosophy of Software Design*.
