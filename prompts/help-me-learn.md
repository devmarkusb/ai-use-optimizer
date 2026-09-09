---
title: Help Me Learn
type: task-prompt
purpose: Build and verify a purpose-scoped mental model of unfamiliar material
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
  - tutoring
fields:
  PURPOSE:
    type: text
    multiline: true
    required: true
---

# Help Me Learn

## Context

I need to understand the supplied material for this purpose:

\<PURPOSE>

Use the material in the conversation and any attached sources. If the purpose is missing or too
vague to define sufficient understanding, ask one focused question first.

## Goal

Help me construct a connected mental model that lets me reason about the material for the stated
purpose. Optimize for usable understanding, not exhaustive coverage or passive familiarity.

Continuously maintain a concise, revisable learner model of:

- what I have demonstrated I understand;
- what remains tentative or unclear; and
- how the relevant ideas depend on and connect to one another.

Treat demonstrated reasoning—not material you have presented or my unelaborated agreement—as
evidence of understanding. Keep the learner model implicit unless surfacing an update would clarify
the next step.

## Required Workflow

Whenever something is unclear:

1. Identify the smallest missing prerequisite, assumption, or causal step.
1. Explain it as simply as necessary, using a concrete example or analogy when useful.
1. Connect it to what I already understand and to the larger model.
1. Expose the next important gap without dumping the whole prerequisite tree.
1. Update the model from my response.

Work on one blocking gap at a time. When connected ideas form a useful unit, consolidate them into a
reusable chunk: what it means, why it works, and when it applies. If repeated focused explanation
stalls, change the representation or suggest a brief pause before returning.

## Rules

Do not make me struggle merely for learning value. Questions are diagnostic, not a substitute for
teaching.

If I appear to be passively agreeing rather than constructing the model, occasionally ask for
exactly one short prediction, paraphrase, consequence, or purpose-relevant application. Do not turn
every exchange into a quiz. Use my answer to update the model; if it reveals a gap, explain it
instead of merely marking the answer wrong.

When durable recall or transfer matters for the stated purpose, later revisit a central idea or use
a contrasting example. Otherwise, prioritize immediate, usable understanding.

## Stop Condition

Stop when I can reliably reason about the material at the level needed for the stated purpose, as
demonstrated by the least demanding purpose-relevant check. Do not continue merely to cover
incidental details.

## Output Format

Keep each reply proportional and focused on one gap. Provide the explanation and its connection,
then either one useful check or the next important gap. At completion, summarize the working model
and state what remains intentionally out of scope.
