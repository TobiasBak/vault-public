# Effect for TypeScript

[Effect](https://effect.website/docs/) gives errors, dependencies, concurrency, resources, scheduling, streams, and observability one typed execution model. It's a library, not a runtime, framework, or build tool.

`Effect<Success, Error, Requirements>` is a lazy, immutable description of a computation. Unlike `Promise`, it exposes expected failures and required services, and its runtime distinguishes defects and interruption from expected errors. Compose effects throughout an area and run them at the edges; scattered Promise conversion defeats the point.

It unifies:
- typed errors and dependency services
- structured concurrency, interruption, and bounded parallelism
- retries, schedules, timeouts, and cancellation
- safe resource cleanup
- streams and Schema validation
- config, caching, logs, metrics, and tracing

The value lies in consistent semantics across these concerns, not in any one feature.

## When to use it

- **Use** for integration-heavy backends, agents, workers, CLIs, and pipelines that juggle unreliable APIs, DBs, queues, or models. Especially when domain failures, cancellation, cleanup, or swappable dependencies matter, or the codebase is growing ad-hoc retry, abort, logging, and DI wrappers.
- **Skip** for small or short-lived apps, mostly synchronous transforms, plain CRUD, public libraries that should expose plain JS APIs, or teams unwilling to learn it. A discriminated union or small `Result` type may be enough.

**Costs:** a big learning surface (fibers, layers, scopes, services), an architectural commitment, heavier inference load, and no soundness. `any` and bad external data still bypass it, so runtime decoding remains necessary.

Adopt it around one genuinely hard workflow, exercise real timeout, cancel, retry, and cleanup behavior, and compare against a Promise version before expanding.

## Alternatives by concern

- neverthrow or unions: typed errors
- Zod or Valibot: boundary validation (Effect Schema inside Effect)
- RxJS: event streams
- XState: state machines
- Temporal: durable distributed workflows (Effect is in-process)
- fp-ts: FP abstractions without the runtime

Effect coexists with React, Next, Hono, Fastify, Prisma, Drizzle, and TanStack Query.
