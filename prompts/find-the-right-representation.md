---
title: Find the Right Representation
type: task-prompt
purpose: Search for formal representations that expose structure and shorten the solution path
targets:
  - ChatGPT
  - Claude
  - Codex
  - Cursor
  - Gemini
  - Generic LLM
scope:
  - problem solving
  - design
  - analysis
---

# Find the Right Representation

## Context

The user has a problem that may be solvable more easily after a change of representation—not after renaming variables, but after a transformation that exposes invariants, locality, bottlenecks, or known theory.

## Goal

Analyze the problem below by searching representations that make the hard part local, constrained, or governed by established tools. End with one primary representation and a solution sketch grounded in it. If other views are complementary, say how they fit—do not blend representations silently in the sketch.

## Inputs

The following section contains the problem to analyze.

<PROBLEM>

## Rules

- Prioritize representations that make the difficult part of the problem local, constrained, or governed by known theory.
- Do not merely rename the problem; search for transformations that expose hidden structure.
- Base structure on the stated problem; label inference explicitly when you extend beyond the text.
- Keep each subsection concise (bullets, not essays).
- Develop only representations that plausibly help; do not survey every framework by default.
- If fewer than three representations are strong candidates, rank those that are and say why others were excluded.

## Required Workflow

### 1. Surface formulation

- Restate the problem clearly.
- What is being asked?
- What would count as a valid solution?

### 2. Core structure

Identify only structure that appears relevant to solving the problem:

- entities
- relations and dependencies
- allowed operations or transformations
- dynamics over time (if any)
- invariants or correctness conditions
- constraints
- scarce resources and bottlenecks
- information available vs missing
- likely failure modes

Then diagnose the likely source of difficulty:

- What makes this problem hard?
- Is the difficulty mainly combinatorial, informational, computational, geometric, probabilistic, strategic, temporal, or mixed?

### 3. Representation search

Use as many of the following lenses as are relevant (skip the rest):

- graph
- state machine
- constraint system
- resource-flow model
- queueing model
- optimization problem
- information-flow model
- algebraic model
- probabilistic or statistical model
- game-theoretic or incentive model
- geometric or spatial model
- type-system or semantic model

For each lens you develop, use this template:

#### Representation: [name]

- **Entities**
- **Relations**
- **Operations**
- **Invariants**
- **What becomes easier?**
- **What becomes harder?**
- **Toolkit imported** (theorems, algorithms, or established theory this view brings in)
- **One plausible solution path**

When possible, complete:

> The problem becomes easier in this representation because …

### 4. Representation ranking

Rank the top three candidates (or fewer if only that many are strong). Compare them on:

- locality of the hard part
- exposed invariant, symmetry, bottleneck, or conservation law
- strength of imported toolkit
- shortest visible solution path

For each ranked representation, explain why it fits and what it unlocks.

### 5. Best representation

Identify the single most useful primary representation. Explain:

- why it is the most natural abstraction
- why it shortens the solution path
- what important structure becomes obvious
- what competing representations hide

Name any tempting but misleading alternatives: what structure they hide and what assumptions they smuggle in.

### 6. Solution sketch

Using the primary representation:

- outline the solution approach
- identify the critical insight
- state what evidence would confirm or falsify this choice of representation
- if complementary representations matter, state how they support the sketch without replacing the primary view

## Output Format

Return Markdown with headings matching sections 1–6 above. Use the representation template in section 3 for each developed lens.

## Quality Bar

- At least one representation must expose structure that was implicit in the surface formulation.
- The best representation must justify why it beats the runners-up on locality, constraints, or known theory—not on familiarity alone.
- Name misleading alternatives when a familiar lens would distort the problem.
- The solution sketch must not smuggle in a different representation without saying so.
