# Vault

Tobias's public knowledge bank. It exists for agents: they retrieve from it and maintain it. Tobias does not read it. The [chief of staff](.agents/skills/chief-of-staff/SKILL.md) owns its quality.

## Find

Start at [index.md](index.md), then search with `rg`; the index is not exhaustive. [projects.md](projects.md) routes to repositories, which own their own implementation detail.

## Write

- Save what would change how a future agent decides or acts: findings, corrections, preferences, rationale, useful failures, established procedures. Skip routine activity, generic advice, and anything cheap to look up again.
- One idea, one home. Search first, edit the owning note, and link instead of restating.
- File a note by its reader, not its subject: `agents/` for how an agent should behave and what its harness does, `software/` for facts about systems and tools, `hardware/` and `tobias/` for their own. Every note links to at least one other note, so a reader can traverse sideways.
- Never record project work in the vault: no status, progress, results, decisions, findings or plans for a specific project. That belongs in the project's repository. The chief of staff keeps its operational state outside the vault, in `~/.local/state/chief-of-staff/`. [projects.md](projects.md) holds only routes to public repositories: path, remote, branch and where to start. Private repositories are never listed. Update it only when a route changes.
- Lead with the conclusion. Prefer rules and short bullets to narrative. Drop hedges and "X does not mean Y" unless the misreading is likely and costly.
- Date only volatile facts such as versions, prices, and availability. Keep sources only where authority or exact numbers matter. For optimizations, keep baseline, change, effect, and conditions.
- A note built on facts someone else owns carries a line `recheck-after: YYYY-MM-DD` near the top: prices and model catalogs, host and CLI behavior, vendor terms, benchmark and licensing claims. Guidance is provisional, so the line marks when to re-derive the fact instead of following the note. Count the date from when the fact was last checked, never from the edit that adds the line. Expiry never means the note was wrong, and it is never a reason to delete it.
- Use kebab-case filenames, relative Markdown links, and no frontmatter. Keep [index.md](index.md) in sync when adding, moving, or removing notes.
- Compress, merge, and restructure freely. When notes contradict, fix them from the best evidence; ask Tobias only when the answer is his preference.
- Deleting knowledge about a specific instance? Move anything that generalizes to its class into the note that owns the class, then delete the rest. Record a rejection in config wherever it can be one: a deny rule or failing check outlives prose, and the note only explains why the rule exists.
- Check links after moving things: `python .agents/skills/audit-knowledge-consistency/scripts/verify_links.py --vault .`
- `scripts/check-vault` runs both checks. It is this repository's commit hook (`ln -sf ../../scripts/check-vault .git/hooks/pre-commit`, which the workstation secret scanner chains after itself); it fails a commit that edits a note still past its recheck date, or adds a knowledge note that links to no other note.
- Check dated facts before relying on a note: `python .agents/skills/audit-knowledge-consistency/scripts/verify_staleness.py --vault .`. A note past its `recheck-after` gets the fact re-derived now, then either the claim corrected or the date moved. A malformed or duplicated line fails the check, because a broken date silently disables the reminder.

## Skills

`skills/<name>/` holds Tobias's global agent skills; `.agents/skills/` holds vault-only ones. `.claude/skills` links to `.agents/skills` so Claude Code sees the vault-only ones too. `chief-of-staff` is the one skill only Tobias invokes; keep it that way. `scripts/install-skills.sh --fix` (or `.ps1 -Fix` on Windows) links every global skill into `~/.agents/skills`, which Codex and Pi read; dotfiles links each global skill into `~/.claude/skills` too.

- Every global skill has `SKILL.md` and `agents/openai.yaml`. All global skills are model-invoked: omit `disable-model-invocation` and `policy.allow_implicit_invocation`. Tobias wants agents to discover relevant skills without him remembering their names. Descriptions must say when the skill applies.
- Keep each global skill self-contained: instructional file links stay inside its own directory, not vault notes or sibling skills. Vault-wide deduplication stops at the skill boundary.
- Skills that guide code changes end with a `Verification` section naming the behavioral check expected.
- `domain-modeling`, `grill-with-docs`, `grilling`: vendored from Matt Pocock; refresh with `scripts/update-vendored-skills.sh`. Keep upstream content byte-identical except local invocation metadata; the updater removes `disable-model-invocation`. Never hand-edit their bodies. `frontend-design` is Anthropic's with local metadata and a `Verification` section; `unslop` is adapted from Lauren Tan's pstack. Adapted skills carry `SOURCE.md` and `LICENSE`.

## Public repository

Keep secrets out of commits: tokens, keys, passwords and credential contents. Also keep out private correspondence and other people's personal data. Everything else may be public (Tobias, 2026-10-18), including customer and order names and private-repo operational detail such as credential file paths, hosted project IDs and infrastructure state. Raw session histories and local runtime state stay out of Git.

Never bypass the workstation's secret-scanning hooks or GitHub push protection. On a finding or scan failure, stop and report only the path, commit SHA and rule ID; do not add scanner suppressions here.

After checking vault changes against these rules, commit directly to `main` and push without asking, with no PRs or branches.
