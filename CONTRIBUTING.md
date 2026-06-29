# How to Contribute

We're so thankful you're considering contributing to this open source project! If
you're unsure about anything, just ask -- or submit the issue or pull request
anyway. The worst that can happen is you'll be politely asked to change something.
We appreciate all friendly contributions.

We encourage you to read this project's CONTRIBUTING policy (you are here), its
[LICENSE](LICENSE), and its [README](README.md).

## Getting Started

First, install the required dependencies.

To create a new repository using repo-scaffolder, run the production version of repo-scaffolder. Subsitute `X` with the tier number you'd like to create in the directory flag.

```
cookiecutter https://github.com/UNDP/repo-scaffolder --directory=tierX
```

More commands on using repo-scaffolder for repository creation and maintenance can be found here: https://github.com/UNDP/repo-scaffolder/blob/main/README.md#Using-repo-scaffolder

### Team Specific Guidelines

- Please try to keep pull requests to a reasonable size; try to split large contributions to multiple PRs
- Please create pull requests into dev unless the contribution is some kind of bugfix or urgent hotfix.
- Document and explain the contribution clearly according to provided standards when possible.
- Feel free to reach out to us if there is any confusion. A list of the project maintainers is found here: [COMMUNITY.md](./COMMUNITY.md)

### Building dependencies

1. Clone the repo

   `git clone https://github.com/UNDP/repo-scaffolder.git`

2. Install the required packages in requirements.txt

   `pip install -r requirements.txt`

### Building the Project

N/A

### Workflow and Branching

We follow the [GitHub Flow Workflow](https://guides.github.com/introduction/flow/)

1.  Fork the project
2.  Check out the `main` branch
3.  Create a feature branch
4.  Write code and tests for your change
5.  From your branch, make a pull request against the upstream `main` branch
6.  Work with repo maintainers to get your change reviewed
7.  Wait for your change to be pulled into the upstream `main` branch
8.  Delete your feature branch

### Testing Conventions

<!--- TODO: Currently, does not have tests. Write tests then discuss where tests can be found, how they are run, and what kind of tests/coverage strategy and goals the project has. -->

### Coding Style and Linters

<!-- TODO - Add the repo's linting and code style guidelines -->

Each application has its own linting and testing guidelines. Lint and code tests are run on each commit, so linters and tests should be run locally before commiting.

### Writing Issues

When creating an issue please try to adhere to the following format:

    module-name: One line summary of the issue (less than 72 characters)

    ### Expected behavior

    As concisely as possible, describe the expected behavior.

    ### Actual behavior

    As concisely as possible, describe the observed behavior.

    ### Steps to reproduce the behavior

    List all relevant steps to reproduce the observed behavior.

    see our .github/ISSUE_TEMPLATE.md for more examples.

### Writing Pull Requests

Comments should be formatted to a width no greater than 80 columns.

Files should be exempt of trailing spaces.

We adhere to a specific format for commit messages. Please write your commit
messages along these guidelines. Please keep the line width no greater than 80
columns (You can use `fmt -n -p -w 80` to accomplish this).

    module-name: One line description of your change (less than 72 characters)

    Problem

    Explain the context and why you're making that change.  What is the problem
    you're trying to solve? In some cases there is not a problem and this can be
    thought of being the motivation for your change.

    Solution

    Describe the modifications you've done.

    Result

    What will change as a result of your pull request? Note that sometimes this
    section is unnecessary because it is self-explanatory based on the solution.

    Some important notes regarding the summary line:

    * Describe what was done; not the result
    * Use the active voice
    * Use the present tense
    * Capitalize properly
    * Do not end in a period — this is a title/subject
    * Prefix the subject with its scope

## Reviewing Pull Requests

When you submit a pull request on GitHub, it will be reviewed by the project
community, and once the changes are approved, your commits will be brought into
a development branch for additional testing. Once the changes are merged, they will
be pushed back to the main branch.

If the issue the pull request is addressing is particularly urgent, the pull request
will be merged directly into the main branch.

## Documentation

We also welcome improvements to the project documentation or to the existing
docs. Please file an [issue](https://github.com/UNDP/repo-scaffolder/issues).

## Policies

### Open Source Policy

This project is developed in the open and aligns with the
[Principles for Digital Development](https://digitalprinciples.org/) and the
[Digital Public Goods Standard](https://www.digitalpublicgoods.net/standard). If
you have any questions, contact the maintainers (see [COMMUNITY.md](COMMUNITY.md))
or email `opensource@undp.org`.

### Security and Responsible Disclosure Policy

If you discover a security vulnerability, please report it privately rather than
opening a public issue. Reports may be submitted anonymously, and we will
acknowledge receipt within 3 business days if you share contact information.

For full details on reporting, coordinated disclosure, and our privacy
commitments, see [SECURITY.md](SECURITY.md).

## License

This project is released under the terms of the license in the
[LICENSE](LICENSE) file. By submitting a pull request or issue, you agree that
your contributions will be licensed under those same terms.
