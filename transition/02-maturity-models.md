# Maturity Models & the Re-Anchored Tier Proposal

> Grounds the redesign of our 5-tier model in established OSS/DPG maturity frameworks, and proposes a concrete re-anchoring so the **top tier ≡ DPG-eligible**.

## 1. Origin of our model — the CMS/DSACMS OSPO model

Our tool forks [DSACMS/repo-scaffolder](https://github.com/DSACMS/repo-scaffolder) (CC0). Its 5 tiers measure **collaboration scope**:

| Tier | Name | Purpose |
|---|---|---|
| 0 | Private Repository | Experimental / single dev |
| 1 | One-Time Release | Public, no planned maintenance |
| 2 | Close Collaboration | Innersource / trusted group |
| 3 | Working in Public | Open source, agency-led |
| 4 | Community Governance | Externally stewarded, open governance |

**Lineage:** OMB M-16-21 Federal Source Code Policy (2016) → code.gov (now retired, redirects to digital.gov) → 18F / USDS "default to open" → CMS OSPO Guide.
**Key limitation:** it's a *governance-scope* ladder, not a *fitness-for-purpose* ladder. DPG-readiness needs the fitness/mission dimension this lacks.

## 2. Established models worth borrowing from

| Model | Shape | What to borrow |
|---|---|---|
| **OpenSSF Best Practices Badge** (bestpractices.dev) | **Passing → Silver → Gold** | The clearest *tiered* analogue; per-tier criteria lists. |
| **OpenSSF Scorecard** (ossf/scorecard) | ~23 checks scored 0–10 | The *automation engine* for security/best-practice gating. |
| **CHAOSS** (chaoss.community) + GrimoireLab | Metrics Models (no tiers) | Community-health metrics to gate higher tiers. |
| **TODO Group OSPO Maturity Model** | 5 stages | Org-level ladder vocabulary. |
| **OpenChain** | ISO/IEC 5230 (license compliance) + 18974 (security) | Formal compliance backbone for top tier. |
| **The Open Source Way / Minimum Viable Governance** | Qualitative | Governance templates for mid/upper tiers. |
| **QSOS** | 0–2 scoring per criterion | Objective, traceable scoring method. |

## 3. DPG-specific & digital-development frameworks

- **DPGA Maturity Tool** (<https://maturity.digitalpublicgoods.net/>) — **the closest existing analogue.** Self-assessment across **7 pillars** (Governance; Security & Privacy; Open Standards; Product Roadmap; Source Code; Total Cost; Composability) mapped to the 9 indicators, with radar-chart output. **Study and align with this.** Indicator defs: [`dpg-maturity-indicators`](https://github.com/DPGAlliance/dpg-maturity-indicators) (CC0-1.0).
- **UNICEF DPG Accelerator Guide** (<https://unicef.github.io/publicgoods-accelerator-guide/>, CC-BY-SA-4.0) — an explicit **OSS→DPG pathway playbook**; mine it for tier-criteria and remediation guidance.
- **Principles for Digital Development** (<https://digitalprinciples.org/>, refreshed 2024) — the "best practices/principles" Indicator 8 points to. Current 9: understand the ecosystem · share/reuse/improve · design with people · design for inclusion · build for sustainability · people-first data · open & transparent practices · anticipate & mitigate harms · use evidence.
- **Country/DPI maturity models** (org-level context, not repo-level): UNDP Digital Maturity Assessment (6 pillars, 5 levels), World Bank DPI Maturity Index (4 tiers), GovStack maturity assessment, DPI Map.

## 4. How DPG-readiness differs from generic OSS maturity

Generic OSS maturity ≈ Indicators **2, 3, 5** (license, ownership, docs) + community health. DPG adds four mission-specific dimensions that the CMS model entirely lacks:
1. **SDG relevance** (Indicator 1)
2. **Do-no-harm + privacy/legal** (Indicators 7, 9A/B/C)
3. **Platform independence + data portability** (Indicators 4, 6)
4. **Open standards & best practices / interoperability** (Indicator 8)

## 5. Proposed re-anchored tier model

Keep the 5-rung ladder (backward compatible with the cookiecutter templates); re-purpose the rungs so indicators accumulate and **Tier 4 ≡ all 9 satisfied → DPG-eligible.**

| New Tier | Name | Theme | DPG indicators that become **mandatory** here |
|---|---|---|---|
| **0** | Private / Prototype | Internal, experimental | (none — internal) |
| **1** | Public Release | Legally open & attributable | **2** approved open license · **3** clear ownership · **5** documentation (basic) |
| **2** | Maintained & Mission-Aligned | Sustained, purposeful | **1** SDG relevance · **5** documentation (full) · **8** (entry: Principles for Digital Development + OpenSSF Badge *passing*) |
| **3** | Open & Safe | Working in public, do-no-harm | **4** platform independence · **6** non-PII data extraction · **7** privacy & applicable laws · **9A** data privacy & security |
| **4** | DPG-Ready / Eligible | Meets the full DPG Standard | **8** (full) · **9B** inappropriate/illegal content · **9C** harassment protection → **all 9 met → nominate to the DPG Registry** |

**Why this ordering:** front-load cheap/legal indicators (2/3/5) at Tier 1; mid-load mission + sustainability (1/8-entry) at Tier 2; reserve the hard do-no-harm/privacy/portability indicators (4/6/7/9) for Tiers 3–4 where projects have real users and data. Each indicator maps to concrete repo artifacts (license file, ownership declaration, docs, `PRIVACY.md`, data-export feature, content-moderation policy, `CODE_OF_CONDUCT.md`), so the cookiecutter scaffolding model still applies.

**Design recommendations:**
1. Make tier advancement **machine-checkable** (Scorecard + Best Practices Badge + license check + secret scan), mirroring the DPGA tool's radar output.
2. Adopt DPGA vocabulary for the top rungs: Tier 3 = *nominee-ready*, Tier 4 = *DPG-eligible* → Registry-listed.
3. Treat **Indicator 9 (do-no-harm) as a distinct gate**, not a checklist line — it's where DPGA expert review concentrates and where generic OSS models are blind.
4. License the redesigned model permissively so it can be contributed back upstream (upstream is CC0; DPG Standard is CC-BY-SA-4.0).
