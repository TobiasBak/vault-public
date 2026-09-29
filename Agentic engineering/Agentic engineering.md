# Agentic engineering

Agentic engineering treats an agent's capability as a property of the whole execution system: model, prompt contract, active context, durable state, tools, orchestration, permissions, evaluator, and feedback loop. Improving one layer without controlling the others can move cost or failure elsewhere rather than improve completed work.

## Agent-native software engineering

"Agent-native software engineering" is local shorthand, not a settled discipline. **Agent-mediated development** describes the working model: planning, design, implementation, review, validation, and resumption all happen through agent conversations and the contexts supplied to them. The human supplies intent, judgment, correction, authority, and consequential acceptance. There is no separate human coding or source-review phase that will repair an agent's local choices later.

An **agent-native codebase** is built to remain understandable, changeable, and verifiable across repeated fresh agent contexts. A fresh agent can recover intent, ownership, invariants, authority boundaries, unfinished state, and completion evidence from durable project state; change behavior at one coherent seam; predict the affected area; verify real behavior; and resume or hand off without private human memory. The repository and its related artifacts are the durable handoff: every context consumes them as prior state and leaves them as the next agent's starting state.

The main failure is patch accretion. A narrow task rewards the smallest plausible change, even when it adds a parallel path, duplicates a rule, blurs ownership, preserves a lying abstraction, or tests only the reported symptom. Each patch expands the context and affected area of the next change. Verification becomes slower and less trustworthy, so later agents narrow their work further and compound the same problem. Cheap patch production can therefore make useful agent work progressively more expensive.

Optimize for cumulative maintainability rather than current-task throughput. Simplicity is a property of the resulting system, not the diff size or implementation time. In this setting, clean and simple code has one source of truth, cohesive ownership, direct domain models, truthful contracts, explicit effects, low accidental coupling, discoverable names, and behavioral checks at stable boundaries. Maintainability is operational: another agent can find where behavior belongs, understand why the structure exists, make the next change without unrelated ripple effects, and prove the result without loading the whole repository.

Before choosing an implementation, reconstruct the relevant end-to-end behavior, owner, invariants, callers, effects, and real verification path. Compare the smallest patch with a local refactor and the simplest coherent redesign. A quick patch is sound when it is genuinely local, reversible, boundary-preserving, and independently verifiable. When the task exposes duplicated knowledge, scattered changes, hidden effects, unclear ownership, a false abstraction, or no stable test seam, repair the touched design at its owning boundary instead of adding another workaround. Concrete friction authorizes focused redesign; it does not authorize unrelated cleanup or speculative abstraction. Apply [[Software architecture#Recognizing an architectural decision|the architecture test]] and bring material choices to the human with a recommendation and tradeoffs rather than treating the requested implementation as a settled design.

Put consequential design into artifacts that survive the trajectory: authoritative definitions, types or schemas that exclude invalid states, enforced dependency directions, inspectable plans and results, idempotent or recoverable effects, actionable diagnostics, behavioral tests, and concise rationale where code cannot express it. Preserve unfinished work and validation evidence in restart-ready state. [[AI-era software durability]] describes the split between agent interpretation, typed plans, deterministic execution, and authoritative results. [[Agent context engineering]] covers reconstructable working state, while [[Agentic end-to-end testing]] covers independent evidence.

This is not a demand for exhaustive plans or constant refactoring. Detailed guesses made too early can spread errors through later agents, and a disposable experiment need not carry production structure. Design goals, contracts, invariants, authority, and acceptance first; discover implementation detail against the real system and deliver in reversible increments. Deep design and narrow delivery are compatible. See [[Tobias's developer preferences#Aspirational engineering method|the engineering method]] for the broader evidence-first loop.

## Constrained codebases for low-context contributors

Lock down routine implementation choices so the easiest path is the right path. Keep feature code together, give behavior and state clear owners, enforce dependency boundaries, and use types that exclude invalid states. Less capable agents then have fewer decisions to get wrong. Busy engineers, designers, and product managers should be able to direct changes without learning the whole architecture or supervising each implementation choice. [[Tobias's developer preferences]] records his preference for this approach.

The codebase is the agent's primary working documentation and memory. Agents read existing code and extend its patterns, so types, APIs, boundaries, and accepted examples teach them what to do more directly than a separate instruction can. Good examples carry engineering knowledge into the next change; bad examples carry mistakes. This does not eliminate the need to document rationale, domain language, or external contracts that code cannot express. See [[Irreducible codebase documentation]].

When you have to correct an agent, choose where that knowledge should live. These five levels are an order of preference, not equally strong pillars:

1. **Codebase.** Express the design through structure and examples. Change the architecture, API, or data structure so the mistake cannot be expressed.
2. **Static analysis.** Build executable compiler/type checks, lint rules, or dependency checks and run them through pre-commit and CI. Violations must produce a failing exit status. Writing instructions in `AGENTS.md`, skills, or other Markdown files does not implement a static check.
3. **Rules and focused review agents.** Tan groups repository rules and Bugbot here. State the engineering rules explicitly and give review agents responsibility for checking changes where applying those rules requires context and judgment. Required review can gate acceptance, but its judgment is not a deterministic guarantee. [[Context-sensitive code review]] covers the review contract and evidence.
4. **Skills.** Preserve reusable engineering methods for debugging, feature development, and performance investigation that still need judgment.
5. **Human-enforced style guides.** Use review findings to discover missing structure, checks, or guidance. Depending on a person to remember and catch every violation does not scale with agent output.

Extract experienced engineers' knowledge into the strongest suitable form instead of defaulting to another instruction or skill. Settled constraints belong in code and checks; context-dependent review criteria belong in reviewer assignments; repeatable mechanics belong in tools; useful investigation choices belong in skills. These forms complement one another, but a skill is not a substitute for a constraint the codebase can enforce. The order guides improvements after a correction, not a mandatory sequence of work for every task.

Expect agents to choose the easiest local patch and copy existing patterns. A workaround can look like an approved example, especially when a comment justifies it. Do not leave the codebase inviting shortcuts while instructions ask agents to resist them. Make the easiest change preserve the design, rather than merely shrink the diff. [[Irreducible codebase documentation]] explains how comments can make workarounds seem acceptable.

Keep one conventional path for each recurring kind of change. Remove bad examples and enforce checks that prevent their return. These changes let contributors follow the team's engineering decisions without needing an expert beside them.

For active codebase hardening, enforce a settled rule across its full agreed scope first, let existing violations fail, then use those failures to drive end-to-end repairs. Do not clean up first and add enforcement afterward, defer type coverage until code is repaired, or hide violations behind migration baselines and suppressions. A failing gate is the work inventory. Follow repairs through owners, callers, tests, and runtime behavior until both the gate and the intended behavior pass. If work stops between passes, leave the gate enabled and visibly failing, with the remaining work recorded. Unfinished repair is acceptable as an explicit handoff; false green is not. This is Tobias's chosen rollout policy. The codebase-first hierarchy describes where knowledge belongs, not an instruction to delay enforcement.

A restriction needs a usable alternative. Give recurring changes an obvious location, a supported API, a clear state owner, and a working example worth copying. Put shared validation and effects behind their owning API rather than making every caller reconstruct them. Checks reject the wrong approach; good interfaces make the right approach easy. When an agent keeps fighting the same boundary, inspect the supported path before adding more instructions. This can be ordinary application design, not a new framework.

Give someone responsibility for this maintenance. Lauren Tan calls it gardening. Strict rules may annoy a human writing code directly but help agents with little context make correct changes.

Tan's Dune framework keeps feature code together and checks imports between execution contexts. For example, it separates Electron main-process and renderer code to keep inappropriate work out of the UI process. Dune also bans comments after agents used them to justify and spread workarounds.

Combine these constraints with engineering skills and [[Agentic end-to-end testing#Reusable verification tools and feature maps|runtime verification]] before increasing parallelism. Once agents can reproduce issues and verify changes, automation can turn user reports and operational alerts into coding tasks with evidence attached. Agents can gather context through existing service connectors and tools without a separate company-wide knowledge system. People remain responsible for product direction and the final outcome.

Constraints preserve settled decisions. [[Agent learning from experience and user feedback#Preserve demonstrated engineering methods|Shared engineering skills]] preserve useful methods that still need judgment. [[Agentic end-to-end testing#Fresh-agent handoff|A fresh-agent handoff]] checks whether another agent can use the codebase and tools without repeated operational coaching. The repo-local [potato-approach skill](../.agents/skills/potato-approach/SKILL.md) provides implementation guidance for these ideas.

Source: Lauren Tan's [September 2026 talk on trusting coding agents](https://x.com/poteto/status/2102050467505430555/video/1), especially 14:45 to 18:45 and 35:30 to the end. The [source and topic index](../.agents/skills/potato-approach/references.md) links the related material and distinguishes local adaptations. Each project still needs its own constraints and verification tools.

## Loop engineering and graph engineering

Loop engineering and graph engineering are emerging 2026 labels for established agent-orchestration concerns, not settled disciplines. Addy Osmani used [loop engineering](https://addyosmani.com/blog/loop-engineering/) for designing the system that repeatedly prompts and checks an agent. LangChain used [graph engineering](https://www.langchain.com/blog/3-years-of-graph-engineering-with-langgraph) for representing constrained paths through agent systems while acknowledging that the label is new and the practice is not.

**Loop engineering** concerns progress over time. It defines the trigger, goal, durable state, context refresh, action, evaluator, recovery, resource budget, and rules for finishing or escalating. Repetition alone is worthless when the evaluator cannot tell improvement from confident drift. [[Agent context engineering]] covers reconstructable state and recovery. [[Autoresearch]] shows the stronger form, with bounded trials, protected evaluation, evidence, selection, and rollback.

**Graph engineering** concerns execution topology. Nodes may be deterministic code, model calls, tools, or complete agents. Edges determine sequence, conditional routing, parallel work, joins, cycles, state transfer, and human gates. A fixed graph fits repeatable work with meaningful dependencies or authority boundaries. Open-ended exploration may need only a capable agent and a thin contract. This usage is separate from knowledge graph engineering.

A graph asks what may run next and what crosses the boundary. A loop asks how the system judges progress, repeats safely, and stops. A graph can contain loops, and a loop can construct or traverse a graph. Prompt engineering shapes one interaction, [[Agent context engineering|context engineering]] controls what each inference sees, and these orchestration structures control execution across interactions. Use agent orchestration as the broader term, and add explicit graphs or loops only when routing, state, evaluation, or recovery needs machinery beyond a provider-native agent loop. See [[Prompting tool-using agents]], [[Subagent delegation]], and [[AI-era software durability#Provider gravity in coding-agent harnesses]].

## Context and orchestration

- [[Prompting tool-using agents]] - define outcomes, evidence, permissions, validation, and stop rules without prescribing every step.
- [[Agent context engineering]] - maintain a reconstructable working set over durable state; treat compaction, retrieval, checkpoints, and handoffs as harness policies.
- [[Search-driven code discoverability]] - shape names, files, types, comments, repository context, tests, and reviewer inputs as a lexical retrieval surface.
- [[Context-sensitive code review]] - separate review orchestration, progressive context retrieval, temporary risk lenses, and evidence-backed findings.
- [[Text-as-image context compression]] - a cautionary hypothesis about lossy, model-specific visual text compression.
- [[Programmatic tool calling]] - distinguish ordinary tool calls, hosted programmatic orchestration, agent-host behavior, and MCP.
- [[Subagent delegation]] - delegate bounded, independently useful work when isolation or parallelism outweighs coordination cost.
- [[Always-on agents and OpenAI dots]] - persistent responsibilities, background follow-through, cloud and local execution, and useful ongoing work.
- [[Irreducible codebase documentation]] - keep rationale, domain language, navigation, and external context in documents while making the code express executable knowledge directly.

## Evaluation and improvement

- [[Coding-agent benchmark trust]] - interpret results as evidence about a versioned task, harness, access policy, configuration, and grader rather than as context-free capability.
- [[Agentic end-to-end testing]] - use tool-using agents as adaptive cross-layer investigators, preserve inspectable evidence, and promote stable discoveries into deterministic protection.
- [[Autoresearch]] - repeatedly improve a bounded intervention surface against a protected evaluator with controlled trials, evidence, selection, and rollback.
- [[Agent learning from experience and user feedback]] - separate evidence, memory, preferences, failure patterns, skills, retrieval, and behavioral compliance.

## Product direction

- [[AI-era software durability]] - distinguish commodity interfaces and provider-owned agent loops from durable state, execution, feedback, accountability, and collaboration.

## Model behavior and policy

- [[Jev and decision models]] - bounded semantic judgments, calibration limits, and relevance to order automation and outcome feedback.
- [[Working with GPT-6 Astra]] - Astra-specific prompting, context management, and integration guidance.
- [[DeepSeek V4.1 Flash in Codex]] - separate Codex/OpenCode Go test option and its verified configuration.
- [[Choosing and steering coding models]] - current GPT-6 and Claude model roles, effort calibration, behavior, and integration boundaries.
- [[AI-generated UI convergence and restrained design]] - recognize generic interface convergence and apply restrained, brief-sensitive design guidance.
