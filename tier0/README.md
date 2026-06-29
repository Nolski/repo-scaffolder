# Tier 0: Private / Prototype

## What is a Tier 0 Project?

A **Tier 0** project is an **experimental or historical** repository that is **private** and generally used by a single developer or a small group. It typically includes working projects, example scripts, or early prototypes that serve as a foundation for future work or experimentation. This type of project is not shared publicly and often remains private due to its preliminary or incomplete nature.

The main purpose of a Tier 0 project is to provide a space for initial development, exploration, and testing. These repositories generally lack formal documentation or governance structures that are typical of more mature projects.

### Key Characteristics of a Tier 0 Project:

- **Private** and often limited to individual or small team access.
- Primarily **experimental or developmental** in nature.

---

## Files for a Tier 0 Project

Although these projects are private, there are specific files that are required and recommended to include in the repository as part of the DPG readiness guidelines (see ../maturity/indicators.md).

| **File**          | **Requirement** | **Description**                                                                                                             |
| ----------------- | --------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `LICENSE`         | Mandatory       | Defines the licensing terms under which the project is distributed.                                                         |
| `README.md`       | Mandatory       | Provides an overview of the project, including its purpose, setup instructions, or any relevant notes for the developer(s). |
| `COMMUNITY.md`    | Mandatory       | Lists project team members and points of contact.                                                                           |
| `SECURITY.md`     | Recommended     | Outlines the project's security policies, including how to report security issues or vulnerabilities in the code.            |
| `CONTRIBUTING.md` | Recommended     | Guidelines for contributing, useful if the project is later opened to collaborators or transitioned to a public repository. |

For more information about sections and content within the files above, please visit [maturity-model-tiers.md](https://github.com/UNDP/repo-scaffolder/blob/main/maturity-model-tiers.md).

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
