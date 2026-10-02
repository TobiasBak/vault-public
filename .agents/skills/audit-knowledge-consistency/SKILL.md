---
name: audit-knowledge-consistency
description: Find and fix duplicated or contradictory knowledge and broken links in this vault. Use when asked to check consistency, deduplicate, reconcile contradictions, or consolidate notes.
---

# Audit knowledge consistency

The goal is one coherent body of knowledge. Note age and missing dates are never findings on their own.

## Run

1. Baseline the links (wikilinks, Markdown links, headings, anchors; external URLs aren't fetched):
   ```bash
   python "$SKILL_DIR/scripts/verify_links.py" --vault "$VAULT_ROOT" --json
   ```
2. Search every in-scope note for overlapping claims. Classify each candidate:
   - **Duplicate:** the same reusable claim in two places with no distinct purpose. Merge into the clearest owning note, keep unique qualifiers and links, rewrite rather than append, and repoint links. A short orientation line in the index is not a duplicate.
   - **Scoped difference:** different versions, dates, environments, or scopes. Make the scope explicit in the notes; it isn't a conflict.
   - **Contradiction:** both can't be true under the same scope. Resolve it from the strongest evidence (explicit supersession by the same authority, verified source, current repo state). Recency alone proves nothing. If the answer is Tobias's preference and the evidence doesn't settle it, ask him.
3. Rerun the link check, search for leftover old wording, and report the changed notes and any open questions.
