# Tobias's developer preferences

User-confirmed through 2026-09-27. Weigh these preferences heavily when they fit the purpose, evidence, risk, and project constraints. They are decision guidance, not requirements to force onto every system. Repository reality and explicit project policy take precedence.

## Priorities and architecture

Tobias performs all software development through agents, including exploration, planning, design, implementation, review, validation, and continuation. He works by supplying context, challenging and judging recommendations, resolving material choices, and accepting consequential outcomes. There is no separate human implementation or routine source-review phase. The codebase, tests, documentation, history, and checkpoints are the durable handoff between agent contexts. See [[Agentic engineering#Agent-native software engineering]].

Tobias values fast experimentation, clean code with low accidental complexity, strong decoupling and cohesion, cloud and system design, AI-agent-optimized feedback loops, and bleeding-edge technology when failures are cheap and reversible. Prototype quickly, then simplify deliberately. Speed should not become permanent disorder, and clean-code ideals should not delay learning.

A prototype is a disposable experiment answering one explicit question. Keep persistence, production hardening, and unrelated concerns out unless they are the question being tested. Preserve the validated decision, then implement it properly rather than shipping the experimental harness.

A modular monorepo is the practical default. Splitting related agent work across many repositories created more coordination cost. Large monorepos can still expose irrelevant context, so use strong package boundaries and narrow, explicit agent context. Treat repository proliferation and Git submodules as hypotheses to test, not assumed solutions; adopt them only when measured isolation and task quality outweigh versioning and coordination cost.

Favor small coherent modules, explicit stable contracts, clear state ownership, direct domain models, high cohesion, low coupling, simple data flow, deletion of obsolete complexity, and behavioral tests that permit internal redesign. Avoid speculative abstractions, inheritance-heavy hierarchies, unnecessary layers, and patterns without a concrete problem. The objective is simpler change, not maximum abstraction or minimum line count.

Measure twice, cut once: understand the problem fully before building, because cleverness is what gets written when you haven't. The biggest simplicity win is refusing to solve problems we don't have. Good code is the most simple thing that delivers full functionality and performance, nothing traded away, nothing bolted on. Push back when you see a more obvious way.

Here, “understand fully” means understanding enough to avoid uninformed implementation; a bounded prototype may be the fastest way to gain that understanding. “Nothing traded away” means simplicity must not come from silently dropping required functionality or performance, not that engineering has no explicit tradeoffs.

Prefer deep modules when a responsibility is cohesive: minimize what callers must know while hiding substantial behavior. Judge depth by caller leverage and maintenance locality, not implementation size. As a diagnostic, imagine deleting the module: unnecessary indirection disappears, while useful hidden complexity reappears across its callers.

Prioritize architectural improvement where a named pain point or repeated change history demonstrates friction. Architecture should make expected future changes easier; awkward but stable code is a weaker refactoring target than code whose ownership, knowledge, or verification repeatedly scatters during real work.

Optimize for cumulative maintainability across agent contexts, not the throughput of the current patch. Choose the simplest coherent resulting system rather than the smallest diff. A local patch is good when it preserves clear ownership, one source of truth, existing boundaries, and a reliable verification path. When the task exposes duplicated rules, scattered changes, hidden effects, lying abstractions, or an unverifiable seam, agents should propose and perform the focused redesign needed at that boundary. Do not turn this into unrelated cleanup, speculative abstraction, or planning ceremony.

Tobias favors locking down codebases so routine work does not need the strongest model or constant human attention. Turn mistakes into architectural constraints and static checks. Less capable agents and busy people should be able to make correct changes without knowing the whole codebase or thinking through every low-level decision. He endorsed this approach from Lauren Tan's talk on 2026-09-27. See [[Agentic engineering#Constrained codebases for low-context contributors]].

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

Tobias prefers direct, conversational language over polished corporate or report-like prose. Natural profanity is welcome when it makes the point sharper or more honest; do not sanitize a clear conclusion into vague professional language, but do not force profanity as decoration. Match the conversation's tone, lead with the actual judgment, and keep ordinary discussion short enough to remain conversational.

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

Testing effort should match consequence, lifetime, integration risk, and expected change. Do not build elaborate infrastructure for disposable prototypes, personal experiments, or low-risk Pi extensions merely to increase coverage. Add tests when they speed iteration, protect difficult behavior, or reduce meaningful risk. Prefer observable behavior over implementation structure. Expected results should come from a source independent of the implementation—such as a specification, worked example, known literal, or externally established behavior—rather than recomputing the implementation's logic and producing a test that passes by construction.

For a difficult bug, first build the fastest repeatable signal for the exact reported symptom. Trace the failure to the first incorrect state and identify the invariant and owner responsible for keeping that state valid. Minimize the reproduction, discriminate falsifiable hypotheses by changing one variable at a time, preserve the minimized case as a regression test at the real behavioral seam, and rerun the original scenario after the fix.

A flaky bug does not need a perfectly deterministic reproduction before investigation. Increase and measure its reproduction rate through repetition, controlled stress, narrowed timing windows, or pinned environmental variables until competing hypotheses can be tested efficiently.

For integration-heavy systems, use realistic black-box service doubles when valuable: run the normal application against a local mock of the external service, record outgoing requests, return realistic responses, and assert externally visible requests, state, and behavior. This checks serialization, configuration, control flow, and integration without mocking internals or contacting production. Favor fidelity, deterministic setup, useful request logs, and reusable scenarios; combine with focused unit tests only where risk justifies them.

AI-agent-oriented engineering is especially interesting: [[Autoresearch]], Pi extensions, orchestration, context engineering, evaluation, and automated improvement. Prefer fast trustworthy compiler and test feedback, locally discoverable machine-readable constraints, automated repetitive work, measured outcomes, bounded experiments, easy rollback, and preserved useful failures. Improve the harness and tools as well as immediate code, but do not add process or abstraction merely because it is agent-oriented.

Treat consequential numeric limits as tripwires rather than unexplained constants. Measure the real behavior before choosing a limit, retain its basis as a receipt near the authoritative definition, and remeasure when conditions change. A limit developers can hit is a limit they must see: every budget failure should name the budget, the limit, and the ask. A silent budget is worse than no budget.

Here, “number” means a consequential engineering limit or threshold. Its receipt is the basis that justifies it: measurement where safe, otherwise an external contract or explicit safety, risk, or resource policy. Hard safety and integrity limits precede experimentation.

As of 2026-09-05, Tobias uses GPT-6 Astra in Codex for day-to-day coding-agent work and prefers Codex's native tooling over custom workers or model-routing policies. T3 Code remains the normal interactive environment; use it with Codex (reconsider Pi there only if T3 Code supports it), or use another interface when the task or available tooling calls for it. See [[Working with GPT-6 Astra]].

Phrase agent authorization guidance as an activatable condition, such as “invoke the live workflow only when Tobias allows it,” rather than as an absolute prohibition. A clear current request to perform the scoped action is the required authorization and should not cause a redundant confirmation or a refusal based on the default-off wording. Reserve “never,” “prohibited,” and equivalent hard language for constraints that Tobias genuinely cannot override in the current instruction hierarchy.

## Dependencies, design decisions, and documentation

Minimize third-party dependencies. Own a small capability locally when correctness, performance, and tool support are comparable. Do not rebuild complex, security-sensitive, or standards-heavy infrastructure. A dependency should earn its place by removing meaningful complexity or risk after accounting for maintenance, updates, compatibility, supply chain, and opportunity cost.

Tobias enjoys system design and refactoring more than repetitive implementation, but all of that work still happens through agents. Agents own source implementation and review as well as mechanical coding, migrations, test generation, and repetitive investigation. Keep Tobias involved through the agent conversation when decisions materially shape system boundaries, architecture and data flow, cloud topology, operations and security, long-term coupling, product behavior, or irreversible technology choices. Bring a recommendation, evidence, and material tradeoffs rather than delegating the design decision back to him without analysis.

For difficult features, do not be afraid to suggest seemingly insane solutions. Treat both the request and current architecture as hypotheses. If friction comes from state ownership, coupling, poor boundaries, or an unsuitable stack, compare feature simplification or removal, a local implementation, and a coherent redesign before accumulating workarounds. Recommend the simplest resulting system, not merely the smallest diff. Bias toward redesign when cheap and reversible; respect compatibility and risk in consequential systems. Act autonomously on routine implementation, give a clear recommendation and material tradeoffs for architecture, and do not reopen a resolved choice without new conflicting evidence.

Make code understandable through names, boundaries, types, tests, and structure. Keep README files short and agent guidance concise and scoped. Document rationale, hazards, external contracts, irreversible decisions, domain language, and unusual workflows that code or executable project state cannot communicate. Do not add development guides or command maps by default for ordinary setup, test, lint, type, or build commands that capable agents can recover from manifests, named scripts, task runners, and CI. Add such context only after representative agents repeatedly make a meaningful wrong choice that clearer executable surfaces cannot prevent. Avoid prose inventories and duplicated implementation descriptions. [[Irreducible codebase documentation]] and [[Concise AGENTS.md for capable coding agents]] hold the general guidance; the personal preference is for short, locally useful documentation. Keep this preference note retrievable rather than copying it into every prompt, and promote only demonstrated durable cross-repository behavior into global instructions.

Tobias favors a repository-wide no-code-comments rule enforced by lint or CI. Comments can justify a workaround and teach the next agent to copy it. Fix the design or add a check instead of explaining why an avoidable patch is acceptable. Do not leave each agent to decide which comments deserve an exception. See [[Irreducible codebase documentation]].

For agent guidance and engineering principles, Tobias prefers vivid, memorable wording that invites judgment over abstract policy prose that merely enumerates caveats. When adapting strong source language to a broader scope, preserve the exact phrasing that still applies and remove sentences that do not belong there; paraphrase only where correctness, scope, authority, or safety requires it.
