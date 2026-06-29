# Automated DPG-Readiness Tooling — Research & Integration Guide

> Research date: **2026-06-23**. Each tool below was verified against its official site **and** its GitHub repository. URLs flagged where confidence is partial. Release/commit dates are "latest at research time," not permanent.

## Background: what we are mapping to

This guide maps open-source tools to the **DPG Standard** (Digital Public Goods Alliance) so they can be wired into an automated DPG-readiness assessment alongside the current `cookiecutter` + `repolinter` setup.

**Canonical Standard URL:** <https://digitalpublicgoods.net/standard>

**The 9 DPG indicators** (verified, in order):

1. **Relevance to Sustainable Development Goals (SDGs)**
2. **Use of an Approved Open License** (OSI-approved for software; Open Data Commons for data; Creative Commons for content)
3. **Clear Ownership**
4. **Platform Independence**
5. **Documentation**
6. **Mechanism for Extracting Data** (non-PII)
7. **Adherence to Privacy and Applicable Laws**
8. **Adherence to Standards & Best Practices**
9. **Do No Harm by Design** — sub-divided into **9A. Data Privacy & Security**, **9B. Inappropriate & Illegal Content**, **9C. Protection from Harassment**

> Indicator-2 evidence requirement: "a public link that explicitly mentions an approved open license." SPDX IDs are the canonical way to reference licenses. Sources: [DPG Indicator 2 (UNICEF inventory)](https://unicef.github.io/inventory/dpg-indicators/2/), [DPGAlliance Open Licensing wiki](https://github.com/DPGAlliance/dpg-resources/wiki/2.-Open-Licensing).

---

## Category A — Repo hygiene / file-presence linting

### Repolinter (TODO Group) — ⚠️ now archived

- **Canonical URL (docs):** <https://todogroup.github.io/repolinter/>
- **GitHub:** <https://github.com/todogroup/repolinter>
- **License:** Apache-2.0 · **Language:** JavaScript
- **Maintenance:** **ARCHIVED / read-only since ~Feb 6, 2026.** Last release v0.12.0 (May 9, 2025). Known open npm-audit advisories will not be fixed. *Treat as legacy — pin a version and plan migration.*
- **Ruleset schema:** JSON **or** YAML. Top-level keys: `version: 2`, `axioms: {}`, `rules: {}`. Each rule has `level` (error/warning/off), `rule` (type + options), optional `where` (axiom condition), optional `fix` (remediation), and `policyInfo`/`policyUrl`.
  - **Rule types:** `file-existence`, `file-contents`, `file-hash` (more in `docs/rules.md`). The same type is reused across rules (e.g. `file-existence` powers both `README-file-exists` and `LICENSE-file-exists`).
  - **Axioms:** external programs that conditionally enable rules — e.g. `package-type`, `contributor-count` (numeric, supports `<`/`>`/`<=`/`>=` in `where`), and a `licensee` axiom that shells out to GitHub's Licensee to detect the repo license.
- **DPG fit:** File-presence/contents checks for LICENSE, README, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY/privacy docs, plus grep for required sections. Helps verify **#2, #5**, partially **#7** and **#9A**.

### Alternatives / complements

- **OpenSSF Scorecard** (see Category C) — actively maintained, CI-friendly, covers license + security-adjacent checks Repolinter handled.
- **GitHub Community Profile API** (see Category D) — cheapest file-presence check (README/LICENSE/CODE_OF_CONDUCT/CONTRIBUTING/ISSUE_TEMPLATE/PR_TEMPLATE + `health_percentage`).
- **saucelabs/check-my-repo** — <https://github.com/saucelabs/check-my-repo> — a Node/Vue UI wrapper **built on Repolinter** (so it inherits the archival risk). Maintenance not separately confirmed *(flag)*.
- **GitHub Licensee** (see Category B) — license detection standalone.

---

## Category B — License compliance & SBOM

> Indicator #2 is the primary target here. The SPDX License List (<https://spdx.org/licenses/>, which flags OSI approval) is the lookup table an automated checker should use to decide whether a detected license ID is "approved."

### REUSE Tool (FSFE)

- **URL:** <https://reuse.software/> · **GitHub:** <https://github.com/fsfe/reuse-tool>
- **License:** GPL-3.0-or-later · **Language:** Python (3.10+) · **Maintenance:** Active (implements REUSE Spec v3.3).
- **Does:** Detect/verify **per-file** SPDX license + copyright (`reuse lint`); emit SPDX BOM (`reuse spdx`). No vuln scanning.
- **DPG fit (#2):** Strong — verifies every file carries a machine-readable SPDX ID and that all referenced licenses exist in the repo.

### SPDX (standard + license list)

- **URL:** <https://spdx.dev/> · **GitHub org:** <https://github.com/spdx> · **License list:** <https://spdx.org/licenses/>
- **License:** License-list data is CC0-1.0; tooling repos vary. · **Maintenance:** Active; ISO/IEC 5962:2021; spec v3.1 RC in early 2026.
- **DPG fit (#2):** Foundational — the canonical registry of license IDs and OSI-approval flags, plus the SPDX SBOM format (supports #7/#8 supply-chain transparency).

### ScanCode Toolkit (AboutCode)

- **GitHub (canonical):** <https://github.com/aboutcode-org/scancode-toolkit> — **moved from `nexB/`; the legacy URL auto-redirects. Use the aboutcode-org path.** *(flag resolved)*
- **License:** Apache-2.0 (code), CC-BY-4.0 (license data) · **Language:** Python · **Maintenance:** Active; v32.5.0 (Jan 15, 2026).
- **Does:** Strong full-text **license detection** across the whole repo, copyrights, dependencies; **SBOM** (SPDX, CycloneDX, JSON/YAML/HTML); surfaces dependency vulns.
- **DPG fit (#2, #7/#8):** Excellent verifier — scans beyond the LICENSE file and emits SPDX IDs to check against the approved list.

### Licensee

- **GitHub:** <https://github.com/licensee/licensee> · **Site:** <https://licensee.github.io/licensee/>
- **License:** MIT · **Language:** Ruby · **Maintenance:** Active; v10.0.0 (May 5, 2026).
- **Does:** **Detect license only** (LICENSE file matched via exact/normalized/Sørensen–Dice similarity); returns SPDX key.
- **DPG fit (#2):** Lightweight and authoritative — **this is the gem GitHub uses** to power repo license detection and the Licenses API / community profile (confirmed via [GitHub Licenses REST docs](https://docs.github.com/en/rest/licenses/licenses)). Caveat: top-level LICENSE only, not dependencies.

### FOSSology

- **URL:** <https://www.fossology.org/> · **GitHub:** <https://github.com/fossology/fossology>
- **License:** GPL-2.0-only (LGPL-2.1 exception for some libs) · **Language:** PHP/C · **Maintenance:** Active; 4.7.1 (Jun 11, 2026).
- **Does:** DB-backed license/copyright/export-control clearance with web UI; one-click SPDX SBOM export. No core vuln scanning.
- **DPG fit (#2):** Heavyweight, auditable clearance — harder to run in CI than REUSE/ScanCode/licensee.

### Syft (Anchore)

- **GitHub:** <https://github.com/anchore/syft> · **License:** Apache-2.0 · **Language:** Go · **Maintenance:** Active; v1.45.1 (Jun 5, 2026).
- **Does:** **Generate SBOMs** (SPDX, CycloneDX, Syft-JSON) from images/filesystems. Records package-declared license metadata only; not authoritative license detection; no vuln scan.
- **DPG fit (#7/#8):** Supply-chain transparency; feeds Grype. Limited for #2.

### Grype (Anchore)

- **GitHub:** <https://github.com/anchore/grype> · **License:** Apache-2.0 · **Language:** Go · **Maintenance:** Active; v0.114.0 (Jun 5, 2026).
- **Does:** **Vulnerability scanning** of images/filesystems/SBOMs (consumes Syft); EPSS/KEV prioritization. No SBOM gen, no license detection.
- **DPG fit (#7/#8):** "Do No Harm" dependency vuln scanning. Not relevant to #2.

### CycloneDX vs SPDX (SBOM standards)

- **CycloneDX:** OWASP-backed. Org <https://github.com/CycloneDX>; CLI <https://github.com/CycloneDX/cyclonedx-cli> (Apache-2.0, C#, v0.32.0 May 14, 2026) — convert/merge/diff/sign, CycloneDX ↔ SPDX-JSON. Security/VEX-oriented (#7/#8).
- **SPDX SBOM:** ISO/IEC 5962:2021; richest license metadata — best for #2 evidence.
- Both are mature and interoperable; ScanCode/Syft/FOSSology emit both, so standardize on one and convert.

#### License/SBOM capability matrix

| Tool | Detect license | Generate SBOM | Scan vulns | Best DPG indicator |
|---|---|---|---|---|
| REUSE Tool | ✅ per-file SPDX | ✅ SPDX | ❌ | **#2** |
| SPDX (standard/list) | n/a (registry) | ✅ format | ❌ | **#2** |
| ScanCode Toolkit | ✅ strong | ✅ SPDX+CDX | ⚠️ deps | **#2**, #7/#8 |
| licensee | ✅ LICENSE file | ❌ | ❌ | **#2** (GitHub's engine) |
| FOSSology | ✅ strong | ✅ SPDX | ❌ | **#2** |
| Syft | ⚠️ pkg metadata | ✅ SPDX+CDX | ❌ | #7/#8 |
| Grype | ❌ | ❌ | ✅ from SBOM | #7/#8 |
| CycloneDX CLI | ❌ | ✅ convert/merge | (VEX) | #7/#8 |

---

## Category C — Open-source security & best-practices scoring

### OpenSSF Scorecard

- **URL:** <https://securityscorecards.dev> (also <https://scorecard.dev>) · **GitHub:** <https://github.com/ossf/scorecard>
- **License:** Apache-2.0 · **Language:** Go · **Maintenance:** Active; v5.5.0 (Apr 23, 2026).
- **Scores:** ~19 checks, each **0–10**, weighted into an aggregate — incl. Binary-Artifacts, Branch-Protection, CI-Tests, CII-Best-Practices, Code-Review, Contributors, Dangerous-Workflow, Dependency-Update-Tool, Fuzzing, License, Maintained, Packaging, Pinned-Dependencies, SAST, Security-Policy, Signed-Releases, Token-Permissions, Vulnerabilities, Webhooks.
- **DPG fit:** Fully automated, no human input. License/Security-Policy/Maintained/CII-Best-Practices/Code-Review → **#8**; Vulnerabilities/SAST/Dangerous-Workflow/Token-Permissions/Signed-Releases → **#9**. The natural actively-maintained replacement for Repolinter's security-adjacent rules.

### OpenSSF Best Practices Badge (formerly CII Best Practices)

- **URL (current):** <https://www.bestpractices.dev> — legacy `bestpractices.coreinfrastructure.org` (renamed 2021-12-24) *(flag: exact legacy-redirect behavior not independently verified)*.
- **GitHub:** <https://github.com/coreinfrastructure/best-practices-badge>
- **License:** MIT (criteria data CDLA-Permissive-2.0 / CC-BY-3.0+) · **Language:** Ruby · **Maintenance:** Active (through Jun 2026).
- **Scores:** Self-certification questionnaire; tiers **passing / silver / gold** (plus newer "OpenSSF Baseline"). Attainment is queryable via public API.
- **DPG fit:** Directly certifies FLOSS best practices → **#8**; security/crypto criteria → **#9**; vuln-reporting/secure-delivery → **#7**.

### SLSA (Supply-chain Levels for Software Artifacts)

- **URL:** <https://slsa.dev> · **GitHub:** <https://github.com/slsa-framework/slsa>
- **License:** Community Specification License 1.0 (no standard SPDX id — *flag*) · **Language:** HTML (spec/docs) · **Maintenance:** Active; v1.0 published, v1.2 current.
- **Levels:** Build **L0** (none) → **L1** (provenance exists) → **L2** (hosted build, signed provenance) → **L3** (hardened builds); v1.2 adds source/build-environment tracks (planned L4).
- **DPG fit:** Framework, not a scanner — assert/verify build level from provenance (SLSA verifier/generators). Supports **#8** and **#9** (authentic, untampered artifacts).

### gitleaks (also Category F)

- **GitHub:** <https://github.com/gitleaks/gitleaks> · **Site:** <https://gitleaks.io>
- **License:** MIT · **Language:** Go · **Maintenance:** **Feature-complete / security-patches only**; v8.30.1 (Mar 21, 2026); successor "Betterleaks" planned.
- **Does:** Secret detection (regex + entropy) over git history, files, stdin; JSON/CSV/JUnit/SARIF.
- **DPG fit:** **#7** (credential exposure = privacy risk) and **#9** (Do No Harm). Already used by this repo.

### Trivy (Aqua Security)

- **URL:** <https://trivy.dev> · **GitHub:** <https://github.com/aquasecurity/trivy>
- **License:** Apache-2.0 · **Language:** Go · **Maintenance:** Very active; v0.71.2 (Jun 19, 2026).
- **Does:** Vulns/CVEs (OS + language deps), IaC/config misconfig, secrets, license scan, SBOM gen; targets images, filesystems, remote git repos, VM images, Kubernetes.
- **DPG fit:** License + vuln → **#8**; vuln/misconfig/secret → **#9**; secrets + dep-vulns → **#7**.

---

## Category D — Community health & maturity metrics

### CHAOSS (Community Health Analytics in Open Source Software)

- **URL:** <https://chaoss.community/> · **GitHub:** <https://github.com/chaoss> · metrics <https://github.com/chaoss/metrics>
- **License:** per sub-repo (code MIT, content often CC-BY-4.0 — *flag, varies*) · **Maintenance:** Active (Linux Foundation project).
- **Structure:** Working groups — Common, Evolution, Risk, Value, Diversity & Inclusion — plus metrics models (bus factor, time-to-first-response, elephant/onion-factor, etc.).
- **DPG fit:** The **taxonomy** defining which health signals an automated assessor should compute (active maintenance, contributor diversity, responsiveness) — the qualitative maturity dimensions DPGA reviewers judge.

### Augur (CHAOSS)

- **URL:** <https://oss-augur.readthedocs.io/> · **GitHub:** <https://github.com/chaoss/augur>
- **License:** MIT · **Language:** Python (successor "Aveloxis" is Go) · **Maintenance:** Active but transitioning — as of Apr 15, 2026 maintainers recommend **Aveloxis** for new pipelines *(flag: evaluate Aveloxis over legacy Augur)*.
- **Does:** Pulls from 30+ sources (GitHub/GitLab/commits/issues/PRs) and computes CHAOSS metrics incl. core/regular/casual contributor analysis.
- **DPG fit:** The **engine** quantifying community health / active maintenance → sustainability maturity dimension; contributor concentration risk informs #7 review.

### GrimoireLab (CHAOSS)

- **URL:** <https://chaoss.github.io/grimoirelab/> · **GitHub:** <https://github.com/chaoss/grimoirelab>
- **License:** GPL-3.0 · **Language:** Shell/Python/Docker · **Maintenance:** Active; v1.21.0 (Jun 19, 2026).
- **Does:** End-to-end analytics (retrieve → store → enrich → visualize) across many sources; dashboards for activity/responsiveness/maintenance.
- **DPG fit:** Same indicators as Augur. **GPL-3.0** matters if embedding into a SaaS assessor.

### GitHub Community Profile API

- **Endpoint:** `GET /repos/{owner}/{repo}/community/profile` · **Docs:** <https://docs.github.com/en/rest/metrics/community>
- **License:** N/A (GitHub-hosted) · **Maintenance:** N/A.
- **Reports:** `health_percentage` + detection of six files (README, LICENSE, CODE_OF_CONDUCT, CONTRIBUTING, ISSUE_TEMPLATE, PULL_REQUEST_TEMPLATE), plus `description`/`documentation`. Non-fork repos only.
- **DPG fit:** Cheapest direct check — **#2** (LICENSE), **#5/#8** (README/CONTRIBUTING), governance signals. `health_percentage` is a direct numeric tier input.

### OpenSSF Criticality Score

- **URL/GitHub:** <https://github.com/ossf/criticality_score>
- **License:** Apache-2.0 · **Language:** Go · **Maintenance:** Beta; latest tagged release v2.0.4 (Apr 30, 2024) — *flag: ~2yr-old release; verify commit recency before calling it "actively maintained"* (bulk data still published via BigQuery/GCS).
- **Does:** 0–1 criticality score from age, update/commit/release frequency, contributor count, org diversity, dependents.
- **DPG fit:** Importance/impact weighting — corroborates **#1 (SDG relevance / scale of use)** and ecosystem reach; high criticality + low health = sustainability flag.

**How D feeds a maturity/tier model:** Tier 0 = Community Profile `health_percentage` threshold (does LICENSE/README/CONTRIBUTING even exist?); Tier 1+ = CHAOSS-defined activity/diversity metrics from Augur/Aveloxis/GrimoireLab crossing thresholds; Criticality Score weights scrutiny and contextualizes sustainability risk.

---

## Category E — Documentation quality / readability

### markdownlint

- **GitHub:** <https://github.com/DavidAnson/markdownlint> · CLI <https://github.com/igorshubovych/markdownlint-cli> · cli2 <https://github.com/DavidAnson/markdownlint-cli2>
- **License:** MIT · **Language:** JavaScript/TypeScript · **Maintenance:** Active *(no GitHub Releases — versions on npm/tags; check npm for latest)*.
- **Does:** 60+ structural rules for Markdown/CommonMark (heading hierarchy, link validity, formatting).
- **DPG fit:** Automated structural documentation-quality scoring → **#5/#8**.

### Vale

- **URL:** <https://vale.sh/> · **GitHub:** <https://github.com/errata-ai/vale>
- **License:** MIT · **Language:** Go · **Maintenance:** Active; v3.15.1 (Jun 12, 2026); largely single-maintainer (bus-factor note).
- **Does:** Syntax-aware **prose** linter (Markdown/AsciiDoc/rST/HTML), customizable style/readability rules, skips code blocks.
- **DPG fit:** Editorial/readability bar for docs → **#5/#8** (complements markdownlint's structural checks).

### standard-readme

- **GitHub:** <https://github.com/RichardLitt/standard-readme> · presets <https://github.com/RichardLitt/standard-readme-preset>, <https://github.com/RichardLitt/generator-standard-readme>
- **License:** MIT · **Language:** JavaScript · **Maintenance:** Active *(latest version/date single-sourced — flag, verify before citing)*.
- **Does:** Canonical README section spec (Background, Install, Usage, API, Contributing, License); generator available, linter WIP.
- **DPG fit:** Check README has required sections → **#5** documentation completeness. ("awesome-readme" is a reference catalog, not a checker.)

---

## Category F — Data privacy / PII / secret scanning

### gitleaks

- **URL:** <https://gitleaks.io> · **GitHub:** <https://github.com/gitleaks/gitleaks> (moved from `zricethezav/`, auto-redirects)
- **License:** MIT · **Language:** Go · **Maintenance:** **Security-patches-only / feature-complete**; v8.30.1 (Mar 21, 2026); successor "Betterleaks."
- **Scans:** git history, working tree, stdin; regex + Shannon entropy; decodes base64/hex/percent + archives; JSON/CSV/JUnit/SARIF.
- **DPG fit:** **#9** (no leaked secrets), supports **#7**. Already in this repo. SARIF integrates into scoring.

### TruffleHog

- **URL:** <https://trufflesecurity.com/trufflehog> · **GitHub:** <https://github.com/trufflesecurity/trufflehog> (moved from `dxa4481/truffleHog`)
- **License:** **AGPL-3.0** (since v3 — *flag in any DPG license matrix*) · **Language:** Go · **Maintenance:** Very active; v3.95.6 (Jun 18, 2026).
- **Scans:** Git/GitHub/GitLab/Docker/S3/GCS/filesystems/Jenkins/Elasticsearch; 800+ detectors; **verified secret detection** (authenticates against provider to confirm a credential is live).
- **DPG fit:** High-confidence secret scanning → **#9**, supports **#7**. Verification cuts false positives. AGPL matters only if bundling/redistributing, not for using as a standalone CI scanner.

### detect-secrets (Yelp)

- **GitHub:** <https://github.com/Yelp/detect-secrets> (repo is canonical)
- **License:** Apache-2.0 · **Language:** Python · **Maintenance:** Mature/slow; v1.5.0 (May 6, 2024) — *flag: verify recent commit activity*.
- **Scans:** Working-tree files, plugin-based (regex/keyword + entropy); **baseline workflow** + pre-commit hook blocks *new* secrets (not full history scan); inline allowlisting.
- **DPG fit:** Preventive pre-commit gate; baseline file = auditable secret-hygiene evidence → **#9**. Apache-2.0 is DPG-friendly.

### Microsoft Presidio (PII in data, not code)

- **URL:** <https://microsoft.github.io/presidio/> · **GitHub:** <https://github.com/microsoft/presidio>
- **License:** MIT · **Language:** Python · **Maintenance:** Active; v2.2.362 (Mar 18, 2026).
- **Scans:** Detect/redact/anonymize **PII in unstructured/structured data** (text, images, tabular) via NLP NER + regex + checksums, multi-language. **Not** a code/secret scanner.
- **DPG fit:** **#7** and **PII dimension of #9** where a DPG ships datasets/fixtures/logs — flags personal data that shouldn't be published. Complements (does not replace) the secret scanners.

> **Division of labor for #7+#9:** secret scanners (gitleaks/trufflehog/detect-secrets) cover *credentials in code & history*; Presidio covers *PII in data/content*. A complete automated check likely needs at least one from each group.

---

## Category G — Existing "DPG checker" / open-source-maturity automated tools

### DPGA-built automation

- **DPG Standard "as code" (`screening-schema.json`):** the machine-readable questionnaire that operationalizes the Standard. Lived in **`unicef/publicgoods-candidates`** — <https://github.com/unicef/publicgoods-candidates> (Unlicense/public-domain, JS) — **ARCHIVED Aug 19, 2024**, superseded by the portal <https://app.digitalpublicgoods.net> and <https://github.com/DPGAlliance/dpg-resources>. This is the authoritative source of the assessment questions; an automated checker should map repo signals back to these schema fields/indicators.
- **DPG Standard spec repo:** <https://github.com/DPGAlliance/dpg-standard> (`standard.md`, `standard-questions.md`, `governance.md`). Standard v1.1.6, Sep 4, 2024 *(version/date from search — flag, not direct-fetched)*.
- **DPG Self-Assessment Tool ("Universal Software Maturity Self-Assessment Tool"):** <https://maturity.digitalpublicgoods.net/> — built by DPGA, UNICEF, FAO, Digital Square at PATH. Guided 3-step wizard mapping answers to the 9 indicators across 7 areas; radar-chart output. **Gated** (login via nomination portal), **no public source repo found** *(flag)*. This is the closest official "DPG checker" but it is questionnaire/self-report and not CI-pluggable.
- **`dpg-shaper`:** **NOT FOUND** in the DPGAlliance org or web search. Treat as nonexistent / unverifiable.

### UNDP-built

- This repo (`undp/repo-scaffolder`) is a **fork of `DSACMS/repo-scaffolder`**, not an original UNDP tool. Recent commits (removing USG/tier0 rules, USG contributing policies) are consistent with re-purposing a US-federal tool toward DPG/UNDP.
- **Upstream — DSACMS/repo-scaffolder:** <https://github.com/DSACMS/repo-scaffolder> · docs <https://dsacms.github.io/repo-scaffolder/>. Maintained by the **Digital Service at CMS (HHS)** with USDS. Active; v1.2.1 (Jan 28, 2026). License CC0-1.0. Implements a **0–4 tier maturity model**, ships templates + **integrated Repolinter via GitHub Actions** + **`code.json`** federal metadata. Relevant to **#3, #5, #8**.
- Other UNDP OSS context (not DPG-checkers): <https://github.com/undp/digital-development-compass> and UNDP Digital Standards (e.g. "9. Default to Open" <https://www.undp.org/digital/standards/9-default-to-Open>).

### code.json / Federal Source Code Policy / Code.gov / Repolinter lineage

- **Federal Source Code Policy:** OMB **M-16-21**, source at <https://github.com/WhiteHouse/source-code-policy>. Mandated agencies publish a public **`code.json`** inventory (the Code.gov metadata schema; schema/portal work in <https://github.com/GSA/code-gov> and <https://github.com/GSA/code-gov-web>). Reinforced by the **SHARE IT Act** (Public Law 118-187, Dec 23, 2024).
- **Code.gov status:** **Effectively decommissioned / migrated** — `https://code.gov` now 301-redirects to digital.gov (<https://digital.gov/resources/requirements-for-achieving-efficiency-transparency-and-innovation-through-reusable-and-open-source-software/>). *(Flag: live redirect confirmed; no dated formal "shutdown" press statement found — characterize as "redirected/migrated," not a formal dated shutdown.)*
- **Repolinter lineage:** Began as a US-gov / OSS-policy compliance tool, originally `codeauroraforum/repolinter` (<https://github.com/codeauroraforum/repolinter>) before moving to the TODO Group. DSACMS adopted it to enforce federal maturity-tier requirements tied to the Federal Source Code Policy / `code.json` ecosystem — the exact lineage inherited by this `undp/repo-scaffolder` fork.

---

## Master Resources / Links table

| Tool | URL | Repo | License | Maps to DPG indicator(s) | Notes |
|---|---|---|---|---|---|
| Repolinter | todogroup.github.io/repolinter | github.com/todogroup/repolinter | Apache-2.0 | #2, #5, #7, #9A | ⚠️ **Archived ~Feb 2026** — currently used here; plan migration |
| OpenSSF Scorecard | securityscorecards.dev | github.com/ossf/scorecard | Apache-2.0 | #8, #9 (#2 license check) | Active v5.5.0; best Repolinter replacement |
| saucelabs/check-my-repo | — | github.com/saucelabs/check-my-repo | (verify) | #8 | Repolinter UI wrapper; inherits archival risk |
| REUSE Tool | reuse.software | github.com/fsfe/reuse-tool | GPL-3.0-or-later | #2 | Per-file SPDX verification |
| SPDX (standard/list) | spdx.dev | github.com/spdx | CC0-1.0 (list) | #2 | OSI-approval lookup table; SBOM format |
| ScanCode Toolkit | — | github.com/aboutcode-org/scancode-toolkit | Apache-2.0 | #2, #7/#8 | Moved from nexB; strong full-repo license detection |
| Licensee | licensee.github.io/licensee | github.com/licensee/licensee | MIT | #2 | **GitHub's own license engine**; LICENSE file only |
| FOSSology | fossology.org | github.com/fossology/fossology | GPL-2.0-only | #2 | Heavyweight; SPDX export; hard to CI |
| Syft | — | github.com/anchore/syft | Apache-2.0 | #7/#8 | SBOM gen (SPDX/CycloneDX); feeds Grype |
| Grype | — | github.com/anchore/grype | Apache-2.0 | #7/#8 | Vuln scan from SBOM |
| CycloneDX CLI | cyclonedx.org | github.com/CycloneDX/cyclonedx-cli | Apache-2.0 | #7/#8 | SBOM convert/merge; security/VEX-oriented |
| OpenSSF Best Practices Badge | bestpractices.dev | github.com/coreinfrastructure/best-practices-badge | MIT | #7, #8, #9 | formerly CII; passing/silver/gold; API queryable |
| SLSA | slsa.dev | github.com/slsa-framework/slsa | Community Spec License 1.0 | #8, #9 | Framework; build levels L0–L3 |
| gitleaks | gitleaks.io | github.com/gitleaks/gitleaks | MIT | #7, #9 | **Already used here**; security-patches-only |
| Trivy | trivy.dev | github.com/aquasecurity/trivy | Apache-2.0 | #7, #8, #9 | All-in-one vuln/config/secret/license/SBOM |
| CHAOSS | chaoss.community | github.com/chaoss | MIT / CC-BY-4.0 (varies) | maturity taxonomy (#1 context) | Defines which health metrics to compute |
| Augur (→ Aveloxis) | oss-augur.readthedocs.io | github.com/chaoss/augur | MIT | maturity/active-maintenance, #7 risk | Use Aveloxis (Go) for new pipelines |
| GrimoireLab | chaoss.github.io/grimoirelab | github.com/chaoss/grimoirelab | GPL-3.0 | maturity/active-maintenance | GPL note if embedding in SaaS |
| GitHub Community Profile API | docs.github.com/en/rest/metrics/community | (GitHub API) | N/A | #2, #5, #8, governance | Cheapest file-presence + health_percentage |
| OpenSSF Criticality Score | — | github.com/ossf/criticality_score | Apache-2.0 | #1 relevance/impact weighting | ⚠️ latest release Apr 2024; verify recency |
| markdownlint | — | github.com/DavidAnson/markdownlint | MIT | #5, #8 | Structural docs lint; versions on npm |
| Vale | vale.sh | github.com/errata-ai/vale | MIT | #5, #8 | Prose/readability lint |
| standard-readme | — | github.com/RichardLitt/standard-readme | MIT | #5 | README section spec; linter WIP |
| TruffleHog | trufflesecurity.com/trufflehog | github.com/trufflesecurity/trufflehog | **AGPL-3.0** | #7, #9 | Verified secret detection; AGPL flag |
| detect-secrets | — | github.com/Yelp/detect-secrets | Apache-2.0 | #9 (#7) | Baseline + pre-commit; v1.5.0 (2024) |
| Microsoft Presidio | microsoft.github.io/presidio | github.com/microsoft/presidio | MIT | #7, #9A (PII in data) | PII in data/content, not code |
| DPG Standard (as code) | digitalpublicgoods.net/standard | github.com/DPGAlliance/dpg-standard | (see repo) | all 9 indicators | Authoritative questionnaire/spec |
| publicgoods-candidates (screening-schema) | — | github.com/unicef/publicgoods-candidates | Unlicense | all 9 indicators | ⚠️ Archived Aug 2024; the "standard as code" JSON |
| DPG Self-Assessment Tool | maturity.digitalpublicgoods.net | (no public repo found) | N/A | all 9 indicators | Gated, self-report; not CI-pluggable |
| DSACMS repo-scaffolder (upstream) | dsacms.github.io/repo-scaffolder | github.com/DSACMS/repo-scaffolder | CC0-1.0 | #3, #5, #8 | Origin of this fork; 0–4 tier model + Repolinter CI |
| Federal Source Code Policy (M-16-21) | digital.gov (migrated) | github.com/WhiteHouse/source-code-policy | (gov) | code.json lineage | Code.gov redirects to digital.gov |

### Uncertainty flags (summary)

- **Repolinter is archived (~Feb 2026)** — the most important finding; the current scaffolder depends on a deprecated linter. OpenSSF Scorecard is the actively-maintained, CI-friendly successor for security/best-practices indicators.
- `securityscorecards.dev` cited widely but not directly fetched.
- SLSA "Community Specification License 1.0" has no standard SPDX id.
- Legacy `bestpractices.coreinfrastructure.org` redirect behavior not independently verified.
- OpenSSF Criticality Score latest *release* is Apr 2024 — verify commit recency before relying on "actively maintained."
- markdownlint uses npm/tags, not GitHub Releases.
- standard-readme latest version/date is single-sourced.
- DPG Standard v1.1.6 (Sep 4, 2024) from search, not direct-fetched.
- DPG Self-Assessment Tool has **no** public source repo found.
- `dpg-shaper` **does not appear to exist** — not found in the DPGAlliance org or via search.
- Code.gov: live redirect to digital.gov confirmed, but no dated formal shutdown announcement found.
- CHAOSS license varies per sub-repo (code MIT, content CC-BY-4.0) — confirm against the specific repo you consume.
- TruffleHog is **AGPL-3.0** — flag in any DPG license-compatibility matrix.
