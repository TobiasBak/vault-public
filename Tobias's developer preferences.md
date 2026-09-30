# Tobias's developer preferences

User-confirmed through 2026-09-29. Weigh these preferences heavily when they fit the purpose, evidence, risk, and project constraints. They are decision guidance, not requirements to force onto every system. Repository reality and explicit project policy take precedence.

## Priorities and architecture

Tobias performs all development through agents: exploration, planning, design, implementation, review, validation, and continuation. He supplies context, challenges recommendations, resolves material choices, and accepts consequential outcomes. No separate human implementation or routine source-review phase follows. Code, tests, documentation, history, and checkpoints are the durable handoff between contexts. See [[Agentic engineering#Agent-native software engineering]].

Tobias values fast experimentation, clean code with low accidental complexity, strong decoupling and cohesion, cloud and system design, AI-agent-optimized feedback loops, and bleeding-edge technology when failures are cheap and reversible. Prototype quickly, then simplify deliberately. Speed should not become permanent disorder, and clean-code ideals should not delay learning.

A prototype is a disposable experiment answering one explicit question. Keep persistence, production hardening, and unrelated concerns out unless they are the question being tested. Preserve the validated decision, then implement it properly rather than shipping the experimental harness.

A modular monorepo is the practical default; splitting related agent work across repositories increased coordination cost. Use strong package boundaries and narrow, explicit context to limit irrelevant exposure. Adopt more repositories or Git submodules only when measured isolation and task quality outweigh versioning and coordination cost.

Favor small coherent modules, explicit stable contracts, clear state ownership, direct domain models, high cohesion, low coupling, simple data flow, and behavioral tests that permit redesign. Delete obsolete complexity. Avoid speculative abstractions, inheritance-heavy hierarchies, unnecessary layers, and patterns without a concrete problem. Aim for simpler change, not maximum abstraction or minimum line count.

Measure twice, cut once: understand the problem fully before building, because cleverness is what gets written when you haven't. The biggest simplicity win is refusing to solve problems we don't have. Good code is the most simple thing that delivers full functionality and performance, nothing traded away, nothing bolted on. Push back when you see a more obvious way.

Here, “understand fully” means understanding enough to avoid uninformed implementation; a bounded prototype may be the fastest way to gain that understanding. “Nothing traded away” means simplicity must not come from silently dropping required functionality or performance, not that engineering has no explicit tradeoffs.

Prefer deep modules for cohesive responsibilities: hide substantial behavior while minimizing what callers must know. Judge depth by caller leverage and maintenance locality, not size. Imagine deleting the module: needless indirection disappears; useful hidden complexity reappears across callers.

Prioritize architectural improvement where a named pain point or repeated change history shows friction. Awkward but stable code is a weaker target than ownership, knowledge, or verification that repeatedly scatters during real changes. Architecture should make expected changes easier.

Optimize for cumulative maintainability across contexts, not current-patch throughput. Choose the simplest coherent resulting system, not the smallest diff. Local patches are good when they preserve ownership, one source of truth, boundaries, and reliable verification. Duplicated rules, scattered changes, hidden effects, lying abstractions, or unverifiable seams call for focused redesign at the affected boundary, not unrelated cleanup, speculative abstraction, or planning ceremony.

Tobias favors architectural constraints and static checks so routine work needs neither the strongest model nor constant human attention. Less capable agents and busy people should make correct changes without knowing the whole codebase or resolving every low-level choice. He endorsed this approach from Lauren Tan's talk on 2026-09-27. See [[Agentic engineering#Constrained codebases for low-context contributors]].

His working assumption is that agents overwhelmingly choose the easiest local patch and copy existing patterns. The codebase should not invite shortcuts or make them look approved. Make the easiest change preserve the design.

No programming paradigm is mandatory. Tobias leans toward object-oriented design because it is familiar, while remaining open to functional, procedural, or data-oriented approaches when they produce the clearest system. Prefer cohesive objects with explicit responsibilities over inheritance-heavy hierarchies.

## Aspirational engineering method

Tobias wants to grow toward this method for unfamiliar or unresolved engineering problems. It is a target practice, not a claim that it already describes his development consistently:

1. Define the problem, desired outcome, constraints, and what “solved” means.
2. Make the problem observable or reproducible and gather evidence before choosing a solution.
3. Inspect the existing system, contracts, domain knowledge, prior art, and open-source options; reuse an existing solution when it actually fits.
4. Form competing hypotheses or designs and make their tradeoffs explicit.
5. Test the riskiest assumption with the smallest useful prototype.
6. Validate against the original problem and representative cases, including material failure modes.
7. Implement incrementally and observe the real result.
8. If blocked, escalate with a precise account of what was tried, what happened, what remains uncertain, and what decision or help is needed.

Research is input to a decision, not the method by itself. The objective is to reduce uncertainty deliberately until the simplest justified solution becomes clear.

## Communication

Tobias prefers direct conversation over polished corporate or report-like prose. Use natural profanity when it sharpens the point, not as decoration; do not sanitize clear judgments into vague professional language. Match the tone, lead with the judgment, and keep ordinary discussion short.

## Languages, data, and APIs

Use Python through [uv](https://docs.astral.sh/uv/) unless an existing project authoritatively requires otherwise. Use uv for Python versions, environments, dependency and lockfile management, workspaces, running tools and applications, and package builds or publication. Do not introduce pip, Poetry, Conda, or manually managed virtual environments into a uv project.

Use [[TypeScript 7 ecosystem|TypeScript 7]] as the TypeScript baseline. Fast compiler and language-server feedback is valuable for agent iteration. Personal prototypes may adopt current or prerelease technology aggressively; long-lived, regulated, or production-critical systems need compatibility checks, runtime and build validation, and rollback. AI can make source migration cheap, but compiler, tests, builds, and observable behavior remain authoritative.

SQLite is the default database because it is simple, local, portable, and capable. Plain JSON files fit very small data, though JSON can often live in SQLite without another storage convention. When a larger database is warranted, PostgreSQL `jsonb` is attractive when the data model benefits from JSON-capable storage.

There is no fixed API-style preference. Choose from consumers, deployment, and interoperability. Python services often fit REST with OpenAPI. Use tRPC, GraphQL, messaging, or another protocol only when its specific benefits match the system.

## Frontend

Tobias has no durable framework preference despite experience with React, Vue, Svelte, Angular, Astro, and others. Choose for the product and current tooling support: content-heavy sites may favor Astro, general interactive applications React, Vue, or Svelte, and standardized enterprise systems Angular. When options fit equally, favor fast setup, strong agent familiarity, tight automated feedback, mainstream integration, and low maintenance. Explain the architecture briefly rather than asking Tobias to choose from implementation details.

Agents implement and review the frontend; Tobias does not rely on manual source review. Protect quality through observable behavior, browser tests, accessibility, type and lint feedback, independent agent critique when warranted, and restrained rendered design.

## Cloud and deployment

Tobias has the most cloud experience with GCP, whose free tier is useful for experiments. Tailscale access to personally managed servers currently works well and may be simpler than more cloud infrastructure.

Containers are the preferred deployment unit. Docker and Kubernetes are familiar and attractive when orchestration is justified, but small prototypes should use the simplest deployment shape that fits. Prefer infrastructure as code and declarative configuration; this motivates NixOS and reproducible machines over undocumented manual setup.

Security, reliability, and production controls are usually low priorities for disposable personal experiments. They become material for work and production-facing systems, where project requirements override this prototype posture.

## Testing and feedback

Match testing to consequence, lifetime, integration risk, and expected change. Add tests that speed iteration, protect difficult behavior, or reduce meaningful risk, not elaborate infrastructure for disposable prototypes, personal experiments, or low-risk Pi extensions merely to increase coverage. Prefer observable behavior over structure. Derive expectations independently from specifications, worked examples, known literals, or established behavior, not by repeating implementation logic in a test that passes by construction.

For a difficult bug, first build the fastest repeatable signal for the exact reported symptom. Trace the failure to the first incorrect state and identify the invariant and owner responsible for keeping that state valid. Minimize the reproduction, discriminate falsifiable hypotheses by changing one variable at a time, preserve the minimized case as a regression test at the real behavioral seam, and rerun the original scenario after the fix.

A flaky bug does not need a perfectly deterministic reproduction before investigation. Increase and measure its reproduction rate through repetition, controlled stress, narrowed timing windows, or pinned environmental variables until competing hypotheses can be tested efficiently.

For integration-heavy systems, use realistic black-box service doubles when valuable. Run the normal application against a local service mock, record requests, return realistic responses, and assert visible requests, state, and behavior. This checks serialization, configuration, control flow, and integration without mocking internals or contacting production. Favor fidelity, deterministic setup, useful logs, and reusable scenarios; add focused unit tests only where risk justifies them.

AI-agent-oriented engineering is especially interesting: [[Autoresearch]], Pi extensions, orchestration, context engineering, evaluation, and automated improvement. Prefer fast trustworthy compiler and test feedback, locally discoverable machine-readable constraints, automated repetitive work, measured outcomes, bounded experiments, easy rollback, and preserved useful failures. Improve the harness and tools as well as immediate code, but do not add process or abstraction merely because it is agent-oriented.

Treat consequential numeric limits as tripwires rather than unexplained constants. Measure the real behavior before choosing a limit, retain its basis as a receipt near the authoritative definition, and remeasure when conditions change. A limit developers can hit is a limit they must see: every budget failure should name the budget, the limit, and the ask. A silent budget is worse than no budget.

Here, “number” means a consequential engineering limit or threshold. Its receipt is the basis that justifies it: measurement where safe, otherwise an external contract or explicit safety, risk, or resource policy. Hard safety and integrity limits precede experimentation.

On 2026-09-29, Tobias chose GPT-6.1 Sol over Astra for day-to-day coding-agent work because of its capability-to-cost-per-task tradeoff, using Artificial Analysis's benchmark comparison rather than only token prices. This replaces the earlier Astra preference; it is a chosen default, not merely a candidate awaiting a benchmark. He still prefers Codex's native tooling over custom workers or model-routing policies, without an added instruction encouraging delegation. T3 Code remains the normal interactive environment; use it with Codex (reconsider Pi there only if T3 Code supports it), or use another interface when the task or available tooling calls for it. [[Choosing and steering coding models]] owns model capabilities and the scoped cost comparison. This decision does not select a new reasoning effort or change installed configuration by itself.

Phrase agent authorization guidance as an activatable condition, such as “invoke the live workflow only when Tobias allows it,” rather than as an absolute prohibition. A clear current request to perform the scoped action is the required authorization and should not cause a redundant confirmation or a refusal based on the default-off wording. Reserve “never,” “prohibited,” and equivalent hard language for constraints that Tobias genuinely cannot override in the current instruction hierarchy.

## Dependencies, design decisions, and documentation

Minimize third-party dependencies. Own a small capability locally when correctness, performance, and tool support are comparable. Do not rebuild complex, security-sensitive, or standards-heavy infrastructure. A dependency should earn its place by removing meaningful complexity or risk after accounting for maintenance, updates, compatibility, supply chain, and opportunity cost.

Tobias prefers system design and refactoring to repetitive implementation, but agents perform all of it, including source review, migrations, tests, and investigation. Involve him through conversation when decisions materially shape boundaries, architecture, data flow, cloud topology, operations, security, long-term coupling, product behavior, or irreversible technology choices. Bring a recommendation, evidence, and material tradeoffs, not an unresolved design decision.

For difficult features, do not be afraid to suggest seemingly insane solutions. Treat the request and architecture as hypotheses. When ownership, coupling, boundaries, or an unsuitable stack cause friction, compare feature simplification or removal, local implementation, and coherent redesign before adding workarounds. Recommend the simplest resulting system, not the smallest diff. Favor redesign when cheap and reversible; respect compatibility and risk in consequential systems. Implement routine choices autonomously, bring architectural recommendations and tradeoffs, and reopen settled choices only with new conflicting evidence.

Make code understandable through names, boundaries, types, tests, and structure. Keep READMEs short and agent guidance concise and scoped. Document rationale, hazards, external contracts, irreversible decisions, domain language, and unusual workflows that executable project state cannot express. Ordinary setup, test, lint, type, and build commands belong in discoverable manifests, scripts, task runners, and CI, not default prose inventories. Add such command context only when representative agents repeatedly make meaningful wrong choices that clearer executable surfaces cannot prevent. [[Irreducible codebase documentation]] and [[Concise AGENTS.md for capable coding agents]] hold the general guidance. Tobias prefers short, locally useful documentation and retrieval of this note rather than copying it into every prompt. Promote only demonstrated durable cross-repository behavior into global instructions.

Tobias favors a repository-wide no-code-comments rule enforced by lint or CI. Comments can justify a workaround and teach the next agent to copy it. Fix the design or add a check instead of explaining why an avoidable patch is acceptable. Do not leave each agent to decide which comments deserve an exception. See [[Irreducible codebase documentation]].

For agent guidance and engineering principles, Tobias prefers vivid, memorable wording that invites judgment over abstract policy prose that merely enumerates caveats. When adapting strong source language to a broader scope, preserve the exact phrasing that still applies and remove sentences that do not belong there; paraphrase only where correctness, scope, authority, or safety requires it.
