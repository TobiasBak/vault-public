---
name: audit-knowledge-consistency
description: Find and fix duplicated or contradictory knowledge and broken links in this vault. Use when asked to check consistency, deduplicate, reconcile contradictions, or consolidate notes.
---

# Audit knowledge consistency

The goal is one coherent body of knowledge. A note's age is not a finding by itself: undated evergreen notes are fine. A dated fact past its `recheck-after` is a finding, because it now tells agents to re-derive before relying on it rather than asserting something false.

## Run

1. Baseline the links (wikilinks, Markdown links, headings, anchors; external URLs aren't fetched):
   ```bash
   python "$SKILL_DIR/scripts/verify_links.py" --vault "$VAULT_ROOT" --json
   ```
2. List the dated facts due for recheck:
   ```bash
   python "$SKILL_DIR/scripts/verify_staleness.py" --vault "$VAULT_ROOT" --json
   ```
   For each expired note, re-derive the fact from its source and then either correct the claim or move the date. Fix a malformed or duplicated `recheck-after` line by hand; its exit code is a real failure, not a reminder.
3. Search every in-scope note for overlapping claims. Classify each candidate:
   - **Duplicate:** the same reusable claim in two places with no distinct purpose. Merge into the clearest owning note, keep unique qualifiers and links, rewrite rather than append, and repoint links. A short orientation line in the index is not a duplicate.
   - **Scoped difference:** different versions, dates, environments, or scopes. Make the scope explicit in the notes; it isn't a conflict.
   - **Contradiction:** both can't be true under the same scope. Resolve it from the strongest evidence (explicit supersession by the same authority, verified source, current repo state). Recency alone proves nothing. If the answer is Tobias's preference and the evidence doesn't settle it, ask him.
4. Rerun both checks, search for leftover old wording, and report the changed notes and any open questions.

## Verification

`verify_links.py` reports no issues and `verify_staleness.py` reports no malformed lines. Expired notes left in place are reported with the reason, never silently dropped.
