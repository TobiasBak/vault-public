# Irreducible codebase documentation

Code owns implemented behavior; tests and examples express and check intended observable behavior. Prose should retain what these cannot express reliably, not copy the implementation. Spend the saved maintenance and context budget on clearer names, types, APIs, boundaries, state models, tests, examples, and UI language.

Manifests, named scripts, task runners, and CI own ordinary setup and validation commands. Where comments are allowed, put non-obvious invariants or rationale on the owning definition, where a searching agent will find them. Usually remove prose that narrates control flow, repeats signatures, inventories changing files, or copies executable command configuration; it will drift.

## Comments as precedent for agents

Agents may treat an explained workaround as permission to copy it. Fix an avoidable compromise through the boundary, data structure, API, or a check rather than justifying it in a comment.

This is why [[Tobias's developer preferences|Tobias favors a no-comments rule]] for agent-written code. See [[Agentic engineering#Constrained codebases for low-context contributors]] for making the easiest change follow the design.

## What prose should preserve

Keep documentation for:

- **Rationale and tradeoffs:** why a design was selected, which alternatives were rejected, and what would justify revisiting it.
- **Invariants and hazards:** constraints whose importance is not visible from ordinary execution.
- **Domain language:** intended concepts, distinctions, and preferred terms that several implementations must share.
- **Navigation:** short maps to authoritative modules, decisions, tests, and operational artifacts.
- **External contracts:** user expectations, organizational constraints, integration behavior, and procedures that cannot safely live in code.

A glossary should constrain implementation. Use one preferred term per concept across names, types, APIs, tests, and UI copy; explain overloaded terms and boundary-specific meanings. Model states and transitions structurally. If the glossary and code disagree, repair the domain-model drift rather than adding another explanation.

When semantics change, resolve vague or overloaded terms against real boundary cases and current code. A definition that cannot distinguish those cases cannot yet constrain implementation.

Use an ADR when a decision is hard to reverse, surprising without context, and reflects a real tradeoff. Record the choice and why; add status, alternatives, or consequences only when future maintainers need them.

## Review test

Ask:

1. Could code structure, naming, types, tests, examples, manifests, named scripts, task runners, or CI express this more faithfully?
2. Does the prose carry rationale, semantics, navigation, an invariant, or external context that code cannot?
3. Which artifact is authoritative, and are all others clearly aids or pointers?
4. Does implementation consistently use the documented domain language?
5. Can a new human or agent reach the right authority through a short link chain?

Use consistent terms in context, filenames, symbols, types, tests, and errors so each leads to the next authority. Clear code and short navigation avoid a parallel manual. [[Search-driven code discoverability]] covers retrieval; [[Agent context engineering]] uses this code-and-prose authority boundary.
