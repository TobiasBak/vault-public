# Context-sensitive code review

Context-sensitive review follows the risks exposed by a change. A single agent can do this with native repository and review tools. It does not require delegated reviewers, a custom orchestrator, or persisted review telemetry.

For a deliberately orchestrated review system, keep three concerns separate:

1. **Review orchestration** owns the review contract, selects temporary lenses, delegates bounded work, tracks coverage, and merges or deduplicates conclusions.
2. **Context retrieval** exposes repository, diff, symbol, relation, history, and validation evidence without embedding a review workflow.
3. **Structured findings** carry the affected artifact and location, violated contract or risk, supporting evidence, consequence, and confidence or unresolved question.

This separation keeps retrieval reusable outside review, lets orchestration evolve without rewriting context tools, and prevents a findings format from dictating how analysis must proceed.

## Initial contract and map

A reviewer needs the change's intent, candidate identity, relevant requirements, and access to evidence. Much of this may already be available in the task and repository. When handing work to separate reviewers, a shared compact contract and change map can preserve the needed context without forwarding the author's entire exploration. Include the non-goals, authority, known risks, and acceptance conditions that affect that review, not a fixed inventory for every task. Requirement fidelity and repository-convention compliance are distinct dimensions; passing one does not establish the other. A map is orientation, not a substitute for source.

Apply progressive disclosure on two axes:

- **Authority:** keep global constraints and project rules available, then retrieve folder-specific instructions when analysis enters that subtree. Nearer authority refines or overrides broader authority; do not flatten all scopes into one duplicated prompt.
- **Evidence:** move from PR intent and change map to a relevant file, changed symbol, and then callers, callees, tests, types, configuration, external boundaries, or history as the emerging hypothesis requires.

Retrieve **semantic neighborhoods**, not fixed token windows. A useful neighborhood may include a declaration, enclosing state transition, related type, call site, test, and configuration despite crossing files, while omitting adjacent code with no bearing on the behavior. Preserve stable source identities, revision, truncation status, and routes for expansion. Let the model choose the next retrieval from its current risk hypothesis; tools should support progressive expansion rather than precompute an oversized universal bundle. This specializes [[Agent context engineering]] and [[Search-driven code discoverability]] for review.

## Reviewers and authority

A review lens focuses attention on a concern such as security, concurrency, data integrity, API compatibility, or test adequacy. It need not imply a separate agent or fixed persona. If the workflow deliberately delegates review, [[Subagent delegation]] covers the relevant handoff and authority boundaries.

Give reviewers broad analytical capability: they may inspect the repository, follow relations, search history, run tools, and test hypotheses. Keep side-effect authority narrow. Review should normally be read-only against the candidate and may mutate only disposable snapshots or dedicated scratch space for shell commands, builds, generated artifacts, and tests. This permits realistic verification without contaminating shared state or granting repository write authority.

## Tools and growth path

When building review tooling, keep retrieval capabilities separate from orchestration. Change mapping, scoped-instruction lookup, source retrieval, relation traversal, search, history, and validation tools return evidence and routes to more detail. They need not decide which reviewer runs or prescribe a fixed sequence.

Start with ordinary repository snapshots, search, language tooling, dependency relations, shell access, and tests. Add specialized AST, semantic-graph, runtime-trace, blame, or domain tools only after a recurring retrieval failure demonstrates their value. Concepts seen in review products such as Hunk—change maps, review lenses, symbol-centered context, and structured findings—are useful examples, not architectural dependencies.

Review is complete when its requested scope is covered, not when every available context source has been exhausted. Findings need supporting evidence; absence of a finding says nothing about an unexamined area.

## Review history and automation discovery

For a review system that deliberately collects history to study repeated findings, store outcomes outside the reviewed worktree. Target identity, staleness, changed files, review scope, model and effort, findings, and compact execution telemetry support comparison without retaining full prompts or tool traces. A commit identity can route back to committed evidence, but a working-tree fingerprint cannot reconstruct unstaged or untracked content after it changes; a compressed target patch can preserve that evidence when exact later inspection matters. This is an optional system design, not a logging requirement for native Codex reviews.

History is evidence for improving the system, not authority to create a rule automatically. Recurring findings may expose a contract that code, a schema, a focused tool, lint, or CI can enforce. Broken local links suit deterministic validation; whether an archived concept is misleading or an abstraction is misplaced usually needs judgment. Validate a mechanical replacement when a real contract will rely on it. Retiring a redundant review instruction needs no replacement. This is the review-specific application of [[Prompting tool-using agents#Promote settled cognition into machinery|promoting settled cognition into machinery]].
