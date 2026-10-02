# Vault

Tobias's public knowledge bank. It exists for agents: they retrieve from it and maintain it. Tobias does not read it.

## Find

Start at [index.md](index.md), then search with `rg`; the index is not exhaustive. [projects.md](projects.md) routes to repositories, which own their own implementation detail.

## Write

- Save what would change how a future agent decides or acts: findings, corrections, preferences, rationale, useful failures, established procedures. Skip routine activity, generic advice, and anything cheap to look up again.
- One idea, one home. Search first, edit the owning note, and link instead of restating.
- Lead with the conclusion. Prefer rules and short bullets to narrative. Drop hedges and "X does not mean Y" unless the misreading is likely and costly.
- Date only volatile facts such as versions, prices, and availability. Keep sources only where authority or exact numbers matter. For optimizations, keep baseline, change, effect, and conditions.
- Use kebab-case filenames, relative Markdown links, and no frontmatter. Keep [index.md](index.md) in sync when adding, moving, or removing notes.
- Compress, merge, and restructure freely. When notes contradict, fix them from the best evidence; ask Tobias only when the answer is his preference.
- Check links after moving things: `python .agents/skills/audit-knowledge-consistency/scripts/verify_links.py --vault .`

## Skills

`skills/<name>/` holds Tobias's global agent skills; `.agents/skills/` holds vault-only ones. `scripts/install-skills.sh --fix` (or `.ps1 -Fix` on Windows) links every global skill into `~/.agents/skills`, which Codex and Pi read; dotfiles symlinks `~/.claude/skills` to it.

- Every global skill has `SKILL.md` and `agents/openai.yaml`. Explicit-only skills set both `disable-model-invocation: true` and `policy.allow_implicit_invocation: false`; model-invoked skills set neither.
- Skills that guide code changes end with a `Verification` section naming the behavioral check expected.
- `domain-modeling`, `grill-with-docs`, `grilling`: byte-identical from Matt Pocock; refresh with `scripts/update-vendored-skills.sh`, never hand-edit. `frontend-design` is Anthropic's with local metadata, explicit-only invocation (so it doesn't fight `ui-design`), and a `Verification` section. Adapted skills carry `SOURCE.md` and `LICENSE`.

## Public repository

Keep secrets, credentials, private correspondence, other people's personal data, and nonpublic employer or customer details out of commits. Tobias's own preferences and project notes are meant to be public. Raw session histories and local runtime state stay out of Git.
