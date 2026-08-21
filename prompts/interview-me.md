---
title: Interview Me
type: task-prompt
purpose: Pause uncertain agent work and interview the user through dependency-aware clarification rounds
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

Reach a shared understanding of the intended outcome, approach, rationale, verification strategy,
and next action by asking only the user-answerable decisions that are currently unblocked.

## Task

Pause the task. Review the visible conversation, attached files, tool results, your stated
assumptions, and your last answer or change.

Then interview the user in rounds. Do not continue implementation, debugging, rewriting, or
finalizing until the interview frontier is empty and the user confirms that you have reached a
shared understanding.

## Required Workflow

1. Reconstruct the user's actual goal, the current claimed result, and the decisions still shaping
   the work.
1. Map those decisions as a dependency tree:
   - root decisions define the outcome, success criteria, constraints, or next action
   - child decisions depend on answers to earlier decisions
   - leaves are concrete implementation, verification, wording, or tradeoff choices
1. Check whether the user's intent is clear across:
   - what outcome they want
   - how they expect the work to be approached, constrained, or verified
   - why the outcome matters, when that could reveal a better framing or alternative path
1. Identify the claims, assumptions, missing context, or verification gaps that could make the work
   wrong or incomplete.
1. Separate gaps you can resolve yourself from decisions only the user can make.
1. Resolve self-answerable gaps yourself with the visible conversation, attached files, tools, and
   available environment. If that work is still running, treat it as an unsettled prerequisite and
   ask only the unrelated frontier questions now.
1. If sub-agents are available, dispatch them for independent fact-finding that would otherwise
   block a frontier question. Do not wait for that work before asking unrelated frontier questions.
1. Compute the current frontier: every user decision whose prerequisites are already settled.
1. Ask the whole frontier in one round, and only that frontier. Do not ask a question in the same
   round if its answer depends on another question still open in that round.
1. After each user reply, update the tree, mark settled decisions, recompute the frontier, and ask
   the next round.
1. Stop interviewing only when the frontier is empty.
1. If a question depends on a concrete artifact, ask for that artifact explicitly.

## Rules

- Be candid about uncertainty. Do not claim high confidence merely because the task took a long time
  or because you already produced an answer.
- Prefer specific questions over broad prompts like "anything else?"
- Ask no more than 7 questions in a single round.
- Order each round's questions by how much the answer could change the result.
- Combine closely related uncertainties into one question when that reduces back-and-forth.
- Do not ask for information already present in the conversation, attached files, or tool results.
- Do not ask the user to do inspection that you can safely do yourself with available tools.
- Do not ask the user for facts you can look up. Ask the user for decisions, preferences,
  constraints, approvals, or unavailable artifacts.
- Do not list every possible doubt; focus on decision-changing gaps.
- Ask about the user's underlying reason only when it could change the task framing, priority,
  tradeoffs, or acceptable solution.
- Do not use a generic confidence label. Name the concrete uncertainty or missing input instead.
- Do not reveal hidden chain-of-thought. State observable evidence, assumptions, and gaps only.
- Include a recommended answer for each question when you can make a defensible recommendation from
  the visible context. The recommendation is advisory; the user decides.
- Do not propose fixes, new designs, or next steps unless needed to explain a recommendation or why
  a question matters.
- Do not mix questions with the empty-state response. If you ask even one question, do not include
  `Shared understanding reached. Please confirm before I continue.`
- If the frontier is empty, do not list self-checks, non-questions, or next steps beyond the exact
  confirmation line.

## Output Format

Return exactly one of the following two outputs.

If the current frontier contains user-answerable decisions, return only the current round: a
numbered list of 1-7 questions. Include only questions whose answers would materially change the
work.

```text
Round <n>

1. <question title>: <question body>
   Recommended answer: <your recommended answer>
   Why this matters: <one short sentence>
```

If the frontier is empty, return only this exact line:

```text
Shared understanding reached. Please confirm before I continue.
```
