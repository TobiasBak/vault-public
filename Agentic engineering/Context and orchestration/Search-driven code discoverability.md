# Search-driven code discoverability

Coding agents usually navigate repositories through a loop of lexical search, narrow reads, and refined searches. Code, filenames, types, tests, and context documents therefore form a retrieval surface as well as a human design surface. A dependency graph or import can point from a caller to a definition, but plain search has no reliable reverse symbol index and becomes noisy around generic names, aliases, barrels, and object methods.

## Build useful search handles

- Give public or cross-cutting concepts distinctive names. A name should retrieve mostly the intended definition, callers, and tests rather than hundreds of unrelated candidates.
- Use one preferred spelling per domain concept across code, types, APIs, tests, context documents, and user-facing language. Synonyms split retrieval and local aliases hide reverse references.
- Let directories supply scope for private implementation names. Global uniqueness does not justify mechanically expanding every local `service.py` or helper into a fully qualified phrase.
- Use concept-named modules when a file otherwise becomes a large grab-bag. Name tests after the source or behavior they protect so a definition search reaches the best executable evidence.
- Prefer precise signatures and domain types. They can answer usage questions without opening implementations, and compiler errors produce concrete names that lead the agent to the next authority. An `Any`-shaped boundary often forces multi-file inference.
- Where repository policy allows comments, put non-obvious invariants or rationale on the owning definition, not a narration of control flow. Under [[Tobias's developer preferences|Tobias's no-comments policy]], use enforceable structure and short linked documentation instead. See [[Irreducible codebase documentation]].
- Remove obsolete paths when possible. If a retained path must not be selected, make that status explicit and locally discoverable.

Longer is not automatically better. Optimize for a stable, discriminating phrase that matches the language a task, error, domain document, or reviewer will use. Over-specific names increase reading friction without adding retrieval value.

## Repository context as a query map

Repository context should help an agent formulate the right searches and recognize the authority it reaches. Keep it compact:

- define preferred domain terms and important distinctions;
- name ownership boundaries and the authoritative module, test, ADR, or runbook;
- record non-obvious hazards and invariants that would be unsafe to discover late;
- provide a short map from shared concepts to narrower package context;
- avoid implementation inventories, duplicated signatures, and prose copies of control flow.

A context file does not compensate for opaque code. Its terms should appear in filenames, symbols, types, tests, errors, and UI language so the route continues after the context leaves the working set. Root guidance should point to narrower authorities rather than preload all subsystem detail.

Ordinary setup and validation commands belong in manifests, named scripts, task runners, and CI. Add a prose route only when representative agents repeatedly make a meaningful wrong choice that clearer executable entrypoints cannot prevent. Encode the applicability cue and owner rather than copying commands. [[Concise AGENTS.md for capable coding agents#Placement and authority]] owns the instruction-placement decision.

## Reviewer-agent context

Distinctive symbols, consistent domain terms, and behavior-named tests help a reviewer move from the diff to affected callers and independent evidence. [[Context-sensitive code review#Initial contract and map]] owns the reviewer's inputs, outward search, evidence requirements, and stopping criteria.

## Local evidence

A 2026-07-21 scan of 371 production Python files in one application found exact-name uniqueness rising from 26.3% for one-word public top-level definitions to 79.1% for three-word and 85.1% for four-word definitions. Filename-stem uniqueness rose from 28.6% for one word to 100% for three words. This supports distinctive multiword names as cleaner lexical handles, not a blanket minimum length.

This pattern resembles Modem's broader bundled experiments in [How coding agents read your code](https://modem.dev/blog/how-coding-agents-read-your-code): weaker readers benefited most from discoverable code, while stronger readers often improved modestly. Modem's public results change naming, typing, comments, and structure together, so they do not establish the effect of each rule independently.

Related: [[Agent context engineering]], [[Irreducible codebase documentation]], [[Concise AGENTS.md for capable coding agents]], [[Subagent delegation]].
