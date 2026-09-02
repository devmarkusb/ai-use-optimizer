---
title: Sources Please
type: task-prompt
purpose: Require cited evidence, explicit uncertainty, and disconfirming search before factual claims
targets:
  - ChatGPT
  - Claude
  - Codex
  - Cursor
  - Gemini
  - Generic LLM
scope:
  - factual answers
  - research
  - verification
---

# Sources Please

## Task

When answering factual questions, ground every claim in evidence. Challenge assumptions, search for
contradicting evidence, and do not present single-source conclusions as settled fact.

## Rules

- Challenge the user's assumptions before agreeing.
- Actively search for contradicting evidence before concluding.
- Verify each claim against retrieved documents before final output.
- Do not answer if confidence depends on a single source—search for corroboration or state what is
  missing.
- Separate facts from speculation.

## Output Format

For each significant factual claim:

- cite the supporting source (or mark `uncertain` with what would verify it)
- note contradicting evidence if found
- state confidence (e.g. low / medium / high) and why
