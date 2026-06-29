# DPG Readiness Checklist

## Tier 3: Open & Safe — *Working in public, do-no-harm*

This checklist is **cumulative**: Tier 3 includes everything in
[Tier 1](../tier1/checklist.md) and [Tier 2](../tier2/checklist.md) plus the indicators
that become mandatory here. Each item maps to a
[DPG Standard](https://www.digitalpublicgoods.net/standard) indicator and names the
evidence that satisfies it. See [`maturity/tier-model.md`](../maturity/tier-model.md).

### Carried over from Tiers 1–2

- [ ] **Indicator 1 — SDG relevance** (specific targets in README).
- [ ] **Indicator 2 — Approved open license** (correct for project type).
- [ ] **Indicator 3 — Clear ownership** (now expanded in `GOVERNANCE.md`).
- [ ] **Indicator 5 — Documentation (full)**.
- [ ] **Indicator 8 (entry) — Principles for Digital Development + OpenSSF badge passing**.

### Mandatory at Tier 3

- [ ] **Indicator 4 — Platform independence**
  - Evidence: README "Platform Independence & Dependencies" section listing core tech and
    declaring closed dependencies with viable open alternatives (or confirming none).

- [ ] **Indicator 6 — Mechanism for extracting non-PII data**
  - Evidence: README "Data Export & Portability" section describing export/import in a
    non-proprietary format (CSV/JSON/XML/API). *Mark not-applicable if the project stores
    no data — state why.*

- [ ] **Indicator 7 — Privacy & applicable laws**
  - Evidence: `PRIVACY.md` answering the Enhanced Privacy Framework's 6 questions; names
    applicable laws (e.g. GDPR, regional data-protection acts) the project is designed to
    comply with.

- [ ] **Indicator 9A — Data privacy & security**
  - Evidence: `PRIVACY.md` security/access-control/integrity section; no leaked secrets
    (`gitleaks`/`trufflehog` clean); OpenSSF Scorecard security checks reasonable.

### Repo hygiene supporting the above

- [ ] `GOVERNANCE.md` expanded (ownership + decision-making + escalation).
- [ ] `CODE_OF_CONDUCT.md`, `SECURITY.md`, `PRIVACY.md` all present.
- [ ] Branch protection, dependency review, secret scanning enabled; accessibility target
  (WCAG 2.1 AA) stated where there is a UI.

### Notes

_Record privacy-law coverage, export formats, dependency declarations, and not-applicable
justifications._
