# Tier 1: Public Release

## What is a Tier 1 Project?

A **Tier 1** project refers to an **informational or historical** project that has been **released publicly**. However, it does **not** have planned future updates or maintenance by the original authors or contributors. These projects typically include code samples, prototypes, public documentation, or other types of resources that are made available for use but won't receive ongoing updates or active development.

The main purpose of a Tier 1 project is to share knowledge and provide information from past work. Though available for public consumption, the project is **not expected to evolve or expand** in the future. Contributors may not engage in continuous development or issue resolution.

### Key Characteristics of a Tier 1 Project:

- **Publicly released** without planned future development or maintenance.
- Primarily **informational or historical** in nature.
- May still provide value to the community, but it is not actively worked on.

---

## Files for a Tier 1 Project

There are specific files that are required and recommended to include in the repository as part of the DPG readiness guidelines (see ../maturity/indicators.md).

| **File**          | **Requirement** | **Description**                                                                                                                                          |
| ----------------- | --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `LICENSE`         | Mandatory       | Defines the licensing terms under which the project is distributed.                                                                                      |
| `code.json`       | Mandatory       | Contains project metadata aligned to the DPG nominee schema (see ../maturity/nominee-schema.json).                                                                                             |
| `README.md`       | Mandatory       | Provides a comprehensive overview of the project, including its purpose, how to install or use it, and any relevant information for users or developers. |
| `COMMUNITY.md`    | Mandatory       | Lists project team members and points of contact.                                                                                                        |
| `SECURITY.md`     | Mandatory       | Outlines the project's security policies, including how to report security issues or vulnerabilities in the code.                                         |
| `CONTRIBUTING.md` | Recommended     | Offers guidelines for contributing to the project, including code standards, how to submit issues, and creating pull requests.                           |

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
