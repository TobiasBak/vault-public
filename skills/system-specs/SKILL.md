---
name: system-specs
description: Write, extend, or check requirement specs that let Tobias understand a system's design without reading code, for systems agents change several times a day. Use when defining or reviewing requirements for data, storage, releases and deploys, APIs, auth and permissions, tenancy, observability and incidents, dependencies, AI features, or other boundaries, when a design question touches version skew or deploy safety, or when implementing code a spec governs.
---

# System specs

A spec tells Tobias what the system must do and why, without code. Agents read it to implement and check against it.

## Version boundaries

When deployments, workers, migrations or clients can run at different versions, specify how they coexist with shared data and messages. A requirement that assumes all components change simultaneously is wrong for that system. Do not impose version-skew machinery where the system has no such boundary.

Where the project adopts a newer-versions-win policy, keep one source of truth, update controlled clients, and refuse versions below its minimum instead of supporting a long tail. Fix forward; never roll back data.

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

Catalogs of candidate requirements. Choose what fits the system, its actual consumers and the authorized scope; they are not requirements until adopted:

| Domain | Catalog |
|---|---|
| Data and persistence | [data.md](references/data.md) |
| Release and deploy | [release.md](references/release.md) |
| APIs and protocols | [api.md](references/api.md) |
| Access and security | [access.md](references/access.md) |
| Observability and incidents | [observability.md](references/observability.md) |
| Dependencies and supply chain | [dependencies.md](references/dependencies.md) |
| AI in the product | [ai.md](references/ai.md) |

A project's spec can adopt catalog requirements by ID and add its own. Check each requirement's implementation assumptions, including language and deployment model, before adopting it.

## Auditing a repo

1. Read the project's spec if it has one. Otherwise select relevant catalog candidates from the actual system and requested audit; do not treat them as existing obligations.
2. Mark adopted requirements met (cite the enforcing type, check or case), gap (what's missing and the cheapest enforcement), or not applicable. Report unadopted candidates as recommendations, not violations.
3. Rank gaps by how likely they are to break production, not by count.
4. Report; change code only when asked.

## Verification

For code a spec governs, show each touched requirement's enforcement working: the type or static check rejects the forbidden form and accepts the supported one, and the black-box case passes against data or peers from both the previous and the next version.
