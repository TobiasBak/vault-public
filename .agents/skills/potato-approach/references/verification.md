# Verification CLIs and feature maps

Successive agents need to operate the same app and collect comparable evidence. The **control CLI** executes stable operations, the **feature map** connects user reports to those operations, and the project skill explains the choices. Build only what's missing; existing task runners, browser tools, and fixtures may already cover most of it.

## Control CLI

It must cover these operations, though they needn't be separate commands:

| Operation | Result |
|---|---|
| Start | Launch the intended build and identify the instance this run owns |
| Ready | Confirm this instance can run the workflow |
| Reset | Establish named data, role, and config with no dependence on earlier runs |
| Exercise | Perform real user actions |
| Inspect | Capture visible results plus persisted state, requests, traces, measurements |
| Stop | Clean up processes and scratch while keeping evidence |

- Isolate mutable state when runs can overlap, or state explicitly that only one session is supported.
- Use the real path. Fixtures set the starting state, but user actions must produce the result; never insert the expected order into the DB.
- Return a short result with run ID, operation, outcome, and artifact path, machine-readable when consumed. Logs go in artifacts.
- A failed prerequisite or incomplete check never looks like success. Report what failed and keep partial evidence.
- Store revision, scenario, fixture, and config with the evidence. Derive expectations from the product contract. Record what a test double proves and what still needs a live check.
- Keep commands in their executable owners; the skill links to them. When a command breaks, distinguish tool drift from product regression.

Start with a workflow that currently needs human help. Run it from setup through cleanup, twice from a clean state, to expose hidden dependencies.

## Feature map

It records what the product does, how users reach each feature, and what result shows it worked. It isn't a file inventory or a test. Keep it with the project's verification skill; split large maps into an index plus feature files (`.agents/skills/verify-<app>/features/`).

Each entry covers:
- the name and the words users use for it
- purpose and entry points
- required starting state
- how to exercise it with real commands and stable control names
- expected results and where to observe them, including non-UI effects
- evidence locations and known limits

Build entries by running the app from a known state and following the user path. Mark anything not exercised as unverified, and never redefine success to match a bug. Update affected entries in the same change that alters navigation or behavior. In a maintenance pass, report which features were checked and which were blocked. Separate a stale map, a broken tool, and a product regression.

```markdown
# Checkout
Customer submits the cart and gets an order confirmation. Report terms: place order, payment.
Start: local test store, signed-in customer, cart fixture; payment is a test double. Launch/reset: ../SKILL.md
Reach: Cart → Checkout → Place order. Empty cart disables Checkout; don't bypass via API.
Run: shop-control scenario checkout --fixture cart-one-item --record
Expect: confirmation with order ID; persisted order has fixture item and total; cart empty.
Evidence: printed artifact dir (trace, screenshot, order record). Test double ≠ live payments.
```

## Fresh-agent handoff check

Use it when judging readiness for independent work, not after every edit. Give a fresh agent a representative report, the repo, and normal tools, with no prior investigation. A rerun by the original agent checks the commands, not the handoff. Then fix whatever it got stuck on:

- couldn't find the feature: feature map or naming
- couldn't start, reset, or inspect: tools
- needed a repeated method: skill
- repeated an architectural mistake: API or boundary
- claimed unsupported success: checks and evidence

Confirm the repair with another representative run.
