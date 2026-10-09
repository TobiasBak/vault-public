# TypeScript 7

TypeScript 7 (the native Go compiler and language service, stable 2026-07-08) is the default for new TypeScript work. Faster compiler feedback means more agent iterations per time budget. Sources: [announcement](https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/), [typescript-go](https://github.com/microsoft/typescript-go), [compat changes](https://github.com/microsoft/typescript-go/blob/main/CHANGES.md); recheck them before consequential upgrades.

## Adoption boundaries

- No stable programmatic compiler API in 7.0, so tools that embed compiler internals need an explicit decision.
- Vue, Svelte, Astro, MDX, and Angular templates may have partial tooling. Verify editor and build support, since CLI success doesn't prove it.
- Parallel workers trade memory for speed; pin concurrency in constrained CI.
- A Vite or framework build is not a type-check. Run `tsc` separately.
- On prerelease lanes, pin exactly and test diagnostics, emit, declarations, editor behavior, builds, and runtime smoke paths, with easy rollback.

## Runtime boundary

Types are erased. Treat HTTP, DB, file, env, queue, user, and model data as untrusted until decoded with a runtime schema. `any`, assertions, unchecked indexing, and wrong declarations are escape hatches. [Effect](effect.md) adds an operational model without changing this.

## One authority per layer

- **Runtime:** pick Node, Bun, Deno, browser, or edge before module resolution.
- **UI:** one primary framework.
- **Build:** Vite for a plain client app; a meta-framework (Next, Nuxt, SvelteKit) when routing, server, and rendering should share one authority. No redundant peer build layers.
- **Server:** one HTTP framework per service. An adapter pairing like NestJS on Fastify is one layer.
- **API:** tRPC for a co-evolving TS client and server; REST plus OpenAPI for public or polyglot consumers.
- **Data:** one migration and data-access authority.
- **State:** separate server-state caching from local client state.
- **Quality:** tests, browser tests, static analysis, and formatting stay distinct. One formatter, one package manager, one lockfile.

## Account-scoped server-state caches

Retire the cache owner when an employee changes, not just its contents. TanStack Query's mutation-cache `clear()` leaves running mutations and their callbacks alive. Swapping a provider's client without remounting can also retarget pending mutation observers to the new client's callbacks. Use a keyed employee-provider lifetime, with stable authentication state outside it. Test delayed success and rejection after logout and another employee's login.

## Defaults

`strict`, `unknown` at untrusted boundaries, discriminated unions for states and expected errors, exhaustive handling, local inference with explicit exported contracts. Match `module` and `moduleResolution` to the real runtime or bundler. Treat `skipLibCheck` as a measured tradeoff.
