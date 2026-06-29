# Tier 3: Open & Safe

## What is a Tier 3 Project?

A **Tier 3** project is an **open collaboration** effort where the work is conducted in public. The project is led by smaller, semi-open teams but encourages **limited external contributions**. The work is typically **open source**, but the direction and maintenance of the project are led by the core team, controlled by a smaller group or team, rather than a large, decentralized community. Tier 3 projects may be public-facing tools, utilities, or websites, where external contributions are welcomed but managed closely by the core team.

### Key Characteristics of a Tier 3 Project:

- **Collaborative in public**, where the work is open to external stakeholders.
- Led by a **core team** (often organizational or tool-specific).
- Accepts **limited contributions from external sources**, typically following specific guidelines.
- Publicly accessible code and documentation.
- Maintenance and decision-making are generally led by the core team.

---

## Files for a Tier 3 Project

There are specific files that are required and recommended to include in the repository as part of the DPG readiness guidelines (see ../maturity/indicators.md).

| **File**             | **Requirement** | **Description**                                                                                                                                                          |
| -------------------- | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `LICENSE`            | Mandatory       | Defines the licensing terms under which the project is distributed.                                                                                                      |
| `code.json`          | Mandatory       | Contains project metadata aligned to the DPG nominee schema (see ../maturity/nominee-schema.json).                                                                                                             |
| `README.md`          | Mandatory       | Provides a comprehensive overview of the project, including its purpose, how to install or use it, and any relevant information for users or developers.                 |
| `COMMUNITY.md`       | Mandatory       | Lists project team members and points of contact with detailed roles and responsibilities.                                                                               |
| `SECURITY.md`        | Mandatory       | Outlines the project's security policies, including how to report security issues or vulnerabilities in the code.                                                         |
| `CONTRIBUTING.md`    | Mandatory       | Offers guidelines for contributing to the project, including code standards, how to submit issues, and creating pull requests.                                           |
| `CODE_OF_CONDUCT.md` | Mandatory       | Establishes guidelines for acceptable behavior within the community, setting expectations for how contributors should interact in a respectful and collaborative manner. |
| `GOVERNANCE.md`      | Recommended     | Describes the governance model of the project, such as decision-making processes and rules for contributing. It ensures a transparent process for managing the project.  |

For more information about required sections and content within the files above, please visit [maturity-model-tiers.md](https://github.com/UNDP/repo-scaffolder/blob/main/maturity-model-tiers.md).

## .github directory

The .github directory includes various files such as GitHub action workflows, code.json metadata cookiecutter creation, and issue templates. For more information, please visit the [.github-directory.md]([../docs/.github-directory.md).

## Checking DPG readiness

Repository hygiene and DPG-indicator coverage are checked by the audit engine in this
project (not repolinter, which is archived). From the scaffolder repo run:

```
python3 scripts/audit/run_audit.py <path-to-this-repo> --type software
```

For a full, evidence-based assessment scored against all 9 DPG indicators (and guidance to
close any gaps), use the `dpg-assess` and `dpg-remediate` Claude skills. See the project
[README.md](https://github.com/UNDP/repo-scaffolder#how-it-works--claude-skills) and
[`maturity/indicators.md`](https://github.com/UNDP/repo-scaffolder/blob/main/maturity/indicators.md).
