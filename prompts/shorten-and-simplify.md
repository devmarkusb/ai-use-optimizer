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
unscoped pull requests—use a branch-wide code-review prompt for those (in this repo:
`prompts/code-review.md`).

## Goal

Shorten and simplify the scoped input without losing meaning, behavior, correctness, or important
detail. Clarity beats brevity when they conflict.

## Scope

- Process only the file or selection the user named; do not edit anything outside it.
- If the scope is unclear, or the input is more than one file or a diff over roughly **500 changed
  lines**, ask once which single file or line range to process—then stop until answered. Do not skim
  the rest and shorten only comments or easy targets.
- For multiple files, process one file at a time across separate runs unless the user explicitly
  asks for a batch plan listing candidates—not bulk edits.
- State at the start which artifact type you are editing: prose, code, comments only, or mixed.

## Rules

- Do not change semantics, remove important constraints, edge cases, or logic, or oversummarize.
- Keep terminology accurate.
- For **comments**:
  - preserve preconditions, invariants, compatibility notes, lifecycle, and "why not X" reasoning
  - do not shorten away qualifiers (`only when`, `must not`, `legacy`, `thread-safe`, etc.)
  - on pure moves or unchanged behavior, do not rewrite comment text
- For **source code**:
  - preserve behavior exactly
  - prefer simpler structure and less redundancy; avoid unnecessary abstractions
  - keep naming consistent unless improvement is clearly beneficial

## Output

- Return only the improved scoped content (or a minimal diff when editing code in an agent).
- If the input is already close to optimal, say `Already minimal.` and return the original.
- Do not summarize or edit material outside the scope.
