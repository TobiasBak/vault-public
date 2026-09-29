# Agentic end-to-end testing

End-to-end testing with capable tool-using agents is now practical and unusually productive. An agent can operate the real interface, vary its path when the application responds unexpectedly, inspect APIs, logs, database state, configuration, and source code, and connect a visible symptom to its likely cause. It acts as an adaptive investigator across the running system rather than as a more verbose browser-test script.

This fills the gap between manual and scripted E2E testing. Humans are adaptable but expensive to repeat and scale. Deterministic browser tests are cheap to repeat but cover paths and assertions anticipated by their authors. Agents can cheaply repeat broad testing while still recognizing semantic anomalies, exploring nearby behavior, and investigating failures that were not specified in advance.

## Why it produces disproportionate value

- **Elastic exploration:** many independent agents can exercise different workflows, configurations, roles, inputs, and failure paths without scheduling a manual test effort.
- **Semantic judgment:** an agent can notice that a result is implausible or inconsistent even when the page rendered and no explicit assertion failed.
- **Cross-layer investigation:** computer use can be combined with request traces, logs, external-system state, source search, and focused commands instead of stopping at a screenshot.
- **Adaptive reproduction:** the agent can narrow a failure, change one condition at a time, and find a repeatable signal rather than merely report that a scripted step failed.
- **Short path from discovery to repair:** the same working context can support diagnosis, a scoped fix, and rerunning the original workflow when authority permits.
- **Low-cost recurrence:** exploratory coverage that was previously affordable only before important releases can run continuously or against every consequential change.

The important evidence is not that an agent can click through a UI, but that it can discover unexpected behavior and follow it across system boundaries.

## Productive loop

1. Give the agent a realistic running environment, representative inputs, relevant tools, and a clear authority boundary.
2. Define the workflow or product area and observable success criteria without prescribing every interaction.
3. Let it explore, preserve artifacts, and investigate anomalies through the narrowest relevant system surfaces.
4. Require a concrete reproduction and evidence such as screenshots, traces, outgoing requests, logs, or resulting database and external-system state.
5. Fix the responsible invariant or boundary when authorized, then rerun both the minimized reproduction and the original scenario.
6. Promote stable discoveries into the cheapest durable protection: a deterministic E2E or integration test, schema, validator, lint rule, permission, monitoring check, or clearer tool error.

The agent's declaration that a workflow works is not itself strong evidence. The harness should retain externally inspectable artifacts and make clean setup, isolation, reset, and replay cheap. Assertions should use a source of expected behavior independent of the implementation where possible; otherwise an agent can reproduce the system's misconception and call it correct.

## Reusable verification tools and feature maps

A verification skill needs a reliable way to operate the application and enough product knowledge to choose the right workflow. Lauren Tan's [Control Glass example](https://x.com/poteto/status/2102050467505430555/video/1) combines:

- A maintained CLI that launches and controls the application and collects traces, heap snapshots, and other evidence. Agents reuse it instead of writing new scripts each session.
- A feature map describing what the application does and how users reach each feature through navigation, controls, and shortcuts. It helps agents interpret vague reports and partial screenshots.

Keep both with the project verification skill and maintain them for the whole team. Tan's team automates feature-map updates. Agents can then find the relevant workflow and run it without a person interpreting each report or performing each check.

Runtime verification checks behavior and measures performance. Engineering skills guide diagnosis and implementation. Formal methods can establish stronger guarantees about specified invariants, but useful runtime checks do not depend on them. See [[Agentic engineering#Constrained codebases for low-context contributors]] for how these tools and architectural constraints support agent autonomy.

### The control CLI is a maintained interface

A feature map does not replace the ability to run the product. A project needs repeatable setup, known starting state, real user actions, inspection, and cleanup that preserves evidence. Existing commands may already supply these operations; a thin project-specific interface can connect the missing pieces. Rebuilding setup and capture scripts in each session leaves agents solving the same operational problems repeatedly.

A command name alone does not make a result reproducible. Keep the revision, scenario, fixture, relevant configuration, and observed result with the evidence. Another agent must be able to reconstruct the conditions and check the claim. Failures and blocked checks need explicit outcomes; an incomplete run is not a pass. Repeated runs must not inherit hidden state from earlier attempts or interfere with another agent's instance.

Maintain this interface alongside the product. Keep ordinary setup and command configuration in their executable owners, product navigation in the feature map, and project-specific investigation choices in the skill. [[Agent learning from experience and user feedback#Preserve demonstrated engineering methods]] covers extracting those choices from useful work.

### Fresh-agent handoff

A useful acceptance check for project tooling is whether a fresh agent can take a representative report, find the feature, reproduce the problem, make an authorized change, and demonstrate the result without extra operational instructions. Give it the repository and normal tools, not the previous agent's investigation. Repeating commands in the original context checks execution but does not establish that the handoff works.

Where it needs help identifies the next improvement. Trouble finding behavior points to the feature map or naming. Setup and inspection failures point to tools. Repeated diagnostic coaching belongs in a skill. Architectural mistakes call for a better supported API or enforced boundary. Unsupported success claims call for better checks and evidence.

Keep the result scoped to the tested workflow, model, and environment. Product decisions reserved for the human still belong to the human. This is a targeted check when improving autonomy, not a mandatory extra run after every edit. Confirm that the repaired gap no longer needs coaching before scaling the same work to more agents.

## Division of responsibility

Agentic E2E testing complements rather than replaces deterministic testing. Static checks and focused unit, integration, and browser tests remain fast hard gates for known invariants. Agents spend reasoning on broad exploration, ambiguous behavior, novel failures, and investigation. Once a behavior and its applicability become mechanically observable, [[Prompting tool-using agents#Promote settled cognition into machinery|promote it into machinery]] rather than paying an agent to rediscover it on every run.

### Prune tests by contract value

A test earns its place by detecting a broken contract or meaningful regression, not by demonstrating that code was added. Prefer assertions that survive an internal rewrite and still fail when observable behavior breaks. The expected result should come from requirements, real consumers, accepted examples, or independently established behavior rather than a copy of the implementation.

Judge the specific assertion, not its category. A provider fixture can protect a protocol boundary, a UI assertion can protect accessibility or an agreed presentation requirement, registration can be a discovery contract, and a performance test can protect a real latency or resource limit. Such tests need evidence that their expectations represent the contract; a simulation cannot establish compatibility with a live provider by itself.

Remove or rewrite tests that protect no independent requirement, merely mirror implementation structure, or duplicate an equally effective cheaper check. Keep useful detection of persistence, ordering, isolation, cleanup, validation, failure behavior, and other outcomes users or external systems rely on. Test count, coverage, and line reduction are not substitutes for that judgment. This is review knowledge, not a requirement to add a testing checklist to every agent prompt.

Routine human E2E execution is likely to become the exception. Humans remain important for unresolved product intent, taste, consequential acceptance decisions, and deciding whether surprising behavior is a defect. Their work moves from manually traversing known paths toward defining outcomes, improving environments and evaluators, reviewing disputed findings, and deciding which discoveries should reshape the product.

This is part of the broader [[AI-era software durability|software-factory shift]]. As implementation and test execution become cheap, clear intent, representative environments, trustworthy evidence, accepted real-world outcomes, and evaluator quality become the bottlenecks. A useful software factory does not merely produce code; it repeatedly exercises the resulting system, investigates divergence, and improves its own protections.
