---
title: Maintainability Review
type: task-prompt
purpose: Find user-based naming and mixed responsibilities in the current branch's changes
targets:
  - ChatGPT
  - Claude
  - Codex
  - Cursor
  - Gemini
  - Generic LLM
scope:
  - code review
  - naming
  - responsibilities
  - git diff
---

# Maintainability Review

## Task

Review the current branch as a pull request to `origin/main`. Fetch if needed and scope the review
to the merge-base diff (`origin/main...HEAD`). If the base cannot be established, report that
limitation and stop.

Find, if present:

- Functions or types named after their users instead of what they actually do or represent.
- Functions or types with multiple responsibilities.

Read enough surrounding code and call sites to support each finding. Do not edit files or broaden
the review beyond these two checks.

## Output Format

Return a concise list of findings. For each, include the file and line, evidence of the naming or
responsibility problem, and a focused suggested improvement. If none are found, say
`No maintainability findings.`
