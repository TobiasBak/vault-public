# Coalescing background work

Coalesce requests only when one attempt satisfies their obligations. Matching a source revision is not enough: a background cache hit does not fulfill an explicit request to execute again.

recheck-after: 2026-11-04

## Preserve request intent

Separate request intent from execution outcome. An automatic request can accept a completed result. An explicit execution request may join a suitable attempt in flight, but cannot be satisfied by a no-op. Preserve that distinction when coalescing them.

Keep admitted demand durable until an attempt covers it. Errors before the worker captures its input must not silently consume the request. Serialize admission with the worker's final pending-work check and ownership release, so a late request is either covered or left for a successor. Check the latest target when deciding whether pending work remains.

Test an explicit request queued behind an automatic no-op, not just two requests that overlap real execution. Also distinguish a failed attempt that must remain retryable from a completed result that can satisfy background demand.

## Publish completion, not just metadata

A record naming the intended revision does not prove that all reusable state was published. Write the completion state after the entire resource set exists, and make every reuse path consult the same completion boundary. An interrupted publication should trigger recovery, not a cache hit.

In the GAH case, a recursive snapshot's root becomes read-only last. Checking that state prevented reuse of a root whose metadata survived but whose nested build snapshot was absent. Do not generalize read-only state as a completion proof unless the publisher enforces that ordering.

## Synchronize tests on the obligation

Repeated admission can legitimately leave durable state unchanged. A test that waits for another file creation or rename can deadlock while the queue works correctly. Synchronize on acknowledged admission, hold execution at a controlled barrier, then assert the final input, attempt count and drained queue.

These lessons came from deterministic failures during qualification of the [GAH preservation case](cargo-target-cache.md#measured-preservation-result). They establish correctness, not a separately measured speedup.

See [API workflow semantics](api-design.md#workflow-semantics) for admission and execution contracts.
