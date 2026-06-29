# The DPG Standard & the DPGA Process

> Reference brief for the DPG-readiness tool. Indicator wording is from the canonical machine-readable standard ([`DPGAlliance/DPG-Standard`](https://github.com/DPGAlliance/DPG-Standard), `standard.md` / `standard-questions.md`), cross-checked against [digitalpublicgoods.net/standard](https://www.digitalpublicgoods.net/standard).
> **Version note:** the GitHub `master` `standard.md` self-reports v1.1.4; the published page reports current v1.1.6. Indicator wording is stable across these — **pin to the latest tagged version** when building.

## What a DPG is

> *"Open source software, open data, open AI models, open standards and open content that adhere to privacy and other applicable laws and best practices, do no harm, and help attain the SDGs."*

The Standard is authored/maintained by the **Digital Public Goods Alliance (DPGA)** (Secretariat co-hosted by UNICEF, UNDP, Norad), developed openly on GitHub under **CC-BY-SA-4.0**.

## The 9 indicators (requirement + evidence to capture)

The single most reusable artifact for our tool is **`standard-questions.md`** — it is the operational questionnaire behind every indicator. Use it verbatim as our assessment checklist.

| # | Indicator (official name) | Requirement (summary) | Evidence the project must provide |
|---|---|---|---|
| 1 | **Relevance to SDGs** | Must demonstrate relevance to advancing the SDGs. **Gating criterion.** | Which SDG(s); 1–2 sentence link to specific SDG *targets* for each. |
| 2 | **Use of Approved Open Licenses** | Must use an approved open license. | Which license(s) + public link to the license file (SPDX ID). See approved lists below. |
| 3 | **Clear Ownership** | Ownership of produced assets must be clearly defined and documented. | Owner identity & org type, country of legal establishment, copyright/trademark/ToS links; if not sole owner, proof of redistribution rights. |
| 4 | **Platform Independence** | If mandatory closed dependencies add restrictions beyond the license, must prove independence or name functional open alternatives. | Core technologies; declare closed deps; name open alternatives swappable without significant changes. |
| 5 | **Documentation** | Must document source code, use cases, and/or functional requirements. | Links to dev docs, architecture, user guides, data dictionaries, or AI model cards. |
| 6 | **Mechanism for Extracting Data** (non-PII) | Non-PII data/content must be exportable/importable in a non-proprietary format. | Whether non-PII data is used; description of CSV/XML/JSON export or API. |
| 7 | **Adherence to Privacy & Applicable Laws** | Must comply with privacy and other applicable laws. | Relevant laws (GDPR, accessibility acts, regional privacy law) + links proving adherence (privacy policy, ToS). *Strengthened by the 2024 Enhanced Privacy Framework.* |
| 8 | **Adherence to Standards & Best Practices** | Must align with relevant standards, best practices, and/or principles. | Open standards adhered to (+ validators); best practices/principles followed (e.g. [Principles for Digital Development](https://digitalprinciples.org/)). |
| 9 | **Do No Harm by Design** | Must anticipate, prevent, and do no harm by design. Three mandatory sub-indicators below. | — |
| 9A | — Data Privacy & Security | If PII is collected/stored/distributed, demonstrate privacy, security, integrity + adverse-impact prevention. | PII types; how privacy/security/integrity ensured. |
| 9B | — Inappropriate & Illegal Content | If content is collected/stored/distributed, must have policies identifying inappropriate/illegal content (incl. **CSAM**) + detection/moderation/reporting/removal processes. | Content types; identification policy; moderation processes & response times. |
| 9C | — Protection from Harassment | If users interact, must have a process to protect against grief/abuse/harassment + systems for underage-user safety. | Code of conduct; protective processes; underage-user safety measures. |

## Enhanced Privacy Framework (2024) — strengthens Indicators 7 & 9A

Six **mandatory** sub-requirements (designed to capture the essence of a DPIA via an accessible question set):
1. **Minimize PII** — is this the minimum PII required to function?
2. **Robust user consent** — how is PII collection communicated to the user?
3. **Transparency in data usage** — provide privacy policy / consent docs; where is PII processed and what can access it?
4. **Privacy-by-design** — are there mechanisms to delete PII?
5. **Data-retention transparency** — retention/deletion posture.
6. **Data governance & access controls** — access-control over PII.

Source PDF: <https://www.digitalpublicgoods.net/dpg-privacy-report> (CC-BY 4.0).

## Approved open licenses (Indicator 2)

Authoritative list: `help-center/licenses.md` in [`publicgoods-candidates`](https://github.com/DPGAlliance/publicgoods-candidates) (The Unlicense / public domain — freely reusable). All referenced by **SPDX ID**.

- **Software:** **OSI-approved licenses only** (~97 SPDX ids) — e.g. `MIT`, `Apache-2.0`, `BSD-3-Clause`, `ISC`, `GPL-3.0`, `AGPL-3.0`, `LGPL-3.0`, `MPL-2.0`, `EPL-2.0`, `EUPL-1.2`. Authority: opensource.org.
- **Content:** **Creative Commons required** — `CC-BY-4.0`, `CC-BY-SA-4.0`, `CC0-1.0` encouraged (+ NC variants, IGO variants).
- **Data:** **Open Definition–conformant** — `CC-BY-4.0`, `CC-BY-SA-4.0`, `CC0-1.0`, `ODbL-1.0`, `ODC-By-1.0`, `PDDL-1.0`, IGO variants.
- **AI models:** not separately enumerated — licensed via the buckets above (code → OSI, weights/data → data/content).
- **Open hardware:** not currently a recognized DPG type — treat as out of scope.

> **Implication for this tool:** our current CC0-for-everything default is *wrong for software*. We must add an OSI-license chooser for software components.

## Submission & review process

1. **Pre-screen** with the DPGA self-assessment / maturity tool (<https://maturity.digitalpublicgoods.net/>).
2. **Apply** via the web app **<https://app.digitalpublicgoods.net>** — only an authorized representative of the solution owner; submitted content is made public; each application gets a unique ID. *(Legacy GitHub-PR flow via `publicgoods-candidates` was archived Aug 2024.)*
3. **Review** against the Standard version current at submission: Internal (L1) → External (L2) → Expert reviewers; Community reviewers advise only. **Binary outcome: "DPG" or "Ineligible."** Final call by the Secretariat's Technical Coordinator. Target ~30 days.
4. **After approval:** listed on the public **DPG Registry** + exposed via the **DPG API**; access to the Global DPG Product Community. **Status valid 1 year → annual re-verification;** non-compliant DPGs are archived.

## Data model (reusable)

`nominee-schema.json` in `publicgoods-candidates` (Unlicense) — the DPG data model our tool should target as output:
- **Required:** `name`, `description`, `license[]` (SPDX id + URL), `organizations` (owners/maintainers/funders/implementers), `SDGs` (which of 1–17 + evidence URLs), `type` (software | data | content | standard | AI model), `stage` (nominee | DPG | archive).
- **Optional:** `aliases`, `website`, `sectors` (controlled list), `repositories` (name + URL).

## UN policy lineage (legitimacy citations)

- **2019** — UN SG High-level Panel on Digital Cooperation, Rec. 1B (platform for DPGs tied to SDGs).
- **June 2020** — SG's *Roadmap for Digital Cooperation* (A/74/821) — adopts the DPG concept & definition.
- **2019–2020** — DPGA founded (UNICEF, Norway/Norad, Sierra Leone/DSTI, iSPIRT).
- **2021** — **UNDP joins DPGA** as Secretariat co-host + Board member.
- **Sept 2024** — **Global Digital Compact** (Annex I, Pact for the Future) — Member-State-adopted DPG/DPI commitments through 2030.

> Flagged uncertainties: default branch may be `master` or `main` for raw-file links; `submission-guide` URL and exact `dpg-review-policy.md` filename not byte-verified; current Standard version (v1.1.4 in repo vs v1.1.6 published).
