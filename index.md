# Index

Not exhaustive. Search with `rg`.

- [AGENTS.md](AGENTS.md): how to use and maintain this vault
- [projects.md](projects.md): public repository routes (Dotfiles, T3 Code)

## Tobias

- [tobias/preferences.md](tobias/preferences.md): engineering taste, stack, testing, how to involve him
- [tobias/partnership.md](tobias/partnership.md): agent character, voice, disagreement, and pressure tests
- [tobias/shopping.md](tobias/shopping.md): shopping priorities and Danish availability
- [tobias/how-to-win.md](tobias/how-to-win.md): Musk's "how to win" principles, Tobias's reflection and open threads; personal, grows over time

## Hardware

- [hardware/agent-era-dev-machine.md](hardware/agent-era-dev-machine.md): cloud-agent build capacity, fleet execution boundaries and genuine hardware deals
- [hardware/colab-in-google-ai-plans.md](hardware/colab-in-google-ai-plans.md): Colab compute units and accelerators bundled with Google AI plans, runtime rules, the Colab CLI

## Agents

- [agents/agent-native-codebases.md](agents/agent-native-codebases.md): patch accretion, making the easy change correct, the knowledge-placement order, enforce-first hardening
- [agents/documentation-and-naming.md](agents/documentation-and-naming.md): what prose keeps, the no-comments rule, code as a search surface
- [agents/instructions-and-prompts.md](agents/instructions-and-prompts.md): what belongs in AGENTS.md, placement, task contracts, execution habits
- [agents/context-engineering.md](agents/context-engineering.md): working set vs record, state tiers, compaction and checkpoints, tool output, skills, text-as-image
- [agents/subagent-delegation.md](agents/subagent-delegation.md): model routing and effort, when and how to split work, handoffs, one writer
- [agents/code-review.md](agents/code-review.md): reviewer inputs, retrieval, lenses, findings
- [agents/orchestration.md](agents/orchestration.md): loops vs graphs, programmatic tool calling (OpenAI and Anthropic), OpenAI dots
- [agents/testing-with-agents.md](agents/testing-with-agents.md): agentic E2E, verification CLIs and feature maps, fresh-agent handoff, refactor equivalence, test pruning, team adoption
- [agents/learning-from-feedback.md](agents/learning-from-feedback.md): memory types, feedback weighting, evidence gates, outcome-based learning, forbidden inferences
- [agents/autoresearch.md](agents/autoresearch.md): experiment-loop requirements, the fast-loop rule (cheap scouts first, rigor only at confirm) and Tobias's scout/screen/confirm system
- [agents/benchmark-trust.md](agents/benchmark-trust.md): benchmark failure types, SWE-Bench Pro vs DeepSWE, evidence ranking
- [agents/coding-models.md](agents/coding-models.md): provider guidance, Sol vs Astra cost, model specifics, Codex/Pi/Claude Code/OpenCode host specifics
- [agents/pi-throughput.md](agents/pi-throughput.md): effective-TPS measurement, subscription rollout claims, local observations
- [agents/ui-design-convergence.md](agents/ui-design-convergence.md): generic AI UI style and the restrained-design fix
- [agents/jev.md](agents/jev.md): TypeSafe's Jev decision model, limits, and where it fits

## Software

- [software/architecture.md](software/architecture.md): spotting architectural decisions, styles, ports and adapters, an order-integration example
- [software/api-design.md](software/api-design.md): consumer-shaped APIs, one contract, lifecycle, events, errors, plugins, persisted-format renames
- [software/ai-era-durability.md](software/ai-era-durability.md): what survives cheap AI, the typed-plan architecture, provider-native harnesses
- [software/performance-aware-data-design.md](software/performance-aware-data-design.md): when data layout dominates hot paths
- [software/cargo-target-cache.md](software/cargo-target-cache.md): shared Cargo target freshness hazards and safe A/B builds
- [software/typescript.md](software/typescript.md): TypeScript 7 baseline, one authority per layer
- [software/effect.md](software/effect.md): Effect, and when it's worth it
- [software/gigatoken.md](software/gigatoken.md): fast Rust tokenizer runtime
- [software/ocr.md](software/ocr.md): Indra OCR candidate, local CPU operation, commercial-license restrictions and vendor benchmark conditions
- [software/browser-derived-clients.md](software/browser-derived-clients.md): turning browser traces into HTTP clients; Danish supermarket offers
- [software/cloudflare.md](software/cloudflare.md): API tokens as JSON policy documents or Terraform/OpenTofu, bootstrap and state caveats, Access with Worker destinations
- [software/supabase.md](software/supabase.md): CLI config-push cwd quirk, privileged Storage completion, free-plan pausing and restore
- [software/windows-gui-automation.md](software/windows-gui-automation.md): UIA-first tools, state capture, keeping the desktop alive after RDP
- [software/t3-code-operations.md](software/t3-code-operations.md): thread/workspace mechanics, secret ownership, webhook setup, Connect and safe restarts
- [software/omarchy-agent-operations.md](software/omarchy-agent-operations.md): package installation, privilege and unprivileged `/proc` safety checks
- [software/omarchy-windows-vm.md](software/omarchy-windows-vm.md): agent use of Tobias's local Windows VM: the `win-vm` CLI, lifecycle ownership, disposable runs, file transfers and setup ownership

## Global skills (`skills/`)

All model-invoked; agents select relevant skills automatically:
- `potato-approach`: make agent-maintained codebases easy to change correctly, including design red flags and mining mistake history
- [`theodore-kaczynski-nullifier`](skills/theodore-kaczynski-nullifier/SKILL.md): self-explanatory, hardened repositories, trustworthy verification and measured feedback costs; shared tools own execution mechanics ([design principles](skills/theodore-kaczynski-nullifier/references/design-principles.md), [tracing](skills/theodore-kaczynski-nullifier/references/tracing.md))
- [`system-specs`](skills/system-specs/SKILL.md): requirement specs for systems agents change several times a day; tolerant at version boundaries, strict elsewhere; [data catalog](skills/system-specs/references/data.md), [release catalog](skills/system-specs/references/release.md), [API catalog](skills/system-specs/references/api.md), [access catalog](skills/system-specs/references/access.md), [observability catalog](skills/system-specs/references/observability.md), [dependencies catalog](skills/system-specs/references/dependencies.md), [AI catalog](skills/system-specs/references/ai.md)
- `benchmark-checklist` (adapted from pstack): vet a performance number before reporting it
- [`hardware-deal-check`](skills/hardware-deal-check/SKILL.md): find and assess Danish-deliverable development-hardware deals against Tobias's price ceilings
- [`disk-cleanup`](skills/disk-cleanup/SKILL.md): free workstation disk space from dead worktrees, agent scratch and unevicted caches; why `du` misleads on compressed btrfs
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
- `chief-of-staff` (Tobias-invoked only): Tobias's single point of contact; delegates to team threads, raises issues without blocking, diagnoses teams, keeps the vault. Its state lives beside it.
