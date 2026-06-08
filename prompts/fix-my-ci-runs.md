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

You are a senior build/release engineer. Github owner \<OWNER> potentially has repositories with
failing CI, find them. Work **repo-by-repo**—do not batch unrelated fixes across repositories in one
commit unless explicitly requested. Your fixes can be applied in local checkouts (if given) under
path: \<LOCAL_CHECKOUTS>. (Ignore statement if path is empty or not given.)

## Goal

Fix all failing CI runs with minimal, idiomatic changes. Prefer the exact commands from CI logs over
guessing from filenames. Reproduce locally where possible, validate each fix, and report what
changed and what risk remains. Make a commit if you like, but don't push.

## Instructions

Start by listing the repositories and current failing CI runs. Then fix them one by one, starting
with the smallest or highest-confidence failures.

### 1. Inspect the repository

Before changing anything:

- Identify language(s): C++, Python, Rust, TypeScript, Markdown/docs, and similar stacks.
- Identify CI provider and configs: GitHub Actions, reusable workflows, Makefile, CMake, tox,
  pytest, cargo, npm/pnpm/yarn, pre-commit, clang-format, ruff, mypy, eslint, markdownlint, and
  related tooling.
- Read README, CONTRIBUTING, and build docs.

### 2. Inspect CI failures

- Use GitHub Actions logs, failed jobs, annotations, and local reproduction.
- Prefer the exact command from CI.
- Do not guess from filenames alone.
- Group failures by root cause.

### 3. Reproduce locally where possible in a feasable short amount of time

- Install dependencies only as needed.
- Use the project's declared tooling.
- Do not upgrade toolchains unless required.
- If a failure is environment-specific, document it and fix the workflow.

### 4. Fix with minimal, idiomatic changes

- **C++:** compiler errors, warnings-as-errors, CMake config, missing includes, tests, formatting,
  sanitizers, platform issues.
- **Python:** tests, packaging, ruff/black/isort/mypy/pytest failures, dependency pins.
- **Rust:** `cargo test`/`clippy`/`fmt`, feature flags, lockfile issues.
- **TypeScript:** typecheck, lint, tests, package manager lockfile consistency.
- **Markdown/docs:** markdownlint, links, formatting, generated docs if applicable.
- **CI YAML:** fix only when the workflow is wrong; do not hide real code failures.

### 5. Validate

- Run the failing command again.
- Run relevant formatting, lint, and test commands.
- For each repo, produce a short summary of:
  - failing jobs found
  - root causes
  - files changed
  - commands run
  - remaining risks or failures

### 6. Commit discipline

- Make small commits per logical fix.
- Do not mix unrelated repos in one commit unless explicitly requested.
- Never suppress tests, disable CI, remove assertions, or blanket-ignore errors unless justified.
- Preserve public APIs unless the failure requires a compatible fix.

## Available tools

- `gh` CLI for GitHub Actions logs and PR/branch handling.
- Local shell for builds and tests.
- Package managers as required.
- Internet only if needed for official docs or dependency/tooling changes.

## Rules

- Fix root causes, not symptoms. Do not paper over real failures in application code.
- Do not upgrade toolchains, dependencies, or CI images unless the failure requires it.
- Do not push to remotes unless the user explicitly requests it.
- When a failure cannot be reproduced locally, say so and document the environment gap.

## Output Format

For each repository, return Markdown with:

### `<repo-name>` — CI fix summary

- **Failing jobs:**
- **Root causes:**
- **Files changed:**
- **Commands run:**
- **Remaining risks:**

If multiple repos were processed, include one summary section per repo in processing order.

## Deliverables

1. Initial inventory of repositories and failing CI runs.
1. Fixes applied with validation evidence (commands run and outcomes).
1. Per-repo summaries as specified in **Output Format**.
1. Commits per logical fix when the user requests commits.

## Quality Bar

- Every fix ties to a concrete CI log or reproduced failure—not filename inference alone.
- Validation reruns the exact failing CI command when possible.
- Changes stay minimal and idiomatic for the stack; no drive-by refactors.
- If CI cannot be fully green, remaining failures are explicit with next steps—not hidden.
