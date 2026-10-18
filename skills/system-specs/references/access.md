# Access and security

Scope: signing in, sessions, permissions, tenant isolation, machine and agent identities, secrets, and the security log. Network and infrastructure hardening are out of scope. Builds on the [data](data.md), [release](release.md) and [API](api.md) catalogs.

Principles:
- Deny by default. Unknown data is tolerated, but it never turns into access.
- Every actor has its own identity: people, agents, jobs, services, API keys.
- Authority comes only from server-side checks in one module.
- Cross-tenant access can't be expressed in ordinary code.

## Signing in

### S1 No passwords

Users sign in with OIDC through their company's identity provider (Microsoft Entra, Google) or with passkeys. SAML only when a customer requires it. MFA is the provider's job. Passkey users recover through a second passkey or a reset by their company admin.

Reason: stored passwords are something to leak, reset and defend; company sign-in lets the customer's IT control who joins and leaves.

Enforcement: the user record has no password field; sign-in has no password path.

### S2 Revocable sessions

User sessions live on the server and are checked on every request, so removing a user or a permission takes effect on the next request. Sessions have a maximum lifetime, after which the user signs in again through the provider; a user disabled there fails at that point. SCIM provisioning is added when a customer asks. Desktop clients keep tokens in the OS keychain. Our own services use short-lived signed tokens between each other.

Reason: "removed, but still had access for an hour" is an incident.

Enforcement: black-box cases: a removed user's next request is refused; a session past its lifetime must sign in again.

### S3 Recent sign-in for sensitive actions

Permissions marked sensitive (changing roles, deleting a company's data, changing payment details) require a sign-in within a short window.

Reason: a stolen or unattended session shouldn't be enough for the most damaging actions.

Enforcement: sensitivity is a property of the permission type, and the authorization module checks sign-in age for it; a black-box case with an old sign-in is refused.

## Permissions

### S4 One authorization module

Authorization is decided in one module and denies by default. Permissions are an enum, and every endpoint declares its permission in its type. A role is a named set of permissions within one company. Per-record rules (only the order's owner) are added when a feature needs them. No policy engine until customers write their own rules.

Reason: scattered role checks get forgotten; a declared permission can't be.

Enforcement: the endpoint type requires a permission; a static check rejects role comparisons outside the module.

### S5 Fail closed

An unknown permission in stored data decodes to `Unknown` ([D4](data.md#d4-unknown-enum-values)) and grants nothing. New permissions deploy server first.

Reason: an older server reading a newer role must not guess what the role allows.

Enforcement: the permission enum's `Unknown` variant has no grant path; a black-box case gives the previous server a role with a new permission.

### S6 Permission sweep

A generated test calls every route with a role that lacks its permission and expects 403. Hand-written cases per endpoint (allowed role succeeds, another company's record returns 404) are suggested, not required.

Reason: one test covers every new endpoint without anyone writing a case.

Enforcement: the sweep reads the route list and runs in CI.

## Tenancy

### S7 Tenant isolation

Each company gets its own database by default; a shared database needs a reason in the project's spec, such as very many small tenants. The tenant comes from the signed-in identity, never from a URL or request field alone. All data access goes through a handle scoped to one tenant, which the types require: the company's connection, or the enforced filter in a shared database. A request never holds handles to two tenants. Work that spans tenants (billing, operations, migrations) uses a separate path that is explicit and logged. Migrations across company databases follow [D11](data.md#d11-migration-execution).

Reason: leaking one customer's data to another is the worst bug a business system can have. With separate databases it takes a wrong connection, not a forgotten filter, and deleting or exporting a customer is one operation.

Enforcement: data access APIs take the tenant handle; a static check rejects raw connections outside the tenancy module; a black-box case tries to reach another company's data.

### S8 Memberships

One identity can belong to several companies, with a role in each and an explicit switch between them.

Reason: accountants and consultants work for several customers; separate accounts per company get shared or forgotten.

Enforcement: roles attach to memberships, not identities; S7 keeps each request to the active company.

## Machines and agents

### S9 Own identities

Agents, background jobs and services have their own identities with narrowly scoped, short-lived credentials, never a human's session. An agent acting for a user records both ("agent X on behalf of user Y") and never has more access than that user.

Reason: without separate identities you can't tell what the agent did, or revoke it without revoking the human.

Enforcement: the authorization module intersects agent and user permissions; the S16 log records both identities; a black-box case has an agent try an action its user lacks.

### S10 Agents in the product

Agent authority comes only from the same server-side checks as any other actor; nothing an agent reads or says grants anything. Sensitive (S3) or irreversible actions by an agent need a human to confirm that specific action.

Reason: an agent reads untrusted text; an order note that says "refund everything" must not refund anything.

Enforcement: agent tools call the same endpoints as users; a black-box case feeds an injected instruction and finds no unauthorized effect.

### S12 API keys

API keys are scoped to one company and a set of permissions, stored only as a hash, prefixed so secret scanners recognize them (`<product>_live_…`), and carry an expiry and a last-used time. Rotation lets old and new keys overlap. Each key is its own identity.

Reason: a leaked key must be detectable, limited and replaceable without downtime.

Enforcement: keys are generated and verified in one module; a black-box case rotates a key with both working during the overlap.

### S13 Local processes

Local processes talk over stdio ([A15](api.md#a15-protocol-choice)). A localhost port, if unavoidable, binds to loopback only and requires a random token issued at startup.

Reason: any local process, including a browser page, can reach an open localhost port.

Enforcement: a black-box case connects without the token and is refused.

## Clients

### S14 Offline permissions

Offline clients read local data under the last permissions they knew. At sync, the server checks every write against current permissions and rejects denied writes visibly to the user, never silently ([D6](data.md#d6-quarantine-undecodable-records)).

Reason: permissions change while a client is offline; the server is the only authority.

Enforcement: black-box case: a permission is removed while the client is offline, and its write is rejected visibly at sync.

## Operations

### S11 Support access

Our staff and agents get access to a customer's data only for a limited time, with a recorded reason and read-only by default. Each access appears in that customer's security log. Nobody has standing access.

Reason: enterprise security reviews reject vendors where everyone can see everything.

Enforcement: support access is a separate identity type with grants that expire; a black-box case finds the access in the customer's log and refused after expiry.

### S15 Rate limits

Sign-in, external endpoints and expensive operations have limits per credential and per company. Exceeding them returns 429 with `Retry-After` ([A8](api.md#a8-retries-and-deadlines)).

Reason: one integration stuck in a loop mustn't take down everyone else.

Enforcement: black-box case: one credential over its limit gets 429 while another company is unaffected.

### S16 Security log

Sign-ins, failed sign-ins, role and permission changes, admin actions, support access and agent actions go to an append-only log, separate from [D15](data.md#d15-traceable-writes)'s data history. Customer admins see their own company's entries. Retention is set per product.

Reason: security reviews ask who gave someone access and when; data history doesn't answer that.

Enforcement: the authorization and sign-in modules write the log, so callers can't skip it; the application has no update or delete path to it.

### S17 Secrets

Git holds secret names; values live in a secret manager or are encrypted in git (sops). Every secret rotates without downtime, with old and new valid during a switch-over window. Secret scanning runs in pre-commit and CI.

Reason: [R1](release.md#r1-everything-goes-through-git) puts config in git, but a plaintext secret there is leaked to everyone with read access.

Enforcement: the secret scanner; a rotation drill switches a secret with no failed requests.
