---
name: audit-knowledge-consistency
description: Audit or consolidate materially duplicated and contradictory knowledge in this vault. Use only when the user explicitly asks to check knowledge consistency, find duplicate notes or claims, find contradictions, reconcile conflicts, or consolidate a stated vault scope. Do not trigger from note age, schedules, routine writing, or ordinary conversation.
---

# Audit knowledge consistency

Use `AGENTS.md` for authority and `Knowledge bank/Knowledge consistency.md` for duplicate and contradiction policy. An audit is read-only; an explicit consolidation request permits safe integration within its scope. Neither authorizes unrelated restructuring or choosing winners in unresolved conflicts.

Resolve `VAULT_ROOT` from the governing vault and `SKILL_DIR` from this skill's directory. Inspect `conflicts.md` alongside the requested notes. The index is orientation, not evidence that an unlisted note does not exist.

## Inspect the requested scope

Search every note in scope for overlapping claims, competing authorities, and materially duplicated knowledge. Distinguish duplicates from complementary knowledge, intentional repetition, scoped differences, clear corrections, contradictions, and uncertainty under the canonical policy. Newer dates alone do not settle a conflict.

For a vault-wide audit, include visible Markdown notes and root operating notes. Hidden runtime and tool directories are separate from living knowledge. Ordinary subject-local writing does not require this workflow.

The read-only link verifier checks visible Markdown across the vault, including wikilinks, headings, block references, ambiguity, and case differences:

```bash
python "$SKILL_DIR/scripts/verify_links.py" --vault "$VAULT_ROOT" --json
```

Keep its output as the structural baseline. Hidden files are not scanned as source notes, but explicit Markdown links to hidden files and directories are checked, including anchors in Markdown targets. External URLs are not fetched. Report unrelated existing link failures without silently widening the edit scope.

## Report or integrate

Make findings reviewable with the affected locations, competing or overlapping claims, proposed treatment, and any unique knowledge or unresolved decision. Do not manufacture duplicates from similar wording.

For authorized integration, use the clearest existing subject note, preserve useful distinctions and provenance, and update affected links. Auto-resolve actual contradictions only for explicit supersession by the same authority or verified transcription/citation errors. Other contradictions go to `conflicts.md` for human resolution. Whole-note deletion, substantial deletion, and broad restructuring require explicit authorization under AGENTS.md.

After integration, reread affected claims, search for obsolete wording, and rerun the link verifier against the baseline. Report changed notes and remaining decisions. No fixed report format is required.
