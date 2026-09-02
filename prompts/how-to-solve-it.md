---
title: How to Solve It
type: task-prompt
purpose: Apply Polya-style heuristics to understand a problem and brute-force a solution plan
targets:
  - ChatGPT
  - Claude
  - Codex
  - Cursor
  - Gemini
  - Generic LLM
scope:
  - problem solving
  - analysis
  - planning
---

# How to Solve It

## Context

The user has a problem that needs disciplined problem solving before execution. Use the first two
parts of George Polya's method from *How to Solve It*: understand the problem and devise a plan.

## Goal

Turn the problem statement into a clear understanding and a justified plan by brute-force trying a
full list of problem-solving heuristics. Stop after planning unless the user explicitly asks for the
solution to be carried out.

## Inputs

The following sections contain the problem to analyze. Optional sections may be empty. Or the user
might only provide the problem, and you will need to distill the remaining placeholders from that.

### Problem

\<PROBLEM>

### Known

\<KNOWN>

### Unknown

\<UNKNOWN>

### Conditions

\<CONDITIONS>

## Required Workflow

### 1. Understand the problem

Answer explicitly:

- What is the unknown? What are the data? What are the conditions?
- Is it possible to satisfy the conditions? Are they sufficient to determine the unknown, or
  insufficient, redundant, or contradictory?
- Would a figure, notation, example, or decomposition help?
- Can the parts of the conditions be written down separately?

State assumptions explicitly when the input is incomplete.

### 2. Brute-force heuristic search

Try every heuristic in the toolbox. For each one, write a concise result:

- **Use** when the heuristic gives a plausible route, simplification, analogy, or test.
- **Weak** when it gives only a small clue.
- **Not applicable** when it does not fit, with one short reason.

After the full pass, select the best strategy or combination of strategies. Explain why it beats the
alternatives.

## Heuristic Toolbox

Try every item below during planning.

- **Have you seen it before?** — the same problem, or one in slightly different form?
- **Do you know a related problem?** — a theorem, pattern, or solved problem whose result or method
  could be reused?
- **Look at the unknown** — what familiar problem has the same or a similar unknown?
- **Analogy** — is there an analogous problem in a simpler or better-understood domain?
- **Could you restate the problem?** — restate it, then restate it differently again.
- **Go back to definitions** — replace terms by their definitions.
- **Draw a figure** — diagram, sketch, or visual model.
- **Introduce suitable notation** — variables, tables, formal structure.
- **Setting up equations** — translate conditions into equations or formal constraints.
- **Decomposing and recombining** — split into parts; solve and recombine.
- **Separate the parts of the condition** — treat each condition part on its own.
- **Auxiliary problem** — is there a more accessible related problem to solve first?
- **Auxiliary elements** — introduce a helper construct that enables reuse of a known method.
- **Specialization** — try extreme, degenerate, or concrete special cases.
- **Generalization** — would the more general problem be easier (inventor's paradox)?
- **Variation of the problem** — change the unknown, the data, or both so they are nearer to each
  other.
- **Drop part of the condition** — keep part, drop the rest; how far is the unknown then determined,
  and how can it vary?
- **Solve part of the problem** — can you solve only a part, or a weaker version?
- **Working backward** — start from the goal and reason toward the data.
- **Reductio ad absurdum / indirect approach** — assume the opposite and derive a contradiction.
- **Induction** — find a pattern from small cases; consider mathematical induction.
- **Symmetry** — exploit symmetry or interchangeable roles in the problem.
- **Test by dimension** — sanity-check candidate relations by units, dimensions, or orders of
  magnitude.
- **Derive something from the data** — what follows directly from the data? What other data would
  determine the unknown?
- **Did you use everything?** — all the data, the whole condition, every essential notion?
- **Examine your guess** — make a guess explicit, then test it.
- **Can you check the result?** — how would the candidate plan's result be verified or derived
  differently?

## Rules

- Stop after understanding and planning; do not carry out the final plan unless the user asks.
- Try the full heuristic list even when many items are weak or not applicable.
- Keep each heuristic trial concise; do not write an essay for every item.
- Do not force a mathematical framing on practical, strategic, or design problems.
- Ask for clarification only when missing information blocks meaningful planning; otherwise proceed
  with stated assumptions.
- If the problem is contradictory or underspecified, explain the issue before proposing a plan.

## Output Format

Return Markdown with exactly these sections:

### Understanding

- Unknown:
- Data:
- Conditions:
- Sufficiency:
- Assumptions:
- Useful representation:

### Heuristic Trial Log

One bullet per heuristic from the toolbox, in order:

- **Heuristic name:** `Use` / `Weak` / `Not applicable` - concise result.

### Plan

- Selected strategy:
- Reason:
- Relevant heuristics used:
- Rejected strategies:
- First step to carry out if the user asks:

## Quality Bar

- The unknown, data, and conditions are explicit before planning.
- Every toolbox heuristic appears in the trial log.
- The selected plan follows from the trial log rather than appearing from nowhere.
- The output stops at a plan and does not solve the problem unless explicitly requested.
