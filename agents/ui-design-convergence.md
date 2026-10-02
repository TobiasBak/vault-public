# AI-generated UI convergence

With vague frontend direction, coding agents of every model family converge on the same look: rounded card grids, pills, purple or blue gradients, generic type, decorative metrics, marketing copy, and SaaS-dashboard layout regardless of the product. It looks finished but is interchangeable. Tobias has seen this in his own dashboard work.

When there's no brief or existing design system (both take precedence):

- Pick a clear visual thesis instead of generic "professional".
- Build hierarchy with spacing, alignment, type, and density before adding containers.
- Reserve color and ornament for meaning, focus, and status.
- Cut copy, metrics, badges, and surfaces that don't help the user compare, diagnose, decide, or act.
- When options tie, use less UI.

Compare structurally different alternatives inside the real product with real data. Isolated mock routes hide composition problems. Rendered output is the authority: run the app and inspect target viewports and interaction states, because source review can't reveal weak hierarchy, overflow, contrast, or bloat.

- The model-invoked skill is [`skills/ui-design/SKILL.md`](../skills/ui-design/SKILL.md). Its first draft ballooned into a full UI process and was cut back to the actual delta: precedence, restraint, utility, and rendered inspection.
- `swe-benchmarking/setup/DESIGN.md` (black-first, no cards) applies only to that product.
