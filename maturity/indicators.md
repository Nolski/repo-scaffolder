# DPG Standard Indicators — Assessment & Remediation Spec

> The knowledge core read by the `dpg-assess` and `dpg-remediate` skills. Each indicator lists: **what it requires**, **evidence** a project must show, **how to detect/verify it** (which audit signal or manual judgment), and the **remediation** artifact to apply when it's unmet.
>
> Source of truth: the [DPG Standard](https://www.digitalpublicgoods.net/standard) v1.1.x ([`DPGAlliance/DPG-Standard`](https://github.com/DPGAlliance/DPG-Standard), CC-BY-SA-4.0). See `transition/01-dpg-standard.md` for the full reference. Detection signals come from `scripts/audit/run_audit.py` (`audit-report.json`); license allow-lists from `licenses.json`; output model is `nominee-schema.json`.

## How to read the `detect` column

- **auto** = decided by an audit-report signal (tool output). The skill trusts the tool but cites the evidence.
- **judgment** = the skill must read the repo and reason (tools cannot score it).
- **hybrid** = tool narrows it down; skill confirms.

A status for each indicator is one of `met` / `partial` / `unmet` / `not-applicable`, always with an evidence link (file path, URL, or audit finding id).

---

## 1. Relevance to the SDGs  *(gating — no SDG relevance ⇒ not a DPG)*
- **Requires:** demonstrated relevance to advancing one or more of the 17 SDGs.
- **Evidence:** which SDG(s); 1–2 sentence link to specific SDG *targets* for each.
- **detect:** judgment. The audit reports whether a README "SDG"/"Sustainable Development" section exists, but the *relevance claim* is Claude's call from the project's purpose.
- **remediate:** add the SDG-mapping README section (`templates/SDG_MAPPING.md`); populate `SDGs[]` in the nominee package.

## 2. Use of an Approved Open License
- **Requires:** an approved open license — OSI (software) / Creative Commons (content) / Open Definition (data).
- **Evidence:** SPDX id + public link to the license file.
- **detect:** auto. `audit-report.json.license` = detected SPDX id (via `licensee`/`reuse`), checked against `licenses.json` for the project `type`. **Flag the CC0-on-software anti-pattern explicitly** (valid for data/content, invalid for software).
- **remediate:** run the license chooser (prompt by type: code/content/data) and write the correct `LICENSE`; never default software to CC0.

## 3. Clear Ownership
- **Requires:** ownership of produced assets clearly defined and documented.
- **Evidence:** owner identity & org type, copyright/trademark/ToS links; redistribution rights if not sole owner.
- **detect:** hybrid. Audit checks for ownership statements in README/GOVERNANCE/LICENSE headers + CODEOWNERS; skill confirms it's unambiguous.
- **remediate:** add ownership statement to README + expand `GOVERNANCE.md`; populate `organizations[]` (owner/maintainer/funder/implementer).

## 4. Platform Independence
- **Requires:** if mandatory closed dependencies add restrictions beyond the license, prove independence or name functional open alternatives.
- **Evidence:** core technologies list; closed-dependency declaration; open alternatives.
- **detect:** hybrid. Audit surfaces manifests (package.json, requirements.txt, go.mod, etc.) and flags known-proprietary deps; skill judges whether lock-in exists and whether alternatives are viable.
- **remediate:** add a "Platform Independence / Dependencies" README section declaring closed deps + open alternatives.

## 5. Documentation
- **Requires:** documentation of source code, use cases, and/or functional requirements.
- **Evidence:** links to dev docs, architecture, user guides, data dictionaries, or AI model cards.
- **detect:** hybrid. Audit scores README presence + section coverage + `markdownlint` + presence of a `docs/` tree; skill judges sufficiency for the project's complexity.
- **remediate:** scaffold missing README sections (install, usage, architecture) from the tier templates.

## 6. Mechanism for Extracting Data (non-PII)
- **Requires:** non-PII data/content exportable/importable in a non-proprietary format.
- **Evidence:** export/import mechanism description (CSV/JSON/XML/API).
- **detect:** judgment (conditional — N/A if the project stores no data). Audit can hint (API specs, export endpoints) but the skill decides applicability.
- **remediate:** add a "Data Export & Portability" README/docs section (`templates/` snippet).

## 7. Adherence to Privacy & Applicable Laws
- **Requires:** designed to comply with privacy and other applicable laws (strengthened by the 2024 Enhanced Privacy Framework).
- **Evidence:** relevant laws (GDPR, accessibility acts, regional privacy law) + links proving adherence (privacy policy, ToS).
- **detect:** hybrid. Audit checks for `PRIVACY.md`/privacy policy presence; skill judges coverage of the 6 mandatory privacy questions.
- **remediate:** instantiate `templates/PRIVACY.md` (Enhanced Privacy Framework's 6 questions).

## 8. Adherence to Standards & Best Practices
- **Requires:** alignment with relevant standards, best practices, and/or principles (e.g. [Principles for Digital Development](https://digitalprinciples.org/)).
- **Evidence:** open standards adhered to (+ validators); best practices/principles followed.
- **detect:** auto + judgment. **OpenSSF Scorecard** score + **OpenSSF Best Practices Badge** criteria from the audit; skill maps to Principles for Digital Development.
- **remediate:** enable Scorecard-recommended practices (branch protection, signed releases, CI, dependency review); add a "Standards & Best Practices" section.

## 9. Do No Harm by Design
Three mandatory sub-indicators — treat as a **distinct gate**, not a checklist line.

### 9A. Data Privacy & Security
- **Requires:** if PII is collected/stored/distributed, demonstrate privacy, security, integrity + adverse-impact prevention.
- **detect:** auto + judgment. `gitleaks`/`trufflehog` findings (leaked secrets/PII), Scorecard security checks; skill judges PII handling posture.
- **remediate:** `templates/PRIVACY.md` data-security section; remediate any leaked secrets; document PII handling.

### 9B. Inappropriate & Illegal Content
- **Requires:** if content is collected/stored/distributed, policies identifying inappropriate/illegal content (incl. **CSAM**) + detection/moderation/reporting/removal processes.
- **detect:** judgment (conditional — N/A if no user content).
- **remediate:** instantiate `templates/CONTENT_MODERATION.md`.

### 9C. Protection from Harassment
- **Requires:** if users interact, a process to protect against grief/abuse/harassment + underage-user safety systems.
- **detect:** hybrid. Audit checks for `CODE_OF_CONDUCT.md`; skill judges harassment-protection + underage-safety coverage.
- **remediate:** extend `CODE_OF_CONDUCT.md` with harassment-protection + underage-safety subsections.

---

## Audit-report → indicator map (quick reference)

| audit-report key | feeds indicator(s) |
|---|---|
| `license` (SPDX + approved?) | 2 |
| `scorecard` (checks, score) | 8, 9A |
| `secrets` (gitleaks/trufflehog) | 9A |
| `files` (presence: README, LICENSE, PRIVACY, CODE_OF_CONDUCT, GOVERNANCE, CONTRIBUTING, SECURITY) | 3, 5, 7, 9C |
| `sections` (README/CONTRIBUTING section coverage) | 1, 5, 6 |
| `docs` (markdownlint, docs/ tree) | 5 |
| `dependencies` (manifests, proprietary flags) | 4 |

Indicators **1, 6, 9B** are primarily **judgment/conditional** — the audit only hints; the skill decides.

## Architecture lens (advisory)

Beyond the binary indicators, `dpg-assess` runs an **advisory software-architecture assessment** (see [`architecture.md`](./architecture.md)) — 12 dimensions clustering under indicators **4, 5, 6, 8, 9A**. It does **not** change the tier or any indicator status; it explains *why* an indicator is strong/fragile (e.g. cloud lock-in behind a partial Indicator 4) and surfaces risks the binary checks miss (no offline support, no API spec, weak observability). Signals come from `audit-report.json.checks.architecture`.
