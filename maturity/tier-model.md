# DPG Readiness Tier Model

> The re-anchored maturity ladder. Unlike the original collaboration-scope model (Private → Community Governance), these tiers measure **distance to DPG eligibility**: indicators accumulate, and **Tier 4 ≡ all 9 DPG indicators met → eligible to nominate to the [DPG Registry](https://www.digitalpublicgoods.net/registry)**.
>
> Used by `dpg-assess` to classify a repo and by `dpg-remediate` to choose what to fix next. Indicator detail is in `indicators.md`.

## Tiers

| Tier | Name | Theme | Indicators that become **mandatory** at this tier |
|---|---|---|---|
| **0** | Private / Prototype | Internal, experimental | *(none — internal)* |
| **1** | Public Release | Legally open & attributable | **2** approved open license · **3** clear ownership · **5** documentation (basic) |
| **2** | Maintained & Mission-Aligned | Sustained, purposeful | **1** SDG relevance · **5** documentation (full) · **8** entry (Principles for Digital Development + OpenSSF Badge *passing*) |
| **3** | Open & Safe | Working in public, do-no-harm | **4** platform independence · **6** non-PII data extraction · **7** privacy & applicable laws · **9A** data privacy & security |
| **4** | DPG-Ready / Eligible | Meets the full DPG Standard | **8** full · **9B** inappropriate/illegal content · **9C** harassment protection → **all 9 met → nominate** |

A tier is **achieved** when every indicator mandatory at that tier *and all lower tiers* is `met` (or `not-applicable`). The repo's current tier is the highest fully-achieved tier; its **target** is the next one up, and the gap report lists exactly the indicators blocking promotion.

## Classification algorithm (for `dpg-assess`)

```
For each indicator, status ∈ {met, partial, unmet, not-applicable} (from indicators.md).
tier = 0
for t in [1, 2, 3, 4]:
    required = mandatory indicators introduced at tiers 1..t
    if every r in required is (met or not-applicable):
        tier = t
    else:
        break
current_tier = tier
target_tier  = min(tier + 1, 4)
blockers     = required-at(target_tier) that are not (met | not-applicable)
```

`partial` never satisfies a mandatory indicator — it appears in the gap report as "started, not done."

## Why this ordering

- **Front-load cheap/legal** indicators (2/3/5) at Tier 1.
- **Mid-load mission + sustainability** (1, 8-entry) at Tier 2.
- **Reserve the hard do-no-harm/privacy/portability** indicators (4/6/7/9) for Tiers 3–4, where projects have real users and data.
- Every indicator maps to a concrete repo artifact, so remediation is mechanical (see `indicators.md` remediate rows).

## Interoperability

This ladder is intentionally compatible with the DPGA's own [7-pillar maturity tool](https://maturity.digitalpublicgoods.net/) (Governance; Security & Privacy; Open Standards; Product Roadmap; Source Code; Total Cost; Composability). When emitting reports, note the equivalent DPGA pillars so output is comparable. The terminal state (Tier 4) is defined to be exactly DPG eligibility — not a separate bar.

## Relationship to the legacy 5-tier model

The original tiers (`maturity-model-tiers.md`) classified by *collaboration scope*. That axis still loosely correlates (a Tier-4 DPG is usually publicly developed), but it is **not** the thing we score. Where the cookiecutter scaffolding still references the old tier numbers, they now carry these DPG-readiness meanings.
