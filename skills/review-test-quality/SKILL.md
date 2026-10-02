---
name: review-test-quality
description: Review selected tests or test-cleanup changes for contract value and classify them keep, rewrite, delete, or uncertain. Use only when this skill is invoked by name, not for ordinary implementation or code review.
disable-model-invocation: true
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
- **Delete:** no independent contract, or a cheaper identified check catches the same failure.
- **Uncertain:** hinges on an unstated requirement. Name the missing evidence.

Split tests that mix useful and disposable assertions. When merging or parameterizing, keep distinctions such as one input vs many, persisted vs returned state, and recovery vs success. For a meaningful contract, name the check that remains or the replacement it needs. Keep maintenance and flake cost proportional to the consequence of a missed regression. Count, line reduction, and coverage are not goals.

## Evidence

Run focused checks when they settle a dispute. An injected fault can show lost detection, but tie it to a real contract before calling it valuable. A passing suite doesn't prove that pruning kept useful coverage. Separate demonstrated loss from inference.

## Report

Lead with the recommendation and the inspected scope. For material findings, give the test, file, class, protected or missing contract, reason, and action, grouping related assertions. Say what ran, what wasn't inspected, and any product question left open. Say when a cut is sound. Background: [testing with agents](../../agents/testing-with-agents.md#pruning-tests).
