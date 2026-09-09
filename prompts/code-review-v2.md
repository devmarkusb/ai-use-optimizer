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
1. For the one to three highest-risk changes, challenge the strongest plausible defense against the
   concern and identify what evidence remains missing.

## Rules

- This is analysis only. Do not edit files.
- Do not run tests, builds, binaries, scripts, migrations, package-manager commands, or any other
  project artifacts. Read-only git and file-inspection commands are allowed.
- Base claims on the diff and repository evidence; do not invent requirements or behavior.
- Separate confirmed defects from hypotheses. Label assumptions, unknowns, and unverified claims.
- Report only actionable findings. If there are no material issues, say so explicitly.
- Do not claim to have run or verified anything that was not actually run or verified.

## Output Format

Return Markdown with exactly these sections:

### Merge Recommendation

Choose one: **Merge**, **Merge with follow-ups**, or **Do not merge**. Give the primary reason in
one or two sentences. State that the review is static-only when relevant.

### Summary

Briefly explain what changed, why it changed, and the main consequence for the system.

### Findings

List findings in descending order of severity. For each finding, include:

- **File / lines**
- **Severity**: `Critical`, `High`, `Medium`, or `Low`
- **Issue**
- **Impact**
- **Evidence**
- **Minimal fix**
- **Suggested read-only verification**

Say `None found.` if there are no material findings.

### Adversarial Challenges

Include only useful challenges for the highest-risk changes. For each, state the concern, the
strongest plausible defense, whether the repository evidence supports that defense, and what would
close any remaining gap. Say `None.` when no separate challenge is useful.

### Unknowns and Assumptions

List only unknowns or assumptions that could affect the merge decision. Say `None.` if empty.

## Quality Bar

- Lead with concrete merge risk, not generic advice.
- Every finding names a failure scenario and cites repository evidence or clearly labels its
  uncertainty.
- Do not manufacture findings to fill sections.
- Keep the review proportional to the size and risk of the diff.
