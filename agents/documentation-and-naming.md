# Documentation and naming for agents

Code owns behavior; tests and examples express intended behavior. Prose keeps only what those can't express. Spend the saved effort on names, types, boundaries, and tests.

## Where knowledge lives

- **Rationale:** first in a check's failure, a product refusal, or the authority line an example test prints on failure. A one-off decision no program can check gets a `Why:` trailer in the final landed commit. Other decisions, rationale and ADRs belong in issues or PRs, not a docs tree.
- **Invariants:** types and checks. A consequential hazard that cannot be checked gets one root `AGENTS.md` boundary line.
- **Domain language:** one preferred term per concept across `GLOSSARY.md`, names, types, APIs, tests and UI. The glossary holds terms only and changes with the code; the [domain-modeling skill](../skills/domain-modeling/SKILL.md) owns it.
- **Navigation:** the test runner's list of behavior-named tests. No handwritten feature map or file inventory.
- **External contracts:** the smallest machine-checked published form its outside consumer needs, at an exact gate-listed path.

Repository prose stays in root `AGENTS.md`, skills, CLI `--help`, example tests' authority lines, the glossary and those published contracts. No README or docs tree. Commands stay in executable owners; skills keep only task steps the CLI cannot perform. See [Theodore's context ownership](../skills/theodore-kaczynski-nullifier/references/agent-context.md).

**Comments:** Tobias prefers a repo-wide no-comments rule enforced by lint or CI. A comment explaining a workaround teaches the next agent to copy it. Fix the boundary or add a check instead; preserve the reason at its owner above.

## Code as a search surface

Agents navigate by lexical search, narrow reads, and refined searches. Plain search has no reverse symbol index and gets noisy around generic names, aliases, barrel files, and methods.

- Give public and cross-cutting concepts distinctive multiword names, so a search returns the definition, callers, and tests rather than hundreds of hits. A 2026-07-21 scan of 371 Python files found exact-name uniqueness rising from 26% for one-word names to 79% for three words and 85% for four. Distinctive is the goal, not long; let directories scope private names like `service.py`.
- Use one spelling per concept everywhere. Synonyms split retrieval.
- Name tests after the behavior or source they protect.
- Use precise signatures and domain types: they answer usage questions without opening implementations, and compiler errors point to the next authority. `Any`-shaped boundaries force multi-file inference.
- Delete obsolete paths. A path that must stay but must not be used needs a locally visible marker.

Root `AGENTS.md` provides orientation and authority boundaries; executable maps and names provide detailed navigation. Use the same terms in filenames, symbols and errors so retrieval still works after the context file leaves the window. Do not preload subsystem inventories or add nested instruction files.

Modem's [experiments](https://modem.dev/blog/how-coding-agents-read-your-code) found that weaker models gain most from discoverable code. They changed naming, typing, comments, and structure together, so no single rule's effect is isolated.
