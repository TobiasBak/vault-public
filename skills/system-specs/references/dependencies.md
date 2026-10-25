# Dependencies and supply chain

Scope: third-party code that runs at build time or in production (crates, npm packages, container base images, CI actions, toolchains) and the external services a system calls.

Principles:
- Agents don't add dependencies freely; an automated gate decides, and humans decide the exceptions.
- The same commit always builds the same thing.
- Stay current in small automated steps.

## Adding

### P1 Dependency gate

A new direct dependency needs a one-line `Why:` trailer in its commit and passes an automated policy: allowed license (P5), actively maintained, published for a minimum time with real downloads, no known vulnerabilities, no build-time scripts (P6). Prefer the standard library or an existing dependency; reject a dependency that replaces a few lines of code. Failing a criterion, or touching crypto, auth or serialization, makes it approval-class.

Reason: agents invent plausible package names, and attackers register them ("slopsquatting"); the age and download check catches it. Every dependency is code nobody on the team wrote or reviews.

Enforcement: a pre-push check on manifest changes runs the policy and requires the trailer.

### P2 Sources

Dependencies come only from official registries. A git dependency is pinned to a commit SHA and needs a reason. A patched dependency links the upstream issue, and the patch is removed when upstream fixes it.

Reason: an unpinned branch or unofficial registry is code that can change under you.

Enforcement: cargo-deny (or the ecosystem's equivalent) restricts sources; the P1 check flags git and patched dependencies.

### P3 Weight

The pre-push check reports how many transitive dependencies a new dependency brings and any duplicate versions. No hard limit.

Reason: a small-looking addition can pull in a hundred crates.

Enforcement: the P1 check prints the report.

## Building

### P4 Pinned everything

The lockfile is committed, and builds refuse to change it (`--locked`, frozen lockfile). CI actions are pinned by commit SHA, container images by digest, toolchains in the repo (`rust-toolchain.toml`, mise).

Reason: [R3](release.md#r3-built-once-signed-verified) assumes the same commit builds the same artifact.

Enforcement: build commands use the locked flags; a static check rejects unpinned actions and images.

### P5 Licenses

Allowed: MIT, Apache-2.0, BSD, ISC, Zlib, MPL-2.0. GPL and AGPL are rejected unless Tobias decides otherwise for a product.

Reason: the products are commercial and closed-source.

Enforcement: cargo-deny license check (or the ecosystem's equivalent) in pre-push and on promotion.

### P6 Build-time code

Package install scripts are off by default, with an explicit allowlist (pnpm `onlyBuiltDependencies`). New dependencies with `build.rs` or proc macros are flagged by P1. CI builds never see production secrets ([R3](release.md#r3-built-once-signed-verified)).

Reason: install scripts, build scripts and proc macros run arbitrary code on the build machine.

Enforcement: package manager config in git; the P1 check.

## Keeping current

### P7 Automated updates

A bot (Renovate) groups updates weekly and lands them through the normal pre-push gates when green. A new release must be a few days old before adoption; security fixes skip the wait.

Reason: small regular updates beat a risky yearly upgrade; malicious releases are usually caught and pulled within days.

Enforcement: the bot's config in git, with a minimum release age.

### P8 Vulnerabilities

Vulnerability scans (cargo-audit, osv-scanner) run on promotion and daily against main and every released version. A vulnerability reachable in production is an incident ([observability](observability.md)). An advisory that doesn't apply may be ignored with a reason and an expiry, after which the build fails, as with flags ([R14](release.md#r14-flags)).

Reason: released versions keep running after new advisories appear.

Enforcement: the scans; the ignore file requires reason and expiry, checked pre-push.

## External services

### P9 Services behind one module

Each external service (payments, email, LLM APIs) sits behind one owning module. Its SDK types never reach domain code. Calls follow [A8](api.md#a8-retries-and-deadlines), failures are typed errors, and swapping the provider changes only that module.

Reason: providers change APIs, models and prices; an SDK spread through the code makes every change a migration.

Enforcement: a static check rejects the SDK's imports outside its module.
