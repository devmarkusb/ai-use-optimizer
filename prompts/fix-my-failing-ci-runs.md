---
title: Fix My Failing CI Runs
type: task-prompt
purpose: Diagnose and fix failing CI runs on main/default branches across repositories
targets:
  - Codex
  - Claude Code
  - Cursor
  - Generic LLM coding agents
scope:
  - brownfield
  - multi-repo
recommended-stage: when default branch CI is red and you need minimal, verified fixes
---

# Fix My Failing CI Runs

## Context

GitHub owner \<USER> has repositories where default branch (`main` or `master`) CI runs are failing.

Git user: \<GIT_USER>. Git email: \<GIT_EMAIL>.

Local checkouts directory (optional): \<LOCAL_CHECKOUTS>. If empty or omitted, work entirely via
`gh` CLI and clone or check out repositories on demand into a temporary scratch workspace.

## Goal

Discover repositories where the default branch CI is failing, diagnose root causes from logs, fix
failures with minimal idiomatic changes, validate each fix locally, and report remaining risks.

## Required Workflow

List repositories and failing default-branch CI runs first, then work **repo-by-repo**, starting
with lowest-level foundational dependencies first (or the smallest, highest-confidence failures for
independent repositories).

### Step 1: Inventory failing default-branch runs

For each non-archived GitHub repository (owner: \<USER>):

1. Query recent workflow runs on the default branch:

   ```bash
   gh run list --repo <owner/repo> --branch main --limit 3 --json databaseId,workflowName,conclusion,status,url
   ```

1. Filter for active failures (`conclusion == "failure"` on the latest completed run).

1. Present an initial inventory table:

   - Repository name
   - Default branch
   - Failing workflow name
   - Run URL

### Step 2: Diagnose and fix repo-by-repo

For each failing repository in processing order:

1. **Inspect CI failures remotely:**

   - Read failed jobs, logs, and annotations:

     ```bash
     gh run view <run-id> --repo <owner/repo> --log-failed
     ```

   - Prefer the exact command and error output from CI over guessing. Group failures by root cause.

1. **Check out repository:**

   - If `<LOCAL_CHECKOUTS>` contains the repository, use it.

   - Otherwise, clone the repo into a temporary scratch workspace:

     ```bash
     gh repo clone <owner/repo> /tmp/scratch/<repo>
     ```

   - Configure the Git committer identity in the repository before committing:

     ```bash
     git config user.name "<GIT_USER>"
     git config user.email "<GIT_EMAIL>"
     ```

1. **Reproduce locally:**

   - Run the failing command using the project's declared package manager and tooling.
   - If a failure is environment-specific, document it clearly before adjusting configuration.

1. **Fix with minimal, idiomatic changes:**

   - Fix compiler errors, broken tests, lint/format failures, lockfile drift, or broken paths.
   - Fix CI YAML only when the workflow itself is wrong; never suppress tests, disable linters, or
     hide real code failures.

1. **Validate:**

   - Rerun the exact failing CI command locally.
   - Run the project's standard test and lint commands to avoid regressions.

1. **Commit:**

   - Create focused commits per logical fix under `<GIT_USER>` and `<GIT_EMAIL>`.
   - Do not push to remote unless explicitly requested.

## Available tools

- `gh` CLI for workflow run discovery, inspection, log retrieval, and repo cloning.
- Local shell, git, builds, tests, and package managers.
- Temporary scratch directory for on-demand clones (when `<LOCAL_CHECKOUTS>` is omitted).
- Web search only if needed for official docs or dependency resolution.

## Rules

- Fix root causes, not symptoms. Never suppress tests, disable CI, remove assertions, or
  blanket-ignore errors unless justified.
- Distinguish flaky from deterministic failures using run history. Fix flake causes or report
  them—never mask them with retries or by disabling tests.
- Do not upgrade unrelated toolchains or dependencies unless required to fix the failure.
- Always configure and use `<GIT_USER>` and `<GIT_EMAIL>` for git operations and commits.
- Preserve public APIs unless a compatible fix is strictly required.
- Do not push to remotes unless the user explicitly requests it.
- When a failure cannot be reproduced locally, document the environment gap.

## Output Format

Start with the initial inventory of repositories and failing runs. Then, for each repository in
processing order:

### `<repo-name>` — CI fix summary

- **Failing workflow & jobs:**
- **Root causes:**
- **Files changed:**
- **Commands run:**
- **Validation result:**
- **Remaining risks:**

## Quality Bar

- Every fix ties to a concrete CI log or reproduced failure—not filename inference alone.
- Validation reruns the exact failing CI command.
- Changes stay minimal and idiomatic for the stack; no drive-by refactors.
- If CI cannot be fully green, remaining failures are explicit with next steps—not hidden.
