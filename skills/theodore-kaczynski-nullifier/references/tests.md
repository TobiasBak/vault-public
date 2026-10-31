# Tests

A test earns its place by catching a broken contract someone relies on, through a published interface, with expectations from an independent source.

Two of Tobias's [repository rules](../SKILL.md#repository-rules) govern every test here: black-box contracts, not private internals, and no GUI tests. Exercise each contract through the cheapest production interface that can prove it, including a model's public API. Test count, suite size and launching the whole app do not establish value.

| Job | Read |
|---|---|
| Choosing the proof boundary, moving UI rules into a production model, renderless builds | [behavioral-boundaries.md](behavioral-boundaries.md) |
| Writing or changing tests: real dependencies and fakes, corpus cases, expected output, runner, budgets, failure output, bug regressions, replacing a suite | [black-box-tests.md](black-box-tests.md) |

## Judge each assertion

Judge each assertion, not its category. Copy, layout, CRUD, SDK arguments, registration, and performance are not deletion categories:

- Returned text may be arbitrary wording or essential result data.
- A provider fake may mirror internal calls or verify required outgoing payloads. It never proves live compatibility.
- A thin wrapper may do nothing, or it may own persistence, cleanup, or discovery that callers rely on.

For each candidate, name the observable failure it detects, who relies on that behavior, and whether another check already catches it. Derive the requirement from a consumer, spec, persisted format, accepted example, or known regression, never from what the implementation happens to do. A real feature doesn't justify every test around it, and you shouldn't invent a contract to keep a test.

## Classify

- **Keep:** protects a meaningful contract at a useful boundary, with independent expectations.
- **Rewrite:** meaningful behavior behind brittle or weak assertions, or behind anything the [box](black-box-tests.md#the-box), [scenario](black-box-tests.md#large-scenario-cases) or [forbidden](black-box-tests.md#forbidden) rules reject: a fake of a dependency the product runs, a write proven by its own response, expected values with no independent source, inputs that can't tell the bug from the fix, an exact snapshot of output another contract owns, fixed delays, or shared mutable starting state.
- **Delete:** no independent contract; a cheaper identified check catches the same failure at a boundary that [can prove it](behavioral-boundaries.md#match-the-proof-to-the-obligation); a copy of another scenario that varies one input; or any GUI test.
- **Uncertain:** hinges on an unstated requirement. Name the missing evidence.

Split tests that mix useful and disposable assertions. When merging or parameterizing, keep distinctions such as one input vs many, persisted vs returned state, and recovery vs success. For a meaningful contract, name the check that remains or the replacement it needs. Keep maintenance, runtime and flake cost proportional to the consequence of a missed regression. Count, line reduction, and coverage are not goals.

Replacing a whole suite is a [migration](black-box-tests.md#migrating-an-existing-suite), not pruning. Deleting GUI tests needs no migration proof: move any rule they protected into its [production model](behavioral-boundaries.md#make-the-model-the-production-owner) and prove it there.

## Evidence

Run focused checks when they settle a dispute.

- **Vacuity:** would the test still pass if the code under test returned nothing or a constant?
- **Discrimination:** name the plausible wrong implementation, such as the bug being fixed, a neighbouring rule, or a dropped dimension like date, period, identity or cached state. Would the case's inputs produce a different output under it? The same value at both dates can't test a date key; one receipt spanning two quarters can't test per-quarter allocation; a fault control without a pre-cached sibling can't test the cached path.
- **Checker blind spots:** a pass is only as good as the comparison behind it. [Prove the checker](black-box-tests.md#prove-the-checker) before relying on a new canonicalizer, comparator, exception or gate.

An injected fault can show lost detection, but tie it to a real contract before calling it valuable. A passing suite doesn't prove that pruning kept useful coverage. Separate demonstrated loss from inference.

## Report

Lead with the recommendation and the inspected scope. For material findings, give the test, file, class, protected or missing contract, reason, and action, grouping related assertions. Say what ran, what wasn't inspected, and any product question left open. Say when a cut is sound.

## Verification

- **Pruning or rewriting:** after an authorized change, run the focused retained or replacement checks against the real consumer boundary. Confirm they still detect the named contract failure, using an existing regression or a targeted fault when needed. Report what remains unverified.
- **Bug fix:** the extended check [fails on the pre-fix build](black-box-tests.md#lifecycle) with the reported symptom, covers the defect's class rather than only the reported witness, and passes on the fix.
- **Suite deletion:** the [replacement proof](black-box-tests.md#migrating-an-existing-suite). A failed pilot can stop a migration, never authorize deletion.
