
:sparkles: Thank you for investing your time in contributing to our project! :sparkles:.

Read our [Code of Conduct](CODE_OF_CONDUCT.md) to keep our community approachable and respectable.

In this guide you will get an overview of the contribution workflow from opening an issue, creating a PR, reviewing, and merging the PR.

## New contributor guide

To get an overview of the project, read the [README](README.md). Here are some resources to help you get started with open source contributions:

- [Finding ways to contribute to open source on GitHub](https://docs.github.com/en/get-started/exploring-projects-on-github/finding-ways-to-contribute-to-open-source-on-github)
- [Set up Git](https://docs.github.com/en/get-started/quickstart/set-up-git)
- [GitHub flow](https://docs.github.com/en/get-started/quickstart/github-flow)
- [Collaborating with pull requests](https://docs.github.com/en/github/collaborating-with-pull-requests)

## Getting started

Check to see what [types of contributions](CONTRIBUTING.md#memo-types-of-contributions) we accept before making changes. Some of them don't even require writing a single line of code :sparkles:.

### :memo: Types of Contributions

You can contribute to our doc content and site in several ways. Our small, but mighty :muscle: docs team is maintaining this repo, to preserve our bandwidth, off topic conversations will be closed.

### :mega: Discussions

Discussions are where we have conversations.

If you'd like help troubleshooting a docs PR you're working on, have a great new idea, or want to share something amazing you've learned in our docs, join us in [discussions](https://github.com/israelabraham/djangorest-routes/discussions).

### :lady_beetle: Issues

[Issues](https://docs.github.com/en/github/managing-your-work-on-github/about-issues) are used to track tasks that contributors can help with. If an issue has a triage label, we haven't reviewed it yet, and you shouldn't begin work on it.

If you've found something in the content or a code smell or bad practice, search open issues to see if someone else has reported the same thing. If it's something new, open an [issue](https://github.com/israelabraham/djangorest-routes/issues/new). We'll use the issue to have a conversation about the problem you want to fix.

### :hammer_and_wrench: Pull requests

A [pull request](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests) is a way to suggest changes in our repository. When we merge those changes, they should be deployed to the live site within 24 hours. :earth_africa:

### :question: Support

We are a small team working hard to keep up with the documentation demands of a continuously changing product.

### Issues

#### Create a new issue

If you spot a problem with the docs, [search if an issue already exists](https://docs.github.com/en/github/searching-for-information-on-github/searching-on-github/searching-issues-and-pull-requests#search-by-the-title-body-or-comments). If a related issue doesn't exist, you can open a new issue using a relevant [issue form](https://github.com/github/docs/issues/new/choose).

#### Solve an issue

Scan through our [existing issues](https://github.com/github/docs/issues) to find one that interests you. You can narrow down the search using `labels` as filters. See [Labels](/contributing/how-to-use-labels.md) for more information. As a general rule, we don’t assign issues to anyone. If you find an issue to work on, you are welcome to open a PR with a fix.

### Make Changes

#### Make changes in the UI

Click **Make a contribution** at the bottom of any docs page to make small changes such as a typo, sentence fix, or a broken link. This takes you to the `.md` file where you can make your changes and [create a pull request](#pull-request) for a review.

#### Make changes in a codespace

For more information about using a codespace for working on GitHub documentation, see "[Working in a codespace](https://github.com/github/docs/blob/main/contributing/codespace.md)."

#### Make changes locally

1. [Install Git LFS](https://docs.github.com/en/github/managing-large-files/versioning-large-files/installing-git-large-file-storage).

2. Fork the repository.
    - Using GitHub Desktop:
        - [Getting started with GitHub Desktop](https://docs.github.com/en/desktop/installing-and-configuring-github-desktop/getting-started-with-github-desktop) will guide you through setting up Desktop.
        - Once Desktop is set up, you can use it to [fork the repo](https://docs.github.com/en/desktop/contributing-and-collaborating-using-github-desktop/cloning-and-forking-repositories-from-github-desktop)!

    - Using the command line:
        - [Fork the repo](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo#fork-an-example-repository) so that you can make your changes without affecting the original project until you're ready to merge them.

3. Install or update to Django>=4.1.

4. Create a working branch and start with your changes!

#### Self review

You should always review your own PR first.

For content changes, make sure that you:

- [ ] Confirm that the changes meet the user experience and goals outlined in the content design plan (if there is one).
- [ ] Compare your pull request's source changes to staging to confirm that the output matches the source and that everything is rendering as expected. This helps spot issues like typos, content that doesn't follow the style guide, or content that isn't rendering due to versioning problems. Remember that lists and tables can be tricky.
- [ ] Review the content for technical accuracy.
- [ ] Review the entire pull request using the [localization checklist](localization-checklist.md).
- [ ] Copy-edit the changes for grammar, spelling, and adherence to the [style guide](https://github.com/github/docs/blob/main/contributing/content-style-guide.md).
- [ ] Check new or updated Liquid statements to confirm that versioning is correct.
- [ ] If there are any failing checks in your PR, troubleshoot them until they're all passing.

### Commit your update

Commit the changes once you are happy with them.

Once your changes are ready, don't forget to [self-review](CONTRIBUTING.md#self-review) to speed up the review process:zap:.

### Pull Request

When you're finished with the changes, create a pull request, also known as a PR.
    - Fill the "Ready for review" template so that we can review your PR. This template helps reviewers understand your changes as well as the purpose of your pull request.
    - Don't forget to [link PR to issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue) if you are solving one.
    - Enable the checkbox to [allow maintainer edits](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/allowing-changes-to-a-pull-request-branch-created-from-a-fork) so the branch can be updated for a merge.
    Once you submit your PR, a Docs team member will review your proposal. We may ask questions or request for additional information.
    - We may ask for changes to be made before a PR can be merged, either using [suggested changes](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/incorporating-feedback-in-your-pull-request) or pull request comments. You can apply suggested changes directly through the UI. You can make any other changes in your fork, then commit them to your branch.
    - As you update your PR and apply changes, mark each conversation as [resolved](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/commenting-on-a-pull-request#resolving-conversations).
    - If you run into any merge issues, checkout this [git tutorial](https://github.com/skills/resolve-merge-conflicts) to help you resolve merge conflicts and other issues.

### Your PR is merged

Congratulations :tada::tada: The GitHub team thanks you :sparkles:.

Once your PR is merged, your contributions will be publicly visible.

Now that you are part of the Djangorest-routes community.
