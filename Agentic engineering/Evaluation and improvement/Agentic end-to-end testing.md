# Agentic end-to-end testing

Tool-using agents can operate an application, adapt to unexpected responses, and investigate symptoms through APIs, logs, database state, configuration, and source. Their value depends on the workflow, environment, model, and evidence.

Deterministic browser tests repeat known paths and assertions. Agents can explore nearby behavior, notice semantic anomalies, and investigate unforeseen failures, but add model cost and variable execution. Flexibility alone proves neither better coverage nor lower cost than manual or scripted tests.

## Where it can help

- **Parallel exploration:** independent agents can exercise different workflows, configurations, roles, inputs, and failure paths when environments and mutable state are isolated.
- **Semantic judgment:** an agent can notice that a result is implausible or inconsistent even when the page rendered and no explicit assertion failed.
- **Cross-layer investigation:** computer use can be combined with request traces, logs, external-system state, source search, and focused commands instead of stopping at a screenshot.
- **Adaptive reproduction:** the agent can narrow a failure, change one condition at a time, and find a repeatable signal rather than merely report that a scripted step failed.
- **Short path from discovery to repair:** the same working context can support diagnosis, a scoped fix, and rerunning the original workflow when authority permits.
- **Repeatable exploration:** maintained setup and inspection tools can make exploratory checks practical to repeat without rebuilding the test environment each session.

Useful evidence shows an agent discovering unexpected behavior and tracing it across system boundaries, not merely clicking through a UI. Agents fit ambiguous behavior and cross-layer investigation where authoritative state can confirm findings. Deterministic checks usually suit stable known invariants. Unclear expectations, unreliable resets, or inaccessible state can produce false alarms, setup failures, and unverifiable claims. [[AI lead developer workflow strategy]] owns the proposed local pilot and comparison criteria, not a demonstrated outcome.

## Productive loop

1. Give the agent a realistic running environment, representative inputs, relevant tools, and a clear authority boundary.
2. Define the workflow or product area and observable success criteria without prescribing every interaction.
3. Let it explore, preserve artifacts, and investigate anomalies through the narrowest relevant system surfaces.
4. Require a concrete reproduction and evidence such as screenshots, traces, outgoing requests, logs, or resulting database and external-system state.
5. Fix the responsible invariant or boundary when authorized, then rerun both the minimized reproduction and the original scenario.
6. Promote stable discoveries into the cheapest durable protection: a deterministic E2E or integration test, schema, validator, lint rule, permission, monitoring check, or clearer tool error.

An agent's success claim is not strong evidence on its own. Retain inspectable artifacts and make clean setup, isolation, reset, and replay cheap. Derive expected behavior independently of the implementation where possible, or the agent may validate the same misconception.

## Reusable verification tools and feature maps

A verification skill needs a reliable way to operate the application and enough product knowledge to choose the right workflow. Lauren Tan's [Control Glass example](https://x.com/poteto/status/2102050467505430555/video/1) combines:

- A maintained CLI that launches and controls the application and collects traces, heap snapshots, and other evidence. Agents reuse it instead of writing new scripts each session.
- A feature map describing what the application does and how users reach each feature through navigation, controls, and shortcuts. It helps agents interpret vague reports and partial screenshots.

Keep both with the shared project verification skill so agents can find and run workflows without repeated human help. Tan's team automates feature-map updates.

Runtime checks verify behavior and measure performance; engineering skills guide diagnosis and implementation. Formal methods can strengthen specified guarantees but are not prerequisites for useful runtime checks. See [[Agentic engineering#Constrained codebases for low-context contributors]].

### The control CLI is a maintained interface

A feature map cannot run the product. Provide repeatable setup, known starting state, real user actions, inspection, and cleanup that preserves evidence. Reuse existing commands and connect missing operations through a thin interface instead of rebuilding setup and capture scripts each session.

Keep revision, scenario, fixture, configuration, and observed result with the evidence so another agent can reconstruct and check it. Report failed and blocked checks explicitly; incomplete runs are not passes. Repeated runs must not inherit hidden state or interfere with another instance.

Maintain the interface with the product. Executable owners hold setup and commands, feature maps hold navigation, and skills hold investigation choices. [[Agent learning from experience and user feedback#Preserve demonstrated engineering methods]] covers extracting those choices.

### Fresh-agent handoff

Give a fresh agent a representative report, the repository, and normal tools, not the previous investigation. Can it find the feature, reproduce the problem, make an authorized change, and prove the result without operational coaching? Repeating commands in the old context checks execution, not handoff.

A fresh agent's difficulties identify the next repair: feature maps or names for discovery, tools for setup and inspection, skills for repeated diagnostic coaching, APIs or enforced boundaries for architectural mistakes, and checks and evidence for unsupported success claims.

Keep conclusions scoped to the workflow, model, and environment, and preserve human product authority. Use this check to improve autonomy, not after every edit. Confirm that repairs remove coaching needs before scaling.

## Division of responsibility

Static checks and focused unit, integration, and browser tests remain hard gates for known invariants. Agents handle exploration, ambiguity, novel failures, and investigation. Once behavior and applicability become mechanically observable, [[Prompting tool-using agents#Promote settled cognition into machinery|promote them into machinery]] instead of paying for repeated rediscovery.

### Prune tests by contract value

Keep tests that detect broken contracts or meaningful regressions across internal rewrites, not merely code additions. Derive expected results from requirements, consumers, accepted examples, or independently established behavior, not copied implementation.

Judge assertions, not categories. Provider fixtures can protect protocols. UI assertions can protect accessibility or agreed presentation; registration can be a discovery contract. Performance tests can protect real latency or resource limits. Their expectations must represent the contract; simulations alone cannot establish live-provider compatibility.

Remove or rewrite tests with no independent requirement, tests that mirror structure, and checks duplicated by equally effective cheaper ones. Keep useful detection of persistence, ordering, isolation, cleanup, validation, failures, and relied-on outcomes. Counts, coverage, and line reduction do not replace judgment or justify a checklist in every prompt.

Automation can reduce manual traversal of known paths. Humans still resolve product intent, apply taste, accept consequential outcomes, and judge surprising behavior.

Clear intent, representative environments, trustworthy evidence, and evaluator quality still limit automation. More code or test runs do not prove the system works. See [[AI-era software durability]].
