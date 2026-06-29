# Master Resource List

> Consolidated index of every external resource gathered for the DPG transition. Grouped by purpose. URLs flagged `⚠` where confidence is partial — verify before hard-coding. Tooling details are in [`03-automation-tooling.md`](./03-automation-tooling.md).

## A. The DPG Standard & DPGA (authoritative)

| Resource | URL | Type / License | Why it matters |
|---|---|---|---|
| DPG Standard (page) | https://www.digitalpublicgoods.net/standard | Webpage | The 9-indicator bar the tool must implement. |
| DPG-Standard repo | https://github.com/DPGAlliance/DPG-Standard | Repo · CC-BY-SA-4.0 | `standard.md`, `standard-questions.md`, `governance.md`, `archiving.md`. Pin to latest tag. |
| `standard-questions.md` (raw) | https://raw.githubusercontent.com/DPGAlliance/DPG-Standard/master/standard-questions.md | File | **Reuse directly as the assessment checklist.** |
| `standard.md` (raw) | https://raw.githubusercontent.com/DPGAlliance/DPG-Standard/master/standard.md | File | Verbatim indicator wording. |
| publicgoods-candidates (registry source) | https://github.com/DPGAlliance/publicgoods-candidates | Repo · The Unlicense | Holds the schemas + approved-license list. ⚠ archived Aug 2024. |
| `nominee-schema.json` (raw) | https://raw.githubusercontent.com/DPGAlliance/publicgoods-candidates/main/nominee-schema.json | File | **Reuse as our output data model.** |
| `screening-schema.json` | https://github.com/DPGAlliance/publicgoods-candidates | File · Unlicense | Operationalizes the review questions. |
| Approved licenses (`help-center/licenses.md`) | https://github.com/DPGAlliance/publicgoods-candidates/blob/main/help-center/licenses.md | File · Unlicense | **Auto-validate Indicator 2** (SPDX allow-lists). |
| DPG API | https://github.com/DPGAlliance/dpg-api | Repo | Programmatic registry access for lookups/comparison. |
| DPG Registry (listing) | https://www.digitalpublicgoods.net/registry | Webpage | Post-approval destination; reference dataset. |
| DPG application web app | https://app.digitalpublicgoods.net | Hosted service | Current nomination entry point — mirror its fields. |
| Enhanced Privacy Framework (PDF) | https://www.digitalpublicgoods.net/dpg-privacy-report | PDF · CC-BY-4.0 | The 6 mandatory privacy requirements (Indicators 7 & 9A). |
| Privacy framework blog | https://www.digitalpublicgoods.net/blog/privacy-and-data-security-framework-for-dpg-standard | Blog | Plain-language summary. |
| DPGA Governance | https://www.digitalpublicgoods.net/governance | Webpage | Authority behind Standard/Registry. |
| DPG Resources / Wiki | https://github.com/DPGAlliance/dpg-resources | Repo · CC-BY-SA-4.0 (badges CC0) | Evidence requirements per indicator & per DPG type. |

## B. DPG maturity / readiness analogues

| Resource | URL | Type / License | Why it matters |
|---|---|---|---|
| DPGA Maturity / Self-Assessment Tool | https://maturity.digitalpublicgoods.net/ | Hosted tool | **Closest existing analogue** — 7 pillars → 9 indicators, radar output. Study before building. |
| dpg-maturity-indicators | https://github.com/DPGAlliance/dpg-maturity-indicators | Repo · CC0-1.0 | Reusable maturity-indicator definitions. |
| maturity-tool (code) | https://github.com/DPGAlliance/maturity-tool | Repo · ⚠ license unconfirmed | Possible code behind the maturity site; reference architecture. |
| UNICEF DPG Accelerator Guide (site) | https://unicef.github.io/publicgoods-accelerator-guide/ | Webpage | OSS→DPG pathway playbook; remediation model. |
| UNICEF Accelerator Guide (repo) | https://github.com/unicef/publicgoods-accelerator-guide | Repo · CC-BY-SA-4.0 | Open source of the above. |
| UNICEF Venture Fund | https://www.unicefventurefund.org/ | Funder / pathway | Treats DPG cert as a graduation milestone. |
| DIAL Catalog of Digital Solutions | https://dial.global/ | Catalog · ⚠ license uncertain | Aggregated DPG catalog + maturity rubric. |
| GovStack Specs | https://specs.govstack.global/ | Spec/framework | Interoperable DPI building blocks + maturity assessment. |

## C. Best-practice principles & standards

| Resource | URL | Type | Why it matters |
|---|---|---|---|
| Principles for Digital Development | https://digitalprinciples.org/ | Principles | The best-practices Indicator 8 points to (refreshed 2024). |
| Principles 2024 refresh | https://digitalprinciples.org/2024/03/29/the-principles-for-digital-development-have-been-refreshed-for-the-next-decade-heres-how/ | Blog | Explains the current 9 principles. |
| OpenChain (ISO/IEC 5230 & 18974) | https://www.openchainproject.org/ | Standards | License-compliance & security-assurance backbone. |
| SPDX License List | https://spdx.org/licenses/ | Reference | Canonical license IDs + OSI-approval flags (Indicator 2). |
| OSI approved licenses | https://opensource.org/licenses | Reference | Authority for software-license approval (Indicator 2). |
| Open Definition (data) | https://opendefinition.org/ | Reference | Authority for open-data licenses (Indicator 2). |

## D. UN / policy context (legitimacy citations)

| Resource | URL | Type | Why it matters |
|---|---|---|---|
| SG's Roadmap for Digital Cooperation | https://www.un.org/en/content/digital-cooperation-roadmap/ | UN webpage | Endorsed DPGs & supplied the definition. |
| Roadmap full report (A/74/821) | https://www.un.org/en/content/digital-cooperation-roadmap/assets/pdf/Roadmap_for_Digital_Cooperation_EN.pdf | UN PDF ⚠ | Primary source; canonical DPG definition. |
| Global Digital Compact (Annex I) | https://www.un.org/pact-for-the-future/en/annex-i-global-digital-compact | UN webpage | Member-State-adopted DPG/DPI commitments (2024). |
| UNDP joins the DPGA | https://www.undp.org/news/undp-joins-digital-public-goods-alliance-accelerate-inclusive-digital-transformation | UNDP news ⚠ (403 to bots) | Documents UNDP's 2021 role. |
| UN SDGs platform | https://sdgs.un.org/ | UN webpage | The 17 SDGs Indicator 1 maps against. |
| UN SDG Goals list | https://sdgs.un.org/goals | UN webpage | Controlled vocabulary for SDG tagging. |

## E. Automation tooling (summary — see `03-automation-tooling.md` for full matrix)

| Tool | URL | License | Maps to |
|---|---|---|---|
| OpenSSF Scorecard | https://github.com/ossf/scorecard | Apache-2.0 | 8, 9A |
| OpenSSF Best Practices Badge | https://www.bestpractices.dev/ | MIT (app) | 8 |
| licensee | https://github.com/licensee/licensee | MIT | 2 |
| REUSE tool | https://reuse.software/ | Apache-2.0/GPL | 2 |
| ScanCode Toolkit | https://github.com/aboutcode-org/scancode-toolkit | Apache-2.0 | 2 |
| gitleaks | https://github.com/gitleaks/gitleaks | MIT | 9A |
| trufflehog | https://github.com/trufflesecurity/trufflehog | AGPL-3.0 | 9A |
| GitHub Community Profile API | https://docs.github.com/rest/repos/community | — | 3, 5 |
| CHAOSS / GrimoireLab | https://chaoss.community/ | GPL-3.0 | community health |
| repolinter (current, ⚠ archived) | https://github.com/todogroup/repolinter | Apache-2.0 | 2, 5 (legacy) |

## F. Upstream / origin (context)

| Resource | URL | Notes |
|---|---|---|
| DSACMS/repo-scaffolder (upstream) | https://github.com/DSACMS/repo-scaffolder | The fork origin (CC0). |
| CMS OSPO Guide | https://dsacms.github.io/ospo-guide/ | Policy behind the model. |
| OMB M-16-21 Federal Source Code Policy | https://obamawhitehouse.archives.gov/sites/default/files/omb/memoranda/2016/m_16_21.pdf | Founding US OSS mandate; `code.json` lineage. |

> **Top reusable artifacts:** `standard-questions.md` (checklist), `nominee-schema.json` + `screening-schema.json` (data model), `help-center/licenses.md` (Indicator-2 allow-lists), `dpg-maturity-indicators` (scoring framework). All permissively licensed.
