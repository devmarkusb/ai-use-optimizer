---
title: Explain Code Level 2
type: task-prompt
purpose: Build an architectural mental model of inspected source without line-by-line explanation
targets:
  - ChatGPT
  - Claude
  - Codex
  - Cursor
  - Generic LLM coding agents
scope:
  - code understanding
  - architecture explanation
  - brownfield code
---

# Explain Code Level 2

## Task

Analyze source code as an architect. Build a mental model instead of explaining line by line.

## Output Format

Return Markdown sections for:

1. Purpose: one paragraph.
1. Input → Processing → Output: inputs, main transformations, and outputs. Mark inputs or outputs
   from outside the inspected code as external.
1. Main Components: for each component, list responsibility, collaborators, and important public
   interfaces.
1. Data Flow: how information moves through the system.
1. Control Flow: who starts work, who calls whom, and who decides.
1. External Boundaries: black-box boundaries for external services, operating system interactions,
   databases, files, networking, configuration, environment variables, and user interaction. Mark
   each boundary as `Known`, `Likely`, or `Unknown`.
1. Side Effects: every observable side effect you can identify.
1. Unknowns: everything this analysis cannot determine without inspecting additional code.
1. Next Files To Inspect: if unknowns remain, files or directories to inspect next. For each, state
   why it matters and what question it would answer.

## Rules

- Be explicit about uncertainty.
- Never speculate.
- Only include follow-up inspection targets that materially improve the architecture understanding.
