# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## About the Project

<!-- This should be a longer-form description of the project. It can include history, background, details, problem statements, links to design documents or other supporting materials, or any other information/context that a user or contributor might be interested in. -->

**{project statement}**

<!--
### Project Mission
**{project mission}**
Provide the core mission and objectives driving this project.-->

<!--
### Agency Mission
TODO: Recommended to include since this is an agency-led project
Provide the mission of the agency and how this project aligns. -->

<!--
### Team Mission
TODO: Recommended to include since this is an agency-led project
Provide the team's mission and how they work together. -->

## Core Team

A list of core team members responsible for the code and documentation in this repository can be found in [COMMUNITY.md](COMMUNITY.md).

<!--
## Repository Structure

TODO: Including the repository structure helps viewers quickly understand the project layout. Using the "tree -d" command can be a helpful way to generate this information, but, be sure to update it as the project evolves and changes over time.

**{list directories and descriptions}**

TODO: Add a 'table of contents" for your documentation. Tier 0/1 projects with simple README.md files without many sections may or may not need this, but it is still extremely helpful to provide "bookmark" or "anchor" links to specific sections of your file to be referenced in tickets, docs, or other communication channels.

**{list of .md at top directory and descriptions}**

-->

<!--
# Development and Software Delivery Lifecycle
The following guide is for members of the project team who have access to the repository as well as code contributors. The main difference between internal and external contributions is that external contributors will need to fork the project and will not be able to merge their own pull requests. For more information on contributing, see: [CONTRIBUTING.md](./CONTRIBUTING.md).
-->

<!--
## Local Development

TODO - with example below:
This project is monorepo with several apps. Please see the [api](./api/README.md) and [frontend](./frontend/README.md) READMEs for information on spinning up those projects locally. Also see the project [documentation](./documentation) for more info.
-->

<!--
## Coding Style and Linters

TODO - Add the repo's linting and code style guidelines

Each application has its own linting and testing guidelines. Lint and code tests are run on each commit, so linters and tests should be run locally before committing.
-->

<!--
## Branching Model

TODO - with example below:
This project follows [trunk-based development](https://trunkbaseddevelopment.com/), which means:

* Make small changes in [short-lived feature branches](https://trunkbaseddevelopment.com/short-lived-feature-branches/) and merge to `main` frequently.
* Be open to submitting multiple small pull requests for a single ticket (i.e. reference the same ticket across multiple pull requests).
* Treat each change you merge to `main` as immediately deployable to production. Do not merge changes that depend on subsequent changes you plan to make, even if you plan to make those changes shortly.
* Ticket any unfinished or partially finished work.
* Tests should be written for changes introduced, and adhere to the text percentage threshold determined by the project.

This project uses **continuous deployment** using [Github Actions](https://github.com/features/actions) which is configured in the [./github/workflows](.github/workflows) directory.

Pull-requests are merged to `main` and the changes are immediately deployed to the development environment. Releases are created to push changes to production.
-->

<!--
## Contributing
Thank you for considering contributing to this open source project! For more information about our contribution guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).
-->

<!--
## Community
The {{ cookiecutter.project_name }} team is taking a community-first and open source approach to the product development of this tool. We believe software in the public interest should be made in the open and be built and licensed such that anyone can download the code, run it themselves without paying money to third parties or using proprietary software, and use it as they will.

We know that we can learn from a wide variety of communities, including those who will use or will be impacted by the tool, who are experts in technology, or who have experience with similar technologies deployed in other spaces. We are dedicated to creating forums for continuous conversation and feedback to help shape the design and development of the tool.

We also recognize capacity building as a key part of involving a diverse open source community. We are doing our best to use accessible language, provide technical and process documents, and offer support to community members with a wide variety of backgrounds and skillsets.
-->

<!--
### Community Guidelines
Principles and guidelines for participating in our open source community are can be found in [COMMUNITY.md](COMMUNITY.md). Please read them before joining or starting a conversation in this repo or one of the channels listed below. All community members and participants are expected to adhere to the community guidelines and code of conduct when participating in community spaces including: code repositories, communication channels and venues, and events.
-->

<!--
## Feedback
If you have ideas for how we can improve or add to our capacity building efforts and methods for welcoming people into our community, please let us know at **{contact email}**. If you would like to comment on the tool itself, please let us know by filing an **issue on our GitHub repository.**
-->

<!--
## Glossary
Information about terminology and acronyms used in this documentation may be found in [GLOSSARY.md](GLOSSARY.md).
-->

<!--
DPG Standard Indicator 1 (Relevance to the SDGs) — gating for DPG eligibility.
Becomes mandatory at Tier 2; including it early is encouraged. Be specific about the
target (e.g. 4.1, 3.8, 16.6), not just the goal number.
-->

## Relevance to the Sustainable Development Goals

{{ cookiecutter.project_name }} advances the following UN Sustainable Development Goals:

| SDG | How this project contributes (link to a specific target) | Evidence |
|-----|----------------------------------------------------------|----------|
| SDG _N_ — _Goal name_ | _1–2 sentences linking to a specific target, e.g. "supports Target 3.8 (universal health coverage) by …"_ | _link to docs / deployment / impact_ |

## Ownership & Governance

<!-- DPG Standard Indicator 3 (Clear Ownership). State who owns this project. -->

- **Owner:** {{ cookiecutter.project_org }} _(organization or individual; state the type: government, non-profit, company, foundation, individual)_
- **Maintainers:** see [COMMUNITY.md](COMMUNITY.md).
- **Copyright / trademark / terms:** _link as applicable._

## Policies

### Security and Responsible Disclosure Policy

We support responsible disclosure of security vulnerabilities. Please report issues
privately — see [SECURITY.md](SECURITY.md) for how to report and our disclosure window.

### Supply-chain security

We aim to keep dependencies up to date and to make dependency / Software Bill of Materials
(SBOM) information available. Automated dependency and secret scanning run in CI; see the
workflows under `.github/`.

### Accessibility

Where this project has a user interface, we aim to meet [WCAG 2.1 AA](https://www.w3.org/TR/WCAG21/).

## License

This project is released under the license declared in [LICENSE](LICENSE). Choose an
approved open license appropriate to your project type — an [OSI-approved](https://opensource.org/licenses)
license for software; a Creative Commons or [Open Definition](https://opendefinition.org/)
license for content or data. (Do not apply CC0 to software; CC0 is appropriate for data
and content only.)

By submitting a contribution, you agree it is released under this project's license.
