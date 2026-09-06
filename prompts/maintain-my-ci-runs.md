---
title: Maintain My CI Runs
type: task-prompt
purpose: Auto-merge green PRs, triage remaining failures, and update or fix selected PRs
targets:
  - Codex
  - Claude Code
  - Cursor
  - Generic LLM coding agents
scope:
  - brownfield
  - multi-repo
recommended-stage: when sweeping multi-repo PRs, triaging blockers, and maintaining branches
---

# Maintain My CI Runs

## Context

GitHub owner \<USER> has repositories with open pull requests and CI runs. Some repositories may
depend on each other (e.g. shared libraries, templates, actions, or packages).

Git user: \<GIT_USER>. Git email: \<GIT_EMAIL>.

Local checkouts directory (optional): \<LOCAL_CHECKOUTS>. If empty or omitted, work entirely via
`gh` CLI and clone or check out selected PRs on demand into a temporary scratch workspace.

## Goal

1. Order repositories by dependency level: lowest-level (foundational/shared) first, downstream
   last.
1. Automatically sweep and merge all ready, green PRs in that bottom-up order.
1. Triage all remaining open PRs with clear root causes and effort estimates.
1. Pause for user direction, then update or fix selected PRs with minimal changes.
1. Give up early on stubborn PRs if simple update tricks do not resolve them, and report back.

## Required Workflow

### Step 1: Map dependencies and order lowest-level first

For each non-archived GitHub repository (owner: \<USER>):

1. **Detect inter-repo dependencies:**
   - Scan package manifests and workflow files (`package.json`, `pyproject.toml`, `Cargo.toml`,
     `go.mod`, GitHub Actions workflows, submodules) for references to `<USER>/<repo>`.
1. **Sort topologically (bottom-up):**
   - **Lowest level (foundational/shared):** Repositories that other repos depend on, with zero or
     few internal dependencies. Process these first.
   - **Higher level (downstream consumers):** Repositories that depend on the foundational packages.
     Process these last.
   - **Independent:** Repositories without internal relationships can be processed in any order.
1. State the processing order before sweeping.

### Step 2: Sweep and merge green PRs

Process repositories in the determined lowest-level-first order:

1. Pre-flight token scope check (once, before sweeping):

   ```bash
   gh auth status
   ```

   - If the token scopes do **not** include `workflow`, the agent cannot merge any PR that touches
     `.github/workflows/` (GitHub rejects it with
     `refusing to allow an OAuth App to create or update workflow ... without 'workflow' scope`).
     Such PRs are classified as **Skipped (workflow scope)** upfront — never attempt to merge them.
   - Only run `gh auth refresh -s workflow` if the user explicitly permits interactive auth. Never
     treat a scope refusal as a sweep-stopping failure.

1. List open PRs:

   ```bash
   gh pr list --state open --json number,title,mergeable,mergeStateStatus,statusCheckRollup,url
   ```

1. Identify merge candidates:

   - Candidates are **ONLY** those with `mergeable == "MERGEABLE"`, `mergeStateStatus` not `DIRTY`
     or `BLOCKED`, and all required checks passing.

1. For each candidate:

   - Show repo (with dependency level), PR number, title, and checks state.

   - Check whether the PR touches workflow files:

     ```bash
     gh pr view <number> --repo <owner/repo> --json files --jq '.files[].path'
     ```

     If any path is under `.github/workflows/` and the token lacks the `workflow` scope, classify
     the PR as **Skipped (workflow scope)** and continue with the next candidate — do not attempt
     the merge.

   - Run:

     ```bash
     gh pr merge --merge --delete-branch <number> --repo <owner/repo>
     ```

1. Rules for sweeping:

   - Process one repository at a time in bottom-up dependency order.
   - Stop and report on any unexpected merge failure. A `workflow`-scope refusal is expected when
     the pre-flight check already flagged it — those PRs are skipped, not failures.
   - Never force-merge.
   - Never merge `DIRTY`, `BLOCKED`, or failing-checks PRs.
   - Never touch archived repositories.

1. Conclude Step 2 with a **Merged / Skipped / Failed** summary table, splitting Skipped into
   `Skipped (failing CI / conflicts / blocked)` and
   `Skipped (workflow scope — merge via web UI or a workflow-scoped token)`.

### Step 3: Triage remaining PRs and estimate effort

For all remaining open PRs across the repositories:

1. **Inspect blockers remotely:** Use `gh pr view`, `gh pr checks`, and `gh run view --log-failed`
   to determine why the PR was skipped (e.g. merge conflicts, failing test, lint failure, missing
   review, or waiting on an upstream repo).
1. **Estimate effort:** Classify the complexity of resolving each PR:
   - **Trivial (\<15m):** Outdated lockfile, minor formatting/lint fix, clean rebase without
     conflicts.
   - **Low (15–30m):** Simple dependency bump incompatibility, broken link, minor test fix.
   - **Medium (30–60m):** Test suite failure requiring code changes, environment or CI workflow bug.
   - **High (>60m):** Semantic merge conflict, major architectural breakage, complex flaky tests.
1. **Present triage table (sorted lowest-level first):** Display:
   - Repo (and dependency tier) and PR number / title
   - Blocker type and root cause summary
   - Estimated effort level and justification
1. **Interactive gate — STOP HERE:** Ask the user:
   > "Which of these remaining PRs would you like me to tackle?" Wait for explicit user selection
   > before cloning, checking out, or modifying any code.

### Step 4: Update and fix selected PRs on demand

Once the user selects one or more PRs to resolve:

1. **Check out:** If `<LOCAL_CHECKOUTS>` contains the repository, use it. Otherwise, check out the
   PR branch on demand:

   ```bash
   gh pr checkout <number> --repo <owner/repo>
   ```

   Configure the Git committer identity in the repository before rebasing or committing:

   ```bash
   git config user.name "<GIT_USER>"
   git config user.email "<GIT_EMAIL>"
   ```

1. **Try simple update tricks first:**

   - If downstream, check whether pulling in newly merged upstream changes/releases resolves it.
   - Rebase or sync against the default branch (`git fetch origin main && git rebase origin/main`).
   - Refresh lockfiles (`uv lock`, `npm install`, `cargo update`, etc.).
   - Apply straightforward lint, format, or type-stub adjustments.

1. **Give up early on stubborn issues:**

   - If simple tricks fail (e.g. semantic merge conflicts, incompatible breaking changes, deep test
     regressions), **do not run in circles** or attempt wide refactors.
   - Stop immediately, document the exact failure log and what was attempted, and ask the user for
     guidance before proceeding or skipping.

1. **Validate:** Rerun the exact failing CI command, then full local test/lint suites.

1. **Commit and update:** Create focused commits under `<GIT_USER>` and `<GIT_EMAIL>`. Push to the
   PR branch only if requested or configured.

## Available tools

- `gh` CLI for repo discovery, PR inspection, merging, and Actions log retrieval.
- Local shell, git, builds, tests, and package managers.
- Temporary scratch directory for on-demand checkouts (when `<LOCAL_CHECKOUTS>` is omitted).
- Web search only if needed for official docs or dependency resolution.

## Rules

- Process lowest-level/foundational repositories first; never process downstream consumers before
  their upstream dependencies.
- Never force-merge or bypass branch protections.
- Never touch archived repositories.
- Always configure and use `<GIT_USER>` and `<GIT_EMAIL>` for git operations, rebases, and commits.
- Never begin fixing PRs in Step 4 without user confirmation from the Step 3 triage table.
- Give up early on complex branch updates; ask the user instead of speculating.
- Fix root causes, not symptoms. Never suppress tests, disable CI, remove assertions, or
  blanket-ignore errors unless justified.
- Distinguish flaky from deterministic failures using run history. Fix flake causes or report
  them—never mask them with retries.
- Do not upgrade unrelated toolchains or dependencies.
- Preserve public APIs unless a compatible fix is strictly required.

## Output Format

### Step 1 & 2: Repository order & sweep summary

- **Dependency order:** list of repos from lowest-level to downstream
- **Merged:** list of `<repo>#<number>` (with title)
- **Skipped:** list of `<repo>#<number>` (reason: failing CI / conflicts / blocked)
- **Skipped (workflow scope):** list of `<repo>#<number>` (green but touching `.github/workflows/`;
  merge via web UI or a workflow-scoped token)
- **Failed merges:** list of any merge errors encountered

### Step 3: Triage & effort estimate (ordered lowest-level first)

| Repository (Tier) | PR  | Blocker / Root Cause | Estimated Effort | Summary & Recommended Fix |
| ----------------- | --- | -------------------- | ---------------- | ------------------------- |
| ...               | ... | ...                  | Low / Medium / … | ...                       |

Followed by the interactive prompt asking which PRs to tackle.

### Step 4: Update & fix summary (per tackled PR)

- **PR:** `<repo>#<number>`
- **Status:** Resolved / Paused (needs user guidance) / Skipped
- **Failing jobs:**
- **Actions taken:**
- **Files changed:**
- **Commands run:**
- **Validation result:**
- **Remaining risks or questions:**

## Quality Bar

- Repositories are processed lowest-level first so upstream changes propagate cleanly.
- Step 2 never merges an unverified, blocked, or dirty PR.
- Every effort estimate in Step 3 is backed by actual CI failure logs or diff inspection.
- The agent halts after Step 3 and does not modify code without user consent.
- Step 4 gives up early on difficult conflicts or regressions rather than guessing.
- Validations rerun the exact failing CI command.
- Changes stay minimal and idiomatic for the stack.
