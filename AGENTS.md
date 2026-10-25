# Vault

Tobias's public knowledge bank. It exists for agents: they retrieve from it and maintain it. Tobias does not read it.

## Purpose

Notes that change how a future agent decides or acts: findings, corrections, preferences, rationale, useful failures, established procedures.

## Values

1. **Transferable knowledge beats completeness.** A note earns its place by changing a decision.
2. **One home per idea beats restating.** Search first, edit the owning note, link instead of copying.
3. **Mechanisms beat reminders.** A failing check first, then config, then a sentence.
4. **Pointers beat an exhaustive index.** One line per note, plus `rg`.

## Loop

**Find.** Start at [index.md](index.md), then search with `rg`.

**Write.** Lead with the conclusion: rules and short bullets, no hedges, and an "X does not mean Y" only where the misreading would be costly. Date volatile facts and keep a source where authority or an exact number matters; for an optimization keep baseline, change, effect, conditions. File a note by its reader, not its subject: kebab-case filenames, relative Markdown links, no frontmatter, and a line in [index.md](index.md) when a note appears, moves or goes. Compress, merge and delete freely; when notes contradict, fix them from the best evidence, and ask Tobias only when the answer is his preference. Every note links to at least one other note.

A note built on facts someone else owns carries `recheck-after: YYYY-MM-DD` near the top: prices, model catalogs, host and CLI behaviour, vendor terms, benchmarks, licenses. Count the date from when the fact was last checked, never from the edit that adds it.

Deleting knowledge about an instance: move anything that generalizes to its class into the note that owns the class, then delete the rest. Record a rejection as a config rule wherever it can be one; the note only explains why the rule exists.

**Skills.** `skills/<name>/` is the source of truth for the global skills; `.agents/skills/` holds vault-only ones, linked from `.claude/skills`, and only `chief-of-staff` keeps `disable-model-invocation` because only Tobias invokes it. Installing, and refreshing a vendored skill, is `scripts/install-skills.sh --help` and `scripts/update-vendored-skills.sh --help`; the scripts own the flags and the vendored list.

**Check.** `scripts/check-vault` runs links, staleness, a note's outbound link, skill shape, duplicate authority, and the shape of this file and the index. It is also this repository's commit hook, installed with `ln -sf ../../scripts/check-vault .git/hooks/pre-commit`; the workstation secret scanner runs first and chains to it.

## Boundaries

- Never record project work: no status, progress, results, decisions, findings or plans for a specific project. That belongs in the project's repository; the chief of staff keeps its operational state in `~/.local/state/chief-of-staff/`.
- [projects.md](projects.md) holds only routes to public repositories: path, remote, branch and where to start. Private repositories are never listed, and a line changes only when a route changes.
- Keep secrets out: tokens, keys, passwords and credential contents. Also keep out private correspondence and other people's personal data. Everything else may be public (Tobias, 2026-10-18), including customer and order names and private-repo operational detail such as credential file paths, hosted project IDs and infrastructure state. Raw session histories and local runtime state stay out of Git.
- Never bypass the workstation's secret-scanning hooks or GitHub push protection. On a finding or scan failure, stop and report only the path, commit SHA and rule ID; never add a scanner suppression here.
- Land on `main` directly and push, with no PRs or branches.
- `README.md` is the public landing page and links only to [index.md](index.md) and this file.
