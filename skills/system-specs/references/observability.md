# Observability and incidents

Scope: telemetry, what counts as broken, alerting, incident response, learning from incidents, and agents reading production. Version attribution is [R16](release.md#r16-version-attributed-telemetry).

Principles:
- Agents are the first readers of telemetry and the first responders. Humans are the escalation.
- Broken means users can't complete their journeys, not that a machine metric crossed a line.
- Agents in production act only through reversible, pre-approved actions and never touch data.
- Every incident leaves behind a check that would have caught it.

## Telemetry

### O1 Wide events

Each request and job emits one structured event with every relevant field: version, request ID, tenant, actor, endpoint, duration, outcome, error code, and domain IDs. Events go through OpenTelemetry into a store queryable with SQL. Metrics and dashboards are derived from events.

Reason: an agent with SQL over wide events answers questions nobody anticipated ("which companies hit this error only after 5.3, only on large orders?"); separate logs, metrics and traces force guessing where the answer is.

Enforcement: the request and job frameworks emit the event, so handlers can't skip it; a black-box case finds a request's event with all required fields.

### O2 No personal values, bounded retention

Events carry IDs, never personal values: no names, emails, addresses or free text. Raw events are kept 30 days, aggregates 13 months, incident records forever, unless the product overrides.

Reason: keeps telemetry outside [D16](data.md#d16-erasable-personal-data) erasure and safe to hand to agents. Thirteen months allows a year-over-year comparison.

Enforcement: event types accept only ID and enumerated fields, no free strings; the store's retention policies are config in git.

### O3 Sampling

Every error and slow request is kept. Normal successes are sampled, and each event records its sample rate so counts and rates stay correct.

Reason: every failure in full, without storing a million identical successes.

Enforcement: tail sampling in the telemetry pipeline; a black-box case finds every injected error and a correct total from sampled successes.

### O4 Telemetry is a contract

Events are typed structs. Alerts, journey targets, dashboards and saved queries live in git ([R1](release.md#r1-everything-goes-through-git)). Renaming or removing an event field follows [D5](data.md#d5-two-step-destructive-changes).

Reason: a broken alert fails silently, and you find out during the incident.

Enforcement: CI checks every query against the event schema.

### O5 Client telemetry

Desktop and web clients send crashes, errors and journey outcomes with their version, buffer while offline, and send nothing personal (O2). Business customers cover it by contract, not a consent prompt.

Reason: most client failures never reach the server.

Enforcement: black-box case: a client crashes offline and the report arrives after reconnecting.

## Detection

### O6 Journey targets

Each user journey (sign-in, placing an order, client sync) has a success-rate and latency target, measured from real traffic and [R8](release.md#r8-verified-server-rollout)'s synthetic journeys. Alerts fire on how fast the error budget burns, not on single spikes or machine metrics.

Reason: CPU at 95% while orders go through isn't an incident; CPU at 20% while orders fail is.

Enforcement: journey targets and burn-rate alerts are defined in git (O4); R8 and [R15](release.md#r15-automatic-freeze) read them.

### O7 Two alert levels

Page: customers are affected and the incident agent hasn't contained it within the product's set time, or data or security is involved. Digest: everything else, daily, linking issues. No severity scales beyond these.

Reason: anything not worth waking a human for belongs in the digest.

Enforcement: alert definitions declare their level; a static check rejects any other level.

### O8 Watching the watcher

A check outside the system pages when telemetry stops arriving, alerting or the incident agent is down, or synthetic journeys stop running. Silence never counts as healthy.

Reason: a dead monitor looks exactly like a healthy system.

Enforcement: an external heartbeat check; a drill stops telemetry and gets paged.

### O9 Proactive sweeps

Daily, agents look through telemetry for problems below the alert line: slow drift, rising tolerance counters ([D7](data.md#d7-visible-tolerance)), new error codes, unused endpoints, releases slightly worse than the one before. They open issues with evidence and change nothing.

Reason: nobody used to have time to read all the telemetry; agents do.

Enforcement: a scheduled agent task whose only write access is the issue tracker.

## Response

### O10 Agent first responder

An incident agent takes each alert first. It reads telemetry, correlates the alert with deploy markers and flag flips, contains the problem with O11's actions, and lands the fix through main, then prepares the qualified production candidate ([R6](release.md#r6-minimal-production-candidates)).

Reason: an agent responds in seconds, at any hour.

Enforcement: alerts route to the incident agent; its credentials cover only telemetry, O11's actions and opening PRs.

### O11 Pre-approved actions

Without asking, the incident agent may revert the server to the previous build ([R9](release.md#r9-automatic-abort)), halt a client rollout, turn a kill switch off, freeze releases, add capacity, and quarantine records ([D6](data.md#d6-quarantine-undecodable-records)). It never changes or restores data, raises the minimum version, deletes anything, or changes permissions or secrets, except revoking a leaked credential.

Reason: everything allowed can be undone, and nothing allowed touches data.

Enforcement: each action is a separate pipeline operation the agent's credentials can call; nothing else is callable.

### O12 Incident agent guardrails

One agent owns each incident. Every action goes to the incident record and the [security log](access.md#s16-security-log). An action that doesn't improve the affected journeys within minutes is undone and the agent pages. After a few actions without improvement, it stops and pages.

Reason: an agent flailing in production makes incidents worse.

Enforcement: the action operations enforce ownership, logging, the improvement check and the action limit.

### O13 Reading production data

When diagnosis needs data, not telemetry, an agent gets read access to one company's data through [support access](access.md#s11-support-access). Nobody has standing database access.

Reason: the same rule for agents and humans.

Enforcement: S11's enforcement.

### O14 Customer communication

Impact is computed per company. The status page updates automatically from confirmed facts. Anything written to customers needs Tobias's approval.

Reason: with a database per company, most incidents affect some companies; telling everyone causes alarm, and what is said in an apology is a human call.

Enforcement: the status page reads incident state; customer messages are drafts until approved.

## Learning

### O15 Incidents close with a check

Every incident gets an automatic record: a timeline from alerts, deploys and actions, the cause, and the fix PR. The fix PR includes a black-box case, built from telemetry with personal values replaced, that fails before the fix and passes after. When a case can't reproduce the cause, as with infrastructure failures, a static check or monitoring rule takes its place. The incident closes only when that case or check exists.

Reason: the system gets harder to break every week, not just fixed.

Enforcement: the incident record can't close without a linked case or check.
