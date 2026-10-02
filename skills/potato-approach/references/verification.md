# Verification tooling

Successive agents need to operate the same app and collect comparable evidence. A **control CLI** runs stable operations (start, readiness, reset, exercise, inspect, stop). A **feature map** connects user reports to those operations: what each feature does, how users reach it, and what result proves it worked. The project's verification skill explains the choices. Build them with `$create-verification-skill` and keep them honest with `$maintain-verification-skill`.

Principles that apply to any project:

- Reuse existing task runners, browser tools, and fixtures, and build only the missing operations. Commands stay in their executable owners.
- Use the real path. Fixtures set the starting state, but user actions must produce the result.
- Isolate mutable state per run, or state that only one session is supported.
- Return a short result with run ID, outcome, and artifact path. Logs go in artifacts.
- A failed prerequisite or incomplete check never looks like success.
- Keep revision, scenario, fixture, and config with the evidence. Derive expectations from the product contract, and note what a test double can't prove.
- Distinguish tool drift, stale map, and product regression. Never redefine expected results to hide a bug.
- Update affected feature-map entries in the same change that alters behavior or navigation.

## Fresh-agent handoff check

Use it when judging readiness for independent work, not after every edit. Give a fresh agent a representative report, the repo, and normal tools, with no prior investigation. A rerun by the original agent only checks the commands. Then fix whatever it got stuck on:

- couldn't find the feature: feature map or naming
- couldn't start, reset, or inspect: tools
- needed a repeated method: skill
- repeated an architectural mistake: API or boundary
- claimed unsupported success: checks and evidence

Confirm the repair with another representative run.
