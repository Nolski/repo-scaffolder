# Transition: repo-scaffolder → DPG-Readiness Maturity Tool

This directory holds the assessment and all external-resource research for transitioning this tool from a **US-Federal open-source repo scaffolder** (forked from [DSACMS/repo-scaffolder](https://github.com/DSACMS/repo-scaffolder)) into an **automated maturity tool that helps projects become fully [DPG](https://www.digitalpublicgoods.net/standard)-ready** (Digital Public Goods, per the DPGA).

## Read in this order

| File | Contents |
|---|---|
| [`00-assessment.md`](./00-assessment.md) | **Start here.** Full current-state assessment + gap analysis (Gaps A–F) + target architecture. |
| [`01-dpg-standard.md`](./01-dpg-standard.md) | The DPG Standard's 9 indicators (with evidence requirements), approved licenses, Enhanced Privacy Framework, DPGA submission/review process, data model, UN policy lineage. |
| [`02-maturity-models.md`](./02-maturity-models.md) | Established OSS/DPG maturity models + a proposed re-anchored 5-tier model where Tier 4 ≡ DPG-eligible. |
| [`03-automation-tooling.md`](./03-automation-tooling.md) | Open-source tools to automate the checks, mapped to DPG indicators (Scorecard, license scanners, secret scanners, CHAOSS, etc.). |
| [`04-resources.md`](./04-resources.md) | Consolidated master list of every external resource, grouped by purpose. |
| [`05-roadmap.md`](./05-roadmap.md) | Phased, actionable transition plan (Phases 0–5) + open decisions. |

## The one-line summary

Today the tool measures **open-source process maturity** (how openly a repo is governed). DPG-readiness requires a **fitness-for-purpose bar** (the 9 indicators: SDG relevance, open licensing, ownership, platform independence, documentation, data portability, privacy/legal, standards & best practices, do-no-harm). The transition keeps the cookiecutter + tier architecture but **re-anchors the model onto the 9 indicators, adds the missing privacy/safety/SDG dimensions, replaces the deprecated repolinter engine with maintained automated checks, fully de-Americanizes the content, and culminates in a pre-filled DPG nomination package.**

## Key reusable upstream artifacts (all permissively licensed)

- [`standard-questions.md`](https://raw.githubusercontent.com/DPGAlliance/DPG-Standard/master/standard-questions.md) — the operational checklist (CC-BY-SA-4.0)
- [`nominee-schema.json`](https://github.com/DPGAlliance/publicgoods-candidates) + `screening-schema.json` — the DPG data model (Unlicense)
- [`help-center/licenses.md`](https://github.com/DPGAlliance/publicgoods-candidates/blob/main/help-center/licenses.md) — approved-license SPDX allow-lists (Unlicense)
- [`dpg-maturity-indicators`](https://github.com/DPGAlliance/dpg-maturity-indicators) — maturity scoring framework (CC0-1.0)
- [DPGA Maturity Tool](https://maturity.digitalpublicgoods.net/) — the closest existing analogue; study before building

> Research compiled 2026-06-23. URLs flagged `⚠` in the resource files have partial confidence — verify before hard-coding.
