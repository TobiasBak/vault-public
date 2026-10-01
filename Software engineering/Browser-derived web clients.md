# Browser-derived web clients

A browser trace can reveal the HTTP requests behind an interaction. A narrow client can replace repeated UI driving with those requests and a stable local interface. This often makes agent use faster and simpler, provided the site permits access and the flow does not require browser-only security or UI state.

## From interaction to client

1. **Record one bounded flow.** Use a clean browser context, start capture before navigation, perform one action, and stop after its result appears. Record separate traces for variants such as anonymous versus logged-in, two locations, or two searches. Playwright can observe request and response events and record a context to HAR; closing the context writes the HAR ([network monitoring](https://playwright.dev/docs/network), [`recordHar`](https://playwright.dev/docs/api/class-browser#browser-new-context-option-record-har)).
2. **Find the data-bearing requests.** Filter out images, fonts, analytics, and ads. For each XHR or fetch request, inspect method, URL and query parameters, request body, response body, initiator, and the user action that caused it. The [HAR 1.2 format](https://w3c.github.io/web-performance/specs/HAR/Overview.html) is JSON containing observed request, response, header, cookie, content, and timing data.
3. **Discover dependencies by comparison.** Repeat the flow and diff traces. Stable values are likely configuration; changing cookies, CSRF tokens, nonces, timestamps, signatures, or IDs need an explicit acquisition step. Remove copied headers one at a time in a controlled replay to find the minimal request. Do not assume browser headers are all required.
4. **Reproduce, then implement.** Sending a copied request to the live service tests whether it works outside the browser. Playwright's [`routeFromHAR`](https://playwright.dev/docs/mock) serves recorded responses locally; it does not establish upstream compatibility. Build the client to discover current IDs and tokens through supported bootstrap steps, construct requests, decode responses, and expose domain data. Do not send old HAR entries verbatim.

A HAR is **observational evidence, not an API schema or permission grant**. It records one browser, account, time, location, experiment cohort, and site revision. It does not identify which fields are optional, which values expire, or which behavior the provider promises to preserve.

## Capture format and scope

HAR is a portable capture format, not a required ingredient. DevTools, Chrome DevTools Protocol events, Chromium network logs, an HTTP proxy, or page HTML and JavaScript can reveal the same requests. Use HAR for recorded response bodies, timing, replay, or trace comparison. Direct network and source inspection can be quicker for a simple anonymous JSON flow. The client need not consume a HAR at runtime.

Capture a **bounded interaction**, not an entire website. One trace might explain catalog loading, search, store selection, or adding an item. Compare separate flows when authentication, location, pagination, experiments, or mutations change the protocol. A HAR cannot derive a client for "any website" when browser-only state or access controls remain necessary.

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

The public [SuperBrugsen weekly paper](https://superbrugsen.coop.dk/avis/) is an Incito publication rendered with Tjek's browser SDK, not an HTML list or PDF. Its anonymous, read-only flow exposed structured data. Chromium network logs, page HTML, SDK inspection, and live request reproduction were enough to derive the prototype; it did not need a HAR at runtime.

The page HTML exposed a current `data-publication-id` and a browser API key, then loaded the public [Tjek SDK bundle](https://d21oefkcnoen8i.cloudfront.net/sgn-sdk-4.x.x.min.js). The key is deliberately shipped to browsers, but that does not make it a reusable credential or grant third-party API rights.

For the observed publication `d7X_kiW8`, the browser flow used:

- `GET https://squid-api.tjek.com/v2/catalogs/{publicationId}` for metadata;
- `POST /v4/rpc/generate_incito_from_publication` and per-section Incito requests for rendering;
- `GET /v2/offers` with `catalog_id`, `types=incito`, `order_by=page`, `offset`, and `limit` for normalized offer rows.

The catalog described "Uge 29-30," valid from 2026-07-16 to 2026-07-30, with `offer_count: 153`, `all_stores: true`, no `store_id`, and type `incito`. Rows contained `id`, `heading`, `description`, page/view IDs, `pricing` with DKK and previous prices, structured quantity, images, validity, dealer, catalog, and optional store fields. Two requests with `limit=100` returned 149 distinct offers, not the declared 153. Validate pagination rather than treating metadata counts as proof of completeness.

The weekly publication was chain-wide; none of the observed rows had a store ID. The page separately requests geolocation, caches coordinates for one hour, and calls Coop `/umbraco/api/Offers/...ClosestStoreWithinRadius` endpoints for local "quick info" offers. One anonymous Copenhagen request returned no rows, leaving radius, store identity, availability, and completeness unverified. SuperBrugsen's [robots file](https://superbrugsen.coop.dk/robots.txt) allows the paper path but disallows `/umbraco/`. Do not automate those local endpoints without explicit permission.

Member-personalized offers are a different authenticated product. Coop says they are selected from member purchasing and must be activated ([personal offers](https://medlem.coop.dk/medlemsfordele/personlige-tilbud/)); Coop also describes behavioral and offer data processing across its digital platforms ([privacy policy](https://coop.dk/privatlivspolitik/behandlinger/cookies-mv/)). Keep them out of a public-offers client unless a documented member integration and explicit user authorization exist.

### Assessment

**Technically feasible, permission unresolved.** A read-only client could discover the current publication ID and normalize Tjek's chain-wide weekly offers without a browser on every fetch. It would not establish local stock or cover personal offers.

Tjek's [API and integration terms](https://tjek.com/terms) describe an agreed service, restrict use to the customer's platforms, and prohibit systematic third-party fetching or reuse without written agreement. They do not settle an unaffiliated visitor's legal position, but they make the browser-exposed key a poor basis for a maintained client. Obtain Coop/Tjek approval or a documented public feed before building the CLI. Low-frequency personal browser viewing still needs to respect applicable terms.

Before implementation, choose supermarkets and stores or postcode, decide whether chain-wide offers suffice and member offers are excluded, set a refresh frequency, and establish a permitted access route. Each retailer needs its own discovery and permission assessment behind the shared CLI schema.

## Føtex, Netto, and Lidl offers feasibility

### Observed on 2026-07-19

Føtex uses iPaper and Salling Group's structured offers service, Netto uses Tjek/ShopGun, and Lidl uses Schwarz's leaflet platform. All three observed national publication flows worked through ordinary HTTP after HTML, network, and first-party JavaScript inspection. They needed neither a HAR nor a browser at runtime.

#### Føtex

The public [Føtex flyer page](https://www.foetex.dk/foetex-avis/) linked to an [iPaper publication](https://avis.foetex.dk/naeste-uges-avis/uge-27282930/). Its HTML exposed `window.staticSettings` with paper ID `3041345`, 88 page numbers and dimensions, publication URLs, and OCR-like `pageTexts` containing names, prices, dates, member restrictions, and format exclusions. Image URLs were signed for the viewer session and should not be persisted. A separate enrichment response had 165 page-coordinate entries with product/search links and alt text, but no structured prices.

First-party JavaScript configured Salling Group's `GET /v1/leaflet-offers`. With `brands=foetex&page=N`, it returned product groups with title, price, original price, discount, unit text, dates, brand, image, category codes, and `membershipOffer` and `personalizedOffer` flags. Pages held 100 groups; page 21 had results and page 22 was empty. The feed did not match the iPaper publication: only 33 observed offers had the weekly date range, while many were longer-running or personalized. The flags allow member and personal offers to be excluded, but exact flyer parity remains unresolved.

The observed iPaper text states that the monthly paper is broadly national but that not every item is stocked in Føtex Food and that it does not apply to Føtex Go or Føtex City. No store selection was required for either tested publication flow.

The structured Salling feed is easier to normalize if its scope fits. The [developer portal](https://developer.sallinggroup.com/) offers public API sign-up, but this review did not establish that `leaflet-offers` is included. Use an independently issued, approved token, not the bearer token from first-party JavaScript. The [iPaper robots file](https://avis.foetex.dk/robots.txt) disallows crawling and the [Salling API robots file](https://api.sallinggroup.com/robots.txt) disallows the offer route. Clarify permission before automating either. If access is limited to the paper, `pageTexts` extraction needs error-prone segmentation and checks against page images; permission to view alone does not establish permission to extract.

#### Netto

The [Netto paper page](https://netto.dk/netto-avisen/) server-rendered a Next.js `leaflets` object with Tjek catalog ID, dates, page images, `page_count: 29`, `offer_count: 156`, and `all_stores: true`. First-party JavaScript exposed the browser API configuration. The SuperBrugsen request sequence worked without browser state: catalog metadata, then paginated `GET /v2/offers?catalog_id=...&order_by=page&offset=...&limit=100`.

Two pages returned 100 and 54 rows, yielding 154 distinct offers rather than the declared 156. Rows had title, description, DKK price, quantity, image, validity, and page fields. Only 4 had a previous price; none had category IDs or a store ID. The paper was chain-wide and needed no location, but did not establish local stock.

Netto can share the SuperBrugsen Tjek adapter with a different bootstrap parser. Its [robots file](https://netto.dk/robots.txt) allows the site, but grants no API license. Tjek's [customer-only API access](https://tjek.com/apis-and-sdks) and terms raise the same permission concern despite the embedded catalog and browser key. Obtain Tjek or Salling approval before maintained use.

#### Lidl

The [Lidl paper page](https://www.lidl.dk/c/tilbudsavis/s10013730) server-rendered leaflet UUIDs and detail URLs for weekly, non-food, and longer-running "fast low price" papers. Viewer JavaScript used Schwarz's `https://endpoints.leaflets.schwarz/v4` base and fetched `GET /flyer?flyer_identifier={uuid}` without a token, cookie, CAPTCHA, or signature.

The [observed weekly response](https://endpoints.leaflets.schwarz/v4/flyer?flyer_identifier=019f4c5f-3449-7e73-b27f-a75b3459ab97) contained global dates, 42 pages with images and links, and 197 products. All had structured titles and prices; descriptions, brands, product URLs, and images were usually present. `categoryPrimary` classified 121 as `Food` and 76 as `Non food`, so food-only requests need filtering. No previous prices were exposed, ruling out percentage-discount sorting from this source. Products inherit flyer dates and join to pages through link IDs.

The response listed only region code `0`; related flyers had no store IDs or region codes. The [Lidl robots file](https://www.lidl.dk/robots.txt) does not disallow the flyer path, and the [Schwarz overview robots file](https://esi.leaflets.schwarz/robots.txt) has an empty `Disallow`. The JSON endpoint has no robots file.

The region data suggests a national publication, not local stock. This review found no documented first-party API program or general reuse grant. Permission remains unresolved despite anonymous technical access.

### Cross-retailer design consequence

Use separate discovery adapters behind one normalized schema:

- Føtex: canonical page to current iPaper URL, then either approved Salling offer pagination or iPaper settings and text extraction;
- Netto: canonical Next.js payload to Tjek catalog ID, current first-party configuration to browser key, then Tjek catalog and offer pagination;
- Lidl: canonical overview to leaflet UUID, then one Schwarz `v4/flyer` response.

Netto has the cleanest existing-adapter fit. Lidl has the strongest unauthenticated structured response and an authoritative food/non-food field, but no previous prices. Føtex has rich structured prices through Salling but unresolved scope and credential permission; its exact iPaper fallback is substantially less reliable. Combined output should therefore report source-level completeness, location scope, food-classification basis, and previous-price availability rather than imply that all retailers provide equivalent discounts. Keep member and personalized offers out, cache at flyer timescales, use low request volumes, and stop rather than add browser automation if an endpoint introduces authentication or access controls.
