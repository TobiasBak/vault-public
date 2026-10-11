# Chief of staff state

Owned by the [chief-of-staff](SKILL.md) skill. Public: no secrets, credentials, source code, or nonpublic employer or customer details.

## Teams

Census 2026-10-11: every unsettled top-level thread.

- [Optimize Agent Workflows for Orderready](t3-thread://v1/7a790d6e-5034-4970-ba3c-56be1bc8e3a9) (orderready): runner fixes merged; five backend cases running across two agents.
- [Developer-Focused Conversation Context](t3-thread://v1/0035fcfe-aea0-4c3e-a978-cc7d54ca50d7) (pi-workspace-view): v3 snapshot view merged (30ae786), replay +1.8% input cost over native. Told to run the 12-run live benchmark (~$2.30, ~45 min) and report whether v3 cuts rereads and cost.

- [Commit orphaned dotfiles changes](t3-thread://v1/mcp:0f4d0fd5-f94c-4d4a-a748-216f0a333353) (dotfiles): 12 uncommitted files from 2026-10-04 to 2026-10-11, including the live global instructions. Committing them in coherent groups, applying nothing, parking anything half-done.
- Omarchy on the 2 TB disk (CoS-owned until designed): read-only survey running of the disk, its current users, dotfiles Arch support, and Omarchy install paths. Constraint: no reboot or disruption to running teams until Tobias moves; config and T3 server must be ready first. Nothing destructive without Tobias's explicit go on the exact disk and data plan.

## Needs Tobias

None.

## Hypotheses

None open. Missing merge authority was resolved by a standing rule (2026-10-11).

## Watch

- Pi failed to start a turn once (2026-10-11); a second failure triggers a diagnosis.
- The merge-authority rule is live in `configs/agents/AGENTS.md` (uncommitted until the dotfiles team lands it) and in the vault (1217807).
- stepkit mutation runs: budget kills are flaky under load, 1 in 44. Parked by the rust-mutants team (thread settled after PR #39 merged as e9d093e). The fix is either kill confirmation, which diverges from rebuild-per-mutant, or dropping per-case wall budgets during mutation runs. Raise it to Tobias only if it starts to bite.
