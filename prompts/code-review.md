---
title: Code Review
type: task-prompt
purpose: Review a branch or PR for bugs, intent, comment clarity, and repo fit
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
---

# Code Review

## Context

Review the current branch as a pull request to `origin/main`. Fetch if needed. Scope the change with
the merge-base diff (`origin/main...HEAD`). Input may be a branch, diff, PR, files, or folder path.

## Goal

Explain what changed and why, find real bugs, fix comment regressions in touched code, and judge
whether the diff is minimal repo-fit work or unnecessary AI-generated churn.

## Task

### Part I — Correctness and intent

1. Model behavior from the diff and nearby context.
1. Find bugs, regressions, and behavioral surprises—not style unless it hides a defect.
1. Fix comment regressions locally using the rules below; keep edits minimal.
1. Explain the change in plain language.

### Part II — Fit and minimalism ("AI slop")

Would an experienced maintainer say this belongs here?

1. Architecture and naming match the repo?
1. Reuses existing utilities, error handling, logging, and ownership patterns?
1. Minimal change—no unnecessary layers, classes, or files?
1. New or modified functions with no callers in the repo (search references; note uncertainty for
   dynamic dispatch, plugins, or intentional public API)?
1. Lifecycle, threading, performance, exception-safety, and ABI/API compatibility considered?
1. Tests assert observable behavior, not implementation details?
1. Overall: "This fits here"?

## Required Workflow

1. Diff scope: `origin/main...HEAD` or user equivalent.
1. Read changed code plus enough context to judge behavior—not every unchanged file.
1. For moved or extracted code, compare the source and destination hunks for comment changes, not
   just changed executable behavior.
1. Separate confirmed defects from hypotheses; mark uncertainty explicitly.
1. Fix unambiguous comment issues; do not refactor unrelated code.
1. Give the smallest verification step per bug finding.
1. For Part II, search the repo for callers of new or touched functions; cite concrete repo files,
   patterns, or utilities to reuse.

## Rules

- Evidence from diff and repo beats generic advice.
- Each bug: file, line range, failure scenario, minimal fix, verification step.
- Comment fixes must match post-change behavior.
- Pure moves must preserve comments exactly; if executable code did not change, comment text,
  placement, and presence should not change either. If behavior changed, restore or adjust comments
  that still explain non-obvious behavior, invariants, constraints, compatibility, lifecycle, or
  edge cases.
- Lead with the risky core; scale detail to diff size.
- Name specific simplifications and reuse targets—not vague "could be cleaner."
- Do not invent repo requirements.

## Output Format

Return Markdown with exactly these sections:

### Brief Summary

Two to four plain-language sentences: what changed and why it matters.

### What It Does and Why

Short narrative of behavior, motivation, and how touched pieces interact.

### Bugs and Risks

Numbered list. Per item: **File / lines**, **Severity** (`Critical`/`High`/`Medium`/`Low`),
**Issue**, **Why it matters**, **Suggested fix** (minimal), **How to verify**. Say "None found." if
empty.

### Comment Fixes

Per item: **File / lines**, **Before**, **After**, **Reason**. Say "None." if empty.

### Slop Assessment

#### Slop risks

Concrete churn, over-abstraction, unused never-called functions, or convention mismatches.

#### Concrete simplifications

Specific deletions, inlines, or rewrites without losing behavior.

#### Existing code to reuse

Repo paths, functions, types, or patterns to align with or call.

#### Requires human confirmation

Product intent, compatibility, rollout, or ownership the diff cannot settle.

## Do Not

- Line-by-line walkthroughs when a risk-focused read suffices.
- Findings on formatting, rename-only hunks, or boilerplate unless they hide defects.
- Rewrites beyond comment clarity or confirmed bugs.
- Confident language that hides uncertainty.
- Large refactors when a minimal fix works.

## Quality Bar

- Bug findings are actionable; Brief Summary stands alone.
- Slop items reference this repo—not generic clean-code advice.
- If the change is sound and minimal, say so; do not invent nits.
