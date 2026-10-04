# Code review with agents

Review should follow the change's risks. One agent with native repository and review tools is enough for most work; no orchestrator or telemetry store is needed.

## Inputs

Reviewers need intent, requirements, invariants, base and candidate revisions, the diff, routes to context, and validation evidence. Keep the author's reasoning out of independent reviewers' inputs. Requirement fidelity and repository compliance are separate checks. Name the failure classes that matter (contract drift, missed callers, state transitions, idempotency, external effects, weak behavioral verification) and ask for findings, not a tour.

## Retrieval

- **Authority:** global and project rules stay available. Load a folder's instructions when entering it; nested rules refine broader ones.
- **Evidence:** start from intent and the change map, then follow symbols to callers, callees, tests, types, config, and history as the hypothesis requires.
- Retrieve semantic neighborhoods (related declarations, types, callers, tests across files), not fixed token windows.
- Search changed symbols and domain terms, then reverse references, alternate spellings, adapters, and legacy paths.
- For shared identity rules, check every supported input shape, not just value variations. The same entity may keep facts under a wrapper at the top level and directly on a nested row. A test for placement or numeric noise alone can miss a false split between those representations.
- Cite exact paths. Missing evidence is not a negative, and no findings does not clear unexamined areas. Stop when the requested concerns are covered.

## Reviewers

A lens (security, concurrency, data integrity, API compatibility, test adequacy) needn't be a separate agent. Independent review pays off when failure is consequential, validation is weak, or fresh eyes can challenge assumptions. Start with one general reviewer and add specialists only for distinct risks in the diff. Reviewers may run tools and tests, but only in disposable snapshots; the candidate stays read-only.

**Stop review loops by problem class.** When consecutive rounds keep finding variants of one class, decide whether the class matters at the tool's consequence instead of patching each variant. For a low-consequence tool, record the class as a known limitation and move on; for a high-consequence one, redesign the mechanism. In order-integration #276 (2026-10-04), four rounds of review chased fork and reaping races in a dev-only `stop` command. Each variant needed adversarially narrowed timing to reproduce, and a missed process cost only one stray local worker.

Findings carry location, violated contract or risk, evidence, consequence, and confidence or open question. Start with search, language tooling, and tests. Add AST, semantic-graph, or trace tools only after recurring retrieval failures show the need.

## Learning from review history

If you log reviews to study recurring findings, store them outside the worktree with the target revision, scope, model, effort, and findings. A working-tree fingerprint can't recover uncommitted content, so keep a compressed patch when exact recovery matters. Recurring findings are candidates for code, schema, lint, or CI enforcement; they don't automatically justify new rules. See [agent-native codebases](agent-native-codebases.md).
