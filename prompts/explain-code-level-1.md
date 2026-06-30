---
title: Explain Code Level 1
type: task-prompt
purpose: Give a short, correct intuition for what an inspected code subtree exists to do
targets:
  - ChatGPT
  - Claude
  - Codex
  - Cursor
  - Generic LLM coding agents
scope:
  - code understanding
  - quick explanation
  - brownfield code
---

# Explain Code Level 1

## Task

Analyze a source code subtree and produce the shortest explanation that gives a correct intuition
for what the code exists to do.

## Output Format

Keep the answer under 250 words. Include:

1. One sentence: "This code is responsible for ..."
1. Input → Processing → Output: 3-6 bullets.
1. Metaphor: an everyday analogy that preserves important relationships and is simple enough for a
   young child to roughly understand.
1. Main moving pieces: only the major components, modules, or classes.
1. Black boxes: what is not understood from the inspected code, including external inputs, hidden
   dependencies, and assumptions.
1. Next files to inspect: if black boxes remain, the smallest files or directories to inspect next,
   with the uncertainty each would likely resolve.

## Rules

- Avoid implementation details.
- Do not fill black boxes with guesses.
