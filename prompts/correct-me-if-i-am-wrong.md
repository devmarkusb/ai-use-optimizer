---
title: Correct Me If I Am Wrong
type: task-prompt
purpose: Check a stated model by solving independently, then naming its errors and gaps
targets:
  - ChatGPT
  - Claude
  - Codex
  - Cursor
  - Gemini
  - Generic LLM
scope:
  - reasoning check
  - assumption review
  - error detection
---

# Correct Me If I Am Wrong

## Task

Solve the question below independently first, then compare your conclusion with my model and point
out errors, missing pieces, and unjustified assumptions.

My current model (treat as untrusted):

\<MODEL>

## Rules

- Do not assume my model is correct; solve from the question alone before comparing.
- Distinguish errors from reasonable inference; say what evidence is missing.
- If the question is absent, say so and stop instead of reviewing the model alone.

## Output

- `Independent conclusion:` your answer with one-sentence reasoning.
- `Verdict:` `Agree` or `Disagree`, then the decisive reason in one sentence.
- `Corrections:` errors, missing pieces, and unjustified assumptions with concrete references.
