# Verification tooling

Successive agents need to operate the same app and collect comparable evidence. A **control CLI** runs stable operations (start, readiness, reset, exercise, inspect, stop). The product CLI generates its **feature map** from case records: user-visible behavior, published entry points and covering cases. Never maintain a parallel map or README. The project's verification skill holds task steps the CLI cannot perform. Build them with `$create-verification-skill` and keep them honest with `$maintain-verification-skill`.

Principles that apply to any project:

- Reuse existing task runners, browser tools, and fixtures, and build only the missing operations. Commands stay in their executable owners.
- Use the real path. Fixtures set the starting state, but user actions must produce the result.
- Isolate mutable state per run, or state that only one session is supported.
- Return a short result with run ID, outcome, and artifact path. Logs go in artifacts.
- A failed prerequisite or incomplete check never looks like success.
- Keep revision, scenario, fixture, and config with the evidence. Derive expectations from the product contract, and note what a test double can't prove.
- Distinguish tool drift, stale map, and product regression. Never redefine expected results to hide a bug.
- Update the authoritative case records in the same change that alters behavior or entry points, then regenerate the map.

## A self-explanatory running system

Observability is an interface for agents, not just an incident add-on. Use inspectable state, structured logs, traces, and diagnostics to connect an operation to its effects, failures, and incomplete work. Preserve operation identities and causal links; collect evidence needed for diagnosis, excluding secrets and unnecessary personal data. A success log is not proof of an external effect: inspect authoritative state or read it back.

When changing recovery, exercise a representative partial failure through the real interface, inspect what actually happened, and use the supported retry, resume, or repair path. Confirm it does not duplicate effects or report incomplete work as success. Scope this proof to the changed contract, not every imaginable failure.

## Fresh-agent handoff check

Use it when judging readiness for independent work, not after every edit. Give a fresh agent a representative report, the repo, and normal tools, with no prior investigation. A rerun by the original agent only checks the commands. Then fix whatever it got stuck on:

- couldn't find the feature: feature map or naming
- couldn't start, reset, or inspect: tools
- couldn't establish what happened: observable state and causal diagnostics
- couldn't recover from relevant partial failure: explicit state and supported recovery
- needed a repeated method: skill
- repeated an architectural mistake: API or boundary
- claimed unsupported success: checks and evidence

Confirm the repair with another representative run.
