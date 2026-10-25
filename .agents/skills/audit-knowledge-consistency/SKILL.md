---
name: audit-knowledge-consistency
description: Find and fix duplicated or contradictory knowledge in a note collection. Use when asked to check consistency, deduplicate, reconcile contradictions, consolidate notes, or audit an instruction file against the knowledge it governs.
---

# Audit knowledge consistency

The goal is one coherent body of knowledge. Age is not a finding by itself: an undated evergreen note is fine. A dated fact past its recheck date is a finding, because it now instructs a reader to re-derive rather than assert.

## Judgment

Run the collection's own checks first and fix what they report. A check settles mechanics; everything below it needs a reader.

For each expired note, re-derive the fact from its source, then either correct the claim or move the date. Never move a date without re-deriving: a fresh date over an unverified fact hides the rot.

For an instruction file, give every line a reader, a moment, and a consequence: which agent reads it, at which point in their work, and what breaks if the line goes. A line whose reader never has that file open belongs at that moment's owner, and the file keeps a pointer or nothing.

Then search the notes for overlapping claims and classify each candidate:

- **Duplicate:** the same reusable claim twice with no distinct purpose. Merge into the clearest owner, keep unique qualifiers, rewrite rather than append.
- **Scoped difference:** different versions, dates, environments or scopes. Make the scope explicit; it is not a conflict.
- **Contradiction:** both cannot hold in the same scope. Resolve from the strongest evidence: explicit supersession by the same authority, a verified source, current state. Recency alone proves nothing.

Report what changed and every open question, including a duplicate whose answer is the owner's preference rather than a fact.

## Verification

Every reported failure is either fixed or stated with its reason. No expired note keeps a moved date without a re-derived fact behind it.
