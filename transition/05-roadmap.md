# Transition Roadmap

> Phased, actionable plan to turn `repo-scaffolder` into an automated DPG-readiness maturity tool. Each phase is independently shippable. See [`00-assessment.md`](./00-assessment.md) for the gaps each item closes (referenced as Gap A–F).

> **Implementation status (2026-06):** The transition has been implemented **skills-first** (Claude skills as the primary UX; tier templates as a remediation content library; cookiecutter kept for greenfield). Decisions taken: software license is *always prompted* (no default; OSI/CC/Open-Definition chooser); existing tiers were *transformed in place* (git history preserves the US-federal originals); skills ship as *checked-in project skills* in `.claude/skills/`. Delivered: `maturity/` knowledge core, `scripts/audit/` engine, `templates/` artifacts, `dpg-assess`/`dpg-remediate`/`dpg-scaffold` skills, de-Americanized tiers, and a `dpgReadinessCheck` CI workflow. The archived **repolinter** machinery was retired in favor of `scripts/audit/run_audit.py`. Remaining/optional follow-ups below are marked where not yet done.

## Phase 0 — De-Americanize & fix correctness bugs (closes Gap D)
*Foundational cleanup; mostly mechanical but includes one substantive fix.*

- [ ] **Relicense software templates** away from CC0/public-domain default → an **OSI license chooser** (MIT / Apache-2.0 / GPL-3.0 / AGPL-3.0). Keep CC0/CC-BY for content & data. *(This is a correctness bug for DPG Indicator 2, not just branding.)*
- [ ] Normalize org defaults: every tier's `cookiecutter.json` should default to `UNDP` (currently tier0/1/4 say `DSACMS`); change topic from `dsacms-tierX` to a UNDP/DPG tag.
- [ ] Strip/replace US-specific policy references (Section 508, Title 17, Anti-deficiency, "Federal policies", `opensource@cms.hhs.gov`) with DPG/UN equivalents (accessibility → WCAG; legal → "applicable privacy & data-protection law").
- [ ] Repoint hard-coded workflow upstreams (`DSACMS/repo-scaffolder`, `DSACMS/repolinter-action`) to this repo / maintained equivalents.
- [ ] Replace `code.json` (US Federal Source Code Policy) emission with **DPG `nominee-schema.json`**-aligned metadata.
- [ ] Update `README.md` acknowledgements/lineage and keep attribution to DSACMS upstream (license requires it).

## Phase 1 — Re-anchor the maturity model (closes Gap A)
- [ ] Rewrite `maturity-model-tiers.md` to the re-anchored 5-tier model ([`02-maturity-models.md` §5](./02-maturity-models.md)): Tier 4 ≡ all 9 DPG indicators met.
- [ ] Add **indicator columns** to the Mandatory/Recommended/Not-recommended matrix (map each indicator → tier → required artifact).
- [ ] Rewrite `tier-determiner.py` questions to probe the 9 indicators (open license? SDG link? handles PII? user interaction? data export?) and route to current tier + nearest unmet indicators (closes Gap F).

## Phase 2 — Add the missing DPG dimensions as scaffold artifacts (closes Gap B)
- [ ] **SDG mapping**: new README section + metadata field tagging SDG(s) + target(s) (Indicator 1). Use the [SDG goals list](https://sdgs.un.org/goals) as a controlled vocabulary.
- [ ] **`PRIVACY.md` template** implementing the Enhanced Privacy Framework's 6 mandatory questions (Indicators 7, 9A).
- [ ] **Content-moderation policy template** covering inappropriate/illegal content incl. CSAM detection/reporting/removal (Indicator 9B).
- [ ] **Harassment-protection + underage-safety** additions to `CODE_OF_CONDUCT.md` (Indicator 9C).
- [ ] **Platform-independence & data-portability** prompts/sections: declare closed deps + open alternatives; document non-proprietary export (Indicators 4, 6).

## Phase 3 — Build the automated assessment engine (closes Gap C)
- [ ] Replace/augment archived **repolinter** with a maintained stack (see [`03-automation-tooling.md`](./03-automation-tooling.md)):
  - [ ] **OpenSSF Scorecard** GitHub Action → Indicators 8, 9A.
  - [ ] **License check** (licensee or REUSE + SPDX OSI-approval lookup) → Indicator 2.
  - [ ] **gitleaks** (already wired) + optionally trufflehog → Indicator 9A.
  - [ ] **GitHub Community Profile API** → Indicators 3, 5 (cheap file-presence replacement).
  - [ ] *(optional)* CHAOSS/GrimoireLab community-health metrics for tier gating.
- [ ] Produce an **indicator-by-indicator gap report** (per repo): met / unmet + evidence links + remediation pointer to the [UNICEF Accelerator Guide](https://unicef.github.io/publicgoods-accelerator-guide/).
- [ ] Wire the assessment into a GitHub Action that comments the gap report on PRs (extend existing `repoHygieneCheck.yml`).

## Phase 4 — Bridge to DPG submission (closes Gap E)
- [ ] At Tier 4, **generate a pre-filled DPG nominee JSON** validated against `nominee-schema.json`.
- [ ] Output a "ready to nominate" summary linking to <https://app.digitalpublicgoods.net>.
- [ ] *(optional)* Cross-check the project against the **DPG API** to detect existing/duplicate registry entries.

## Phase 5 — Interoperate & contribute back
- [ ] Align pillar/tier vocabulary with the DPGA [7-pillar maturity tool](https://maturity.digitalpublicgoods.net/) so output is comparable.
- [ ] Consider upstreaming the DPG-readiness extensions to DSACMS and/or DPGA.

## Suggested sequencing
**Phase 0 → 1** first (foundation + correct model). **Phase 2 and 3 in parallel** (templates vs. automation are independent). **Phase 4** once Tiers 3–4 are defined. **Phase 5** ongoing.

## Open decisions for the maintainer
1. **Scope of "tool":** stay a CLI/cookiecutter + CI Actions, or add a hosted web assessment like the DPGA tool?
2. **Software license default** when a project hasn't chosen one (recommend Apache-2.0 or MIT).
3. **How strict is tier-gating** — advisory report vs. hard CI failure on unmet mandatory indicators?
4. **Multi-type support:** software-only, or also data/content/AI-model DPG types (changes license logic & metadata)?
