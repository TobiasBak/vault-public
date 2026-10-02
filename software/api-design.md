# API design

Make domain semantics explicit and transport mechanics incidental. Pick the protocol from actual consumers, deployment, and interoperability; no style is intrinsically best.

## Consumer-shaped interfaces

- Organize around concepts callers think in. Prefer `session.prompt({ sessionID, text })` over generated `path`, `query`, and `body` plumbing. Use action operations where the domain has lifecycle semantics instead of forcing CRUD.
- The interface includes everything callers must know: invariants, ordering, errors, config, and relevant performance. Keep internal or test-only seams out of it.
- Treat code generators as a design layer that projects the wire contract into a domain interface:
  - flatten path, query, header, and body into one input
  - omit empty arguments
  - unwrap `{ data: A }`
  - map no-content to `void`
  - expose streams as `AsyncIterable`
  - reject ambiguous names at generation time

## One authoritative contract

- Define request, response, error, and stream schemas once. Derive validation, docs, and clients from them, and check generated artifacts for drift in CI.
- Clients may project differently (a plain Promise client vs an [Effect](effect.md) client with typed errors). The contract is shared, not one type package.
- Keep the direction `public schemas → protocol → implementation`. Use explicit public DTOs and never serialize internal models, which leak options, headers, and credentials. Decode all external data at runtime.
- Keep environment concerns (browser, Node process, embedded host) in separate entrypoints.

## Workflow semantics

- Separate durable admission from execution, admission receipts from results, start, resume, wait, interrupt, and cancel, and immediate steering from queued work. One request must not ambiguously mean "accept, run, wait forever, maybe return".
- **Retry safety:** a caller-supplied operation ID returns the original admission on exact retry and fails explicitly on conflicting reuse. A timeout must never leave the caller unsure whether a retry duplicates work.
- **Live vs durable events:** live events are low-latency and may be lost; durable history supports replay. Document disconnect, overflow, ordering, cursor, and backpressure behavior. Advance cursors only on committed events and order by an authoritative sequence, not timestamps. Robust clients treat live events as a doorbell and reconcile from history pages.
- **Errors:** declare expected domain failures per operation, with a stable tag, IDs, message, and status. Keep them distinct from transport, decode, and unexpected-status failures and from defects. Callers should never parse strings.

## Transports and extensions

- An embedded SDK should route through the real server router in memory, preserving routes, middleware, auth, errors, and codecs, not reimplement them. Keep genuinely transport-specific features (WebSocket terminal, SSE) explicit.
- Plugins get a namespaced, scoped capability surface rather than internal services. Keep config transforms separate from runtime interception, use deterministic registration order, and tie registrations and cleanup to the plugin scope. Expose only the fields a hook may change.

## Redesign

A major version is the moment to remove transport leakage, duplicate concepts, aliases, and accidental coupling. Prefer a coherent breaking contract over compatibility paths, unless an external consumer or durable data requires them. Success means ordinary use is easier, misuse is harder, recovery is explicit, and all projections agree.

**Example:** OpenCode 2 generates server and clients from one typed `HttpApi`, flattens inputs, runs the embedded SDK through the real router, separates prompt admission from execution and live from durable events, and scopes plugins. ([migration](https://v2.opencode.ai/migrate-v1.md), [client](https://v2.opencode.ai/build/client.md), [SDK](https://v2.opencode.ai/build/sdk.md), [plugins](https://v2.opencode.ai/build/plugins.md))
