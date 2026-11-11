# Contributing Guidelines

Thank you for your interest in contributing to our project. Whether it's a bug report, new feature, correction, or additional
documentation, we greatly value feedback and contributions from our community.

Please read through this document before submitting any issues or pull requests to ensure we have all the necessary
information to effectively respond to your bug report or contribution.


## Reporting Bugs/Feature Requests

We welcome you to use the GitHub issue tracker to report bugs or suggest features.

When filing an issue, please check existing open, or recently closed, issues to make sure somebody else hasn't already
reported the issue. Please try to include as much information as you can. Details like these are incredibly useful:

* A reproducible test case or series of steps
* The version of our code being used
* Any modifications you've made relevant to the bug
* Anything unusual about your environment or deployment


## Contributing via Pull Requests
Contributions via pull requests are much appreciated. Before sending us a pull request, please ensure that:

1. You are working against the latest source on the *main* branch.
2. You check existing open, and recently merged, pull requests to make sure someone else hasn't addressed the problem already.
3. You open an issue to discuss any significant work - we would hate for your time to be wasted.

To send us a pull request, please:

1. Fork the repository.
2. Modify the source; please focus on the specific change you are contributing. If you also reformat all the code, it will be hard for us to focus on your change.
3. Ensure local tests pass.
4. Commit to your fork using clear commit messages.
5. Send us a pull request, answering any default questions in the pull request interface.
6. Pay attention to any automated CI failures reported in the pull request, and stay involved in the conversation.

GitHub provides additional document on [forking a repository](https://help.github.com/articles/fork-a-repo/) and
[creating a pull request](https://help.github.com/articles/creating-a-pull-request/).


## Releasing

Merging to `main` publishes nothing, and nobody writes a version or release notes by hand. Give each pull request a clear title, such as `fix(signals): stop on personal data in production records only`: the titles become the release notes.

To release:

1. **Actions**, **Release**, **Run workflow** on `main`.
2. Choose by [Semantic Versioning](https://semver.org/): **patch** for fixes (3.0.0 to 3.0.1), **minor** for new behaviour (3.0.1 to 3.1.0), **major** for a breaking change (3.1.0 to 4.0.0).

The workflow then:

1. Takes the latest `vX.Y.Z` tag and works out the next version (`scripts/bump_version.py`).
2. Asks GitHub for the notes: every pull request merged since that tag, with its author, and a link to the full comparison.
3. Writes the version into `plugin.json` and every `skills/*/SKILL.md`, and the notes into `CHANGELOG.md` as the version's section. Anything left under `## [Unreleased]` goes on top as highlights; that is optional.
4. Runs the tests and builds `dist/aidlc-discovery-vX.Y.Z.zip`.
5. Commits `release: vX.Y.Z` to `main`, tags it, and publishes the release with the zip and the same notes.

It stops, changing nothing, if nothing was merged since the latest tag, or if the version would go backwards or under an older major version.

## Finding contributions to work on
Looking at the existing issues is a great way to find something to contribute on. As our projects, by default, use the default GitHub issue labels (enhancement/bug/duplicate/help wanted/invalid/question/wontfix), looking at any 'help wanted' issues is a great place to start.


## Code of Conduct
This project has adopted the [Amazon Open Source Code of Conduct](https://aws.github.io/code-of-conduct).
For more information see the [Code of Conduct FAQ](https://aws.github.io/code-of-conduct-faq) or contact
opensource-codeofconduct@amazon.com with any additional questions or comments.


## Security issue notifications
If you discover a potential security issue in this project we ask that you notify AWS/Amazon Security via our [vulnerability reporting page](http://aws.amazon.com/security/vulnerability-reporting/). Please do **not** create a public github issue.


## Licensing

See the [LICENSE](LICENSE) file for our project's licensing. We will ask you to confirm the licensing of your contribution.
