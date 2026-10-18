# APIs and protocols

Scope: every interface where one process calls another: HTTP APIs, webhooks and events, local IPC between processes, and interfaces agents call (MCP tools, CLIs). Builds on the [data catalog](data.md) and the [release catalog](release.md): commands are strict, servers deploy before clients, clients below the minimum version are refused.

Principles:
- Strict requests, tolerant responses.
- Rust types are the contract; schemas are generated from them.
- Every effect is safe to repeat.
- Add a mechanism when a tier needs it, not because large public APIs have it.

Tiers:
- **Internal:** we own both ends and ship them in one release. No API versions; additive changes are free, and the minimum supported version ([D13](data.md#d13-minimum-supported-version)) bounds skew.
- **External:** third parties we don't update. URL major versions (`/v1`).
- **Peer:** both ends installed independently and neither side controls the other's version, such as a host and its CLIs, plugins or MCP servers. A handshake (A12).

## Contracts

### A1 Declared tier

Every interface declares its tier. Our own components are internal even across processes; peer applies only where we don't control both installs.

Reason: each tier's rules cost something; the tier decides which apply.

Enforcement: each interface's generated schema (A3) carries its tier, and A4 applies that tier's rules.

### A2 Strict requests, tolerant responses

Servers reject unknown request fields and invalid values with a field error ([D8](data.md#d8-strict-commands)). Clients ignore unknown response fields and decode unknown enum values to a typed `Unknown` variant ([D4](data.md#d4-unknown-enum-values)). Command arguments are strict; protocol envelopes and capability lists are tolerant.

Reason: an unknown request field is a typo; an unknown response field is a newer server.

Enforcement: request types use `deny_unknown_fields`, response and envelope types never do, response enums have `Unknown(String)`; a static check enforces all three. Black-box cases: a misspelled request field gets a field error; the previous client reads a response with an extra field and an unknown enum value.

### A3 Code first

Rust types define the contract. The schema (OpenAPI for HTTP, JSON Schema for JSON-RPC) is generated from them and committed. API types are separate from storage types, converted in one place.

Reason: a hand-written spec drifts from the code; a shared type turns a storage refactor into an API break.

Enforcement: CI fails when the committed schema differs from the generated one; a static check rejects storage types in API signatures.

### A4 Breaking-change gate

CI diffs the generated schema against the last release. Breaking: removing or renaming a field, making a field required or adding a required request field, changing a type or default, narrowing accepted values, removing or repurposing an error code, and adding nulls or weakening a presence guarantee. Safe: adding optional request fields, response fields, endpoints and error codes. Changes to ordering, permissions or side effects are breaking too; the schema can't show them, so cross-version black-box cases cover them. Internal breaking changes take [D5](data.md#d5-two-step-destructive-changes)'s two steps; external ones need a new major (A5).

Reason: an agent will rename a field in one PR, and review won't catch every one.

Enforcement: the schema diff in pre-commit and CI; a black-box case runs the previous release's client against the new server.

### A5 External versions and retirement

A new external major is approval-class, and the old major stays for a published period. External enums are documented as open from v1, so new values are safe. Retiring an endpoint or major sends `Deprecation` ([RFC 9745](https://www.rfc-editor.org/rfc/rfc9745)) and `Sunset` ([RFC 8594](https://www.rfc-editor.org/rfc/rfc8594)) headers and tracks usage per API credential ([R16](release.md#r16-version-attributed-telemetry)). Removal is approval-class and waits for the sunset date and zero usage.

Reason: third parties don't auto-update; removing what they still call breaks them silently.

Enforcement: A4 blocks breaking changes within a major; the pipeline blocks removal while usage is nonzero.

## Calls

### A6 Errors

Errors are [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457) problem details plus a stable machine `code`, field-level errors and a `retryable` flag. Codes are never reused or removed. Clients branch on the code, never on message text. JSON-RPC `error.data` carries the same fields.

Reason: clients and agents need to know what failed and whether trying again helps, without parsing prose.

Enforcement: codes are one Rust enum in the generated schema; A4 treats removing a code as breaking; black-box cases assert codes, not messages.

### A7 Idempotent effects

Commands with effects follow [D18](data.md#d18-idempotent-commands). Reusing an ID with a different payload is an error (422); a duplicate while the original is still running gets 409. Callers keep the original ID and payload across retries and never issue a fresh ID after an uncertain outcome.

Reason: a timeout leaves the outcome unknown; a fresh ID turns the retry into a second order.

Enforcement: black-box cases: the same command twice gives one effect and the original result; the same ID with a different payload gets 422.

### A8 Retries and deadlines

One shared client library owns retries; no other layer retries. It retries only errors marked retryable, with exponential backoff, jitter and a cap, within a retry budget, and follows `Retry-After`. Every call has a deadline that propagates downstream, and servers stop work past it. 429 means the caller is over its limit; 503 means the server is overloaded. A timeout means the outcome is unknown: retry with the same operation ID (A7).

Reason: retries at several layers multiply (three layers of three tries is 27 calls) and turn a blip into an outage. Jitter keeps clients from retrying in lockstep ([AWS](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)).

Enforcement: a static check rejects network clients outside the shared library; black-box cases: a 503 with `Retry-After` gets bounded, spaced retries; a non-retryable error gets none.

### A9 Pagination and long work

List endpoints return cursors from the first version, with a stable sort, a unique tie-breaker and a maximum page size. No offsets. Work longer than a few seconds returns an operation resource the caller checks or gets an event for.

Reason: adding pagination later is breaking; offsets skip or repeat records under concurrent writes; long requests time out and get retried.

Enforcement: list response types require a cursor; black-box case: paging while records are inserted returns each record once.

### A10 Events and webhooks

Events are delivered at least once within a documented retry window, each with a unique ID and no ordering unless the event type states one. Payloads follow A2. Outgoing webhooks are signed. Receivers verify the signature, store the event durably before acknowledging, and dedupe by event ID. Missed events can be replayed from a point in time.

Reason: networks drop and repeat deliveries; a receiver that acknowledges before storing loses events on a crash.

Enforcement: black-box cases: a failed delivery is retried, a duplicate is processed once, a replay delivers missed events, a bad signature is rejected.

### A11 Interfaces for agents

MCP tools and CLIs that agents call follow the internal tier, plus errors that say how to fix the call, bounded output with a way to fetch more, and tool lists that are re-read, not cached.

Reason: agents act on error text and lose context to unbounded output; a cached tool list calls tools that changed.

Enforcement: black-box cases: an invalid call returns the field and the fix; a large result is bounded with a continuation.

## Process protocols

### A12 Peer handshake

Peers negotiate protocol version and capabilities before any work. A missing capability means the feature is unsupported. A version mismatch fails with an error naming both versions and what to update. Internal interfaces have no handshake.

Reason: independently installed peers meet at any versions; guessing breaks mid-session ([MCP lifecycle](https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle)).

Enforcement: A16's version-pair cases.

### A13 Bidirectional requests

Either side may send requests. The reader never blocks on a handler. Request IDs are unique per connection and direction. Each operation ends in exactly one final state; a cancel acknowledgement isn't one. Replies to unknown or finished requests are ignored and counted.

Reason: a reader blocked on a handler that waits for the peer deadlocks both.

Enforcement: A16's hostile-peer cases.

### A14 Transport and lifecycle

Messages are newline-delimited UTF-8 JSON. Stdout carries only protocol; logs go to stderr. Message size, queues and in-flight requests are bounded, and every request has a deadline. Shutdown closes stdin, waits, then terminates and finally kills the whole process group. A dead peer's connection is discarded and its pending requests end as unknown outcome; after a restart, uncertain writes are checked and resent only with their original operation ID.

Reason: one stray print corrupts the stream; unbounded queues turn a slow peer into memory exhaustion; orphaned children outlive the host.

Enforcement: A16's hostile-peer cases; a static check rejects stdout writes outside the protocol writer.

### A15 Protocol choice

JSON-RPC 2.0 over stdio between local processes; HTTP with JSON over the network. No gRPC without a concrete reason in the project's spec.

Reason: readable on the wire, debuggable with a text editor, and the shape MCP, LSP and ACP use.

Enforcement: a dependency check rejects gRPC crates unless the spec names the reason.

### A16 Protocol tests

Recorded real sessions replay as black-box cases. A hostile fake peer sends malformed and oversized messages, hangs, crashes, reads slowly, interrupts the handshake and replies late. Every supported pair of peer versions runs the handshake and a representative session.

Reason: protocol bugs show up at the edges real peers hit only in production.

Enforcement: these cases run in CI.
