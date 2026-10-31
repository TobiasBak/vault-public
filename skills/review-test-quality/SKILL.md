---
name: review-test-quality
description: Review tests for contract value and classify them keep, rewrite, delete, or uncertain. Use when writing, reviewing, refactoring, or pruning tests, especially when assertions mirror internals or tests obstruct changes.
---

# Review test quality

Judge each assertion, not its category. Copy, layout, CRUD, SDK arguments, registration, and performance are not deletion categories:

- Rendered text may be arbitrary wording or essential result data.
- A provider mock may mirror internal calls or verify required outgoing payloads. It never proves live compatibility.
- A thin wrapper may do nothing, or it may own persistence, cleanup, or discovery that callers rely on.

For each candidate, name the observable failure it detects, who relies on that behavior, and whether another check already catches it. Derive the requirement from a consumer, spec, persisted format, accepted example, or known regression, never from what the implementation happens to do. A real feature doesn't justify every test around it, and you shouldn't invent a contract to keep a test.

## Classify

- **Keep:** protects a meaningful contract at a useful boundary, with independent expectations.
- **Rewrite:** meaningful behavior behind brittle or weak assertions.
- **Delete:** no independent contract, or a cheaper identified check catches the same failure at a boundary that can prove it. Another entry point doesn't cover this one, and a model or unit check doesn't cover a native binding such as focus, key delivery or accessibility.
- **Uncertain:** hinges on an unstated requirement. Name the missing evidence.

Split tests that mix useful and disposable assertions. When merging or parameterizing, keep distinctions such as one input vs many, persisted vs returned state, and recovery vs success. For a meaningful contract, name the check that remains or the replacement it needs. Keep maintenance and flake cost proportional to the consequence of a missed regression. Count, line reduction, and coverage are not goals.

Rewrite signals, each a defect to fix:

- A fake of a dependency the product itself runs, such as its database, queue or cache. Test against the real one at the production version. Fake only external systems the product doesn't run, and base those fakes on recorded exchanges or the provider's published contract.
- A write proven by its own response instead of a readback through the interface or environment.
- Expected output accepted from a run without checking it against its source, or assertions on diagnostic dumps or incidental call order.
- Fixed sleeps, a real clock or randomness, shared mutable starting state, or GUI steps addressed by coordinates or test-only markup.

A test that breaks under an internal rewrite with no behavior change depends on internals. A regression test that passes on the pre-fix build doesn't reproduce its bug.

Replacing a whole suite, or moving GUI assertions into model checks, is a migration rather than pruning. In repositories that follow `$theodore-kaczynski-nullifier`, its proof boundaries, one case per behavior and entry point, suite migration proof and assertion transfer govern.

## Evidence

Run focused checks when they settle a dispute. A cheap vacuity probe: would the test still pass if the code under test returned nothing or a constant? An injected fault can show lost detection, but tie it to a real contract before calling it valuable. A passing suite doesn't prove that pruning kept useful coverage. Separate demonstrated loss from inference.

## Report

Lead with the recommendation and the inspected scope. For material findings, give the test, file, class, protected or missing contract, reason, and action, grouping related assertions. Say what ran, what wasn't inspected, and any product question left open. Say when a cut is sound.

## Verification

After an authorized test change, run the focused retained or replacement checks against the real consumer boundary. Confirm they still detect the named contract failure, using an existing regression or a targeted fault when needed. Report what remains unverified.
