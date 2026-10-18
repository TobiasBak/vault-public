---
name: system-specs
description: Write, extend, or check requirement specs that let Tobias understand a system's design without reading code, for systems agents change several times a day. Use when defining or reviewing requirements for data, storage, releases and deploys, APIs, or other boundaries, when a design question touches version skew or deploy safety, or when implementing code a spec governs.
---

# System specs

A spec tells Tobias what the system must do and why, without code. Agents read it to implement and check against it.

## The world specs assume

Agents merge several times a day, staging updates continuously, and production releases up to daily plus hotfixes. So at any moment:
- Two or more versions of the code run against the same data and talk to each other: rolling deploys, workers that haven't restarted, migrations applied before or after the code that uses them.
- Every boundary sees data written by both newer and older code than itself.
- No human is around to fix a halted system by hand.

A requirement that only holds when every component runs the same version is wrong.

Newer versions win. Keep one source of truth, auto-update clients, and refuse versions below a minimum instead of supporting a long tail. Fix forward; never roll back data.

## Tolerate versions, never ambiguity

Tolerance and hardening don't conflict. They live in different places:
- **Tolerant only at version boundaries:** where data crosses between code versions (persisted data, events, messages between services). Tolerance is modeled in types there: an unknown enum value is a typed `Unknown` variant, unrecognized fields are a typed container that the write path must carry. The compiler then makes every caller handle them. That's more hardening, not less.
- **Strict everywhere else:** domain code uses exact types and exhaustive matches, with no `Value`, stringly typed fields or catch-all defaults. Inbound commands from clients and agents reject unknown fields, because there an unknown field is a typo, not version skew.
- Decode once at the boundary into domain types; never pass raw data inward.

## Spec shape

- One spec per domain. Each requirement has a stable ID (`D1`, `D2`), a one-sentence rule stated as observable behavior, and a one-line reason.
- Each requirement names what enforces it: a type, a static check, or a black-box case. A requirement with no enforcement is listed as a gap, not passed off as met. Prefer a black-box case that runs two versions or old and new data together.
- No implementation narrative, plans or status. Those go in issues and PRs.
- In a repository shaped by `theodore-kaczynski-nullifier`, a spec is an approved published contract whose consumer is Tobias: register its path in the prose gate.
- Requirements change only by an explicit decision from Tobias. Agents report spec conflicts, not silently diverge.

## Requirement catalogs

General requirements every system meets unless its spec says otherwise:

| Domain | Catalog |
|---|---|
| Data and persistence | [data.md](references/data.md) |
| Release and deploy | [release.md](references/release.md) |

A project's spec adopts catalog requirements by ID and adds its own.

## Verification

For code a spec governs, show each touched requirement's enforcement working: the type or static check rejects the forbidden form and accepts the supported one, and the black-box case passes against data or peers from both the previous and the next version.
