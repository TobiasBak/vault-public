# Search-driven code discoverability

Coding agents usually navigate repositories through a loop of lexical search, narrow reads, and refined searches. Code, filenames, types, tests, and context documents therefore form a retrieval surface as well as a human design surface. A dependency graph or import can point from a caller to a definition, but plain search has no reliable reverse symbol index and becomes noisy around generic names, aliases, barrels, and object methods.

## Build useful search handles

- Give public or cross-cutting concepts distinctive names. A name should retrieve mostly the intended definition, callers, and tests rather than hundreds of unrelated candidates.
- Use one preferred spelling per domain concept across code, types, APIs, tests, context documents, and user-facing language. Synonyms split retrieval and local aliases hide reverse references.
- Let directories supply scope for private implementation names. Global uniqueness does not justify mechanically expanding every local `service.py` or helper into a fully qualified phrase.
- Use concept-named modules when a file otherwise becomes a large grab-bag. Name tests after the source or behavior they protect so a definition search reaches the best executable evidence.
- Prefer precise signatures and domain types. They can answer usage questions without opening implementations, and compiler errors produce concrete names that lead the agent to the next authority. An `Any`-shaped boundary often forces multi-file inference.
- Put a short comment on the owning definition when a real invariant or rationale is not recoverable from mechanics. Do not narrate control flow. The valuable comment explains why an apparently reasonable change is unsafe.
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

Progressive disclosure does not require a prose route for every discoverable fact. Current capable agents can ordinarily recover standard setup and validation commands from manifests, named scripts, task runners, and CI. A separate development guide or command map earns its maintenance and retrieval cost only when representative agents repeatedly make a meaningful wrong choice and the executable surfaces cannot make the correct path obvious. When a route is justified, encode the applicability cue and owning executable surface rather than copying a command inventory or CI workflow.

## Reviewer-agent context

A fresh reviewer should receive the requirements and governing invariants, the base and candidate artifact identities, the actual diff, relevant repository context routes, and the validation contract. Do not preload the author's exploration trace or conclusions; independence is lost when the reviewer merely confirms the same narrative.

The reviewer should use the diff as a starting point, then search outward:

1. locate definitions and tests through distinctive changed symbols and domain terms;
2. search reverse references, alternate spellings, adapters, external boundaries, and retained legacy paths;
3. inspect the authoritative type, context, or rationale at each affected seam;
4. compare behavior with the best named regression or public-interface evidence;
5. report exact paths and evidence for findings, distinguish absence of evidence from a verified negative, and stop when the stated review concerns are covered.

Ask reviewers for risk-focused findings, not a generic repository tour. A review contract should name the failure classes that matter, such as contract drift, missed callers, state transitions, idempotency, external side effects, or inadequate behavioral verification. Searchability raises the chance that a bounded reviewer reaches those seams before its budget expires.

## Local evidence

A 2026-07-21 scan of 371 production Python files in one application found exact-name uniqueness rising from 26.3% for one-word public top-level definitions to 79.1% for three-word and 85.1% for four-word definitions. Filename-stem uniqueness rose from 28.6% for one word to 100% for three words. This supports distinctive multiword names as cleaner lexical handles, not a blanket minimum length.

This pattern resembles Modem's broader bundled experiments in [How coding agents read your code](https://modem.dev/blog/how-coding-agents-read-your-code): weaker readers benefited most from discoverable code, while stronger readers often improved modestly. Modem's public results change naming, typing, comments, and structure together, so they do not establish the effect of each rule independently.

Related: [[Agent context engineering]], [[Irreducible codebase documentation]], [[Concise AGENTS.md for capable coding agents]], [[Subagent delegation]].
