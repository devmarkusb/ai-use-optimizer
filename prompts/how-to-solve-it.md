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

## Task

Act as a structured problem-solving partner. Clarify what is being asked, identify the data and
conditions, try the full heuristic toolbox, and choose a practical solution strategy.

## Required Workflow

### 1. Understand the problem

Answer explicitly:

- What is the unknown?
- What are the data?
- What are the conditions?
- Is it possible to satisfy the conditions?
- Are the conditions sufficient to determine the unknown?
- Are they insufficient, redundant, contradictory, or uncertain?
- Would a figure, notation, example, or decomposition help?
- Can the different parts of the conditions be written down separately?

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

- Analogy
- Auxiliary Elements
- Auxiliary Problem
- Bolzano
- Bright Idea
- Can You Check the Result?
- Can You Derive the Result Differently?
- Can You Use the Result?
- Carrying Out
- Condition
- Contradictory
- Corollary
- Could You Derive Something Useful from the Data?
- Could You Restate the Problem?
- Decomposing and Recombining
- Definition
- Descartes
- Determination, Hope, Success
- Diagnosis
- Did You Use All the Data?
- Do You Know a Related Problem?
- Draw a Figure
- Examine Your Guess
- Figures
- Generalization
- Have You Seen It Before?
- Here Is a Problem Related to Yours and Solved Before
- Heuristic
- Heuristic Reasoning
- If You Cannot Solve the Proposed Problem
- Induction and Mathematical Induction
- Inventor's Paradox
- Is It Possible to Satisfy the Condition?
- Leibnitz
- Lemma
- Look at the Unknown
- Modern Heuristic
- Notation
- Pappus
- Pedantry and Mastery
- Practical Problems
- Problems to Find, Problems to Prove
- Progress and Achievement
- Puzzles
- Reductio ad Absurdum and Indirect Proof
- Redundant
- Routine Problem
- Rules of Discovery
- Rules of Style
- Rules of Teaching
- Separate the Various Parts of the Condition
- Setting Up Equations
- Signs of Progress
- Specialization
- Subconscious Work
- Symmetry
- Terms, Old and New
- Test by Dimension
- The Future Mathematician
- The Intelligent Problem-Solver
- The Intelligent Reader
- The Traditional Mathematics Professor
- Variation of the Problem
- What Is the Unknown?
- Why Proofs?
- Wisdom of Proverbs
- Working Backward

## Planning Questions

Use these questions while applying the toolbox:

- Have you seen the problem before?
- Have you seen the same problem in a slightly different form?
- Do you know a related problem?
- Do you know a theorem, pattern, or method that could be useful?
- Looking at the unknown, what familiar problem has the same or a similar unknown?
- Is there a related solved problem whose result or method could be reused?
- Should you introduce an auxiliary element to make that reuse possible?
- Could you restate the problem?
- Could you restate it differently again?
- Should you go back to definitions?
- If you cannot solve the proposed problem, what related problem can you solve first?
- Is there a more accessible related problem?
- Is there a more general, more special, or analogous problem?
- Can you solve only part of the problem?
- What happens if you keep part of the condition and drop the rest?
- How far is the unknown then determined, and how can it vary?
- Can you derive something useful from the data?
- Can you think of other data that would determine the unknown?
- Can you change the unknown, the data, or both so they are nearer to each other?
- Did you use all the data?
- Did you use the whole condition?
- Have you accounted for all essential notions involved in the problem?

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
