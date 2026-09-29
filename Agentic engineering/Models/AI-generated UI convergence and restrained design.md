# AI-generated UI convergence and restrained design

AI coding agents often converge on a familiar visual center when frontend direction is underspecified: rounded card grids, pills, purple or blue gradients, generic typography, decorative metrics, marketing copy, and SaaS-dashboard structure regardless of the product. The result can look complete while remaining interchangeable and poorly fitted to the user's work.

This pattern is not unique to one model family. Vague prompts invite high-frequency training patterns, framework defaults make them cheap to assemble, and completeness pressure rewards visible components even when they do not help a decision or action. Tobias has observed the same convergence in local dashboard work. That correction is useful feedback, not a universal design system.

## Precedence and intervention

An explicit user brief and an established product design system take precedence. Preserve an existing coherent visual language unless the task asks to change it. When direction is absent, apply a restrained intervention:

- choose a clear visual thesis rather than a generic "professional" default;
- create hierarchy through spacing, alignment, typography, density, and subtle separation before adding containers;
- reserve color and ornament for meaning, focus, and status;
- remove copy, metrics, badges, and surfaces that do not help the user compare, diagnose, decide, or act;
- when choices are otherwise equal, preserve clarity with less UI.

The rules in `/home/tobias/code/swe-benchmarking/setup/DESIGN.md`, including black-first composition and no cards, are scoped to that benchmark's product direction. They are not universal defaults for unrelated interfaces.

Compare structurally different UI alternatives inside the real product context, using representative data, density, navigation, and surrounding layout. Isolated mock routes make weak alternatives appear acceptable because they hide integration and composition problems.

Rendered behavior is the authority. Run the real interface and inspect target viewports and relevant interaction states. Source review alone does not reveal weak hierarchy, overflow, density, contrast, focus behavior, or visual bloat. Revise the rendered result rather than trusting that plausible component code produces a coherent experience.

The model-invoked guidance lives at `/home/tobias/code/skills/skills/ui-design/SKILL.md`. Keep it focused on the behavior-changing intervention and rendered verification; rationale belongs here.

## Distillation lesson

The first skill draft expanded a correction about generic visual convergence into a full UI-development workflow: product analysis, composition exploration, implementation, and exhaustive state review. That was broader than the observed failure. Removing generic steps did not weaken the useful delta: precedence, restrained composition, utility, and rendered inspection.

This illustrates the rule in [[Agent learning from experience and user feedback]]: distill the smallest behavior change that prevents the evidenced failure, not an ideal process the model already knows. More instructions can compete with the correction and turn a local preference into a rigid universal workflow.
