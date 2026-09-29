---
name: review-test-quality
description: Review selected tests or test-cleanup changes for contract value and recommend keep, rewrite, delete, or uncertain classifications. Use only when Tobias explicitly invokes this named skill, not for ordinary implementation or code review.
---

# Review test quality

Review only the requested scope. Treat the review as read-only unless Tobias also authorizes editing or pruning tests. Preserve this skill's explicit-only invocation policy.

## Judge the assertion, not its category

Inspect assertions alongside the production behavior, real consumers, applicable contracts, and remaining tests or static checks. A test name, implementation shape, or use of mocks does not establish its value.

For each proposed removal, identify the observable failure it detects, who relies on that behavior, and whether another check detects the same failure. Derive the requirement from a consumer, specification, persisted format, accepted example, or known regression, not merely from what the implementation currently does.

Copy, layout, CRUD, SDK arguments, registration, and performance are not deletion categories. For example:

- Rendered text may be arbitrary wording or essential result data. Form fields may be an inventory or the browser's save contract. Judge those assertions separately.
- A provider mock may mirror internal calls or verify required outgoing payloads and routing. It cannot by itself establish compatibility with the live provider.
- A thin wrapper may do nothing worth testing or own persistence, cleanup, isolation, or discovery that callers rely on. Its size does not decide.

Conversely, the presence of a real feature does not justify every test around it. Delete unsupported presentation preferences, implementation inventories, and redundant checks when they protect no independent requirement. Do not invent a contract to retain them.

## Choose the smallest useful protection

- **Keep:** protects a meaningful contract at a useful boundary, with expectations independent of the implementation under test.
- **Rewrite:** protects meaningful behavior through brittle or weak assertions. Preserve that behavior while changing how it is checked.
- **Delete:** protects no meaningful independent contract, or an identified cheaper check already detects the same failure.
- **Uncertain:** depends on an unstated requirement or consumer. Name the missing evidence; do not guess that the behavior is required or disposable.

A test may contain both useful and disposable assertions. Remove the latter without losing the former. When merging or parameterizing tests, preserve important distinctions such as multiple inputs versus one, persisted state versus returned state, and failure recovery versus successful completion.

For a meaningful contract, name the remaining check or the replacement needed before removal. No replacement is needed for a test with no useful contract. Prefer a focused assertion or a coherent existing test over restoring a whole suite or adding a new test layer.

Keep the cost of maintenance, execution, and false failures proportional to the consequence of a missed regression. Test count, line reduction, and coverage percentages are not success criteria.

## Use evidence without overstating it

Run focused checks when they resolve a disputed finding or validate an authorized change. An injected fault can show that an old assertion detected a failure and the remaining suite does not. That demonstrates lost detection, not automatically a valuable test or a likely regression. Tie the failure to a real contract and assess the cost of retaining protection separately.

A passing suite does not prove that pruning preserved useful coverage. A test-only change that loses coverage is not itself a runtime defect. Distinguish demonstrated loss, inferred impact, and unverified assumptions; do not require mutation testing for every deletion.

## Report

Lead with the recommendation and inspected scope. For material findings, give the exact test and file, classification, protected or missing contract, reason, and proposed action. Explain which remaining or replacement checks own the important affected behaviors; group related assertions when clearer.

Report what ran, what remains uninspected, and any unresolved product decision. Say when a cut is sound. Do not manufacture findings or turn the report into an inventory of every test.

Background: [Agentic end-to-end testing](../../../Agentic%20engineering/Evaluation%20and%20improvement/Agentic%20end-to-end%20testing.md#prune-tests-by-contract-value).
