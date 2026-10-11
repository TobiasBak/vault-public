# Chief of staff state

Owned by the [chief-of-staff](SKILL.md) skill. Public: no secrets, credentials, source code, or nonpublic employer or customer details.

## Teams

Census 2026-10-11: every unsettled top-level thread.

- [Compile-once mutation engine for Rust](t3-thread://v1/mcp:59b74fed-0a50-4a67-b357-da1e1490a157) (rust-mutants): rmut engine done; stepkit-geometry PR #39 open, local gate green, no CI checks. Waiting on the merge decision.
- [Optimize Agent Workflows for Orderready](t3-thread://v1/7a790d6e-5034-4970-ba3c-56be1bc8e3a9) (orderready): runner fixes merged; five backend cases running across two agents.
- [Developer-Focused Conversation Context](t3-thread://v1/0035fcfe-aea0-4c3e-a978-cc7d54ca50d7) (vault): context-layout experiment; snapshot variant lost (+33% cost, +20% time); pulling tool-mix data.
- [Get AX Backend Working With Import GUI](t3-thread://v1/992c5212-f034-4046-8f77-177c546e9822) (work integration project): idle since 2026-10-06 after answering a runner question.

## Needs Tobias

- Merge stepkit-geometry PR #39 (sg mutants on rmut)? Recommend merge: warm run 11–12× faster, 95/100 agreement, gate green. Cold isn't 10× (70–96s) and it changes defaults (changed lines only, `--jobs` removed). Waits: rust-mutants thread.
- Standing merge authority for your own repos (readiness bar: reviews clean, gate green on head)? Recommend yes, via the global instructions; threads otherwise stop at "merging is your call". Waits: nothing now.
- Settle the work integration thread (idle since 2026-10-06)? Recommend settle.

## Hypotheses

- Top-level threads stop at an open PR because no brief gives them merge authority. Matches the pattern in [subagent delegation](../../../agents/subagent-delegation.md#authority-and-shared-state); one fresh incident (rust-mutants).

## Watch

- `coding-models.md` compressed to 1,936 words (f907b4c); throughput split into `agents/pi-throughput.md`. Haiku is reviewing it for lost facts and fixing a design-routing contradiction.
- Pi failed to start a turn once (2026-10-11); a second failure triggers a diagnosis.
