# DPG Readiness Checklist

## Tier 1: Public Release — *Legally open & attributable*

This checklist tracks the [DPG Standard](https://www.digitalpublicgoods.net/standard)
indicators that become **mandatory at Tier 1**. Each item maps to one indicator and names
the evidence that satisfies it. See [`maturity/indicators.md`](../maturity/indicators.md)
and [`maturity/tier-model.md`](../maturity/tier-model.md) for the full model.

> A tier is achieved when every indicator mandatory at it (and all lower tiers) is **met**
> or **not-applicable**. Tier 4 ≡ all 9 indicators met → eligible to nominate to the
> [DPG Registry](https://www.digitalpublicgoods.net/registry).

### Mandatory at Tier 1

- [ ] **Indicator 2 — Approved open license**
  - Evidence: a `LICENSE` file with an [OSI-approved](https://opensource.org/licenses)
    license (software) or a Creative Commons / [Open Definition](https://opendefinition.org/)
    license (content/data); SPDX id recorded.
  - ⚠️ Do **not** apply CC0 to software (valid for data/content only).

- [ ] **Indicator 3 — Clear ownership**
  - Evidence: README "Ownership & Governance" section names the owner, org type, and
    (where relevant) copyright/trademark/ToS and redistribution basis for assets not solely
    owned. `CODEOWNERS` / `COMMUNITY.md` identify maintainers.

- [ ] **Indicator 5 — Documentation (basic)**
  - Evidence: `README.md` with project description, install, and usage; `CONTRIBUTING.md`
    present; passes `markdownlint`.

### Repo hygiene supporting the above

- [ ] `SECURITY.md` present with a responsible-disclosure path (Indicator 9A foundation).
- [ ] No secrets in the repo or git history (run `gitleaks`/`trufflehog`).
- [ ] Dependabot/dependency alerts and secret scanning enabled.
- [ ] Branch protection on `main`.

### Notes

_Record evidence links, SPDX id, and any not-applicable justifications here._
