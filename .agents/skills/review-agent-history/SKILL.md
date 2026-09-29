---
name: review-agent-history
description: Review Pi or Codex histories for reusable knowledge or recurring patterns where agents need correction or excess steering. Use only when the user explicitly requests a history or session-pattern review, never during ordinary sessions.
---

# Review agent history

Review the requested histories for reusable findings or recurring correction patterns. `AGENTS.md` governs promotion into living knowledge and instructions; a history review alone does not authorize those edits.

## Select and inspect histories

Resolve `VAULT_ROOT` from the vault and `SKILL_DIR` from this skill's directory, then scan the requested window:

```bash
python "$SKILL_DIR/scripts/history_review.py" --vault "$VAULT_ROOT" scan --source all
```

The helper defaults to each source's last successful checkpoint, or the last seven days on first use. `--since`, `--until`, `--all`, and `--include-children` adjust selection. Filtering uses whole-file modification time, so resumed sessions are reconsidered. Review every selected normalized session before marking the scan complete.

The helper leaves source histories unchanged and writes normalized data under ignored `.knowledge-bank/state/`. Its credential redaction is incomplete; inspect excerpts before reproducing or saving them.

## Interpret findings

Compare candidate knowledge with existing subject notes and relevant repository authority. Provide source routes and proposed changes where a finding is worth retaining, rather than copying transcripts into living notes.

For recurring-pattern reviews, distinguish observable correction or recovery from changed intent, ambiguity, or justified clarification. Tone, silence, and turn count alone do not establish dissatisfaction. Normally support a recurring pattern with at least two independent sessions; label an isolated incident as isolated.

Let the requested scope and material findings determine the report. An improvement may be a tool fix, instruction removal, a scoped knowledge change, or no change. Repetition does not automatically justify another rule.

## Finish the reviewed scan

Present candidates before integration unless promotion is already explicitly authorized. Once every candidate has been handled, including rejection or deferral, complete the exact scan manifest:

```bash
python "$SKILL_DIR/scripts/history_review.py" --vault "$VAULT_ROOT" complete "/absolute/path/to/manifest.json" --review-complete
```

Do not advance checkpoints after a failed scan, extraction error, or incomplete review. The shared helper also provides `search` and `show` for exact session recall; preserve those commands when changing this workflow.
