# Index

Not exhaustive. Search with `rg`.

- [AGENTS.md](AGENTS.md): how to use and maintain this vault
- [projects.md](projects.md): repository routes and ownership (Dotfiles, T3 Code)

## Tobias

- [tobias/preferences.md](tobias/preferences.md): engineering taste, stack, testing, how to involve him
- [tobias/partnership.md](tobias/partnership.md): agent character, voice, disagreement, and pressure tests
- [tobias/shopping.md](tobias/shopping.md): shopping priorities and Danish availability

## Agents

- [agents/agent-native-codebases.md](agents/agent-native-codebases.md): patch accretion, making the easy change correct, the knowledge-placement order, enforce-first hardening
- [agents/documentation-and-naming.md](agents/documentation-and-naming.md): what prose keeps, the no-comments rule, code as a search surface
- [agents/instructions-and-prompts.md](agents/instructions-and-prompts.md): what belongs in AGENTS.md, placement, task contracts, execution habits
- [agents/context-engineering.md](agents/context-engineering.md): working set vs record, state tiers, compaction and checkpoints, tool output, skills, text-as-image
- [agents/subagent-delegation.md](agents/subagent-delegation.md): when and how to split work, handoffs, one writer
- [agents/code-review.md](agents/code-review.md): reviewer inputs, retrieval, lenses, findings
- [agents/orchestration.md](agents/orchestration.md): loops vs graphs, programmatic tool calling (OpenAI and Anthropic), OpenAI dots
- [agents/testing-with-agents.md](agents/testing-with-agents.md): agentic E2E, verification CLIs and feature maps, fresh-agent handoff, refactor equivalence, test pruning, team adoption
- [agents/learning-from-feedback.md](agents/learning-from-feedback.md): memory types, feedback weighting, evidence gates, outcome-based learning, forbidden inferences
- [agents/autoresearch.md](agents/autoresearch.md): experiment-loop requirements and Tobias's scout/screen/confirm system
- [agents/benchmark-trust.md](agents/benchmark-trust.md): benchmark failure types, SWE-Bench Pro vs DeepSWE, evidence ranking
- [agents/coding-models.md](agents/coding-models.md): Opus-orchestrates-Sol setup, model roles and effort, Sol vs Astra cost, model specifics, Codex/Pi/Claude Code/OpenCode host specifics
- [agents/ui-design-convergence.md](agents/ui-design-convergence.md): generic AI UI style and the restrained-design fix
- [agents/jev.md](agents/jev.md): TypeSafe's Jev decision model, limits, and where it fits

## Software

- [software/architecture.md](software/architecture.md): spotting architectural decisions, styles, ports and adapters, an order-integration example
- [software/api-design.md](software/api-design.md): consumer-shaped APIs, one contract, lifecycle, events, errors, plugins, persisted-format renames
- [software/ai-era-durability.md](software/ai-era-durability.md): what survives cheap AI, the typed-plan architecture, provider-native harnesses
- [software/performance-aware-data-design.md](software/performance-aware-data-design.md): when data layout dominates hot paths
- [software/typescript.md](software/typescript.md): TypeScript 7 baseline, one authority per layer
- [software/effect.md](software/effect.md): Effect, and when it's worth it
- [software/gigatoken.md](software/gigatoken.md): fast Rust tokenizer runtime
- [software/browser-derived-clients.md](software/browser-derived-clients.md): turning browser traces into HTTP clients; Danish supermarket offers
- [software/cloudflare.md](software/cloudflare.md): API tokens as JSON policy documents or Terraform/OpenTofu, bootstrap and state caveats, Access with Worker destinations
- [software/supabase.md](software/supabase.md): CLI config-push cwd quirk, free-plan pausing and restore
- [software/windows-gui-automation.md](software/windows-gui-automation.md): UIA-first tools, state capture, keeping the desktop alive after RDP

## Global skills (`skills/`)

All model-invoked; agents select relevant skills automatically:
- `potato-approach`: make agent-maintained codebases easy to change correctly, including design red flags and mining mistake history
- `theodore-kaczynski-nullifier`: shape repos so agent feedback outruns agent thinking; black-box-only tests, cached verdicts, always-on watchers
- `benchmark-checklist` (adapted from pstack): vet a performance number before reporting it
- `unslop`: concise, natural prose
- `domain-modeling` (Matt Pocock): glossary and ADRs
- `grilling` (Matt Pocock): stress-test a plan by interview
- `frontend-design` (Anthropic): distinctive, intentional visual design
- `grill-with-docs` (Matt Pocock): grilling plus domain docs
- `maintainability-audit`: how easily fresh agents can change the source
- `repo-context-audit`: which instructions and docs earn their place
- `retro`: repo improvements from session friction
- `review-test-quality`: keep, rewrite, or delete tests
- `create-verification-skill`, `maintain-verification-skill` (adapted from pstack): project verification skills and feature maps

## Vault-only skills (`.agents/skills/`)

- `audit-knowledge-consistency`: find and fix duplicate or contradictory knowledge, and verify links
- `review-agent-history`: mine Pi and Codex histories for reusable knowledge
