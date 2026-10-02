# Documentation and naming for agents

Code owns behavior; tests and examples express intended behavior. Prose keeps only what those can't express. Spend the saved effort on names, types, boundaries, and tests.

## What prose keeps

- **Rationale:** why this design, which alternatives were rejected, and what would justify revisiting it.
- **Invariants and hazards** that ordinary execution doesn't make visible.
- **Domain language:** one preferred term per concept across names, types, APIs, tests, and UI. When glossary and code disagree, fix the model drift. A definition that can't separate real boundary cases can't constrain anything yet.
- **Navigation:** short maps to the authoritative module, test, ADR, or runbook.
- **External contracts:** integrations, organizational constraints, user expectations.

Everything else drifts. That includes control-flow narration, repeated signatures, file inventories, and copied commands. Setup and validation commands belong in manifests, scripts, task runners, and CI. Add a prose route only when agents repeatedly choose wrong and a clearer executable entrypoint can't prevent it.

Write an ADR only for decisions that are hard to reverse, surprising, and real tradeoffs. Record the choice and the reason.

**Comments:** Tobias prefers a repo-wide no-comments rule enforced by lint or CI. A comment explaining a workaround teaches the next agent to copy it. Fix the boundary or add a check instead. Rationale goes in linked docs.

## Code as a search surface

Agents navigate by lexical search, narrow reads, and refined searches. Plain search has no reverse symbol index and gets noisy around generic names, aliases, barrel files, and methods.

- Give public and cross-cutting concepts distinctive multiword names, so a search returns the definition, callers, and tests rather than hundreds of hits. A 2026-07-21 scan of 371 Python files found exact-name uniqueness rising from 26% for one-word names to 79% for three words and 85% for four. Distinctive is the goal, not long; let directories scope private names like `service.py`.
- Use one spelling per concept everywhere. Synonyms split retrieval.
- Name tests after the behavior or source they protect.
- Use precise signatures and domain types: they answer usage questions without opening implementations, and compiler errors point to the next authority. `Any`-shaped boundaries force multi-file inference.
- Delete obsolete paths. A path that must stay but must not be used needs a locally visible marker.

Repository context files should be query maps: preferred terms, ownership boundaries, the authoritative module per concept, and hazards that are unsafe to discover late. Their terms must also appear in filenames, symbols, and errors so the trail continues once the context file leaves the window. Root guidance points to narrower context; it doesn't preload subsystems.

Modem's [experiments](https://modem.dev/blog/how-coding-agents-read-your-code) found that weaker models gain most from discoverable code. They changed naming, typing, comments, and structure together, so no single rule's effect is isolated.
