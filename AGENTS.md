# Vault

Tobias's public knowledge bank is for agents. Keep knowledge that changes a future decision or action; project-specific work belongs in its own repository, not here.

## Work in the vault

Start at [index.md](index.md), then search with `rg`. Give each idea one home; link rather than copy. A pointer names the idea and where it lives; it does not restate the conditions, because the copy is what drifts. Index every note and skill, and link each note to another note. Resolve contradictions from the best evidence; ask Tobias only when the answer is his preference.

Lead each note with its actionable conclusion, and file it where its reader will look. Use kebab-case filenames, relative Markdown links and no note frontmatter. Date volatile facts and cite sources where authority or exact numbers matter. For an optimization, keep the baseline, change, effect and conditions.

Notes based on externally owned facts such as prices, model catalogs, tool behavior, benchmarks and licenses carry `recheck-after: YYYY-MM-DD` near the top. Count from the last real verification, not the edit adding the date.

Global skills live in `skills/`; [dotfiles](projects.md#dotfiles) owns their installation. Vault-only skills live in `.agents/skills/`, linked from `.claude/skills/`. Only `chief-of-staff` is explicit-invocation-only.

Run `scripts/check-vault` to check the vault before landing. It rejects thirteen identical consecutive words in two files; attribution notices and the index's note summaries quote by design and stay exempt.

## Boundaries

- [projects.md](projects.md) holds public repository routes only; never list private repositories.
- Keep raw session histories and local runtime state out of Git. Never add a secret-scanner suppression in this vault.
- Land directly on `main` and push, without branches or PRs.
- `README.md` is the public landing page and links only to [index.md](index.md) and this file.
