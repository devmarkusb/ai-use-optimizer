---
title: Explain Pull Request
type: task-prompt
purpose: >
  Explain what a pull request changes, why it exists, and how it is used without implementation
  detail
targets:
  - ChatGPT
  - Claude
  - Codex
  - Cursor
  - Gemini
  - Generic LLM
scope:
  - pull requests
  - branch explanation
  - code understanding
recommended-stage: when you need a concise behavioral explanation before deeper review
---

# Explain Pull Request

## Context

Explain the current branch as a pull request to the repository's `main` branch. Use the appropriate
merge-base diff, normally `origin/main...HEAD` or `main...HEAD`. If the base is missing or may be
stale, state that limitation instead of guessing.

## Goal

Give a technically literate reader a short, usable understanding of what the pull request changes,
why it exists, and how the changed behavior or capability is used. This is an explanation, not a
code review or implementation walkthrough.

## Task

Inspect the diff and only enough surrounding code, tests, documentation, and available pull request
or commit description to establish behavior and intent. Do not edit files or run project artifacts.
Read-only git and file inspection are allowed.

## Output Format

Keep the explanation as short as the pull request allows. Scale detail to the number and
significance of distinct behavioral changes, not to files or lines changed. Stop once the reader can
explain what changes, why it exists, and how it is used. Do not omit material behavior or important
uncertainty merely to stay brief.

Use exactly these sections:

### In One Sentence

State the practical effect of the pull request.

### What Changes

Describe the observable user, developer, or operational behavior. Use a brief before-and-after
comparison when helpful.

### Why

Explain the problem or need the change addresses. Distinguish documented motivation from inference;
say when the motivation cannot be determined from available evidence.

### How It Is Used

State who or what triggers, calls, configures, or encounters the changed behavior. Include one
concrete usage example when evidence supports it. For an internal change, explain its practical
effect and when it takes effect.

### Boundaries and Unknowns

State what remains unchanged and list only unknowns that materially limit the explanation. Say
`None.` if there are none.

## Rules

- Explain behavior and purpose, not implementation mechanics.
- Avoid file-by-file summaries, symbol lists, internal data structures, control-flow detail, and
  architectural inventories unless one detail is essential to explain observable behavior.
- Do not assess bugs, code quality, merge risk, or possible fixes.
- Do not invent motivation, usage, or effects. Label important inference and uncertainty.
- If the pull request has no user-facing effect, explain the developer or operational effect in
  plain language.
- Prefer common language over repository jargon.
