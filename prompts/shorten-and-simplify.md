---
title: Shorten and Simplify
type: task-prompt
purpose: Shorten scoped text or source code without losing meaning or behavior
targets:
  - ChatGPT
  - Claude
  - Codex
  - Cursor
  - Gemini
  - Generic LLM
scope:
  - text
  - source code
  - single file
  - selection
---

# Shorten and Simplify

## Context

Use this prompt on a **scoped** input: one file, one pasted section, or one prose artifact (PR
description, comment block, doc section). It is not for whole branches, large multi-file diffs, or
unscoped pull requests.

If the user attaches more than one file or a diff larger than roughly **500 changed lines**, stop
and ask which single file or line range to process first. Do not skim the rest and shorten only
comments or easy targets.

For branch-wide review, comment regression fixes, or repo-fit judgment, use `prompts/code-review.md`
instead.

## Goal

Shorten and simplify the scoped input without losing meaning, behavior, correctness, or important
detail.

## Scope

Process only what the user scoped:

- **Default:** one file or one explicit selection the user named.
- **If scope is unclear:** ask once which file, artifact, and whether to touch code, comments, or
  prose only—then stop until answered.
- **Do not** edit files outside the named scope.

State at the start which artifact type you are editing: prose, code, comments only, or mixed.

## Goals

- Reduce unnecessary length
- Preserve all essential information and functionality
- Improve clarity and readability
- Make the result easier to understand
- Avoid changing semantics

## Rules

- Do not remove important constraints, edge cases, or logic
- Do not oversummarize
- Keep terminology accurate
- Clarity beats brevity when they conflict
- For **comments**:
  - preserve preconditions, invariants, compatibility notes, lifecycle, and "why not X" reasoning
  - do not shorten away qualifiers (`only when`, `must not`, `legacy`, `thread-safe`, etc.)
  - on pure moves or unchanged behavior, do not rewrite comment text
- For **source code**:
  - preserve behavior exactly
  - prefer simpler structure and less redundancy
  - keep naming consistent unless improvement is clearly beneficial
  - avoid unnecessary abstractions
- If the input is already close to optimal, say so and return it unchanged or with minimal edits

## Process

1. Confirm scope (file path, line range, artifact type). If too large or ambiguous, ask and stop.
1. Detect redundancy, verbosity, repetition, or unclear structure within that scope only.
1. Compress and simplify where possible without dropping essential detail.
1. Preserve meaning and intent completely.
1. Return only the improved result for the scoped input.

For multiple files, process **one file at a time** across separate runs unless the user explicitly
asks for a batch plan listing candidates—not bulk edits.

## Output

- Return only the improved scoped content (or a minimal diff when editing code in an agent).
- If unchanged, say `Already minimal.` and return the original.
- Do not summarize or edit material outside the scope.
