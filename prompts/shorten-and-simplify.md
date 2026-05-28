---
title: Shorten and Simplify
type: task-prompt
purpose: Shorten text or source code without losing meaning or behavior
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
---

# Shorten and Simplify

Your task is to shorten and simplify the provided text or source code without losing meaning, behavior, correctness, or important detail.

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
- For source code:
  - preserve behavior exactly
  - prefer simpler structure and less redundancy
  - keep naming consistent unless improvement is clearly beneficial
  - avoid unnecessary abstractions

## Process

1. Detect redundancy, verbosity, repetition, or unclear structure
2. Compress and simplify where possible
3. Preserve meaning and intent completely
4. Return only the improved result

If the original is already close to optimal, say so and make only minimal improvements.
