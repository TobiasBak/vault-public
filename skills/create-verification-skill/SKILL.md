---
name: create-verification-skill
description: Create a project-local verification skill and feature map that drive the real app. Use when asked to build a reusable verification or control workflow for a project.
disable-model-invocation: true
---

# Create a verification skill

Give the next agent a tested way to launch the real app, exercise features, and keep proof. Write for an agent arriving cold.

## Learn from the repo, not the user

Discover these yourself, and ask only about what you can't find:
- the primary interface (browser, CLI/TUI, desktop, mobile, API, library)
- how the build starts, becomes ready, and gets data, config, and auth
- how to drive it, reusing existing commands, tests, browser tools, PTY helpers, or endpoints first
- what proves a result: visible state, responses, exit codes, persisted data, requests, traces
- how to isolate runs (data dirs, profiles, ports, sessions), or else state a single-driver restriction

Use a verification-owned instance with disposable state, never the user's live instance. If the checkout can't start, fix it or report the blocker. Don't write instructions against a broken base.

## Write the skill

Default to `.agents/skills/verify-<app>/` unless the project has its own convention. Include `SKILL.md` and `agents/openai.yaml` (starter prompt `$verify-<app>`), with invocation policy matching the repo. Ground every step in commands you actually ran:

- **Launch:** start the intended build, identify this run's instance, check readiness, and tear down. A short-lived CLI gets a fresh invocation or PTY per drive.
- **Doctor:** a cheap read-only check that this is the intended build with its prerequisites. Run it before driving and after surprises.
- **Drive:** real commands and stable handles (accessible names, routes, prompt strings), not coordinates.
- **Evidence:** a named artifact location capturing actions and resulting state. Confirm side effects through a second view. No secrets in shareable artifacts.
- **Cleanup:** stop only what this run owns, never by process name. Remove scratch, keep proof, and clean failed attempts too.
- **Verification:** real user paths. Fixtures set the starting state, but internal setters and test-only endpoints must not manufacture the result. Use doubles only at external boundaries and note what needs a live check.

Shipped helpers must be executable and documented. Command definitions stay in their executable owners. Don't trust a mode's name: check what "dry-run" or "test" mode actually writes or contacts.

## Seed the feature map

Add `features/README.md` plus feature files covering a few important workflows. Each entry gives what the feature does, how users reach it (including entry points that change behavior), starting state, how to drive it, the observable proof, and gotchas. Shared setup stays in the skill. For the shape, see the fictional [example](references/feature-map-example/README.md); don't copy its commands.

## Verification

Run the generated instructions end to end: launch, doctor, at least one mapped feature, cleanup. Confirm the proof survives cleanup and nothing owned by the run remains. Fix and rerun failed steps; a skill never run against the app is a draft. Report what passed and what's blocked. Point to `$maintain-verification-skill` for upkeep.
