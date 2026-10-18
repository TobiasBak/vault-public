# Data and persistence

Requirements for any store that code versions share: databases, document stores, queues, event logs, caches with a long life.

## D1 Tolerant reads

Code reading persisted data accepts fields it doesn't recognize and keeps them intact.

Reason: older code reads rows newer code wrote. Halting on an unknown field turns every deploy into an outage.

Enforcement: persisted record types never reject unknown fields (serde: no `deny_unknown_fields`); a static check rejects it on persisted types. Black-box case: a row with an extra field is read, modified and still has the field afterward.

## D2 Owned-field writes

A writer changes only the fields it owns, through a typed partial update (`UPDATE ... SET status`, JSON patch). Whole-record overwrites of shared records are forbidden.

Reason: read-modify-write of a whole record by older code silently deletes fields newer code wrote, with no error.

Enforcement: the persistence API exposes typed update commands and no `save(record)` for shared records. Where a whole-document write is unavoidable, the record type round-trips unknown fields (`#[serde(flatten)] extra`), covered by the D1 case.

## D3 Defaults for missing fields

A field newer code adds has a defined default for rows written before it existed.

Reason: newer code reads old rows. D1 covers old code reading new data; D3 covers the reverse.

Enforcement: new fields are optional or have a declared default in the record type; the D1 case also runs an old-version row.

## D4 Unknown enum values

An enum value the reader doesn't recognize decodes to a typed `Unknown` variant carrying the raw value. Logic over it fails safe for that record.

Reason: newer code adds states (`on_hold`) older code has never seen.

Enforcement: persisted enums have an `Unknown(String)` variant; exhaustive matching forces every caller to handle it. Domain enums used only in memory have no such variant.

## D5 Stable meaning

A field's meaning and type never change once written. Change goes expand, migrate, contract: add the new field, backfill, switch readers, and remove the old field only after no running code reads it.

Reason: tolerant reads can't save a reader from a field that now means something else.

Enforcement: to be specified.

## D6 Record-scoped failure

A record that can't be decoded fails that record alone, is logged with its key, and never stops the process or the batch.

Reason: one bad row shouldn't halt the system.

Enforcement: black-box case with one corrupt record among valid ones; the valid ones are processed and the corrupt one is reported.

## D7 Visible tolerance

Unknown fields, unknown enum values and decode failures are counted per record type and exposed in metrics or logs.

Reason: tolerance that nobody sees hides drift, typos and stalled migrations.

Enforcement: the D1, D4 and D6 cases assert the counters.

## D8 Strict commands

Inbound commands from clients and agents reject unknown fields and invalid values with an error naming the field.

Reason: on input, an unknown field is almost always a typo (`delivery_adress`) that would otherwise drop data silently. A client may send a new field only after the server that understands it is deployed.

Enforcement: command types reject unknown fields (serde: `deny_unknown_fields`); a black-box case sends a misspelled field and gets the error.
