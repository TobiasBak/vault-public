# Verification CLIs

A verification CLI lets successive agents operate the same application and collect comparable evidence. The skill describes the method; the CLI executes stable operations; the [feature map](feature-map.md) connects user reports to those operations.

Build only what the project lacks. Existing task runners, browser tools, test fixtures, and application commands may already provide most of the interface. Add a thin project-specific command where agents otherwise repeat fragile setup or invent scripts.

## Establish a repeatable run

Inspect how the project starts, acquires test data, exposes controls, and reports results. Reuse that machinery. The interface needs to cover the following operations, though they need not be separate commands:

| Operation | Required result |
|---|---|
| Start | Launch the intended build and identify the instance this run owns |
| Check readiness | Establish that this instance is reachable and ready for the requested workflow |
| Prepare or reset | Establish the named data, role, and configuration without depending on a previous run |
| Exercise | Perform the real user actions through the existing control tool |
| Inspect and record | Capture visible results and relevant persisted state, requests, traces, or measurements |
| Stop | Clean up this run's processes and scratch state while preserving its evidence |

Isolate mutable state when runs may overlap. If the application only supports one verification session, make that restriction explicit rather than letting agents interfere with each other.

Use the real application path. Do not make a checkout scenario pass by inserting the expected order directly into the database. Fixtures establish starting state; user actions must produce the result under test.

## Make results usable

Return a short result with the run identifier, requested operation, outcome, and artifact location. Use machine-readable output when another tool consumes it. Keep detailed logs and traces in artifacts rather than flooding the agent's context.

A failed prerequisite or incomplete check must not look like success. Report what failed, what was attempted, and which required input or condition is missing. Preserve partial evidence so the next attempt starts from facts.

Keep the revision, scenario, fixture, relevant configuration, and observed results with the evidence. Control time, randomness, or external dependencies when they affect the comparison. Reproducibility means another run can reconstruct the conditions and check the claim; it does not require byte-identical logs.

Derive expected results from the product contract or known examples, not from the implementation being checked. Record what a test double establishes and what still needs a live integration check.

## Build and maintain the interface

Start with a workflow that currently requires human help. Implement its missing operations and run it from setup through cleanup. Repeat from a clean starting state to expose hidden dependencies. Confirm that the evidence survives cleanup.

Keep command definitions and ordinary setup in their existing executable owners. A verification skill should explain the project-specific choices and link to the commands, not maintain a second copy of their configuration.

When an application change breaks a command, distinguish tool drift from a product regression. Repair the responsible component and rerun the original scenario. Never turn a skipped or blocked check into a passing result to keep automation moving.

Use [Engineering workflows](engineering-workflows.md) for the investigation method, including before-and-after performance comparisons. A CLI should provide the operations without hard-coding every diagnosis.

## Check the fresh-agent handoff

Use this when judging whether the project's verification setup is ready for more independent work. It is a focused real-use check, not an extra ritual for every edit.

Give a fresh agent a representative report, the repository, its normal skills and tools, and a clear task boundary. Do not supply the previous investigation or an extra sequence of operational steps. If a fresh session is unavailable, a rerun by the original agent can check the commands but does not establish that the handoff works.

Observe whether it can find the feature, reproduce the problem, make an authorized change, and demonstrate the result. Keep its evidence and the places where it needed help. Product decisions reserved for the user remain user decisions; needing those does not mean the tooling failed.

Use the failure to choose the repair:

- Could not find the behavior: improve the feature map or naming.
- Could not start, reset, or inspect it: improve the control tools.
- Needed a repeated investigation method: improve the project skill.
- Repeated an architectural mistake: improve the supported API or enforced boundary.
- Claimed success without the required result: improve the check and its evidence.

Confirm the repaired gap in another representative run. Judge the result for that workflow, model, and environment. One successful task does not establish independence across the entire project.

This handoff check is our practical test of reduced human dependence, not a procedure quoted from Lauren Tan's talk.
