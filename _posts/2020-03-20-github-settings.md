---
title: Setup a new github project
author: Diane Delallée
date: 2020-03-20 20:55:00 +0800
categories: [Blog, Configuration]
tags: [Configuration, github]
---

When you start a new github repo, just create the folder .github and create these three files, to help you in your day-to-day job:

- auto_assign.yml
- pull_request_template.md
- settings.yml

auto_assign.yml

```yml
# Set to true to add reviewers to pull requests
addReviewers: true

# Set to true to add assignees to pull requests
addAssignees: false

# A list of reviewers to be added to pull requests (GitHub user name)
reviewers:
  - user_name_1
  - user_name_2
  - user_name_3

# A number of reviewers added to the pull request
# Set 0 to add all the reviewers (default: 0)
numberOfReviewers: 0
# A list of assignees, overrides reviewers if set
# assignees:
#   - assigneeA

# A number of assignees to add to the pull request
# Set to 0 to add all of the assignees.
# Uses numberOfReviewers if unset.
# numberOfAssignees: 2

# A list of keywords to be skipped the process that add reviewers if pull requests include it
# skipKeywords:
#   - wip
```

pull_request_template.md

```md
### What ([name of your link to the description]())

Changes made.

### Why

Reason for change. Problem solved.

### UI

Before/after.
```

settings.yml

```yml
repository:
  # See https://developer.github.com/v3/repos/#edit for all available settings.

  # The name of the repository. Changing this will rename the repository
  name: Name of your repo

  # A short description of the repository that will show up on GitHub
  description: Description of your repo

  # A comma-separated list of topics to set on the repository
  topics:

  # A URL with more information about the repository
  homepage: https://github.com/path/to/your/repo

  # Either `true` to make the repository private, or `false` to make it public.
  private: true

  # Either `true` to enable issues for this repository, `false` to disable them.
  has_issues: true

  # Either `true` to enable projects for this repository, or `false` to disable them.
  # If projects are disabled for the organization, passing `true` will cause an API error.
  has_projects: true

  # Either `true` to enable the wiki for this repository, `false` to disable it.
  has_wiki: true

  # Either `true` to enable downloads for this repository, `false` to disable them.
  has_downloads: true

  # Updates the default branch for this repository.
  default_branch: staging

  # Either `true` to allow squash-merging pull requests, or `false` to prevent
  # squash-merging.
  allow_squash_merge: true

  # Either `true` to allow merging pull requests with a merge commit, or `false`
  # to prevent merging pull requests with merge commits.
  allow_merge_commit: false

  # Either `true` to allow rebase-merging pull requests, or `false` to prevent
  # rebase-merging.
  allow_rebase_merge: false

# Labels: define labels for Issues and Pull Requests
labels:
  - name: "🦋 Not a bug - A feature"
    color: CC0000
    description: "Something is not working"
  - name: "work in progress 🚧"
    color: febc2f
    description: "No need to check it for the moment"
  - name: "help wanted 🚁"
    color: 00917D
    description: "Need helps from another colleague"
  - name: "blocked ⛔"
    color: FC93A3
    description: "When this PR is blocked by another PR"

# Milestones: define milestones for Issues and Pull Requests
#milestones:
#- title: milestone-title
#description: milestone-description
# The state of the milestone. Either `open` or `closed`
#state: open

# Collaborators: give specific users access to this repository.
#collaborators:
#- username: bkeepers
# Note: Only valid on organization-owned repositories.
# The permission to grant the collaborator. Can be one of:
# * `pull` - can pull, but not push to or administer this repository.
# * `push` - can pull and push, but not administer this repository.
# * `admin` - can pull, push and administer this repository.
#permission: push

# NOTE: The APIs needed for teams are not supported yet by GitHub Apps
# https://developer.github.com/v3/apps/available-endpoints/
teams:
  - name: name_of_the_groups
    permission: push
  - name: name_of_other_groups
    permission: admin

branches:
  - name: staging
    # https://developer.github.com/v3/repos/branches/#update-branch-protection
    # Branch Protection settings. Set to null to disable
    protection:
      # Required. Require at least one approving review on a pull request, before merging. Set to null to disable.
      required_pull_request_reviews:
        # The number of approvals required. (1-6)
        required_approving_review_count: 2
        # Dismiss approved reviews automatically when a new commit is pushed.
        dismiss_stale_reviews: false
        # Blocks merge until code owners have reviewed.
        require_code_owner_reviews: false
        # Specify which users and teams can dismiss pull request reviews. Pass an empty dismissal_restrictions object to disable. User and team dismissal_restrictions are only available for organization-owned repositories. Omit this parameter for personal repositories.
        dismissal_restrictions:
          users: []
          teams: []
      # Required. Require status checks to pass before merging. Set to null to disable
      required_status_checks:
        # Required. Require branches to be up to date before merging.
        strict: false
        # Required. The list of status checks to require in order to merge into this branch
        contexts: [continuous-integration/jenkins/pr-merge]
      # Required. Enforce all configured restrictions for administrators. Set to true to enforce required status checks for repository administrators. Set to null to disable.
      enforce_admins: false
      # Required. Restrict who can push to this branch. Team and user restrictions are only available for organization-owned repositories. Set to null to disable.
      restrictions:
        users: []
        teams: name_of_the_team
  - name: master
    protection:
      restrictions:
        users: []
        teams: name_of_the_team
```
