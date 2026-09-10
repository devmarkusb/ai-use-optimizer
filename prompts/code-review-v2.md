---
title: Code Review v2
type: task-prompt
purpose: Perform a read-only, evidence-based adversarial pre-merge review of the current branch
targets:
  - ChatGPT
  - Claude
  - Codex
  - Cursor
  - Gemini
  - Generic LLM
scope:
  - code review
  - pull requests
  - diffs
  - brownfield
version: 2
recommended-stage: before merging when project artifacts must not be run
---

# Code Review v2

## Context

Review the current branch against the repository's `main` branch. Use the appropriate merge-base
diff, normally `origin/main...HEAD` or `main...HEAD`. If the base is missing or may be stale, state
that limitation instead of guessing.

## Goal

Find concrete issues that matter before merging this branch. Produce a read-only, adversarial review
grounded in the diff and relevant repository evidence.

## Task

1. Read the diff and enough surrounding code, tests, configuration, and documentation to understand
   the changed behavior. Do not inspect every unchanged file without a reason.
1. Look for bugs, regressions, security, performance, concurrency, API, lifecycle, compatibility,
   and important test blind spots introduced by this branch.
1. Prioritize issues that could change the merge decision. Ignore style and speculative concerns
   unless they hide or create a real defect.
1. For the one to three highest-risk changes, test each concern against its strongest plausible
   defense using repository evidence. Discard concerns that do not hold up. Use this check to refine
   the findings; do not print a separate adversarial discussion.

## Rules

- This is analysis only. Do not edit files.
- Do not run tests, builds, binaries, scripts, migrations, package-manager commands, or any other
  project artifacts. Read-only git and file-inspection commands are allowed.
- Base claims on the diff and repository evidence; do not invent requirements or behavior.
- Report only actionable, evidence-backed findings. Do not present unsupported hypotheses as
  findings. State any uncertainty essential to a finding within that finding.
- If there are no actionable issues, say so explicitly.
- Do not claim to have run or verified anything that was not actually run or verified.

## Output Format

Return only a Markdown list of findings in descending order of severity. For each finding, include:

- **Severity and issue**: `Critical`, `High`, `Medium`, or `Low`, followed by a short issue title.
- **File / lines**: the relevant location.
- **Problem and evidence**: the concrete failure scenario, its impact, and supporting repository
  evidence. Include any uncertainty essential to assessing the finding here.
- **Minimal fix**: the smallest change that addresses the problem.

If there are no actionable findings, say `No actionable issues found.`

Include a brief review limitation only if it materially restricted the review, such as a missing
base branch or unavailable relevant files. Do not add a summary, merge recommendation, separate
adversarial discussion, or standalone list of speculative concerns.

## Quality Bar

- Lead with concrete merge risk, not generic advice.
- Every finding names a failure scenario and cites supporting repository evidence. Labeling a
  concern as uncertain does not substitute for evidence.
- Do not manufacture findings to fill the output.
- Keep the review proportional to the size and risk of the diff.
