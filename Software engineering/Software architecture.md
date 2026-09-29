# Software architecture

Software architecture is the consequential structure and decisions that make a system fit its requirements. It covers boundaries, ownership of state and side effects, contracts, data and control flow, deployment and operations, safety and authority, and deliberate tradeoffs.

Architecture design is the work of choosing that structure from the problem, constraints, and desired qualities. It is not the act of selecting a fashionable pattern. Microservices are one possible deployment and ownership style, not a synonym for architecture.

## Recognizing an architectural decision

A decision is architectural when changing it would materially alter several components, state or side-effect ownership, contracts, deployment, operations and recovery, safety boundaries, or long-term coupling. Architecture usually answers:

- What forces and constraints shape the system?
- What are the major parts, and what does each own?
- Where is authoritative state, and who may change it?
- How do data and control cross boundaries?
- How is the system deployed, operated, observed, and recovered?
- Which quality is prioritized, what does that cost, and what change would invalidate the decision?

A class name or local algorithm is usually implementation design. Choosing a local worker instead of a remote service, separating probabilistic output from authoritative state, or deciding which component owns an external side effect is architectural because it shapes the wider system.

## Styles describe different dimensions

Real systems combine architectural styles rather than belonging to one exclusive category:

- **Layered architecture** organizes dependencies and responsibilities, often into presentation, application, domain, and infrastructure concerns.
- **Modular monolith** keeps one deployment while enforcing strong internal ownership boundaries.
- **Client-server** separates an interactive client from shared processing and state.
- **Pipeline** moves work through explicit transformation or validation stages.
- **Ports and adapters** isolate stable application capabilities from external mechanisms.
- **Worker architecture** assigns bounded background work to scheduled or queued workers.
- **Event-driven architecture** lets components react asynchronously to published facts.
- **Microservices** split independently deployed services and usually their state ownership, accepting distributed-system cost for independent deployment, scaling, or organizational ownership.

The same system may be a pipeline in its control flow, use ports and adapters at ERP boundaries, run through supervised workers, and deploy locally as one installation. The useful description names the dimensions that explain actual decisions.

## Design from drivers and tradeoffs

Use the method in [[Tobias's developer preferences#Aspirational engineering method]]:

1. Define the problem, outcome, constraints, and important qualities.
2. Inspect the existing domain, system, contracts, and failure modes.
3. Assign boundaries, state ownership, authority, and data flow.
4. Compare structures and make their benefits and costs explicit.
5. Prototype the riskiest architectural assumption.
6. Validate representative behavior and failure recovery.
7. Implement and observe incrementally.
8. Record what future change would justify revisiting the architecture.

Explain an architectural decision as **driver → decision → structure → consequence → change trigger**. Naming components without the driver and tradeoff describes a diagram, not the reasoning behind it.

## Ports and adapters in plain terms

A port expresses a capability the application needs in business terms. An adapter translates that capability into the API, GUI, protocol, and data model of a concrete external system. The application depends on the port; vendor mechanics stay in the adapter.

Adapters do not need to perform identical technical steps. They must satisfy the same business contract: compatible meaning, required information, success conditions, and failure behavior. A useful test is whether the shared workflow can use either adapter and continue correctly without vendor-specific branching.

If one adapter attaches a drawing while another creates a part, both operations can implement the same port only when they produce the business outcome promised by that port. If one silently omits a required outcome, or callers must add vendor flags and exceptions, the shared interface is lying. Keep only genuinely shared semantics in the port and model materially different capabilities or workflows explicitly. This is the same shared-semantics principle described in [[API design]].

## Integration architecture examples

An order-integration system illustrates decisions that matter without requiring microservices:

- **Probabilistic output is not authoritative state.** Extraction produces a draft; validation and human approval guard consequential ERP actions. This trades full autonomy for correctness, accountability, and recoverability. [[AI-era software durability]] describes the broader boundary.
- **ERP-specific mechanics stay behind target adapters.** The shared workflow deals in target plans and results rather than vendor API calls. This keeps vendor volatility out of the workflow while accepting installation-specific adapters.
- **Workers run close to customer systems.** Supervised Windows workers fit ERP and GUI constraints and avoid distributed orchestration, at the cost of customer-specific deployment and weaker centralized scaling.
- **Receipts, archives, evidence, and telemetry are structural.** They make retries, diagnosis, recovery, and operational ownership possible rather than treating failures as incidental exceptions.

Repositories remain authoritative for implementation and live deployment topology.
