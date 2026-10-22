---
name: hardware-deal-check
description: Find and assess new or used development hardware deliverable in Denmark. Use when Tobias asks to search for hardware deals, compare offers or check whether a specific offer is suitable or genuinely discounted.
---

# Hardware deal check

## Discovery and limits

Actively search public shops, price-comparison and price-history sites, and public used marketplaces. Start with PriceRunner DK, Proshop, Komplett, Computersalg, Elgiganten, Power, DBA and eBay; include reputable EU shops that deliver to Denmark. Read the exact public listing and vendor specification pages. Research missing facts before asking Tobias, and use independently found price history as discount evidence.

Never buy, bid, reserve, contact sellers or log into Tobias's accounts. Every purchase requires his explicit approval; a ceiling or review verdict is not approval. Never bypass captchas, paywalls or access controls. If a source blocks access, report the gap and try another public source.

Keep private sellers' personal details and private-listing URLs only in the in-session report, never in the vault or any tracked file. Do not create price databases or history files in the vault. Keep deal results in the current report rather than maintaining a vault price record. Do not ingest mail or schedule recurring sweeps unless separately requested. Cloud-model context is not zero-retention; do not promise deletion of host or provider transcripts.

Record the observation date and source links in the report. Separate fetched evidence, Tobias's supplied facts and assumptions. Unavailable evidence stays unknown.

## Target and ceilings

The target is a second Omarchy PC running full autonomous T3 teams, controlled from the existing PC. Keep Intel Core Ultra 9 285K AND AMD Ryzen 9 9950X shortlisted, default to 128GB RAM / 2TB local NVMe, and wait for a deal. Intel Core Ultra 7 265K and AMD Ryzen AI Max+ 395 are watch-only. The 395 is AMD, not Intel. Do not promote watch-only types without Tobias's choice.

Reject Macs for development. Do not recommend a Mac mini as a CI box unless a project needs macOS verdicts: the required x86 Linux (Omarchy, Wayland) and Windows verdicts are not supplied by its ARM VMs. This table gives Macs no ceiling. Cloud-served models justify no GPU/NPU inference premium.

Tobias's willingness-to-pay choices, 2026-10-13; not benchmark-derived or proof of a discount

| Complete configuration | New landed DKK | Used landed DKK |
|---|---:|---:|
| 128GB / 2TB, Intel Core Ultra 9 285K | 24,000 | 16,000 |
| 128GB / 2TB, AMD Ryzen 9 9950X | 21,000 | 14,000 |
| 128GB / 2TB, AMD Ryzen 9 9900X | 18,000 | 12,000 |
| 128GB / 2TB, Intel Core Ultra 7 265K, watch-only | 20,000 | 13,000 |
| 128GB / 2TB, AMD Ryzen AI Max+ 395, watch-only | 24,000 | 16,000 |
| 128GB ECC / 2TB, 5975WX-class P620 | No ceiling | 20,000 |
| 64GB / 2TB fallback, exact CPU still required | 15,000 | 10,000 |
| 96GB / 2TB, AMD Ryzen 9 9950X | 21,000 | 14,000 |

The P620 used ceiling is before the extra operating-cost adjustment below. A 64GB fallback is a separate capacity qualification, not an assumed upgrade path. Do not invent ceilings for other configurations or change these from benchmarks.

## Hard filters

Separate sourced evidence, known failures and unknowns. An unknown fact stays unknown, never zero or an inferred pass. Require:

- Exact CPU and variant, installed RAM, usable Linux RAM after GPU carve-out, and host/VM/team headroom. Check DIMM type, population, trained speed and supported configuration. Distinguish soldered capacity limits from verified replaceable-memory upgrades. A maximum supported capacity is not installed RAM.
- At least 2TB local NVMe, complete case, PSU and sustained CPU/chassis cooling. Include required console, mains/display cables and adapters. Confirm a working wired path of at least 2.5GbE, including needed NIC, switch ports and cabling.
- Exact board/NIC, Omarchy kernel and firmware compatibility, and qualification evidence for the required native UI/display and KVM/guest paths. Vendor Linux support, a Windows driver fix or Xvfb alone does not prove those paths. Full-team operation needs demonstrated host-owned admission and sufficient usable RAM, not an advertised core count.
- Sustained power, cooling and noise evidence at the intended setting. Label workload, duration, wall-power boundary and acoustic conditions; a different variant or workload leaves limits. TDP, boost clocks, a PSU rating or a seller's quiet label is not evidence.
- Exact selected-variant stock, observation date, Denmark delivery and complete VAT treatment. Distinguish preorder, family availability and selectable options from verified selected-variant stock evidence. Establish actual consumer/business buyer status, warranty, defect/return rights and return costs; do not assume consumer rights for a business purchase.
- For used systems, condition and SSD model/health. For ECC claims, CPU/board/firmware/DIMMs and Linux correction reporting, plus populated channels. On-die ECC alone is not system ECC.
- Funds for the complete usable system and every required addition. Add a Windows licence only if this new box actually hosts a separate Windows guest and no valid applicable licence is stated. If licence need or entitlement is unclear, ask. Do not assume an OEM host licence covers the guest or impose a fixed retailer price.

## Landed cost

Use transparent arithmetic, not a new script:

`landed DKK = item with correct VAT + shipping + payment/FX fees + import costs + required parts/accessories/software + required network/cooling additions`

Convert foreign-currency components with a sourced FX rate and date or Tobias's supplied rate; include payment-provider FX fees separately. Verify Denmark delivery and shipping from public shop terms or the selected listing. Never add VAT twice to a gross price, automatically deduct VAT on used-margin goods, assume tax recovery or rely on false customs declarations. Show each component, currency and VAT basis. Explicitly evidenced zero or not-required costs are valid; unknown costs are not. An incomplete total is only a known subtotal, not a landed price.

## Electricity adjustment

Use measured wall watts or clearly labelled comparable scenario assumptions, not TDP/PSU ratings or wholesale electricity prices:

`annual kWh = (idle W × annual idle hours + load W × annual load hours) / 1000`

`annual energy cost DKK = annual kWh × actual all-in Danish tariff DKK/kWh`

`used adjusted ceiling = base used ceiling - max(0, H × (annual energy cost used - annual energy cost reference))`

H is Tobias's submitted ownership horizon in years. Tariff, duty cycle and reference must also be submitted facts or explicit scenario inputs, never assumptions attributed to Tobias. If measured or explicitly comparable assumptions are absent, leave the base ceiling unchanged and mark the adjustment uncomputed, with the missing inputs. Label scenario-adjusted ceilings as scenarios, not measurements. Report duty cycle and throughput separately; equal hours do not prove equal work or energy efficiency. Do not invent an adjustment to rescue or reject a candidate.

## Discount evidence

No reliable price-history or comparable-baseline evidence means `discount_unproven`, even below the ceiling. MSRP, crossed-out prices and an old quote do not establish a market discount. Do not invent a 90-day baseline or treat the prior proposed 20% rule as Tobias's approved contract.

Use public price history, researched comparable offers or Tobias's supplied baseline facts to compare like-for-like complete delivered variants and conditions:

`observed discount % = (comparable baseline landed DKK - candidate landed DKK) / comparable baseline landed DKK × 100`

Require a positive baseline cost. Label observation dates, sample count, coverage, gaps, variant/condition and cost-basis limits. Cite the baseline source in the report; do not retain a vault history file, fill missing days or call a sparse comparison a market low. Report the observed comparison without an arbitrary hard percentage rule. If it does not support a genuine discount, keep `discount_unproven`.

## Verdict

Use this fixed format:

- **Status:** `rejected` / `needs_information` / `discount_unproven` / `qualifies_for_Tobias_review`.
- **Capacity tier + CPU:** minimal approved type, exact CPU, installed and usable RAM, local NVMe, new/used condition.
- **Landed cost + breakdown:** complete total or known subtotal with unknown components.
- **Ceiling including energy adjustment:** base, any evidence-backed used adjustment and result; otherwise uncomputed adjustment or no approved ceiling.
- **Hard-filter unknowns:** failures, evidence limits and outstanding requirements.
- **Discount basis / limits:** sourced comparison and coverage, or absent/unproven.
- **Exact additional facts needed:** only the missing minimal facts or Tobias choices; write “none” if complete.

A known hard-filter failure or a known cost exceeding the applicable ceiling is `rejected`. Otherwise missing required facts, an unapproved tier/role or an unresolved required operating-cost adjustment is `needs_information`. Once suitability and cost are complete, absent/insufficient discount evidence is `discount_unproven`. Only a suitable, within-ceiling candidate with supported discount evidence is `qualifies_for_Tobias_review`. That last status is not purchase approval. Recheck public stock, price and Denmark delivery before a purchase recommendation; ask Tobias only for facts or choices that public research cannot establish.

## Verification

For discovery, inspect public listings and vendor specifications, cite current price and delivery evidence, and leave blocked or missing facts unknown. Confirm that no account access, seller contact or purchasing action occurred and that no private-listing URLs or seller personal details entered tracked files. No script or retained fixture is needed. Dry-run the assessment logic with these synthetic facts:

1. A complete, qualified 128GB / 2TB 9950X new system at 20,000 landed DKK, with all cost components explicit and no history, returns `discount_unproven`, not purchase approval.
2. The same facts with unknown Denmark shipping return `needs_information`. Show the known subtotal and unknown shipping, never zero shipping.
3. A 64GB soldered system cannot qualify as 128GB or promise that upgrade. Reject it for the 128GB target; assess it as a 64GB fallback only with its own full-team capacity qualification.
4. Pure energy scenario: explicitly set H = 3 years, tariff = 2.5 DKK/kWh, 20 idle + 4 load hours/day for 365 days, used = 80/300W and reference = 30/160W. Annual hours are 7,300 idle and 1,460 load. `(80 × 7300 + 300 × 1460) / 1000 = 1022 kWh`; `(30 × 7300 + 160 × 1460) / 1000 = 452.6 kWh`. Extra cost is `(1022 - 452.6) × 2.5 = 1423.50 DKK/year`, or `4270.50 DKK` over three years. A `20000 DKK` base yields `15729.50 DKK` scenario-adjusted ceiling. This is neither a product measurement nor an equal-throughput claim.
