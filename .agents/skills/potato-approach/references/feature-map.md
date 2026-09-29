# Feature maps

A feature map teaches an agent what a product does, how users reach each feature, and what observable result shows it worked. It connects a vague bug report or screenshot to a workflow the agent can run.

It is not a source-file inventory or a substitute for tests. A control CLI gives the agent operations; the map tells it which operations matter for the reported behavior. Keep setup and command definitions in the verification skill and tools, then link to them from the map. Use [Verification CLIs](verification-cli.md) when those operations are missing or unreliable.

This is a guide and worked example, not a feature map of the vault. Keep each application's actual map beside its project-local verification skill. A small map can be one file. Split larger maps into a short index and feature files, for example:

```text
.agents/skills/verify-shop/
  SKILL.md
  features/
    README.md
    checkout.md
```

## What an entry needs

- A recognizable feature name, relevant user vocabulary, and its purpose.
- Ways users reach it, including distinct entry points when they affect behavior.
- Required starting state, such as user role, fixture data, configuration, or feature flags.
- How to exercise it through the existing CLI or other control tool. Use actual commands and stable control names, not guessed selectors.
- Expected results and where to observe them, including important effects beyond the screen.
- Checks, evidence locations, and known limitations that change how an agent should investigate it.

Link to the owning code or tests when that helps investigation. Keep those links selective. Record only details the next agent needs to find, run, and judge the feature.

## Build one

Inspect the product's routes, menus, commands, tests, and existing verification tools. Start with workflows relevant to current work or recurring reports. Search for an existing map before creating another.

Run the application from a known starting state. Follow the user path and observe the result. Source code helps locate a feature; running it establishes whether the documented route works. Mark anything not exercised as unverified rather than inventing instructions.

Write entries from the observed behavior and the intended contract. Do not redefine success to match a bug. Use requirements, accepted examples, or existing behavioral contracts to decide what should happen.

Move repeated setup, reset, interaction, and evidence collection into maintained commands when existing tools do not cover them. Keep user navigation and feature meaning in the map. Do not copy changing command definitions into every entry.

Rerun a mapped workflow using only the written instructions and linked tools. Keep the result inspectable after cleanup. Record the revision, scenario, and relevant configuration with the run evidence so another agent can reproduce it.

## Worked example

This fictional entry illustrates the shape. Its commands and paths are examples, not tools installed in this vault. A real map must use commands checked against the target project.

```markdown
# Checkout

A customer submits the current cart and receives an order confirmation.
Related report terms: place order, payment, cart submission.

## Starting state

Use the local test store with the signed-in customer and cart fixture.
The payment provider is the project's test double.
Launch and reset commands live in ../SKILL.md.

## Reach and exercise

Open Cart, choose Checkout, then Place order.
An empty cart keeps Checkout disabled; do not bypass that state through an API.

Run: shop-control scenario checkout --fixture cart-one-item --record
The scenario follows the same user path.

## Expected result

Show an order confirmation containing the created order ID.
The order contains the fixture's item and total, and the cart is empty.
Check the persisted order as well as the visible confirmation.

## Evidence and limits

The scenario prints its artifact directory with the interaction trace,
confirmation screenshot, and resulting order record.
The test double verifies the application flow, not live payment processing.
```

## Keep it useful

Update affected entries when a change alters navigation, prerequisites, commands, or expected behavior. Rerun the changed path and correct the map in the same work. Add new features and remove retired ones from both entries and index.

For a full maintenance pass, compare every mapped feature with current source and exercise each in the running application. Report which features were checked and which were blocked. Do not imply full coverage from one successful path.

Separate a stale map, a broken control tool, and a product regression. Correct stale instructions, repair and rerun the tool, or report the regression. Do not make a broken feature look correct by changing its expected result.

Give the verification skill and map a clear owner. Automation can suggest updates after product changes, but confirm changed instructions against the running product. Keep run logs with the evidence, not in the map, and leave unrelated documentation alone.

## Sources

Lauren Tan explains the CLI and feature-map combination between 09:00 and 12:30 in [her talk](https://x.com/poteto/status/2102050467505430555/video/1). Her public pstack skills show [creation](https://github.com/cursor/plugins/blob/main/pstack/skills/create-verification-skill/SKILL.md) and [maintenance](https://github.com/cursor/plugins/blob/main/pstack/skills/maintain-verification-skill/SKILL.md). The layout and example above adapt that approach for this skill.
