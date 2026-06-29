# Tier 2: Maintained & Mission-Aligned

## What is a Tier 2 Project?

A **Tier 2** project is a **collaborative effort** that typically occurs within a team or operational division (OpDiv). The project follows an **innersource working style**, where internal teams collaborate using open source best practices but within the confines of a private or internal environment. The project is not meant for broad public contribution but rather for **internal collaboration**.

Innersource projects often allow different teams within the same organization to contribute, fostering collaboration and code-sharing internally while maintaining control over external access.

### Key Characteristics of a Tier 2 Project:

- Focuses on **collaborating within a smaller team** or internal group.
- Utilizes **innersource practices**, where internal teams work collaboratively on code, borrowing from open source workflows but keeping the work within the organization.
- Projects may be shared among internal stakeholders or divisions.
- **Not necessarily accepting contributions** from the broader community.

---

## Files for a Tier 2 Project

There are specific files that are required and recommended to include in the repository as part of the DPG readiness guidelines (see ../maturity/indicators.md).

| **File**             | **Requirement** | **Description**                                                                                                                                          |
| -------------------- | --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `LICENSE`            | Mandatory       | Defines the licensing terms under which the project is distributed.                                                                                      |
| `code.json`          | Mandatory       | Contains project metadata aligned to the DPG nominee schema (see ../maturity/nominee-schema.json).                                                                                             |
| `README.md`          | Mandatory       | Provides a comprehensive overview of the project, including its purpose, how to install or use it, and any relevant information for users or developers. |
| `COMMUNITY.md`       | Mandatory       | Lists project team members and points of contact.                                                                                                        |
| `SECURITY.md`        | Mandatory       | Outlines the project's security policies, including how to report security issues or vulnerabilities in the code.                                         |
| `CONTRIBUTING.md`    | Mandatory       | Offers guidelines for contributing to the project, including code standards, how to submit issues, and creating pull requests.                           |
| `CODE_OF_CONDUCT.md` | Mandatory       | Establishes guidelines for professional and respectful behavior to foster a collaborative environment.                                                   |

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
