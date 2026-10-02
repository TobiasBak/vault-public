# Browser-derived web clients

A browser trace reveals the HTTP requests behind an interaction. A narrow client built on them replaces repeated UI driving with a stable local interface, which is faster and simpler for agents. This works if the site permits access and the flow doesn't depend on browser-only security state.

## From interaction to client

1. **Record one bounded flow** in a clean context: start capture, do one action, stop. Record variants (logged in or out, two locations) separately. Playwright can [observe network](https://playwright.dev/docs/network) and [record HAR](https://playwright.dev/docs/api/class-browser#browser-new-context-option-record-har). DevTools, CDP, a proxy, or reading page HTML and JS work too, and are often quicker for simple anonymous JSON.
2. **Find data-bearing XHR and fetch calls**, ignoring assets and analytics. For each, note method, URL, body, response, and the user action that triggered it.
3. **Diff repeated traces.** Stable values are config. Changing cookies, CSRF tokens, nonces, signatures, and IDs need an acquisition step. Drop copied headers one at a time to find the minimal request.
4. **Reproduce live, then implement.** The client discovers current IDs and tokens through bootstrap requests and never replays old HAR entries. `routeFromHAR` mocks locally; it doesn't prove upstream compatibility.

A HAR is observational evidence from one account, time, location, cohort, and site revision. It isn't a schema or a permission.

## Where it stops

- **Rediscoverable:** public config and publication IDs, from the current page.
- **Needs a bootstrap and cookie jar:** session cookies and CSRF tokens.
- **Needs an authorized login flow and secure storage:** auth and refresh tokens. Never put captured tokens in source or fixtures.
- **Keep the browser:** signatures, attestation, CAPTCHA, WebAuthn, anti-bot challenges, and interaction-bound state. Never bypass access controls or rate limits.
- Plain browser automation is also simpler for rare use, DOM-only data, churning endpoints, or UI-coupled uploads. A hybrid that uses the browser for login and HTTP for reads is fine if the site allows it.

## Maintenance

- Decode at the boundary. Distinguish "no results" from transport, auth, parse, and contract failures.
- Discover volatile IDs instead of hard-coding them.
- Bound concurrency, cache for the data's lifetime, honor `Retry-After`, and treat declared counts as hints until pagination agrees.
- Keep sanitized fixtures and a light canary. When it breaks, re-record the same flow.
- Put each source behind a small adapter so the agent-facing contract stays fixed.

**Privacy and terms:** HARs contain secrets and account data (Chrome strips cookies and auth only by default). Capture with least privilege, keep traces out of Git, and delete them when done. Check the site's terms, the actual API provider's terms, and database rights. `robots.txt` is a crawl signal to honor, not authorization ([RFC 9309](https://www.rfc-editor.org/rfc/rfc9309.html)).

## Agent-facing CLI

Usage rules must travel through what the agent actually sees: `--help`, schema, output metadata, diagnostics. A README is useless if the harness never loads it.

```text
offers stores --near <postcode> --json
offers list --retailer <name> [--store <id>] [--query <text>] [--valid-at <time>] --json
```

- **Envelope:** versioned, with `source`, `fetchedAt`, validity, locality, and `offers`.
- **Offer fields:** stable fields (`id`, `title`, `price`, `currency`, `previousPrice`, unit, validity, URLs).
- **Behavior:** deterministic order, diagnostics on stderr, meaningful exit codes, filters and pagination.
- **Ranking:** return facts and objective filters and let the agent rank against stated preferences. No baked-in "good deal" score.

## Danish supermarket offers (observed 2026-07-19)

All four weekly papers are national or chain-wide, need no browser at runtime, and say nothing about local stock. **Permission is unresolved for every one.** Get approval before building a maintained client, and exclude member and personalized offers.

| Retailer | Source | Notes |
|---|---|---|
| Netto | Next.js `leaflets` payload with Tjek catalog ID, then Tjek `/v2/offers` paginated | Cleanest fit. Declared 156 offers, got 154. Few previous prices, no categories. |
| SuperBrugsen | Page `data-publication-id`, then Tjek `/v2/catalogs/{id}` and `/v2/offers` | Same Tjek adapter as Netto. Declared 153, got 149. Tjek [terms](https://tjek.com/terms) forbid third-party systematic fetching. Coop's local `/umbraco/` endpoints are disallowed by robots. |
| Lidl | Leaflet UUID from page, then Schwarz `endpoints.leaflets.schwarz/v4/flyer?flyer_identifier=` | Richest anonymous response, with a food/non-food field. No previous prices, so no discount sorting. No documented API program. |
| Føtex | Salling `/v1/leaflet-offers?brands=foetex`, or iPaper `staticSettings.pageTexts` | The Salling feed doesn't match the paper and includes personalized items (flagged). It needs an approved developer token, not the first-party one. The iPaper fallback is OCR-like and unreliable. Robots disallow both. |

Combined output must report per-source completeness, location scope, classification basis, and whether previous prices are available. Stop if an endpoint adds auth.
