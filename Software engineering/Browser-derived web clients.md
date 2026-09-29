# Browser-derived web clients

A browser trace can reveal the HTTP contract behind a web interaction. A narrow client then replaces repeated UI driving with a few deliberate requests and a stable local interface. This is often faster and easier for an agent to use, but it is only appropriate when the site permits the access and the interaction does not depend on browser-only security or UI state.

## From interaction to client

1. **Record one bounded flow.** Use a clean browser context, start capture before navigation, perform one action, and stop after its result appears. Record separate traces for variants such as anonymous versus logged-in, two locations, or two searches. Playwright can observe request and response events and record a context to HAR; closing the context writes the HAR ([network monitoring](https://playwright.dev/docs/network), [`recordHar`](https://playwright.dev/docs/api/class-browser#browser-new-context-option-record-har)).
2. **Find the data-bearing requests.** Filter out images, fonts, analytics, and ads. For each XHR or fetch request, inspect method, URL and query parameters, request body, response body, initiator, and the user action that caused it. The [HAR 1.2 format](https://w3c.github.io/web-performance/specs/HAR/Overview.html) is JSON containing observed request, response, header, cookie, content, and timing data.
3. **Discover dependencies by comparison.** Repeat the flow and diff traces. Stable values are likely configuration; changing cookies, CSRF tokens, nonces, timestamps, signatures, or IDs need an explicit acquisition step. Remove copied headers one at a time in a controlled replay to find the minimal request. Do not assume browser headers are all required.
4. **Reproduce, then implement.** A one-off replay, "Copy as cURL," or Playwright's [`routeFromHAR`](https://playwright.dev/docs/mock) proves that a sample can be matched. The actual client should deliberately construct the small set of HTTP requests, obtain current IDs and tokens through supported bootstrap steps, decode responses, and expose domain data. It should not send an old HAR entry verbatim.

A HAR is **observational evidence, not an API schema or permission grant**. It records one browser, account, time, location, experiment cohort, and site revision. It does not identify which fields are optional, which values expire, or which behavior the provider promises to preserve.

## Capture format and scope

HAR is a convenient portable capture format, not a required ingredient. Browser DevTools, Chrome DevTools Protocol events, Chromium network logs, an HTTP debugging proxy, or inspection of page HTML and JavaScript can reveal the same requests. Use HAR when a replayable artifact, response bodies, timing, or comparison between runs is useful; direct network and source inspection can be faster when an anonymous read-only flow exposes a few obvious JSON endpoints. The resulting client should discover current values and construct requests itself rather than depend on a recorded HAR at runtime.

The useful unit is a **bounded interaction**, not an entire website. A single trace might explain loading a catalog, searching, selecting a store, or adding an item, but it rarely defines a client for a whole web application. Record and compare separate flows when authentication, location, pagination, experiments, or mutations change the protocol. Claims that a HAR can derive a client for "any website" omit this scope and the cases where browser-only state or access controls keep automation necessary.

## Session and browser boundary

Classify every apparent prerequisite:

- Public configuration and publication IDs can often be rediscovered from the current page.
- Session cookies and CSRF tokens usually require a bootstrap request and a cookie jar.
- Login cookies, bearer tokens, and refresh tokens require an authorized account flow and secure credential storage. Never promote a captured session token into source code or a fixture.
- Request signatures, device attestation, CAPTCHA, WebAuthn, complex anti-bot challenges, or interaction-dependent state are signs to keep the browser in the loop rather than bypass controls.

Browser automation also remains the simpler choice for low-frequency use, workflows whose rendered DOM is the only useful representation, frequently changing internal endpoints, uploads and downloads coupled to UI state, or actions requiring human review. A hybrid can use a browser only for supported login/bootstrap and ordinary HTTP for stable read-only requests, but only if the site's contract allows it.

## Validation and maintenance

Decode external data at the boundary and distinguish "no offers" from transport, authentication, parse, and upstream-contract failures. Validate dates, currency, pagination, and required identifiers. Preserve sanitized response fixtures and check a few visible UI examples against client output. A lightweight scheduled canary can detect endpoint or shape drift; re-record the same bounded browser flow when it fails.

Discover volatile IDs instead of hard-coding them, bound concurrency, cache within the data's useful lifetime, honor `Retry-After`, and back off on throttling. Treat counts as hints until pagination agrees. Keep endpoint-specific parsing behind a small adapter so replacing one retailer does not alter the agent-facing contract.

## Security, privacy, and site contract

HARs can contain query secrets, POST bodies, account data, cookies, and authorization headers. Chrome now sanitizes `Cookie`, `Set-Cookie`, and `Authorization` by default but can export them when sensitive-data export is enabled ([Chrome DevTools](https://developer.chrome.com/docs/devtools/network/reference/#save-as-har)). Capture with the least privileged account, avoid recording unrelated tabs, redact before sharing, store traces outside version control, and delete raw traces when no longer needed.

Before operational use, review the site's terms, the actual API provider's terms, copyright/database rights, privacy implications, and any documented API. Do not bypass authentication, access controls, CAPTCHA, or rate limits. `robots.txt` is a crawl signal to honor, not a complete legal answer and not authorization: the standard explicitly says its rules are not access authorization ([RFC 9309](https://www.rfc-editor.org/rfc/rfc9309.html)). A permissive file does not license reuse, and a disallow rule should not be evaded.

## Agent-facing CLI

Give the agent a compact deterministic interface rather than raw upstream JSON. Correct-use instructions must travel through the interface the agent actually receives, such as the tool schema, `--help`, structured output metadata, or diagnostics. A README-only constraint is ineffective when the harness does not place that README in context.

A useful shape is:

```text
offers stores --near <postcode-or-coordinates> --json
offers list --retailer superbrugsen [--store <id>] [--query <text>] [--valid-at <time>] --json
```

JSON should have a versioned envelope with `source`, `fetchedAt`, publication validity, selected store or locality, and `offers`. Normalize each offer to stable fields such as `id`, `title`, `description`, `price`, `currency`, `previousPrice`, quantity/unit, calculated unit price only when unambiguous, validity, image URL, and source URL. Sort deterministically, put diagnostics on stderr, use meaningful exit codes, and bound output with filters and pagination. A human table can be secondary.

"Good" is not an upstream fact. Return factual offers plus objective filters such as discount, unit price, category, validity, and distance. Let the agent rank them against explicit household preferences rather than silently embedding a subjective score.

## SuperBrugsen weekly offers feasibility

### Observed on 2026-07-19

The public [SuperBrugsen weekly paper](https://superbrugsen.coop.dk/avis/) is an Incito publication rendered with Tjek's browser SDK, not an HTML list or a PDF. Building the prototype was therefore still derivation of a narrow web-application client, not merely downloading a flyer. It was unusually simple because the relevant flow was anonymous, read-only, and exposed structured data. Chromium network logging, page HTML and SDK inspection, and controlled request reproduction supplied the evidence; retaining a HAR was optional and the operational client does not consume one.

The page HTML exposed a current `data-publication-id` and a browser API key, then loaded the public [Tjek SDK bundle](https://d21oefkcnoen8i.cloudfront.net/sgn-sdk-4.x.x.min.js). The key is deliberately shipped to browsers, but that does not make it a reusable credential or grant third-party API rights.

For the observed publication `d7X_kiW8`, the browser flow used:

- `GET https://squid-api.tjek.com/v2/catalogs/{publicationId}` for metadata;
- `POST /v4/rpc/generate_incito_from_publication` and per-section Incito requests for rendering;
- `GET /v2/offers` with `catalog_id`, `types=incito`, `order_by=page`, `offset`, and `limit` for normalized offer rows.

The catalog response described "Uge 29-30," validity from 2026-07-16 to 2026-07-30, `offer_count: 153`, `all_stores: true`, no `store_id`, and type `incito`. Offer rows contained `id`, `heading`, `description`, page/view IDs, `pricing` with price, previous price and DKK currency, structured quantity, image links, per-offer validity, dealer, catalog, and optional store fields. Two requests at the documented maximum observed page size of 100 returned 149 distinct rows rather than the catalog's count of 153. This mismatch is a concrete reason to validate pagination and not promise completeness from metadata alone.

The ordinary weekly publication was chain-wide: all observed offer rows had no store ID. Separately, the page asks browser geolocation, caches coordinates for one hour, and calls Coop `/umbraco/api/Offers/...ClosestStoreWithinRadius` endpoints to append small local "quick info" offers. One anonymous request using Copenhagen coordinates returned no local rows, so that endpoint's availability, radius, store identity, and data completeness remain unverified. SuperBrugsen's [robots file](https://superbrugsen.coop.dk/robots.txt) allows the public paper path but disallows `/umbraco/`; an automated client should therefore not use those local endpoints without explicit permission.

Member-personalized offers are a different authenticated product. Coop says they are selected from member purchasing and must be activated ([personal offers](https://medlem.coop.dk/medlemsfordele/personlige-tilbud/)); Coop also describes behavioral and offer data processing across its digital platforms ([privacy policy](https://coop.dk/privatlivspolitik/behandlinger/cookies-mv/)). Keep them out of a public-offers client unless a documented member integration and explicit user authorization exist.

### Assessment

**Technically feasible, contractually unresolved.** A small read-only client could discover the current publication ID from the public page and normalize the Tjek offer list without running a browser on every fetch. It would likely cover SuperBrugsen's chain-wide weekly offers, not prove stock at a particular local store and not cover personal offers.

Do not implement the Tjek route merely because it works from a browser trace. Tjek's current [API and integration terms](https://tjek.com/terms) frame API access as an agreed service, restrict use to the customer's own platforms, and prohibit third parties from systematically fetching or reusing API content without written agreement. Those business terms are not a legal determination of an unaffiliated visitor's position, but they are strong evidence that the browser-exposed key is not intended as a general public API. Obtain approval from Coop/Tjek or use a documented public feed before making this a maintained CLI. If approval is unavailable, browser-based personal viewing at low frequency is less technically elegant but should still be checked against applicable terms.

A useful first implementation decision would require: the supermarkets and specific stores or postcode, whether chain-wide flyer offers are sufficient, whether member-only offers are excluded, desired refresh frequency, and whether Coop/Tjek grants an acceptable access route. Each additional supermarket will need its own discovery and contract assessment behind the same normalized CLI schema.

## Føtex, Netto, and Lidl offers feasibility

### Observed on 2026-07-19

These retailers do not share one publication provider. Føtex uses iPaper for its flyer and also exposes Salling Group's structured offers service, Netto uses Tjek/ShopGun, and Lidl uses Schwarz's leaflet platform. All three anonymous flows could be reproduced with ordinary HTTP after inspecting HTML, browser network activity, and first-party JavaScript. A HAR or operational browser is not required for the observed national publications.

#### Føtex

**Evidence.** The public [Føtex flyer page](https://www.foetex.dk/foetex-avis/) linked to an [iPaper publication](https://avis.foetex.dk/naeste-uges-avis/uge-27282930/). Plain publication HTML exposed `window.staticSettings` with paper ID `3041345`, 88 page numbers and dimensions, publication URLs, and OCR-like `pageTexts`. Those texts contained offer names, prices, validity statements, member restrictions, and format exclusions. Signed image URLs were generated for the current viewer session and should not be persisted. A separate iPaper enrichment response had 165 page-coordinate entries with product or search links and alt text, but no structured price fields.

The tested first-party Føtex JavaScript also configured Salling Group's `GET /v1/leaflet-offers` service. With `brands=foetex&page=N`, it returned product groups containing structured offers with title, price, original price, calculated discount, unit text, dates, brand, image, category codes, and `membershipOffer` and `personalizedOffer` flags. Pagination used 100 product groups per page, continued through page 21, and returned no rows on page 22. Its scope did not equal the iPaper publication: only 33 observed offers had the current weekly date range, while many results were longer-running or personalized promotions. Member or personalized rows can be identified and must be excluded, but exact flyer parity remains unresolved.

The observed iPaper text states that the monthly paper is broadly national but that not every item is stocked in Føtex Food and that it does not apply to Føtex Go or Føtex City. No store selection was required for either tested publication flow.

**Inference and unresolved contract.** The structured Salling feed is the better normalization source if its intended product scope is acceptable. The [Salling Group developer portal](https://developer.sallinggroup.com/) describes public APIs with free sign-up, so an operational client should use an independently issued, approved token rather than extract or persist the bearer token shipped to first-party JavaScript. It remains unverified that `leaflet-offers` is part of that documented public product. The [iPaper robots file](https://avis.foetex.dk/robots.txt) disallows all crawling, and the [Salling API robots file](https://api.sallinggroup.com/robots.txt) disallows the offer route. Do not automate either route without clarifying permission. If permission exists only for viewing the paper, extracting normalized offers from `pageTexts` is technically possible but will require error-prone text segmentation and validation against page images.

#### Netto

**Evidence.** The [Netto paper page](https://netto.dk/netto-avisen/) server-rendered a Next.js `leaflets` object containing the current Tjek catalog ID, dates, page image URLs, `page_count: 29`, `offer_count: 156`, and `all_stores: true`. A current first-party JavaScript chunk exposed the corresponding browser API configuration. The same Tjek requests used for SuperBrugsen then worked without browser state: catalog metadata followed by paginated `GET /v2/offers?catalog_id=...&order_by=page&offset=...&limit=100`.

The observed catalog returned 100 rows and then 54 rows, for 154 distinct offers rather than its declared 156. Rows had normalized title, description, DKK price, quantity, image, validity, and page fields. Only 4 of 154 had a previous price, and none had category IDs. The catalog and rows had no store ID, so the observed paper was chain-wide and did not require location. This does not prove local stock.

**Inference and unresolved contract.** Netto is the smallest technical extension because it can share the SuperBrugsen Tjek adapter while using a different bootstrap parser. Its [robots file](https://netto.dk/robots.txt) allows the site, but that is not an API license. Tjek says its [APIs are available only to customers](https://tjek.com/apis-and-sdks) and invites prospective users to contact it. The existing Tjek terms concern therefore applies even though Netto itself embeds the catalog and browser key. Obtain Tjek or Salling approval before maintained use.

#### Lidl

**Evidence.** The [Lidl paper page](https://www.lidl.dk/c/tilbudsavis/s10013730) returned a server-rendered overview with current leaflet UUIDs and detail URLs. The observed entries separated a weekly paper, a non-food paper, and a longer-running "fast low price" paper. First-party viewer JavaScript declared Schwarz's `https://endpoints.leaflets.schwarz/v4` base and fetched `GET /flyer?flyer_identifier={uuid}` without a token, cookie, CAPTCHA, or signature.

The [observed weekly flyer response](https://endpoints.leaflets.schwarz/v4/flyer?flyer_identifier=019f4c5f-3449-7e73-b27f-a75b3459ab97) contained global offer dates, 42 pages, page images and links, and 197 products. Every product had a structured title and price; descriptions, brands, product URLs, and images were usually present. `categoryPrimary` classified 121 products as `Food` and 76 as `Non food`, so the nominal weekly paper still requires category filtering for food-only requests. No product exposed a previous price, so percentage-discount sorting cannot be computed from this source. Products inherit the flyer's offer dates and can be associated with pages through link IDs.

The response listed only region code `0`; related flyers had no store IDs or region codes. The [Lidl robots file](https://www.lidl.dk/robots.txt) does not disallow the flyer path, and the [Schwarz overview robots file](https://esi.leaflets.schwarz/robots.txt) has an empty `Disallow`. The JSON endpoint has no robots file.

**Inference and unresolved contract.** The region data supports, but does not prove, a nationwide publication and says nothing about local stock. No first-party documented API program or general content-reuse grant was found in this review, so legal permission remains unresolved even though the technical flow is anonymous.

### Cross-retailer design consequence

Use separate discovery adapters behind one normalized schema:

- Føtex: canonical page to current iPaper URL, then either approved Salling offer pagination or iPaper settings and text extraction;
- Netto: canonical Next.js payload to Tjek catalog ID, current first-party configuration to browser key, then Tjek catalog and offer pagination;
- Lidl: canonical overview to leaflet UUID, then one Schwarz `v4/flyer` response.

Netto has the cleanest existing-adapter fit. Lidl has the strongest unauthenticated structured response and an authoritative food/non-food field, but no previous prices. Føtex has rich structured prices through Salling but unresolved scope and credential permission; its exact iPaper fallback is substantially less reliable. Combined output should therefore report source-level completeness, location scope, food-classification basis, and previous-price availability rather than imply that all retailers provide equivalent discounts. Keep member and personalized offers out, cache at flyer timescales, use low request volumes, and stop rather than add browser automation if an endpoint introduces authentication or access controls.
