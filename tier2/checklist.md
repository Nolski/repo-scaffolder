# DPG Readiness Checklist

## Tier 2: Maintained & Mission-Aligned — *Sustained, purposeful*

This checklist is **cumulative**: Tier 2 includes everything in
[Tier 1](../tier1/checklist.md) plus the indicators that become mandatory here. Each item
maps to a [DPG Standard](https://www.digitalpublicgoods.net/standard) indicator and names
the evidence that satisfies it. See [`maturity/tier-model.md`](../maturity/tier-model.md).

### Carried over from Tier 1

- [ ] **Indicator 2 — Approved open license** (correct license for project type; SPDX id).
- [ ] **Indicator 3 — Clear ownership** (owner + maintainers documented).
- [ ] **Indicator 5 — Documentation (basic)** (README install/usage; CONTRIBUTING).

### Mandatory at Tier 2

- [ ] **Indicator 1 — Relevance to the SDGs** *(gating for DPG eligibility)*
  - Evidence: README "Relevance to the Sustainable Development Goals" section linking the
    project to one or more **specific SDG targets** (e.g. 3.8, 4.1, 16.6), not just goal
    numbers.

- [ ] **Indicator 5 — Documentation (full)**
  - Evidence: README also covers architecture/use cases; user or developer docs (a `docs/`
    tree, data dictionary, or model card as applicable). Sufficient for the project's
    complexity.

- [ ] **Indicator 8 (entry) — Standards & best practices**
  - Evidence: README "Standards & Best Practices" section referencing the
    [Principles for Digital Development](https://digitalprinciples.org/); an
    [OpenSSF Best Practices Badge](https://www.bestpractices.dev/) at **passing** level; CI,
    tests, and dependency review enabled.

### Repo hygiene supporting the above

- [ ] `CODE_OF_CONDUCT.md` present.
- [ ] `SECURITY.md` responsible-disclosure path; no secrets in history.
- [ ] Dependabot, secret scanning, and branch protection enabled.

### Notes

_Record SDG targets, OpenSSF badge URL, docs links, and any not-applicable justifications._
