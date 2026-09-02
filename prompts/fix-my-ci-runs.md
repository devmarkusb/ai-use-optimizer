---
title: Fix My CI Runs
type: task-prompt
purpose: Diagnose and fix failing CI across one or more repositories
targets:
  - Codex
  - Claude Code
  - Cursor
  - Generic LLM coding agents
scope:
  - brownfield
  - multi-repo
recommended-stage: when CI is red and you need minimal, verified fixes
---

# Fix My CI Runs

## Context

GitHub owner \<OWNER> potentially has repositories with failing CI; find them. Apply fixes in local
checkouts (if given) under path: \<LOCAL_CHECKOUTS>. (Ignore if empty or not given.)

## Goal

Fix all failing CI runs with minimal, idiomatic changes. Reproduce locally where possible, validate
each fix, and report what changed and what risk remains.

## Required Workflow

List the repositories and current failing CI runs first, then work **repo-by-repo**, starting with
the smallest or highest-confidence failures.

Per repository:

1. **Inspect the repository:** language stack, CI provider and configs (workflows, Makefile, CMake,
   tox, pytest, cargo, npm/pnpm/yarn, pre-commit, formatters, linters, type checkers), README and
   contributing/build docs.
1. **Inspect CI failures:** read the failed jobs, logs, and annotations. Prefer the exact command
   from CI over guessing from filenames. Group failures by root cause.
1. **Reproduce locally** where feasible in a short amount of time. Install dependencies only as
   needed and use the project's declared tooling. If a failure is environment-specific, document it
   and fix the workflow.
1. **Fix with minimal, idiomatic changes** for the stack (compiler errors, tests, lint/format/type
   failures, packaging, lockfile consistency, links). Fix CI YAML only when the workflow itself is
   wrong; do not hide real code failures.
1. **Validate:** rerun the exact failing command, then relevant format, lint, and test commands.
1. **Commit:** one small commit per logical fix; do not mix unrelated repos in one commit unless
   explicitly requested. Do not push.

## Available tools

- `gh` CLI for GitHub Actions logs and PR/branch handling.
- Local shell, builds, tests, and package managers as required.
- Internet only if needed for official docs or dependency/tooling changes.

## Rules

- Fix root causes, not symptoms. Never suppress tests, disable CI, remove assertions, or
  blanket-ignore errors unless justified.
- Do not upgrade toolchains, dependencies, or CI images unless the failure requires it.
- Preserve public APIs unless the failure requires a compatible fix.
- Do not push to remotes unless the user explicitly requests it.
- When a failure cannot be reproduced locally, say so and document the environment gap.

## Output Format

Start with the initial inventory of repositories and failing runs. Then, for each repository in
processing order:

### `<repo-name>` — CI fix summary

- **Failing jobs:**
- **Root causes:**
- **Files changed:**
- **Commands run:**
- **Remaining risks:**

## Quality Bar

- Every fix ties to a concrete CI log or reproduced failure—not filename inference alone.
- Validation reruns the exact failing CI command when possible.
- Changes stay minimal and idiomatic for the stack; no drive-by refactors.
- If CI cannot be fully green, remaining failures are explicit with next steps—not hidden.
