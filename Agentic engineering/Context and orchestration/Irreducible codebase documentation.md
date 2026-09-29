# Irreducible codebase documentation

Code is authoritative for implemented behavior; tests and examples document and check intended observable behavior. Documentation should preserve knowledge they cannot express reliably, not maintain a prose copy of the implementation. Use the saved maintenance and context budget to make names, types, APIs, module boundaries, state models, tests, examples, and user-facing language more legible.

Tests and examples demonstrate observable behavior. Manifests, named scripts, task runners, and CI own ordinary setup and validation commands. Comments should capture a local invariant or rationale that is not evident from mechanics and sit on the definition that owns it. This is also the location a search-driven agent is most likely to read. Prose that narrates control flow, repeats signatures, inventories changing files, or copies executable command configuration will drift and should usually be removed.

## Comments as precedent for agents

Agents can treat a comment explaining a workaround as permission to keep it and copy it elsewhere. Before explaining an avoidable compromise, fix the boundary, data structure, or API, or add a check. A comment is no substitute for that work.

This is why [[Tobias's developer preferences|Tobias favors a no-comments rule]] for agent-written code. He wants to stop agents from justifying bad patterns that later agents will copy. [[Agentic engineering#Constrained codebases for low-context contributors]] covers making the easiest change follow the intended design.

## What prose should preserve

Keep documentation for:

- **Rationale and tradeoffs:** why a design was selected, which alternatives were rejected, and what would justify revisiting it.
- **Invariants and hazards:** constraints whose importance is not visible from ordinary execution.
- **Domain language:** intended concepts, distinctions, and preferred terms that several implementations must share.
- **Navigation:** short maps to authoritative modules, decisions, tests, and operational artifacts.
- **External contracts:** user expectations, organizational constraints, integration behavior, and procedures that cannot safely live in code.

A glossary should constrain implementation rather than merely explain it. Use one preferred term per concept across names, types, APIs, tests, and UI copy. Make overloaded terms and boundary-specific meanings explicit. Represent meaningful states and transitions structurally. A disagreement between glossary and implementation is domain-model drift, not a reason to add another explanatory layer.

When domain semantics change, resolve vague or overloaded terms against concrete edge cases and current code before treating the glossary as settled. A definition that cannot distinguish realistic boundary cases is not yet precise enough to constrain implementation.

Use an ADR when a decision is hard to reverse, surprising without context, and the result of a real trade-off. Record the decision and why; add status, alternatives, or consequences only when they carry information future maintainers will need.

## Review test

Ask:

1. Could code structure, naming, types, tests, examples, manifests, named scripts, task runners, or CI express this more faithfully?
2. Does the prose carry rationale, semantics, navigation, an invariant, or external context that code cannot?
3. Which artifact is authoritative, and are all others clearly aids or pointers?
4. Does implementation consistently use the documented domain language?
5. Can a new human or agent reach the right authority through a short link chain?

Compact semantic anchors and navigation improve retrieval; self-explanatory code lets an agent continue without loading a parallel manual. Use the same preferred terms in context, filenames, symbols, types, tests, and errors so each artifact provides a route to the next authority. [[Search-driven code discoverability]] covers this lexical retrieval surface. This is the code-and-prose authority boundary used by [[Agent context engineering]].
