---
title: Interview Me
type: task-prompt
purpose: Pause uncertain agent work and clarify user intent before continuing
targets:
  - ChatGPT
  - Claude
  - Codex
  - Cursor
  - Gemini
  - Generic LLM
scope:
  - agent recovery
  - uncertainty review
  - clarification
  - intent clarification
---

# Interview Me

## Context

You have just completed, nearly completed, or spent significant time on a difficult task. The user
is not fully confident in your result, progress, or direction. They suspect you may be missing
relevant context, carrying an unverified assumption, misunderstanding the user's intent, or running
in circles.

The user wants you to stop defending the work and interview them for the missing information that
would most improve correctness.

## Goal

Expose the smallest useful set of user-answerable questions that would change your understanding of
the intended outcome, approach, rationale, verification strategy, or next action.

## Task

Pause the task. Review the visible conversation, attached files, tool results, your stated
assumptions, and your last answer or change.

Then ask the user direct questions about the gaps that remain. Do not continue implementation,
debugging, rewriting, or finalizing until the user answers, unless no user clarification is needed.

## Required Workflow

1. Reconstruct the user's actual goal and the current claimed result.
1. Check whether the user's intent is clear across:
   - what outcome they want
   - how they expect the work to be approached, constrained, or verified
   - why the outcome matters, when that could reveal a better framing or alternative path
1. Identify the claims, assumptions, missing context, or verification gaps that could make the work
   wrong or incomplete.
1. Separate gaps you can resolve yourself from gaps only the user can answer.
1. Ask only the user-answerable questions whose answers would materially change the work.
1. If a question depends on a concrete artifact, ask for that artifact explicitly.

## Rules

- Be candid about uncertainty. Do not claim high confidence merely because the task took a long time
  or because you already produced an answer.
- Prefer specific questions over broad prompts like "anything else?"
- Ask no more than 7 questions.
- Order questions by how much the answer could change the result.
- Combine closely related uncertainties into one question when that reduces back-and-forth.
- Do not ask for information already present in the conversation, attached files, or tool results.
- Do not ask the user to do inspection that you can safely do yourself with available tools.
- Do not list every possible doubt; focus on decision-changing gaps.
- Ask about the user's underlying reason only when it could change the task framing, priority,
  tradeoffs, or acceptable solution.
- Do not use a generic confidence label. Name the concrete uncertainty or missing input instead.
- Do not reveal hidden chain-of-thought. State observable evidence, assumptions, and gaps only.
- Do not propose fixes, new designs, or next steps unless needed to explain why a question matters.
- Do not mix questions with the empty-state response. If you ask even one question, do not include
  `No user clarification needed.`
- If no user clarification is needed, do not list self-checks, non-questions, or next steps.

## Output Format

Return exactly one of the following two outputs.

If user clarification is needed, return only a numbered list of 1-7 user-answerable questions.
Include only questions whose answers would materially change the work.

```text
1. <question> Why this matters: <one short sentence>
```

If no user-answerable clarification is needed, return only this exact line:

```text
No user clarification needed.
```
