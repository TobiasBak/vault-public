# Data and persistence

Scope: any data that outlives the process that wrote it or crosses between processes: databases, documents, files, events, queue messages, client-local stores, caches.

Principles:
- One source of truth. Newer versions win: auto-update and a minimum supported version replace supporting old clients.
- Additive changes are free at any time. Destructive changes (remove, rename, change type or meaning) take two steps (D5).
- Fix forward. No down migrations.

## Reading

### D1 Tolerant reads

Readers accept fields they don't recognize and keep them intact.

Reason: old code still running reads data new code wrote. Halting on an unknown field turns a deploy into an outage.

Enforcement: persisted record types never reject unknown fields (serde: no `deny_unknown_fields`); a static check rejects it on persisted types. D12's cross-version case reads, modifies and rewrites a record with an extra field, and the field survives.

### D3 Defaults for missing fields

A new field has a declared default for records written before it existed.

Reason: new code reads old records.

Enforcement: new fields are optional or defaulted in the record type; D12's cross-version case reads old-version records.

### D4 Unknown enum values

A value the reader doesn't recognize in a field it knows decodes to a typed `Unknown` variant carrying the raw value. The record is hands off for that version: displayed read-only, marked "handled by a newer version", with no state change or side effect.

Reason: the reader can't ignore a field it decides on. Guessing a default ships the order that is on hold.

Enforcement: persisted enums have an `Unknown(String)` variant, and exhaustive matching forces every caller to handle it. Enums used only in memory have none.

### D6 Quarantine undecodable records

A record that can't be decoded fails alone. It is marked failed with the error, shown to the operator as needing attention, and reprocessed automatically once a fixed version is deployed. It never stops the process or batch.

Reason: halting takes the system down; a log line nobody reads silently drops business work.

Enforcement: black-box case with one corrupt record among valid ones: the valid ones are processed, the corrupt one is quarantined and visible, and it is processed after the fix.

### D7 Visible tolerance

Unknown fields, unknown enum values and quarantined records are counted per record type and exposed in metrics.

Reason: tolerance nobody sees hides drift, typos and stalled migrations.

Enforcement: the D1, D4 and D6 cases assert the counters.

## Writing

### D2 Owned-field writes

Each record type has one owning module; all writes go through it. A writer changes only the fields it owns, through a typed partial update. Whole-record overwrites of shared records are forbidden.

Reason: a whole-record write from code that doesn't know a field deletes it silently.

Enforcement: the owning module exposes typed update commands and no `save(record)` for shared records. An unavoidable whole-document write round-trips unknown fields (`#[serde(flatten)] extra`), covered by the D1 case.

### D8 Strict commands

Inbound commands from clients and agents reject unknown fields and invalid values with an error naming the field. Servers deploy before the clients that send their new fields.

Reason: on input, an unknown field is a typo (`delivery_adress`) that would otherwise drop data silently.

Enforcement: command types reject unknown fields (serde: `deny_unknown_fields`); a black-box case sends a misspelled field and gets the error. Release tooling blocks a client release whose required server version is not live.

### D9 Optimistic concurrency

Shared records carry a version. A write states the version it read; a stale write fails, and the writer reloads and retries.

Reason: two writers that load the same version and both save lose the first change with no error.

Enforcement: the owning module's update commands take the read version; a black-box case runs two conflicting writes and asserts one retries and both changes survive.

### D18 Idempotent commands

Creates carry a client-generated record ID (UUIDv7). Other commands with effects carry a client-generated operation ID that is stored on the record they create or update, behind a unique constraint. Repeating a command is a no-op. No time-limited key cache.

Reason: retries (D9), offline replay (D13) and network timeouts resend writes that may already have landed. A unique constraint dedupes for the record's lifetime with no expiry to tune.

Enforcement: command types require the ID; the database enforces uniqueness; a black-box case sends the same command twice and gets one effect.

## Changing the schema

### D5 Two-step destructive changes

To remove, rename or retype a field: version X stops reading and writing it. A separate change raises the minimum supported version to X or higher. The field is dropped only when the minimum is at least X and no live client below X has been seen. Meaning never changes in place; a new meaning gets a new field.

Reason: tolerant reads can't save code that still needs a removed field or reads a changed meaning.

Enforcement: D12's compatibility check.

### D10 Migrations own the schema

Migrations are the schema's source of truth. The build fails when code doesn't match the schema.

Reason: one place to change; generated migrations hide destructive changes in a diff nobody reads.

Enforcement: compile-time-checked queries or an equivalent schema check in the build.

### D11 Migration execution

Additive migrations run as a separate step before the code that needs them. Backfills run as resumable jobs that are safe to repeat, never at startup. Nothing destructive runs at startup. A client that owns its local store migrates it additively on open.

Reason: old code must keep working on the new schema during a deploy; long rewrites at startup block or race instances.

Enforcement: the deploy pipeline runs migrations before rollout; a static check rejects destructive statements outside D5 changes.

### D12 Compatibility gate

CI compares the schema and stored formats with the last release and classifies every change as additive or destructive. A destructive change is blocked unless D5's conditions hold. A black-box case runs the new code on data written by the previous release, and the previous release on data written by the new code.

Reason: an agent will rename a field in one PR; review won't catch every one.

Enforcement: the check and case run in pre-commit and CI.

## Clients and versions

### D13 Minimum supported version

Clients auto-update. The server refuses requests from clients below the minimum supported version with "update required". Such a client never writes to the source of truth: it updates, then the new version sends its unsent local work. If the update fails, it stays read-only and says why. Every request carries the client version, which is how the server knows the live versions (D5).

Reason: supporting a long tail of old clients makes every change destructive for someone.

Enforcement: black-box case: a client below the minimum is refused, updates, and its local work arrives once (D18).

## Recovery and history

### D14 Record-level repair

The source of truth has point-in-time recovery. Each backfill keeps the old values until it is verified, so individual records can be restored without rolling back the store.

Reason: fixing forward repairs code, not data already written wrong, and a whole-store restore discards every good write since.

Enforcement: backfill jobs write old values before changing them; a recovery drill restores a record from a past point.

### D15 Traceable writes

Every record has audit columns (`created_at`, `updated_at`, writer identity). Business-critical records (orders, money, anything with external side effects) have a history maintained by the database, including deletes, with each change carrying its request ID. Logs and traces carry the release version and request ID.

Reason: diagnosing and repairing bad data starts with what changed, when, and which deploy did it.

Enforcement: history comes from the database (temporal tables, audit trigger or change data capture), so app code can't skip it; a black-box case changes and deletes a critical record and finds both in the history.

### D16 Erasable personal data

Personal data lives in its own records that other records and history only reference. Erasure deletes or pseudonymizes those records. Personal data that reaches history anyway is pseudonymized in place.

Reason: GDPR erasure must work without destroying the record of what happened.

Enforcement: black-box case erases a person and finds no personal values in current records or history.

### D17 Disposable derived data

Caches, indexes, materialized views and aggregates are rebuildable from the source of truth, keyed by the version of the code that computed them, and never the only copy of anything.

Reason: when an agent changes a computation, old entries are silently wrong. Rebuilding beats migrating.

Enforcement: the key includes the computation version; a black-box case deletes derived data and gets identical results after the rebuild.
