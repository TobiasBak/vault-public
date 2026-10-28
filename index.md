# Index

Not exhaustive. Search with `rg`.

Where a note goes: `agents/` how an agent should behave and what its harness does · `software/` facts about systems, tools and APIs · `hardware/` machines, compute and buying them · `tobias/` preferences, working style and open threads · `skills/` global skills, `.agents/skills/` vault-only ones · root holds only the routers and the landing page.

- [AGENTS.md](AGENTS.md): how to use and maintain this vault
- [projects.md](projects.md): public repository routes (Dotfiles, T3 Code)
- [topics-to-explore.md](topics-to-explore.md): open topics for future exploration

## Tobias

- [tobias/preferences.md](tobias/preferences.md): engineering taste, stack, testing, how to involve him
- [tobias/partnership.md](tobias/partnership.md): agent character, voice, disagreement, and pressure tests
- [tobias/shopping.md](tobias/shopping.md): shopping priorities and Danish availability
- [tobias/how-to-win.md](tobias/how-to-win.md): Musk's "how to win" principles, Tobias's reflection and open threads; personal, grows over time

## Hardware

- [hardware/agent-era-dev-machine.md](hardware/agent-era-dev-machine.md): cloud-agent build capacity, fleet execution boundaries and genuine hardware deals
- [hardware/colab-in-google-ai-plans.md](hardware/colab-in-google-ai-plans.md): Colab compute units and accelerators bundled with Google AI plans, runtime rules, the Colab CLI

## Agents

- [agents/agentic-engineering-loop.md](agents/agentic-engineering-loop.md): choosing worthwhile work, establishing verification, equipping agents and removing demonstrated blockers
- [agents/agent-native-codebases.md](agents/agent-native-codebases.md): patch accretion, making the easy change correct, decode once then trust types, the knowledge-placement order, enforce-first hardening
- [agents/documentation-and-naming.md](agents/documentation-and-naming.md): what prose keeps, the no-comments rule, code as a search surface
- [agents/instructions-and-prompts.md](agents/instructions-and-prompts.md): what belongs in AGENTS.md, placement, task contracts, execution habits
- [agents/context-engineering.md](agents/context-engineering.md): working set vs record, state tiers, compaction and checkpoints, tool output, skills, text-as-image
- [agents/subagent-delegation.md](agents/subagent-delegation.md): who may delegate (top-level agents splitting a large task into whole packages; no explorers; review subagents fine), whole-outcome splits, when a specialist earns its own context and how to fold it in, model routing and effort, bounded tasks and fresh contexts, checkpoint budgets, handoffs, one writer
- [agents/compute-routing.md](agents/compute-routing.md): model roles, targets and effort for delegated work, T3 inheritance, routing hook
- [agents/code-review.md](agents/code-review.md): reviewer inputs, retrieval, lenses, findings
- [agents/orchestration.md](agents/orchestration.md): loops vs graphs, why a fixed graph is a bet against the model, tool surface and deferred loading, programmatic tool calling (OpenAI and Anthropic), OpenAI dots
- [agents/testing-with-agents.md](agents/testing-with-agents.md): agentic E2E, verification CLIs and feature maps, real-session handoff check, refactor equivalence, test pruning, team adoption
- [agents/verification-latency.md](agents/verification-latency.md): sub-minute verification goal, shared compute and compiler/runtime research; live Rust UI is parked
- [agents/learning-from-feedback.md](agents/learning-from-feedback.md): preserving evidence strength and scope, memory types, feedback weighting, evidence gates, outcome-based learning, forbidden inferences
- [agents/autoresearch.md](agents/autoresearch.md): experiment-loop requirements, the fast-loop rule (cheap scouts first, rigor only at confirm) and Tobias's scout/screen/confirm system
- [agents/benchmark-trust.md](agents/benchmark-trust.md): benchmark failure types, SWE-Bench Pro vs DeepSWE, evidence ranking
- [agents/coding-models.md](agents/coding-models.md): effort guidance, Sol vs Astra cost, Terra vs Sol trial, API specifics, Haiku/Luna limits, free-model trials
- [agents/harness-operations.md](agents/harness-operations.md): routes to the harness notes plus global CLI install traps (pnpm release-age gating)
- [agents/codex-operations.md](agents/codex-operations.md): app-server daemon pin, quota fields, context management, subagent inheritance
- [agents/claude-code-operations.md](agents/claude-code-operations.md): attribution, effort defaults, compaction windows, discovery, auto memory
- [agents/pi-operations.md](agents/pi-operations.md): verbosity, session usage, print-mode stdin, ChatGPT quota and credits, OpenRouter model overrides
- [agents/opencode-operations.md](agents/opencode-operations.md): v2 install and update failure, migration, Go/Zen data policies
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
- [software/sql-type-inference.md](software/sql-type-inference.md): typed SQL-file imports, colinhacks demo, what it does and does not establish
- [software/effect.md](software/effect.md): Effect, and when it's worth it
- [software/gigatoken.md](software/gigatoken.md): fast Rust tokenizer runtime
- [software/ocr.md](software/ocr.md): Indra OCR candidate, local CPU operation, commercial-license restrictions and vendor benchmark conditions
- [software/browser-derived-clients.md](software/browser-derived-clients.md): turning browser traces into HTTP clients; Danish supermarket offers
- [software/openrouter.md](software/openrouter.md): listed vs effective prices, input-only price sort, speed floors, default routing, sticky sessions, ZDR, quantization labels, direct vs OpenRouter prices
- [software/uncensored-model-hosting.md](software/uncensored-model-hosting.md): why uncensored frontier MoEs live only on specialist hosts, NanoGPT/Venice/Abliteration prices, self-host VRAM and GPU rent
- [software/cloudflare.md](software/cloudflare.md): API tokens as JSON policy documents or Terraform/OpenTofu, bootstrap and state caveats, Access with Worker destinations
- [software/supabase.md](software/supabase.md): CLI config-push cwd quirk, privileged Storage completion, free-plan pausing and restore
- [software/windows-gui-automation.md](software/windows-gui-automation.md): UIA-first tools, state capture, keeping the desktop alive after RDP
- [software/t3-code-operations.md](software/t3-code-operations.md): thread/workspace mechanics, secret ownership, webhook setup, Connect and safe restarts
- [software/omarchy-agent-operations.md](software/omarchy-agent-operations.md): package installation, privilege and unprivileged `/proc` safety checks
- [software/omarchy-windows-vm.md](software/omarchy-windows-vm.md): agent use of Tobias's local Windows VM: the `win-vm` CLI, lifecycle ownership, disposable runs, file transfers and setup ownership

## Global skills (`skills/`)

All model-invoked; agents select relevant skills automatically:
- [`potato-approach`](skills/potato-approach/SKILL.md): make agent-maintained codebases easy to change correctly, including design red flags and mining mistake history
- [`theodore-kaczynski-nullifier`](skills/theodore-kaczynski-nullifier/SKILL.md): make repositories understandable, changeable, verifiable and recoverable by agents
- [`system-specs`](skills/system-specs/SKILL.md): requirement specs for systems agents change frequently, including version boundaries
- [`benchmark-checklist`](skills/benchmark-checklist/SKILL.md) (adapted from pstack): vet a performance number before reporting it
- [`hardware-deal-check`](skills/hardware-deal-check/SKILL.md): find and assess Danish-deliverable development-hardware deals against Tobias's price ceilings
- [`disk-cleanup`](skills/disk-cleanup/SKILL.md): reclaim unused compiler output and caches without disrupting concurrent agents; gah ownership and compressed-btrfs measurements
- [`unslop`](skills/unslop/SKILL.md): concise, natural prose
- [`grilling`](skills/grilling/SKILL.md) (Matt Pocock): stress-test a plan by interview
- [`frontend-design`](skills/frontend-design/SKILL.md) (Anthropic): distinctive, intentional visual design
- [`maintainability-audit`](skills/maintainability-audit/SKILL.md): how easily fresh agents can change the source
- [`repo-context-audit`](skills/repo-context-audit/SKILL.md): which instructions and docs earn their place
- [`retro`](skills/retro/SKILL.md): repo improvements from session friction
- [`review-test-quality`](skills/review-test-quality/SKILL.md): keep, rewrite, or delete tests
- [`create-verification-skill`](skills/create-verification-skill/SKILL.md), [`maintain-verification-skill`](skills/maintain-verification-skill/SKILL.md) (adapted from pstack): project verification skills and feature maps

## Vault-only skills (`.agents/skills/`)

- [`audit-knowledge-consistency`](.agents/skills/audit-knowledge-consistency/SKILL.md): judge duplicate, scoped and contradictory knowledge, including instruction files, and verify links
- [`review-agent-history`](.agents/skills/review-agent-history/SKILL.md): mine Pi and Codex histories for reusable knowledge
- [`chief-of-staff`](.agents/skills/chief-of-staff/SKILL.md) (Tobias-invoked only): Tobias's single point of contact; delegates to team threads, raises issues without blocking, diagnoses teams, keeps the vault. Its state lives outside the vault, in `~/.local/state/chief-of-staff/`.
