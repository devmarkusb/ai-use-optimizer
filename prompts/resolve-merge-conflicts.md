---
title: Resolve Merge Conflicts
type: task-prompt
purpose: Resolve an in-progress git merge or rebase conflict with minimal, verified changes
targets:
  - Claude Code
  - Codex
  - Cursor
  - Generic LLM coding agents
scope:
  - git conflict resolution
  - merge
  - rebase
recommended-stage: when a merge or rebase is stopped on conflicts
---

# Resolve Merge Conflicts

## Task

Resolve the current in-progress git merge or rebase. Preserve the intent of both sides where
possible, make only the changes needed to complete the operation, run the project's relevant checks,
and finish the merge or rebase.

## Required Workflow

1. Inspect the current git state: merge/rebase status, conflicted files, branch names, recent
   history, and the staged and unstaged diff.
1. Find the primary sources for each conflict: commit messages, surrounding code, tests, linked PRs,
   issues, or docs available in the workspace.
1. Resolve each hunk by preserving both intents where they are compatible.
1. When the intents conflict, choose the resolution that matches the merge or rebase goal and note
   the trade-off.
1. Do not invent unrelated behavior while resolving conflicts.
1. Discover and run the relevant automated checks, typically typecheck, tests, then format or lint.
1. Fix failures caused by the conflict resolution.
1. Stage only the resolved files and required follow-up fixes.
1. Finish the operation: commit the merge, or continue the rebase until all commits are applied.

## Rules

- Do not abort, reset, or restart the merge/rebase as a shortcut.
- Do not stage unrelated local changes.
- Do not use one side's version wholesale unless the other side is truly obsolete or incompatible.
- Prefer existing project behavior, style, and tests over new abstractions.
- If a conflict depends on intent that cannot be inferred from available sources, stop and ask the
  user for that specific decision.

## Output Format

Return a concise summary with:

- files resolved
- conflict intent preserved or trade-offs made
- checks run and results
- merge/rebase status
