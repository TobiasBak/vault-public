# TypeScript 7 ecosystem

TypeScript 7 is the default baseline for new TypeScript work. The native Go compiler and language tooling reached stable release on 2026-07-08. Compatibility remains most volatile around embedded-language tools and programmatic compiler integrations.

## Runtime boundary

TypeScript is JavaScript with an erased structural type system and compiler tooling. It does not supply a runtime. Emitted JavaScript runs in browsers, Node.js, Bun, Deno, edge workers, and other JavaScript environments.

Static types disappear at runtime. Treat HTTP, database, file, environment, queue, user, and AI-model data as untrusted until decoded or validated. `any`, assertions, unchecked indexing, and inaccurate external declarations remain escape hatches. TypeScript provides excellent practical feedback, not proof of correctness.

TypeScript's strength is gradual JavaScript adoption, the npm ecosystem, browser and server portability, expressive structural types, editor navigation and refactoring, and one language across application and tooling layers. [[Effect for TypeScript]] can add a typed operational model without changing this erased runtime boundary.

## TypeScript 7 baseline

The native toolchain aims to preserve existing TypeScript semantics while adding faster execution and parallel parsing, checking, emit, project builds, and language-server work. Faster feedback is especially valuable for coding agents because more compiler-guided iterations fit into the same time budget.

Use stable TypeScript 7 by default for ordinary `.ts` and React `.tsx` projects. Pin the version and lockfile. Keep compiler checking distinct from transformation or bundling: a successful Vite or framework build may not establish a full type-check. Validate runtime behavior and published declarations where those are part of the contract.

Current adoption boundaries:

- TypeScript 7.0 has no stable programmatic compiler API. Tools that embed compiler internals need an explicit compatibility decision.
- Vue, Svelte, Astro, MDX, Angular templates, and similar embedded-language workflows may use different or partial language tooling. Verify current editor and build support rather than assuming CLI success proves full adoption.
- Parallel workers trade memory for throughput. Fix relevant concurrency settings in constrained or reproducible CI environments.
- For prerelease lanes, pin an exact version, test diagnostics, emit, declarations, editor behavior, framework tooling, builds, and runtime smoke paths, and retain easy rollback.

AI can reduce migration effort but cannot validate compiler defects, declaration regressions, language-server failures, or runtime behavior.

## Layer boundaries

Choose one authority at each layer and add specialized libraries only for a concrete need:

- **Runtime:** select Node.js, Bun, Deno, browser, or edge assumptions before module resolution and deployment.
- **UI:** choose one primary system such as React, Angular, Vue, Svelte, or Astro.
- **Application/build:** use Vite when assembling a client application directly, or a meta-framework such as Next.js, Nuxt, or SvelteKit when routing, server behavior, rendering, and deployment should share one authority. Do not add a redundant peer build layer without a separate-package need.
- **Server:** choose one primary HTTP/application framework per service. Adapter relationships, such as NestJS using Fastify, are not two independent architecture layers.
- **API:** tRPC suits a jointly evolving TypeScript client and server; REST with OpenAPI usually fits public or polyglot boundaries. Choose from actual consumers.
- **Data:** choose one primary migration and data-access authority unless a deliberate transition requires overlap.
- **Validation:** decode untrusted data with a runtime schema. Static inference cannot replace this boundary.
- **State:** distinguish browser server-state caching from local client state rather than putting both into one general store by default.
- **Quality:** keep unit or integration tests, browser tests, static analysis, and formatting as distinct responsibilities. Use one formatter and one package manager with one lockfile per repository.

## High-value practices

Use `strict`, `unknown` at untrusted boundaries, discriminated unions for domain states and expected errors, and exhaustive handling. Prefer local inference with explicit stable exported contracts. Match module and module-resolution settings to the actual runtime or bundler. Run a real type-check independently of tests and transformation. Treat `skipLibCheck` as a measured tradeoff rather than a way to ignore dependency faults.

Release and status provenance is retained because adoption guidance is version-sensitive: [TypeScript 7.0 announcement](https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/), [typescript-go status and source](https://github.com/microsoft/typescript-go), and [intentional compatibility changes](https://github.com/microsoft/typescript-go/blob/main/CHANGES.md). Recheck these and framework-specific support before consequential upgrades.
