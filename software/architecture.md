# Software architecture

Architecture is the consequential structure that makes a system fit its requirements: boundaries, state and side-effect ownership, contracts, data and control flow, deployment and operations, safety and authority, and deliberate tradeoffs. Microservices are one deployment style, not a synonym for it.

## Is this decision architectural?

It is when changing it would materially alter several components, state ownership, contracts, deployment, recovery, safety boundaries, or long-term coupling. Examples: a local worker vs a remote service, separating probabilistic output from authoritative state, or deciding who owns an external side effect. A class name or local algorithm is implementation design.

Questions architecture answers: What forces shape the system? What are the parts and what does each own? Where is authoritative state and who may change it? How do data and control cross boundaries? How is it deployed, observed, and recovered? Which quality wins, at what cost, and what would invalidate the choice?

## Styles are dimensions, not categories

Real systems combine them: layered, modular monolith, client-server, pipeline, ports and adapters, workers, event-driven, microservices (independent deploys and state, at distributed-systems cost). One system can be a pipeline in control flow, use ports and adapters at ERP boundaries, run on supervised workers, and ship as one install. Name the dimensions that explain real decisions.

## Explaining a decision

Use **driver → decision → structure → consequence → change trigger**. Naming components without drivers and tradeoffs just describes a diagram. The design process follows [Tobias's method](../tobias/preferences.md#method-for-hard-problems), plus a recorded trigger for revisiting.

## Ports and adapters

A port is a capability the application needs, in business terms. An adapter translates it to a concrete system's API, GUI, or data model. Adapters may take different technical steps but must satisfy the same business contract: meaning, required information, success, and failure. The test is whether the shared workflow can use either adapter with no vendor branching. If one adapter silently omits an outcome, or callers need vendor flags, the port is lying. Keep only genuinely shared semantics in it and model different capabilities explicitly.

## Integration example (order automation)

- **Extraction yields a draft, not truth.** Validation and human approval guard consequential ERP actions, trading autonomy for accountability.
- **ERP mechanics stay behind target adapters.** The workflow deals in target plans and results.
- **Workers run near customer systems.** Supervised Windows workers fit ERP and GUI constraints and avoid distributed orchestration, at the cost of per-customer deployment.
- **Receipts, archives, evidence, and telemetry are structural.** They make retry, diagnosis, and recovery possible.
