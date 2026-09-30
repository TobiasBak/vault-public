# Context-sensitive code review

Context-sensitive review follows a change's risks. One agent with native repository and review tools can do it without delegation, a custom orchestrator, or stored review telemetry.

For a deliberately orchestrated review system, keep three concerns separate:

1. **Review orchestration** owns the review contract, selects temporary lenses, delegates bounded work, tracks coverage, and merges or deduplicates conclusions.
2. **Context retrieval** exposes repository, diff, symbol, relation, history, and validation evidence without embedding a review workflow.
3. **Structured findings** carry the affected artifact and location, violated contract or risk, supporting evidence, consequence, and confidence or unresolved question.

This keeps retrieval reusable, orchestration independent of context tools, and findings formats from dictating analysis.

## Initial contract and map

Reviewers need intent, requirements, invariants, base and candidate identities, the diff, context routes, and validation evidence. Reuse what the task and repository already provide. Keep the author's investigation and conclusions out of separate reviewers' inputs. Include relevant non-goals, authority, risks, and acceptance criteria. Requirement fidelity and repository compliance are separate checks; neither proves the other. A change map guides reading; it does not replace source.

Name the relevant failure classes: contract drift, missed callers, state transitions, idempotency, external effects, or inadequate behavioral verification. Ask for findings, not a repository tour.

Apply progressive disclosure on two axes:

- **Authority:** keep global and project rules available; retrieve folder-specific instructions when entering that subtree. Nested rules refine or override broader rules. Preserve their scopes rather than flattening them into one prompt.
- **Evidence:** start with PR intent and the change map, then follow relevant files and symbols to callers, callees, tests, types, configuration, external boundaries, or history as the hypothesis requires.

Retrieve **semantic neighborhoods**, not fixed token windows. Include related declarations, transitions, types, callers, tests, and configuration across files; omit unrelated adjacent code. Retain source identities, revision, truncation status, and expansion routes. Let the current risk hypothesis guide retrieval rather than precomputing a universal bundle. See [[Agent context engineering]] and [[Search-driven code discoverability]].

Search changed symbols and domain terms for definitions and tests, then follow reverse references, alternate spellings, adapters, external boundaries, and retained legacy paths. Check owning types and rationale against regression or public-interface evidence. Cite exact paths and evidence. Missing evidence is not a verified negative. Stop when the requested concerns are covered.

## Reviewers and authority

A review lens focuses attention on security, concurrency, data integrity, API compatibility, or test adequacy; it need not be a separate agent or persona. [[Subagent delegation]] covers delegated handoffs and authority.

Independent review helps most when failure is consequential, validation is weak, or fresh context can challenge assumptions. For delegated PR review, start with one general reviewer; add specialists only for distinct risks in the diff. Give each a narrow responsibility and evidence access beyond the diff. Irrelevant panel members add cost and duplicate findings.

Reviewers may inspect code, follow relations, search history, run tools, and test hypotheses. Review should normally leave the candidate read-only, with verification mutations confined to disposable snapshots or dedicated scratch space. This allows realistic verification without changing shared state or granting repository write authority.

## Tools and growth path

Retrieval tools supply change maps, scoped instructions, source, relations, search, history, validation evidence, and expansion routes. Orchestration decides which reviewer runs; retrieval need not prescribe a sequence.

Start with repository snapshots, search, language tooling, dependency relations, shell access, and tests. Add AST, semantic-graph, runtime-trace, blame, or domain tools only when recurring retrieval failures demonstrate their value. Hunk's change maps, review lenses, symbol-centered context, and structured findings are examples, not architectural dependencies.

Finish when the requested scope is covered, not when every source is exhausted. Support findings with evidence. The absence of findings does not clear an unexamined area.

## Review history and automation discovery

If collecting history to study repeated findings, store outcomes outside the reviewed worktree. Retain target identity, staleness, changed files, scope, model, effort, findings, and compact telemetry rather than full prompts or traces. A commit identifies committed evidence; a working-tree fingerprint cannot recover changed unstaged or untracked content. Retain a compressed target patch when exact recovery matters. Native Codex reviews do not require this logging system.

History informs improvements; it does not authorize new rules. Recurring findings may reveal contracts enforceable through code, schemas, tools, lint, or CI. Broken links suit deterministic validation; misleading concepts or misplaced abstractions usually need judgment. Validate mechanical replacements for real contracts. Redundant review instructions need no replacement. See [[Prompting tool-using agents#Promote settled cognition into machinery|promoting settled cognition into machinery]].
