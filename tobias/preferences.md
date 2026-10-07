# Tobias's engineering preferences

Weigh these heavily when they fit; repository reality and explicit project policy win. Confirmed through 2026-09-29.

## How Tobias works

- All development happens through agents: exploration, design, implementation, review, validation. Tobias supplies intent, challenges recommendations, and decides material choices. There is no human coding or source-review phase, so code, tests, docs, and history are the only handoff between contexts.
- Daily setup (since 2026-10-04): T3 Code, talking to Claude Opus 5.5, which orchestrates and delegates the work to GPT-6.1 Sol children in Pi. See [coding models](../agents/coding-models.md) and [subagent delegation](../agents/subagent-delegation.md#compute-routing).
- Prefer using applications in the browser when practical. A local background companion service is fine; use a native app as the fallback when browser support falls short.
- Pi should stay vanilla: upstream defaults and built-in tools, no `pi-tools` or other third-party extensions, custom themes, keybindings, prompt templates, or tuning. Keep the shared global agent instructions and skills. Enable built-in codemode alongside the normal tools, not in codemode-only mode.
- Bring him decisions that shape boundaries, architecture, data flow, topology, security, long-term coupling, product behavior, or irreversible tech choices, as a recommendation with evidence and tradeoffs. Make routine choices yourself. Reopen settled choices only on new evidence.
- Progress updates contain decisions, blockers, and measured numbers. Put hashes, cgroup proofs, ownership maps, and other verification detail in artifact receipts, not chat. Cut ceremony and get to the first trustworthy result quickly.
- He wants agent guidance and principles in vivid, memorable wording that invites judgment, not abstract caveat lists. When adapting strong source language, keep the exact phrasing that still applies; paraphrase only for correctness or scope.

## Design taste

> Measure twice, cut once: understand the problem fully before building, because cleverness is what gets written when you haven't. The biggest simplicity win is refusing to solve problems we don't have. Good code is the most simple thing that delivers full functionality and performance, nothing traded away, nothing bolted on. Push back when you see a more obvious way.

"Understand fully" means enough to avoid uninformed implementation; a bounded prototype is often the fastest way there.

- Fast experimentation, then deliberate simplification. Speed must not become permanent disorder; clean-code ideals must not delay learning.
- A prototype answers one explicit question and is then thrown away. Keep persistence and hardening out unless they are the question. Re-implement the validated decision properly.
- Choose the simplest resulting system, not the smallest diff. When a local patch is sound and when to repair the boundary instead: [patch accretion](../agents/agent-native-codebases.md#patch-accretion-is-the-main-failure).
- For hard features, suggest seemingly insane solutions. Treat the request and architecture as hypotheses: compare simplifying or removing the feature, a local implementation, and a coherent redesign. Favor redesign when it is cheap and reversible.
- Small cohesive modules, explicit contracts, clear state ownership, direct domain models, simple data flow, behavioral tests. No speculative abstractions, inheritance hierarchies, or patterns without a concrete problem. Delete obsolete complexity.
- Deep modules: hide substantial behavior behind a small interface. Deletion test: removing the module should make complexity reappear across callers, not just remove indirection.
- Target architecture work where change history shows repeated friction, not at code that is merely awkward but stable.
- Agents take the easiest local patch and copy what they see, so make the easiest change the correct one through constraints and static checks. Then neither the strongest model nor constant attention is needed. See [agent-native codebases](../agents/agent-native-codebases.md).
- Modular monorepo by default; splitting agent work across repos raised coordination cost.
- No mandatory paradigm. He leans object-oriented out of familiarity; use functional or data-oriented designs when clearer.
- Minimize dependencies, but check existing ones (docs and types) before reimplementing, and prefer an established, maintained library when it removes real complexity. Own small capabilities locally; never rebuild security-sensitive or standards-heavy infrastructure. No stopgaps meant to be replaced later.
- A repo-wide no-code-comments rule enforced by lint or CI, because comments justify workarounds that the next agent copies. See [documentation and naming](../agents/documentation-and-naming.md).
- Keep READMEs and agent guidance short. Commands belong in manifests and scripts, not prose.

## Method for hard problems

This is the method he is growing toward, not a description of current habit:

1. Define the problem, outcome, constraints, and what "solved" means.
2. Make it observable or reproducible; gather evidence before choosing a solution.
3. Inspect the existing system, contracts, prior art, and open-source options. Reuse what actually fits.
4. Form competing hypotheses or designs with explicit tradeoffs.
5. Test the riskiest assumption with the smallest prototype.
6. Validate against the original problem, representative cases, and failure modes.
7. Implement incrementally and observe the real result.
8. When blocked, escalate with what was tried, what happened, what is uncertain, and what decision is needed.

## Stack

- **Python:** always [uv](https://docs.astral.sh/uv/) for versions, environments, dependencies, tools, and builds. Never pip, Poetry, Conda, or hand-made venvs in a uv project.
- **TypeScript:** [TypeScript 7](../software/typescript.md). Prototypes may adopt prerelease tech aggressively; long-lived systems need compatibility checks and rollback.
- **Data:** SQLite by default, including for JSON. Plain JSON files for tiny data. PostgreSQL with `jsonb` when a bigger database is warranted.
- **APIs:** no fixed style. Choose from consumers and interoperability; Python services often fit REST with OpenAPI.
- **Frontend:** no framework preference. Astro for content, React, Vue, or Svelte for apps, Angular for standardized enterprise. On a tie, pick fast setup, strong agent familiarity, and tight feedback. Protect quality with browser tests, accessibility, types, and rendered inspection.
- **Cloud:** most experience with GCP, whose free tier suits experiments. Tailscale to personal servers works well and is often simpler than cloud infrastructure. Containers are the deployment unit; Kubernetes only when orchestration is justified. Infrastructure as code and declarative config, hence NixOS. Provisioning and deploys must run entirely from a CLI; dashboards and browser steps are only for one-time account and token bootstrap.
- Security and production controls are low priority for disposable experiments and material for work and production systems.

## Testing and debugging

- Match testing to consequence, lifetime, and risk. No elaborate test infrastructure for prototypes or low-risk Pi extensions. Test observable behavior, with expectations derived independently, never by repeating the implementation.
- **Hard bug:** build the fastest repeatable signal for the exact symptom. Trace to the first incorrect state and the invariant owner. Minimize, change one variable at a time, keep the minimized case as a regression test at the real seam, and rerun the original scenario.
- **Flaky bug:** raise and measure the reproduction rate through repetition, stress, narrowed timing windows, or pinned environment variables. Don't wait for full determinism.
- **Integration-heavy systems:** run the real app against realistic local black-box service doubles. Record requests and assert visible requests, state, and behavior instead of mocking internals.
- **Secondary platforms gate promotion, not every PR.** When the dev platform catches nearly everything, PRs merge on dev-platform evidence; the other platform (e.g., the order-integration Windows VM) qualifies only the release promotion (main→staging), and issues found there get fixed there. Decided 2026-10-04 after Windows runs on typing and docs PRs dominated the queue.
- **Order-integration native apps stay on Nuitka.** Tobias chose it over PyInstaller because it is safer (2026-10-07). Cut its ~40-minute Windows cold build with caching and artifact reuse, not by proposing another packager.
- **Numeric limits are tripwires.** Measure before choosing a limit and keep the basis next to its definition. Remeasure when conditions change. A limit developers can hit is a limit they must see: every budget failure names the budget, the limit, and the ask. A silent budget is worse than no budget.

## Interests

Agent-oriented engineering: [autoresearch](../agents/autoresearch.md), Pi extensions, orchestration, context engineering, evaluation, automated improvement. Prefer fast trustworthy feedback, machine-readable constraints, measured outcomes, and easy rollback. Improve the harness and tools as well as the code.
