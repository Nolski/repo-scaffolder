# repo-scaffolder — DPG Readiness & Compliance Tool

Assess any repository's maturity against the **[Digital Public Goods (DPG) Standard](https://www.digitalpublicgoods.net/standard)** and guide it toward becoming a fully DPG-ready open-source project.

## About the Project

This tool helps open-source projects progress from an early-stage repository to a **Digital Public Good** — open-source software, data, content, AI models, or standards that adhere to privacy and applicable laws, do no harm, and help attain the Sustainable Development Goals (SDGs).

It does three things:

1. **Assess** — audit a repository against the DPG Standard's 9 indicators and classify its maturity tier (0–4), using open-source tooling (license, security, secrets, documentation checks).
2. **Remediate** — close the gaps that block the next tier, scaffolding the missing DPG-grade artifacts (privacy policy, governance, content-moderation policy, SDG mapping, an approved open license, and more).
3. **Scaffold** — for brand-new projects, generate a repository that starts DPG-ready at a chosen maturity tier.

The maturity model is a re-anchored version of the [CMS/DSACMS OSPO](https://github.com/DSACMS/repo-scaffolder) framework this scaffolder was adapted from: instead of measuring *collaboration scope*, the tiers now measure **distance to DPG eligibility**, where **Tier 4 ≡ all 9 indicators met → eligible to nominate to the [DPG Registry](https://www.digitalpublicgoods.net/registry)**.

## How it works — Claude skills

The primary interface is a set of [Claude Code](https://claude.com/claude-code) skills (in `.claude/skills/`). When you open this repo in Claude Code, they're available automatically:

| Skill | Use it to… |
|---|---|
| **`dpg-assess`** | Audit any repo, score the 9 indicators, and get a tier classification + indicator-by-indicator gap report (`dpg-assessment.json`). |
| **`dpg-remediate`** | Close the gaps — instantiate the missing DPG artifacts, fix the license, and at Tier 4 produce a pre-filled DPG nominee package for submission. |
| **`dpg-scaffold`** | Bootstrap a brand-new repo at a chosen tier (wraps cookiecutter). |

Typical flow: **assess → remediate → re-assess**, repeating until the repo reaches Tier 4 and is ready to nominate at <https://app.digitalpublicgoods.net>.

## Repository structure

| Path | What it is |
|---|---|
| [`maturity/`](./maturity) | The knowledge core: `indicators.md` (the 9 DPG indicators + how each is detected/remediated), `tier-model.md` (the tier ladder), `nominee-schema.json` (DPG output data model), `licenses.json` (approved-license allow-lists). |
| [`scripts/audit/`](./scripts/audit) | `run_audit.py` — the open-source audit engine (license, security, secrets, docs, file/section presence) that produces the evidence the skills reason over. |
| [`templates/`](./templates) | DPG-grade artifacts the remediation skill drops into a repo (PRIVACY.md, CONTENT_MODERATION.md, SDG mapping, governance, …). |
| [`tier0/`–`tier4/`](./tier0) | Cookiecutter templates for greenfield scaffolding, one per maturity tier. |
| [`.claude/skills/`](./.claude/skills) | The three DPG skills. |
| [`transition/`](./transition) | Background research and the transition assessment that shaped this tool. |
| [`maturity-model-tiers.md`](./maturity-model-tiers.md) | Human-readable overview of the tier model + file requirements per tier. |

## The 9 DPG indicators

1. Relevance to the SDGs · 2. Approved open license · 3. Clear ownership · 4. Platform independence · 5. Documentation · 6. Mechanism for extracting (non-PII) data · 7. Privacy & applicable laws · 8. Standards & best practices · 9. Do no harm by design (9A data privacy & security, 9B inappropriate/illegal content, 9C protection from harassment).

See [`maturity/indicators.md`](./maturity/indicators.md) for the full requirements, evidence, and detection logic.

`dpg-assess` also runs an **advisory [software-architecture assessment](./maturity/architecture.md)** — 12 dimensions (modularity, API-first, cloud-agnosticism, offline resilience, accessibility/i18n, security architecture, data portability, testing/CI, observability, docs, maintainability) especially relevant to **web apps** becoming DPGs. It's diagnostic only and does not change the DPG tier.

## Using the audit engine directly (no Claude required)

```bash
python3 scripts/audit/run_audit.py <path-to-repo> --type software -o audit-report.json
```

The audit uses only the Python standard library. Optional tools (`licensee`, `gitleaks`, `trufflehog`, OpenSSF `scorecard`, `markdownlint`) enrich the report when installed — see [`scripts/audit/README.md`](./scripts/audit/README.md). Run it locally or through the `dpg-assess` skill; scaffolded repos additionally ship secret-scanning CI (gitleaks + trufflehog) that supports DPG Indicator 9A.

## Scaffolding a new repository

### Prerequisites

- Python 3.8+
- [cookiecutter](https://github.com/cookiecutter/cookiecutter) (`pip install -r requirements.txt`)
- [GitHub CLI](https://cli.github.com/) (`gh`) — only if you want the hook to create the repo for you

### Pick a tier

If unsure which tier fits, run the quick estimator:

```bash
python3 tier-determiner.py
```

For an evidence-based classification of an *existing* repo, use the `dpg-assess` skill instead.

### Generate

```bash
cookiecutter . --directory=tierX     # X = 0–4
```

You'll be prompted for project details and an **open license**. The license prompt is type-aware: software must use an OSI-approved license; content uses Creative Commons; data uses an Open Definition license. (Unlike the original scaffolder, software is **never** defaulted to CC0 — that is invalid for software under DPG Indicator 2.) Approved lists live in [`maturity/licenses.json`](./maturity/licenses.json).

### Update an existing project

Use `-f -s` to avoid overwriting existing files:

```bash
cookiecutter -f -s . --directory=tierX
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and our [COMMUNITY.md](COMMUNITY.md). Feedback is welcome — please file an issue on this repository.

## License

This project is licensed under the **GNU General Public License v3.0** — see [LICENSE](LICENSE). GPL-3.0 is an OSI-approved license, so this tool itself satisfies DPG Indicator 2 for software.

## Acknowledgements

This project was adapted from the [CMS/DSACMS](https://github.com/DSACMS/repo-scaffolder) Open Source Program Office's `repo-scaffolder` and re-anchored onto the [Digital Public Goods Standard](https://www.digitalpublicgoods.net/standard) maintained by the [Digital Public Goods Alliance](https://www.digitalpublicgoods.net/). We thank both communities for their work.
