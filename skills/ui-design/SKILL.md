---
name: ui-design
description: Design, implement, or review graphical interfaces including product UI, dashboards, admin tools, forms, tables, settings, websites, and app screens. Use whenever layout, controls, hierarchy, density, iconography, interface copy, interaction states, or visual polish matters.
---

# UI Design

Honor an explicit brief and the established product design system. Inspect existing components, tokens, and interaction patterns before inventing new ones. Otherwise:

1. **Neutral foundations.** Use white or near-white foundations for light designs and black or grayscale foundations for dark designs. Keep the palette simple, reserving chromatic color for meaning, focus, action, and status.
2. **Structure without cards.** Create hierarchy with spacing, alignment, typography, density, and subtle dividers. Use contained surfaces only where the boundary aids interaction or comprehension.
3. **Professional and sleek.** Use restrained typography, precise alignment, consistent density, and quiet interaction states. Keep visual effects purposeful.
4. **Only useful UI.** Every visible element must help the user orient, compare, diagnose, decide, or act. Reveal secondary detail deliberately.
5. **Less UI wins.** When valid options compete, preserve clarity with the smaller composition.

## Product UI Judgment

- **Choose controls by task.** Match the control type and footprint to the value, available choices, and use frequency. Size fields for expected input; keep numeric fields compact with visible units; use a select or combobox when values are constrained. Do not give unrelated controls identical widths merely to fill a row.
- **Use icons where they outperform words.** Use familiar icons for repeated, spatially constrained actions such as edit, remove, search, help, and sorting. Use text for unfamiliar or ambiguous actions. Pair icon and text for primary or consequential actions. Give every icon-only control an accessible name and tooltip. Keep text labels for unfamiliar domain navigation.
- **Make tables serve comparison.** Use a table when users compare the same attributes across rows. Let content determine column width; align text left and numbers right with tabular numerals; keep row actions in a narrow, consistent column; mute headers relative to data; show sorting only on sortable columns. Use inline editing only for fields users commonly edit.
- **Design forms as decisions, not grids.** Group related fields, place labels and errors close to their controls, and keep helper text only when it prevents error or explains a constraint. Use native semantics or accessible, battle-tested primitives and provide default, hover, focus, disabled, loading, and error states as relevant.
- **Cut interface copy.** Remove duplicated titles, values, instructions, and metadata. Prefer short labels and correct grammar over explanatory prose. Keep provenance or constraints when they change user behavior. Place save, loading, and error status beside the scope it describes.
- **Choose working density deliberately.** Favor compact, scan-friendly layouts for repeated expert workflows; use more space for occasional focused tasks. Put whitespace between groups, not indiscriminately inside every control and row. Keep one action visually dominant within each action scope and quiet destructive actions until relevant.

## Verification

Run and inspect the affected interface at its target viewport. Exercise the affected workflow and relevant states. Check that the control choices, icon meanings, field widths, table alignment, copy, and density still make sense in the rendered result, then report residual visual or behavioral uncertainty.
