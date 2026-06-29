# DPG Readiness Checklist

## Tier 4: DPG-Ready / Eligible — *Meets the full DPG Standard*

This checklist is **cumulative**: Tier 4 includes everything in Tiers
[1](../tier1/checklist.md)–[3](../tier3/checklist.md) plus the final indicators. When every
item here is **met** or **not-applicable**, all 9 DPG Standard indicators are satisfied and
the project is **eligible to nominate to the [DPG Registry](https://www.digitalpublicgoods.net/registry)**.
See [`maturity/tier-model.md`](../maturity/tier-model.md).

### Carried over from Tiers 1–3

- [ ] **Indicator 1 — SDG relevance** (specific targets).
- [ ] **Indicator 2 — Approved open license**.
- [ ] **Indicator 3 — Clear ownership** (`GOVERNANCE.md`).
- [ ] **Indicator 4 — Platform independence**.
- [ ] **Indicator 5 — Documentation (full)**.
- [ ] **Indicator 6 — Non-PII data extraction** (or justified N/A).
- [ ] **Indicator 7 — Privacy & applicable laws** (`PRIVACY.md`).
- [ ] **Indicator 9A — Data privacy & security**.

### Mandatory at Tier 4

- [ ] **Indicator 8 (full) — Standards & best practices**
  - Evidence: open standards adhered to (with validators); OpenSSF Best Practices Badge and
    a healthy Scorecard; signed releases / branch protection / CI / dependency review all in
    place; documented alignment with the Principles for Digital Development.

- [ ] **Indicator 9B — Inappropriate & illegal content**
  - Evidence: if the project collects/stores/distributes user content, `CONTENT_MODERATION.md`
    defines prohibited content (incl. **CSAM**) and the detection/reporting/moderation/removal
    process. *Mark not-applicable if there is no user-generated content — state why.*

- [ ] **Indicator 9C — Protection from harassment**
  - Evidence: `CODE_OF_CONDUCT.md` includes the harassment-protection and underage-user
    safety subsections (block/mute/report flow, triage timeline, minor-safety escalation).
    *Mark not-applicable if users do not interact through the product.*

### Final step

- [ ] **All 9 indicators met or N/A** → assemble the nominee package
  (see [`maturity/nominee-schema.json`](../maturity/nominee-schema.json)) and submit to the
  [DPG Registry](https://www.digitalpublicgoods.net/registry).

### Notes

_Record content-moderation applicability, harassment/underage-safety coverage, OpenSSF
results, and the nominee-package status here._
