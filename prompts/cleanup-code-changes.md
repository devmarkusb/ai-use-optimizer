---
title: Cleanup Code Changes
type: task-prompt
purpose: Reduce a working tree to the minimal patch that still achieves the intended code change
targets:
  - ChatGPT
  - Claude
  - Codex
  - Cursor
  - Gemini
  - Generic LLM
scope:
  - bug fix
  - feature
  - refactor
  - git diff
  - working tree cleanup
recommended-stage: after extended work when the diff is larger than the final outcome
---

# Cleanup Code Changes

## Context

After extended work on a code change (bug fix, feature, or refactor), some working-tree edits are
the intended outcome; others are experiments, diagnostics, speculative refactors, workarounds,
formatting noise, or dead ends.

## Goal

Reduce the current changes to the smallest coherent patch that still achieves the intended outcome.

## Required Workflow

1. Inspect repository status and the full diff before editing.
1. Start from context you already have: the conversation, your prior reasoning, tool results, failed
   attempts, and conclusions about what worked. Use that to identify the intended change and likely
   dead ends before broad repo search or re-reading unchanged files.
1. Infer the intended change from the diff, history, surrounding code, tests, and user-provided
   context.
1. Classify every hunk: required for the intended change, required test coverage, harmless but
   unnecessary, abandoned experiment, unrelated change, or uncertain.
1. Map production changes, tests, and auxiliary edits the intended change depends on.
1. Revert everything else. Judge hunks, not whole files.
1. Reinspect for scope creep, diagnostics, dead code, formatting-only noise, and mismatched tests.
1. Run focused regression tests, then broader checks where practical.
1. If a test fails, restore only the minimal required part.
1. Stop when the patch is minimal, coherent, and verified.

## Rules

- Prefer the smallest behavior-preserving patch; do not redesign because you prefer another
  approach.
- Do not brute-force rediscovery when the session already establishes what worked, what failed, and
  why.
- No unrelated refactoring, renaming, formatting, or cleanup.
- Do not drop a change because it looks unusual—establish whether the intended change depends on it
  first.
- Suspect debug logging, commented-out code, temporary flags, duplicated code, broad exception
  handling, disabled tests, hard-coded values, and unrelated formatting.
- Keep changes needed for correctness, regression prevention, compilation, API consistency, and
  relevant documentation.
- Keep or strengthen tests that demonstrate the intended change; do not weaken tests to pass.
- Do not revert user changes outside the current change diff.
- Use Git-aware operations; do not reset the worktree or destroy uncommitted work.
- If a change's purpose is unclear, keep it and report uncertainty instead of guessing.
- Do the workflow silently. Classify hunks, revert, and test without narrating reasoning in the
  reply.

## Response style

- The reply is a short audit note, not a report. Say as little as possible.
- Do not recap the prompt, restate the workflow, or explain how you analyzed the diff.
- Bullets and one-line facts only. No preamble, methodology, or play-by-play.
- Every line must carry new information: path, hunk, command, or decision.
- Use `None.` when a section has nothing to report.

## Output Format

Return Markdown with exactly these sections. Bullets only; one line per item unless quoting a
command.

### Intent

One sentence on what the patch should accomplish. For bug fixes, add a second sentence with root
cause only when it is not obvious from the diff.

### Essential changes

`- path` — one-line why. Merge paths into one bullet when the reason is identical.

### Removed changes

`- path` or hunk — one-line what was reverted.

### Verification

`- command` — pass/fail or one-line result.

### Remaining uncertainty

`- path` or hunk — one-line why it was kept despite unclear purpose.

### Final diff summary

One or two sentences: why the remaining patch is minimal and coherent.
