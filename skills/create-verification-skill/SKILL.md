---
name: create-verification-skill
description: Create a project-local verification skill and case-derived feature map that launch the real app and prove behavior through its published non-GUI interfaces. Use when a project needs a reusable verification or control workflow and lacks tested instructions for launching and exercising the real app.
---

# Create a verification skill

Give the next agent a tested way to launch the real app, exercise features, and keep proof. Write for an agent arriving cold.

Tobias allows no GUI tests: verification never drives a GUI, browser or accessibility tree as a verdict and never compares screenshots. Behavior is proved through the CLI, HTTP or MCP API, file contract, or a production model's public API. `$theodore-kaczynski-nullifier` owns those test rules; this skill doesn't restate them.

## Learn from the repo, not the user

Discover these yourself, and ask only about what you can't find:
- the published non-GUI interfaces (CLI, HTTP or MCP API, file contract, library or production model) and, for a GUI app, the model that owns its UI rules
- how the build starts, becomes ready, and gets data, config, and auth
- how to drive it, reusing the product verification CLI, existing cases, PTY helpers, or endpoints first
- what proves a result: responses, exit codes, persisted data, model output, recorded requests, traces
- how to isolate runs (data dirs, profiles, ports, sessions), or else state a single-driver restriction

Use a verification-owned instance with disposable state, never the user's live instance. If the checkout can't start, find out why, then fix it or report the cause and blocker. Don't write instructions against a broken base.

## Write the skill

Default to `.agents/skills/verify-<app>/` unless the project has its own convention. Include `SKILL.md` and `agents/openai.yaml` (starter prompt `$verify-<app>`), with invocation policy matching the repo. Ground every step in commands you actually ran:

- **Launch:** start the intended build, identify this run's instance, check readiness, and tear down. A short-lived CLI gets a fresh invocation or PTY per drive.
- **Doctor:** a cheap read-only check that this is the intended build with its prerequisites. Run it before driving and after surprises.
- **Drive:** real commands, requests and stable handles (routes, prompt strings, operation names), never a GUI driver or coordinates.
- **Explore:** for a GUI app, how to open it so an agent can reproduce a reported bug or judge a design. Capture only the app window, never the host desktop. Exploration never produces a verdict; what it finds becomes a model or API case.
- **Evidence:** a named artifact location capturing actions and resulting state. Confirm side effects through a second view. No secrets in shareable artifacts.
- **Cleanup:** stop only what this run owns, never by process name. Remove scratch, keep proof, and clean failed attempts too.
- **Verification:** real user paths. Fixtures set the starting state, but internal setters and test-only endpoints must not manufacture the result. Use doubles only at external boundaries and note what needs a live check.

Shipped helpers must be executable and documented. Command definitions stay in their executable owners. Don't trust a mode's name: check what "dry-run" or "test" mode actually writes or contacts.

## Derive the feature map from cases

The product CLI's `map [area]` generates behavior, entry points and covering cases from the case records. Never add a handwritten feature map or README. Reuse the repository's case schema, runner and map command; if they are missing, establish the first real scenario and derive its navigation from that record rather than creating a second authority.

A case records the outcomes and entry points it covers, its input and starting state, expected output and effects, an independent oracle, and its measured budget, in the case layout `$theodore-kaczynski-nullifier` defines. Domain behavior is covered once, at its cheapest entry point; each other entry point has a case for its own mechanism. Extend an existing scenario before adding another; different starting states remain isolated. GUI interactions are never map entries. Commands stay in executable owners. The skill holds only task steps the CLI cannot perform.

## Verification

Run the generated instructions end to end: launch, doctor, find a behavior with the generated map, execute its covering case through the published interface, read back its effects, and clean up. Confirm the map reflects the case records without a separately maintained feature file. Confirm the proof survives cleanup and nothing owned by the run remains. Fix and rerun failed steps; a skill never run against the app is a draft. Report what passed and what's blocked. Point to `$maintain-verification-skill` for upkeep.
