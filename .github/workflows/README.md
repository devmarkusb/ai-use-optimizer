# Workflows

CI is [`.github/workflows/ci.yml`](ci.yml). It runs on push and pull request to `main`.

## Required checks

GitHub rejects pull request auto-merge when the base branch has no required status checks. Those
requirements are a repository ruleset, not workflow YAML:

[main: required CI checks](https://github.com/devmarkusb/ai-use-optimizer/rules/26124779)

The ruleset targets `refs/heads/main` and requires the check names below. Each name is the job
`name:` in `ci.yml`, reported by GitHub Actions. Renaming a job `name` without updating the ruleset
blocks merges that wait on that check.

| Check name                    | Job id              | What it runs                                          |
| ----------------------------- | ------------------- | ----------------------------------------------------- |
| Lint (pre-commit)             | `pre-commit`        | pre-commit (Markdown, gitleaks, actionlint, YAML)     |
| Markdown link check           | `linkcheck`         | lychee on README and prompt files                     |
| README path guard             | `readme-paths`      | `.github/scripts/verify-readme-paths.sh`              |
| promptfill (pytest)           | `promptfill`        | pytest in `promptfill/`                               |
| Dependency audit (pip-audit)  | `dependency-audit`  | pip-audit on the root lockfile and `promptfill/`      |
| Workflow security (zizmor)    | `zizmor`            | zizmor                                                |

Repository admins can bypass the ruleset, so a direct push to `main` still works. Pull requests do
not have to be up to date with `main` before they merge.

## Dependabot

Dependabot config is [`.github/dependabot.yml`](../dependabot.yml). It opens weekly update pull
requests. This workflow does not merge them.

Do not add a Dependabot auto-merge job back into `ci.yml`. That job called
`gh pr merge --auto --squash` after CI passed, and GitHub rejected it while `main` had no required
checks. The ruleset above is what makes auto-merge possible. Enabling it
(`gh pr merge --auto --squash`) is a step on the pull request, not a CI job.
