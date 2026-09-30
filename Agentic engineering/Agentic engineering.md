# Agentic engineering

Agentic engineering treats capability as a property of the whole execution system: model, prompt contract, active context, durable state, tools, orchestration, permissions, evaluator, and feedback loop. Improving one layer without controlling the others can shift cost or failure instead of improving completed work.

## Agent-native software engineering

"Agent-native software engineering" is local shorthand, not a settled discipline. In **agent-mediated development**, planning, design, implementation, review, validation, and resumption happen through agent conversations and contexts. The human supplies intent, judgment, correction, authority, and consequential acceptance. No separate human coding or source-review phase repairs an agent's choices later.

An **agent-native codebase** remains understandable, changeable, and verifiable across fresh agent contexts. Durable project state lets an agent recover intent, ownership, invariants, authority boundaries, unfinished work, and completion evidence; change behavior at a coherent seam; predict effects; verify behavior; and resume or hand off without private human memory. The repository and related artifacts are each context's starting state and durable handoff.

Patch accretion is the main failure: a narrow task rewards the smallest plausible change even when it adds a parallel path, duplicates a rule, blurs ownership, preserves a lying abstraction, or tests only the symptom. Each patch expands the next change's context and affected area. Slower, less trustworthy verification pushes later agents toward narrower work, compounding the problem. Cheap patches can make useful agent work progressively more expensive.

Optimize for cumulative maintainability, not current-task throughput. Simplicity belongs to the resulting system, not the diff size or implementation time: one source of truth, cohesive ownership, direct domain models, truthful contracts, explicit effects, low accidental coupling, discoverable names, and behavioral checks at stable boundaries. Another agent should find where behavior belongs, understand the structure, change it without unrelated effects, and prove the result without loading the whole repository.

Before implementation, reconstruct the relevant end-to-end behavior, owner, invariants, callers, effects, and verification path. Compare the smallest patch, a local refactor, and the simplest coherent redesign. A quick patch is sound when local, reversible, boundary-preserving, and independently verifiable. Duplicated knowledge, scattered changes, hidden effects, unclear ownership, a false abstraction, or no stable test seam call for repair at the owning boundary, not another workaround. Concrete friction authorizes focused redesign, not unrelated cleanup or speculative abstraction. Apply [[Software architecture#Recognizing an architectural decision|the architecture test]] and bring material choices to the human with a recommendation and tradeoffs; the requested implementation is not a settled design.

Preserve consequential design in authoritative definitions, types or schemas that exclude invalid states, enforced dependency directions, inspectable plans and results, idempotent or recoverable effects, actionable diagnostics, behavioral tests, and rationale code cannot express. Keep unfinished work and validation evidence restart-ready. [[AI-era software durability]] separates agent interpretation, typed plans, deterministic execution, and authoritative results. [[Agent context engineering]] covers reconstructable working state; [[Agentic end-to-end testing]] covers independent evidence.

This requires neither exhaustive plans nor constant refactoring. Premature detail can spread errors through later agents; disposable experiments need no production structure. Establish goals, contracts, invariants, authority, and acceptance first, then discover implementation detail against the real system and deliver reversible increments. Deep design and narrow delivery are compatible. See [[Tobias's developer preferences#Aspirational engineering method|the engineering method]].

## Constrained codebases for low-context contributors

Lock down routine implementation choices so the easiest path is the right path. Keep feature code together, give behavior and state clear owners, enforce dependency boundaries, and use types that exclude invalid states. Less capable agents have fewer decisions to get wrong; busy engineers, designers, and product managers should be able to direct changes without learning the whole architecture or supervising each choice. See [[Tobias's developer preferences]].

The codebase is the agent's primary working documentation and memory. Types, APIs, boundaries, and accepted examples teach agents more directly than separate instructions because agents extend existing patterns. Good examples carry knowledge into the next change; bad ones carry mistakes. Document rationale, domain language, and external contracts that code cannot express. See [[Irreducible codebase documentation]].

When you have to correct an agent, choose where that knowledge should live. These five levels are an order of preference, not equally strong pillars:

1. **Codebase.** Express the design through structure and examples. Change the architecture, API, or data structure so the mistake cannot be expressed.
2. **Static analysis.** Build executable compiler/type checks, lint rules, or dependency checks and run them through pre-commit and CI. Violations must produce a failing exit status. Writing instructions in `AGENTS.md`, skills, or other Markdown files does not implement a static check.
3. **Rules and focused review agents.** Tan groups repository rules and Bugbot here. State the engineering rules explicitly and give review agents responsibility for checking changes where applying those rules requires context and judgment. Required review can gate acceptance, but its judgment is not a deterministic guarantee. [[Context-sensitive code review]] covers the review contract and evidence.
4. **Skills.** Preserve reusable engineering methods for debugging, feature development, and performance investigation that still need judgment.
5. **Human-enforced style guides.** Use review findings to discover missing structure, checks, or guidance. Depending on a person to remember and catch every violation does not scale with agent output.

Preserve experienced engineers' knowledge in its strongest suitable form: settled constraints in code and checks, context-dependent criteria in reviewer assignments, repeatable mechanics in tools, and investigation choices in skills. These complement one another, but skills cannot replace enforceable constraints. The order guides improvements after a correction, not every task's sequence.

Expect agents to choose the easiest local patch and copy existing patterns. A workaround can look approved, especially when a comment justifies it. Make the easiest change preserve the design rather than relying on instructions to resist shortcuts. [[Irreducible codebase documentation]] explains how comments can legitimize workarounds.

Keep one conventional path for each recurring change. Remove bad examples and enforce checks against their return so contributors can follow the team's decisions without an expert beside them.

For active hardening, enforce a settled rule across its full agreed scope first. Let existing violations fail and drive end-to-end repairs. Do not clean up before enforcement, defer type coverage until repair, or hide violations behind migration baselines and suppressions. A failing gate is the work inventory. Follow owners, callers, tests, and runtime behavior until the gate and intended behavior pass. If work stops, leave the gate enabled and visibly failing and record remaining work. Unfinished repair is acceptable as an explicit handoff; false green is not. This is Tobias's chosen rollout policy. The codebase-first hierarchy locates knowledge; it does not delay enforcement.

A restriction needs a usable alternative: an obvious location, supported API, clear state owner, and example worth copying. Put shared validation and effects behind their owning API, not in every caller. Checks reject the wrong approach; interfaces make the right one easy. When agents repeatedly fight a boundary, inspect the supported path before adding instructions. Ordinary application design may suffice; no new framework is required.

Give someone responsibility for this maintenance. Lauren Tan calls it gardening. Strict rules may annoy a human writing code directly but help agents with little context make correct changes.

Tan's Dune framework keeps feature code together and checks imports between execution contexts. For example, it separates Electron main-process and renderer code to keep inappropriate work out of the UI process. Dune also bans comments after agents used them to justify and spread workarounds.

Combine constraints, engineering skills, and [[Agentic end-to-end testing#Reusable verification tools and feature maps|runtime verification]] before increasing parallelism. Once agents can reproduce issues and verify changes, automation can turn reports and alerts into coding tasks with evidence. Existing service connectors and tools can supply context without a separate company-wide knowledge system. People remain responsible for product direction and the outcome.

Constraints preserve settled decisions; [[Agent learning from experience and user feedback#Preserve demonstrated engineering methods|shared engineering skills]] preserve methods needing judgment. [[Agentic end-to-end testing#Fresh-agent handoff|A fresh-agent handoff]] checks whether another agent can use the codebase and tools without repeated coaching. The repo-local [potato-approach skill](../.agents/skills/potato-approach/SKILL.md) guides implementation.

Source: Lauren Tan's [September 2026 talk on trusting coding agents](https://x.com/poteto/status/2102050467505430555/video/1), especially 14:45 to 18:45 and 35:30 to the end. The [source and topic index](../.agents/skills/potato-approach/references.md) links the related material and distinguishes local adaptations. Each project still needs its own constraints and verification tools.

## Loop engineering and graph engineering

Loop engineering and graph engineering are emerging 2026 labels for established orchestration concerns, not settled disciplines. Addy Osmani's [loop engineering](https://addyosmani.com/blog/loop-engineering/) designs the system that repeatedly prompts and checks an agent. LangChain's [graph engineering](https://www.langchain.com/blog/3-years-of-graph-engineering-with-langgraph) represents constrained paths through agent systems; the label is new, the practice is not.

**Loop engineering** concerns progress over time. It defines the trigger, goal, durable state, context refresh, action, evaluator, recovery, resource budget, and rules for finishing or escalating. Repetition alone is worthless when the evaluator cannot tell improvement from confident drift. [[Agent context engineering]] covers reconstructable state and recovery. [[Autoresearch]] shows the stronger form, with bounded trials, protected evaluation, evidence, selection, and rollback.

**Graph engineering** concerns execution topology. Nodes may be deterministic code, model calls, tools, or complete agents. Edges determine sequence, conditional routing, parallel work, joins, cycles, state transfer, and human gates. A fixed graph fits repeatable work with meaningful dependencies or authority boundaries. Open-ended exploration may need only a capable agent and a thin contract. This usage is separate from knowledge graph engineering.

A graph controls what runs next and crosses boundaries; a loop judges progress, repeats safely, and stops. Graphs can contain loops, and loops can construct or traverse graphs. Prompt engineering shapes one interaction, [[Agent context engineering|context engineering]] controls what each inference sees, and orchestration controls execution across interactions. Use agent orchestration as the broader term. Add explicit graphs or loops only when routing, state, evaluation, or recovery needs machinery beyond a provider-native loop. See [[Prompting tool-using agents]], [[Subagent delegation]], and [[AI-era software durability#Provider gravity in coding-agent harnesses]].

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
