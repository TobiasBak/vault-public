# AI-generated UI convergence

With vague frontend direction, coding agents of every model family converge on the same look: rounded card grids, pills, purple or blue gradients, generic type, decorative metrics, marketing copy, and SaaS-dashboard layout regardless of the product. It looks finished but is interchangeable. Tobias has seen this in his own dashboard work.

When there's no brief or existing design system (both take precedence):

- Pick a clear visual thesis instead of generic "professional".
- Build hierarchy with spacing, alignment, type, and density before adding containers.
- Reserve color and ornament for meaning, focus, and status.
- Cut copy, metrics, badges, and surfaces that don't help the user compare, diagnose, decide, or act.
- When options tie, use less UI.

Compare structurally different alternatives inside the real product with real data. Isolated mock routes hide composition problems. Rendered output is the authority: run the app and inspect target viewports and interaction states, because source review can't reveal weak hierarchy, overflow, contrast, or bloat.

- The model-invoked skill is [`frontend-design`](../skills/frontend-design/SKILL.md).
- On trial since 2026-11-05: [taste-skill](https://github.com/leonxlnx/taste-skill) (`design-taste-frontend`), pinned at `9b4bf93` in `~/.local/share/agent-skills/taste-skill` and linked into `~/.claude/skills` and `~/.agents/skills` by hand. It stays out of the vault because it bundles 39 MB of photos under Unsplash and CC BY-SA terms and commented JavaScript. It targets marketing sites with photography and shader scenes, which cuts against the restraint above. Judge it on rendered output against `frontend-design`, then vendor a trimmed copy or delete the clone and its links.
