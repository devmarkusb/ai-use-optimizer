---
title: Don't Understand
type: task-prompt
purpose: Re-explain confusing material from the likely missing prerequisite idea
targets:
  - ChatGPT
  - Claude
  - Codex
  - Cursor
  - Gemini
  - Generic LLM
scope:
  - explanation
  - learning
  - clarification
---

# Don't Understand

## Task

Identify the prerequisite idea, term, assumption, or reasoning step I am likely missing, then
re-explain the confusing material from that point.

## Rules

- Do not assume the hidden premise is understood.
- Make the necessary intermediate steps explicit.
- Keep the explanation proportional to the original material.
- If the missing piece cannot be inferred, ask one focused question.

## Output

`Likely missing piece:` one sentence naming the gap.

`Explanation:` re-explain from that gap onward.
