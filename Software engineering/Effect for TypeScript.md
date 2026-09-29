# Effect for TypeScript

[Effect](https://effect.website/docs/) is an application-foundation library within TypeScript. It does not replace [[TypeScript 7 ecosystem|TypeScript 7]], a UI framework, build tool, runtime, or database. It gives errors, dependencies, concurrency, resources, scheduling, streams, and observability one typed execution model.

## Core model

```ts
Effect<Success, Error, Requirements>
```

An Effect is an immutable, lazy description of a computation that can produce `Success`, fail with an expected `Error`, and require services represented by `Requirements`. Unlike `Promise<Success>`, the type can expose expected failure and dependency requirements. The runtime also distinguishes defects and interruption from expected errors.

Keep Effect values composed through an architectural area and execute them at application edges. Scattered conversion to and from Promise weakens the model and adds ceremony.

## What it unifies

Effect makes operational concerns compose under one program model:

- typed expected errors and explicit dependency services;
- structured concurrency, interruption, races, and bounded parallelism;
- retries, schedules, repetition, timeouts, and cancellation;
- safe resource acquisition and cleanup;
- streams and runtime schema validation;
- configuration, caching, logs, metrics, tracing, and telemetry context.

The benefit is not that each feature is unique. It is that callers can reason about them through consistent types and runtime semantics.

## Decision boundary

Effect is a strong candidate for integration-heavy backends, agents, workers, CLIs, and pipelines that coordinate unreliable APIs, databases, queues, filesystems, or AI models. Its value rises when domain failures need explicit handling, cancellation and cleanup matter, dependencies need controlled replacement, or a codebase is accumulating wrappers for Promise, retry, abort, logging, and dependency injection.

Conventional TypeScript is simpler for small or short-lived applications, mostly synchronous transformation, straightforward CRUD, public libraries that should expose ordinary JavaScript APIs, and teams unwilling to adopt the runtime model. A discriminated union, small `Result`, or focused validation library may solve the actual problem without Effect.

## Costs

The learning surface includes lazy effects, typed error channels, fibers, interruption, contexts, layers, scopes, and service provision. Broad composition is an architectural commitment. Plain async TypeScript is more widely understood, and Effect-heavy inference can increase tooling load. Effect also cannot make TypeScript sound: `any`, assertions, inaccurate declarations, and invalid external data still bypass static guarantees, so runtime decoding remains necessary.

Adopt incrementally around one genuinely difficult workflow. Model domain failures, introduce replaceable services only where needed, exercise real timeout, cancellation, retry, cleanup, and tracing behavior, and compare against a Promise implementation. Expand only when important behavior becomes clearer, more composable, and harder to misuse than the added model is to learn.

## Nearby alternatives

- Discriminated unions or **neverthrow** provide narrower typed recoverable errors.
- **Zod** or **Valibot** focus on runtime boundary validation; Effect Schema fits an Effect architecture.
- **RxJS** centers multi-value asynchronous event streams.
- **XState** centers explicit states and transitions.
- **Temporal** is a durable distributed workflow engine; ordinary Effect execution is in-process.
- **fp-ts** provides functional abstractions without the same integrated application runtime.

These are concern-level distinctions, not a stack catalog. Effect can coexist with React, Vite, Next.js, Hono, Fastify, Prisma, Drizzle, TanStack Query, and ordinary Promise APIs. Start where unified operational semantics have concrete value rather than replacing familiar layers by default.
