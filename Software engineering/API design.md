# API design

A good API makes domain semantics explicit and transport mechanics incidental. Choose the protocol style from actual consumers, deployment, and interoperability rather than treating REST, RPC, GraphQL, or a TypeScript-native protocol as intrinsically best. See [[TypeScript 7 ecosystem]].

## Design from the consumer's domain

Organize operations around the concepts callers understand. Prefer `session.prompt({ sessionID, text })` over exposing generated HTTP plumbing such as separate `path`, `query`, and `body` objects. Group methods by domain capability and use action operations where the domain has meaningful lifecycle semantics; forcing every operation into CRUD can obscure rather than simplify.

An interface includes everything callers must understand to use it correctly: values and operations, invariants, ordering constraints, errors, configuration, and relevant performance behavior. Introduce seams for concrete variability, and keep internal or test-only seams from widening the caller-facing contract.

A client projection may be more ergonomic than the wire representation:

- flatten path, query, header, and payload fields into one unambiguous input;
- omit an argument when there is no input and make it optional only when every field is optional;
- unwrap trivial `{ data: A }` envelopes;
- map no-content success to `void`;
- expose streams directly as `AsyncIterable` or the runtime's stream type;
- reject duplicate names or ambiguous response contracts during generation.

Code generation does not automatically produce a good API. Treat the generator as an API design layer that deliberately projects a transport contract into a domain-oriented interface.

## Keep one authoritative contract

Define request, response, error, and streaming schemas once, then derive server validation, API documentation, and clients from that contract. Check generated artifacts for deterministic drift in CI. This prevents the implementation, documentation, and clients from quietly describing different systems.

Different clients can project the same contract appropriately. A plain Promise client may use structural JavaScript values, while an [[Effect for TypeScript|Effect]] client can preserve decoded domain values, typed errors, and streams. The shared authority should be the contract, not one generated type package that every runtime must adopt.

## Separate schema, protocol, and implementation

Keep a directed boundary:

```text
public schemas -> protocol -> server implementation
```

- **Public schemas** define serializable values and identifiers.
- **Protocol** defines endpoints, middleware requirements, errors, and transport semantics.
- **Implementation** owns databases, internal services, credentials, request construction, and side effects.

Use explicit public DTOs rather than serializing internal models. Internal records often contain provider options, headers, credentials, or implementation state that should never cross the boundary. Decode all external data at runtime; static TypeScript types do not validate HTTP or persisted input.

Keep environmental concerns out of portable clients. For example, browser-compatible networking, Node process management, and an embedded host should be separate entrypoints rather than one client with many conditional behaviors.

## Specify workflow semantics, not just payload shapes

Long-running and failure-prone operations need an explicit lifecycle. Do not make one request ambiguously mean "accept this work, run it, wait indefinitely, and maybe return the result."

Separate concepts such as:

- durable admission from execution;
- admission receipts from final results;
- start, resume, wait, interrupt, and cancel;
- immediate steering from queued work;
- accepted work from active process ownership.

Support retry safety where duplicate work is consequential. A caller-supplied operation or message ID can make an exact retry return the original admission while conflicting reuse fails explicitly. A connection timeout must not leave the caller unable to determine whether retrying will duplicate work.

## Distinguish notifications from durable truth

A live event stream and a durable history log serve different purposes:

- live events provide low-latency notification and may be volatile;
- durable events support replay and reconciliation after disconnects;
- streamed fragments can remain ephemeral while completed values form replayable checkpoints.

Document disconnection, overflow, ordering, cursor, and backpressure behavior. Advance durable cursors only from committed events. Order durable history by an authoritative sequence, not wall-clock timestamps or caller-generated IDs. A robust client can treat live events as a doorbell and reconcile authoritative state from bounded history pages.

[[Agent context engineering]] owns the analogous working-set, checkpoint, and recovery policy for agent harnesses.

## Make errors part of the contract

Declare expected domain failures per operation, with a stable machine-readable tag, relevant identifiers, a useful message, and an HTTP status where applicable. Distinguish them from transport failures, malformed responses, unsupported content types, unexpected statuses, defects, and interruption.

This lets callers handle `SessionNotFound`, `Conflict`, or `ServiceUnavailable` without parsing strings, while still recognizing that a network or decoding failure is not a domain rejection. Preserve required request bodies and precise field validation rather than weakening the contract to accommodate a generator.

## Reuse semantics across transports

Remote and embedded access should not become separate implementations. An embedded SDK can route the generated client through the real server router in memory, removing the network hop while preserving routes, middleware, codecs, authorization, errors, and schemas. Shared semantics matter more than sharing method names.

Keep genuinely transport-specific capabilities explicit. A WebSocket terminal, SSE stream, and ordinary request-response endpoint do not need to be forced through one generic abstraction.

## Design extensions as scoped capabilities

Plugins should receive a namespaced capability surface rather than unrestricted access to internal services. Separate configuration transforms from runtime interception. Make registration order deterministic when composition depends on it, and tie registrations and cleanup to a plugin scope so reload and unload cannot leave stale behavior behind.

Replayable transforms are easier to reconcile than mutations that each plugin must manually undo. Expose only mutable fields that a hook is allowed to change, and keep the extension boundary independent of UI and transport details.

## Redesign deliberately

A major-version or beta redesign is an opportunity to remove transport leakage, duplicate concepts, historical aliases, and accidental coupling. Prefer a coherent breaking contract and update its consumers over accumulating compatibility paths. Preserve compatibility only where an external contract, deployed consumer, or durable data requires it.

Judge the redesign by whether ordinary use is easier, invalid use is harder, recovery behavior is explicit, and all projections remain consistent. Framework choice is secondary.

## Review questions

1. What concepts and operations do callers actually think in?
2. Is there one authoritative contract for values, errors, and streams?
3. Can internal state or secrets cross the public serialization boundary?
4. Are admission, execution, cancellation, retry, and idempotency semantics explicit?
5. Which events are volatile, and which state can be replayed after disconnection?
6. Can callers handle expected failures without parsing messages?
7. Do remote and embedded forms exercise the same behavior?
8. Are extension capabilities scoped, composable, and cleanly disposable?
9. Does generated code hide transport ceremony rather than reproduce it?
10. Which compatibility constraints are real, and which are merely historical?

## OpenCode 2 example

OpenCode 2's redesign illustrates these principles. Its server API and clients are generated from one typed `HttpApi`; the Promise client flattens HTTP input channels and unwraps simple responses; the embedded SDK runs the real router in memory; session prompt admission is durable and separate from execution; live notifications and durable session history have distinct contracts; and the plugin API is namespaced and scoped.

Primary design references: [migration guide](https://v2.opencode.ai/migrate-v1.md), [client](https://v2.opencode.ai/build/client.md), [embedded SDK](https://v2.opencode.ai/build/sdk.md), [plugin API](https://v2.opencode.ai/build/plugins.md), and [client-generation rules](https://github.com/anomalyco/opencode/blob/deb5b144c3b0f575e478f02f8b9d979cf8d01b8c/packages/httpapi-codegen/README.md#L7-L28).
