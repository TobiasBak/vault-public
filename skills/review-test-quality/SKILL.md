---
name: review-test-quality
description: Write, review, prune, and migrate tests as black-box checks of published contracts. Use when writing or changing tests, choosing a proof boundary, real dependencies or fakes, designing corpus or GUI cases, reviewing or deleting tests, or when assertions mirror internals or tests obstruct changes.
---

# Review test quality

A test earns its place by catching a broken contract someone relies on, through a published interface, with expectations from an independent source.

**Black-box contracts, not private internals,** is Tobias's chosen policy for agent-maintained repositories; changing it needs his explicit agreement. Exercise each contract through the cheapest production interface that can prove it, including a model's public API. Test count and launching the whole app do not establish value.

| Job | Read |
|---|---|
| Choosing the proof boundary, separating model rules from native mechanisms, renderless builds, transferring GUI assertions | [behavioral-boundaries.md](references/behavioral-boundaries.md) |
| Writing or changing tests: real dependencies and fakes, corpus and GUI cases, expected output, runner, failure output, bug regressions, replacing a suite | [black-box-tests.md](references/black-box-tests.md) |

## Judge each assertion

Judge each assertion, not its category. Copy, layout, CRUD, SDK arguments, registration, and performance are not deletion categories:

- Rendered text may be arbitrary wording or essential result data.
- A provider fake may mirror internal calls or verify required outgoing payloads. It never proves live compatibility.
- A thin wrapper may do nothing, or it may own persistence, cleanup, or discovery that callers rely on.

For each candidate, name the observable failure it detects, who relies on that behavior, and whether another check already catches it. Derive the requirement from a consumer, spec, persisted format, accepted example, or known regression, never from what the implementation happens to do. A real feature doesn't justify every test around it, and you shouldn't invent a contract to keep a test.

## Classify

- **Keep:** protects a meaningful contract at a useful boundary, with independent expectations.
- **Rewrite:** meaningful behavior behind brittle or weak assertions, or behind anything the [box](references/black-box-tests.md#the-box), [scenario](references/black-box-tests.md#large-scenario-cases), [GUI](references/black-box-tests.md#gui-cases) or [forbidden](references/black-box-tests.md#forbidden) rules reject: a fake of a dependency the product runs, a write proven by its own response, expected values with no independent source, fixed delays, coordinates, or shared mutable starting state.
- **Delete:** no independent contract, or a cheaper identified check catches the same failure at a boundary that [can prove it](references/behavioral-boundaries.md#match-the-proof-to-the-obligation). Another entry point doesn't cover this one, and a model check doesn't cover a native binding.
- **Uncertain:** hinges on an unstated requirement. Name the missing evidence.

Split tests that mix useful and disposable assertions. When merging or parameterizing, keep distinctions such as one input vs many, persisted vs returned state, and recovery vs success. For a meaningful contract, name the check that remains or the replacement it needs. Keep maintenance and flake cost proportional to the consequence of a missed regression. Count, line reduction, and coverage are not goals.

Replacing a whole suite is a [migration](references/black-box-tests.md#migrating-an-existing-suite), and moving GUI assertions into model checks is an [assertion transfer](references/behavioral-boundaries.md#transfer-assertions-without-transferring-away-the-native-proof). Neither is pruning.

## Evidence

Run focused checks when they settle a dispute. A cheap vacuity probe: would the test still pass if the code under test returned nothing or a constant? An injected fault can show lost detection, but tie it to a real contract before calling it valuable. A passing suite doesn't prove that pruning kept useful coverage. Separate demonstrated loss from inference.

## Report

Lead with the recommendation and the inspected scope. For material findings, give the test, file, class, protected or missing contract, reason, and action, grouping related assertions. Say what ran, what wasn't inspected, and any product question left open. Say when a cut is sound.

## Verification

- **Pruning or rewriting:** after an authorized change, run the focused retained or replacement checks against the real consumer boundary. Confirm they still detect the named contract failure, using an existing regression or a targeted fault when needed. Report what remains unverified.
- **Bug fix:** the extended check [fails on the pre-fix build](references/black-box-tests.md#lifecycle) with the reported symptom and passes on the fix.
- **Assertion transfer:** its [five steps](references/behavioral-boundaries.md#transfer-assertions-without-transferring-away-the-native-proof), including the retained native scenario.
- **Suite deletion:** the [replacement proof](references/black-box-tests.md#migrating-an-existing-suite). A failed pilot can stop a migration, never authorize deletion.
