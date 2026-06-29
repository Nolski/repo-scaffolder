# Transition Assessment: From US-Federal Repo-Scaffolder to a DPG-Readiness Maturity Tool

> **Date:** 2026-06-23 · **Author:** assessment compiled for the repo-scaffolder → DPG transition
> **Goal:** Turn this tool from a US-Federal open-source *scaffolder* into an **automated maturity tool that helps projects transition into fully DPG-ready open source goods**, where "DPG-ready" means *meets all 9 indicators of the [Digital Public Goods Standard](https://www.digitalpublicgoods.net/standard)*.

This document is the **gap analysis and plan of record**. Supporting research lives alongside it:

- [`01-dpg-standard.md`](./01-dpg-standard.md) — the DPG Standard's 9 indicators + the DPGA submission/review process
- [`02-maturity-models.md`](./02-maturity-models.md) — established OSS/DPG maturity models + a proposed re-anchored tier model
- [`03-automation-tooling.md`](./03-automation-tooling.md) — open-source tools we can integrate to *automate* the checks
- [`04-resources.md`](./04-resources.md) — consolidated master list of every external resource
- [`05-roadmap.md`](./05-roadmap.md) — phased, actionable transition roadmap

---

## 1. What the tool is today

`repo-scaffolder` is a fork of **[DSACMS/repo-scaffolder](https://github.com/DSACMS/repo-scaffolder)** — the open-source scaffolding tooling built by the US Centers for Medicare & Medicaid Services (CMS) Open Source Program Office (OSPO). Its core mechanics:

| Component | What it does |
|---|---|
| **Cookiecutter templates** (`tier0/`–`tier4/`) | Generate a repo pre-populated with graduated governance files (LICENSE, README, COMMUNITY, SECURITY, CONTRIBUTING, CODE_OF_CONDUCT, GOVERNANCE) per maturity tier. |
| **5-tier maturity model** (`maturity-model-tiers.md`) | Tier 0 Private → Tier 1 One-Time Release → Tier 2 Close Collaboration → Tier 3 Working in Public → Tier 4 Community Governance. Each file/section is marked Mandatory / Recommended / Not-recommended per tier. |
| **`tier-determiner.py`** | Interactive CLI that asks 5 yes/no questions to classify a project into a tier. |
| **repolinter rulesets** (`repolinter.json` per tier) | File-presence / file-content checks; the *only* existing "automated assessment" surface. |
| **GitHub Actions** (`.github/workflows/`) | Ecosystem automation: push templated files to tagged repos, extend/merge JSON, auto-changelog, contributors, gitleaks secret-scan, `code.json` metadata, repo-hygiene check via repolinter. |
| **`code.json`** | US Federal Source Code Policy metadata file collected per repo. |

### What this tool measures today
Essentially **one axis: open-source process maturity / collaboration scope** — "how openly is this developed and governed?" It checks that the *right files exist with the right sections*. It does **not** assess fitness-for-purpose, mission relevance, privacy/safety, data portability, or standards adherence.

---

## 2. What "DPG-ready" actually requires

The DPG Standard is a **fitness-for-purpose compliance bar**, not a process ladder. A project is a DPG only if it satisfies **all 9 indicators** (full detail in [`01-dpg-standard.md`](./01-dpg-standard.md)):

1. **Relevance to the SDGs** — demonstrated link to specific SDG targets *(gating criterion; open source alone ≠ DPG)*
2. **Use of an approved open license** — OSI (software) / Creative Commons (content) / Open Definition (data), referenced by SPDX ID
3. **Clear ownership** — documented ownership of produced assets
4. **Platform independence** — no hard lock-in to closed components; open alternatives exist
5. **Documentation** — of source code, use cases, and/or functional requirements
6. **Mechanism for extracting non-PII data** in a non-proprietary format
7. **Adherence to privacy & applicable laws** — incl. the 2024 Enhanced Privacy Framework
8. **Adherence to standards & best practices** — e.g. the Principles for Digital Development
9. **Do no harm by design** — 9A data privacy & security · 9B inappropriate/illegal content (incl. CSAM policies) · 9C protection from harassment & underage-user safety

---

## 3. Gap analysis — the heart of the transition

### Gap A — The maturity model measures the wrong thing
**Current:** tiers measure *collaboration scope* (private → community-governed).
**Needed:** tiers must measure *distance to DPG eligibility*, accumulating the 9 indicators so the **top tier ≡ "all 9 indicators satisfied → eligible to nominate to the DPG Registry."**
**Action:** Re-anchor the 5-tier model onto the 9 indicators (proposed mapping in [`02-maturity-models.md` §5](./02-maturity-models.md)). Keep the familiar 5-rung ladder for backward compatibility; repurpose the top rung(s) from "community governance" to "DPG-ready."

### Gap B — Four whole DPG dimensions are absent
The CMS model has **no concept** of:
- **SDG relevance** (Indicator 1) — needs a new prompt + `code.json`/metadata field tagging SDG(s) and targets.
- **Do-no-harm / safety** (Indicator 9) — needs CSAM/illegal-content policy templates, harassment-protection processes, underage-user safety. Currently only a generic `CODE_OF_CONDUCT.md` exists.
- **Privacy & applicable laws** (Indicators 7 & 9A) — needs a privacy-policy template, PII-minimization questionnaire, consent/retention/deletion prompts (the Enhanced Privacy Framework's 6 mandatory questions). `SECURITY.md` ≠ privacy.
- **Platform independence & data portability** (Indicators 4 & 6) — needs prompts/checks for proprietary dependencies and a non-proprietary data-export mechanism.

**Action:** Add new template artifacts (`PRIVACY.md`, content-moderation policy, SDG-mapping section) and new assessment questions for each.

### Gap C — "Assessment" is shallow and the engine is deprecated
**Current:** repolinter checks only file/section presence — and **repolinter is now archived/read-only (since ~Feb 2026)** with unpatched advisories.
**Needed:** real, automated, evidence-producing checks mapped to indicators.
**Action:** Replace/augment repolinter with a maintained stack (full matrix in [`03-automation-tooling.md`](./03-automation-tooling.md)):
- **OpenSSF Scorecard** → security & best-practices (Indicators 8, 9A)
- **OpenSSF Best Practices Badge** criteria → tiered best-practices (Indicator 8)
- **licensee / REUSE / ScanCode** → verify license is OSI/CC/Open-Definition approved by SPDX ID (Indicator 2)
- **gitleaks / trufflehog** (gitleaks already wired in) → secrets/PII (Indicator 9A)
- **GitHub Community Profile API** → cheap file-presence replacement (Indicators 3, 5)
- **CHAOSS / GrimoireLab** → community-health metrics for tier gating

### Gap D — The whole thing is still US-Federal, not UN/DPG
The fork is **only partially** rebranded. Confirmed leftovers (grep across the repo):
- **License model is wrong for DPG.** Everything defaults to **CC0 / US public domain** (justified via *Title 17 §105*). DPG software needs an **OSI-approved license** (MIT/Apache-2.0/GPL/etc.); CC0 is fine for content/data but **not** an OSI license for software. This is a correctness bug, not just branding.
- **`code.json`** is the US Federal Source Code Policy metadata schema. The DPG equivalent is the **DPGA `nominee-schema.json`** (name, license[], organizations, SDGs, type, stage, sectors, repositories). We should emit DPG-aligned metadata.
- **Org defaults inconsistent:** `tier2/`, `tier3/` cookiecutter say `UNDP`; `tier0/`, `tier1/`, `tier4/` still say `DSACMS`. Topics added are `dsacms-tierX`.
- **US policy references** throughout: Section 508, Title 17, "Federal policies," "Anti-deficiency," CMS/USDS/HHS/18F acknowledgements, `opensource@cms.hhs.gov` feedback address.
- Workflows hard-code `DSACMS/repo-scaffolder` and `DSACMS/repolinter-action` upstreams.

**Action:** A systematic rebrand + a *substantive* relicensing/metadata change (not just find-replace).

### Gap E — No bridge to the actual DPG submission
The tool stops at "good repo." DPG-readiness should culminate in **producing the DPGA nomination artifact** and pointing to [app.digitalpublicgoods.net](https://app.digitalpublicgoods.net).
**Action:** Add a Tier-4 output that generates a pre-filled DPG nominee JSON (against `nominee-schema.json`) + a gap report listing which of the 9 indicators are met / unmet with evidence links.

### Gap F — Tier-determiner asks the wrong questions
The 5 yes/no questions are about contributors/releases/external collaboration. They should instead probe the DPG indicators (Is it open-licensed? Does it relate to an SDG? Does it handle PII? etc.) to route a project to its current tier *and* surface the nearest unmet indicators.

---

## 4. What we keep (assets worth preserving)

- The **cookiecutter scaffolding engine** and per-tier template structure — sound architecture, reuse it.
- The **graduated Mandatory/Recommended/Not-recommended matrix** concept — extend it with indicator columns.
- **GitHub Actions ecosystem automation** (push updates to tagged repos, auto-changelog, contributors, gitleaks) — retarget, don't rebuild.
- The **tier-determiner UX** — keep the interactive flow, swap the question set.
- The **outbound checklists** per tier — extend into DPG-readiness checklists.

---

## 5. Target architecture (one-paragraph vision)

A project runs the tool and gets: (1) a **tier classification** based on DPG-indicator coverage; (2) **scaffolded files** that fill the gaps for its target tier (now including privacy, content-moderation, SDG-mapping, and an OSI license chooser); (3) an **automated assessment** (Scorecard + license check + secret scan + community profile) that produces an **indicator-by-indicator gap report**; and (4) at the top tier, a **pre-filled DPG nomination package** ready to submit to the DPGA registry. The model stays interoperable with the DPGA's own [7-pillar maturity tool](https://maturity.digitalpublicgoods.net/).

See [`05-roadmap.md`](./05-roadmap.md) for the phased plan to get there.
