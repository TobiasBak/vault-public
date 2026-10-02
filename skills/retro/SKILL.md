---
name: retro
description: Review coding-agent sessions for concrete improvements to a repository's navigation, checks, tools, and instructions. Use for a repo-focused retrospective, not a vault knowledge review.
disable-model-invocation: true
---

# Repo retrospective

Improve the agent's environment from what actually happened in sessions. The goal is easier work for the next agent, not more rules. Leave source histories unchanged and keep transcripts and runtime state out of commits.

## Select sessions

Use the requested repo and window; default to the current session. "Last N sessions" means the latest N for this repo, not the machine's latest N files. Child-agent work counts as part of its parent run. Read the exchanges and tool results around each candidate, not just summaries. State which sessions you reviewed and any gaps.

## Trace friction to the current repo

Find today's owner, callers, manifests, scripts, checks, and instructions before proposing anything. A problem that has since been fixed needs no patch.

- **Navigation:** failed searches, misleading names, stale pointers, hidden dependencies, scattered ownership. Fix names and boundaries before adding file maps.
- **Checks:** mistakes a deterministic check could catch. Repair an unwired or broken existing check before inventing one. Missing CI alone doesn't justify new infrastructure.
- **Review and instructions:** repeated steering, contradictory or duplicated rules, no-op coaching. Mechanical rules go to checks and judgment to scoped review guidance. Reviewers need callers and contracts, not just the diff.
- **Tools:** repeated expensive calls, missing logs, awkward control interfaces, inaccessible evidence.

Separate recurring friction from isolated mistakes, normal exploration, changed intent, and useful clarification. Turn count, tone, or one slow search proves nothing.

## Recommend

Strongest first. For each, give the session event, the current location, the likely cause, and a concrete fix, with enough provenance to revisit it without quoting private transcripts. "No findings" is a valid result. Prefer fixes to ownership, names, tooling, and feedback over more AGENTS prose.

## Verification

Name what would show each fix worked. After fixing, repeat the failed lookup, command, or user path and run the relevant behavioral checks; for navigation, confirm a fresh search reaches the owner. A shorter doc or green build doesn't prove the friction is gone.
