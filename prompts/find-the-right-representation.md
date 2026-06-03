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

Analyze the problem below by searching representations that make the hard part local, constrained, or governed by established tools. End with one best representation and a solution sketch grounded in that representation only.

## Inputs

The following section contains the problem to analyze.

<PROBLEM>

## Rules

- Prioritize representations that make the difficult part of the problem local, constrained, or governed by known theory.
- Do not merely rename the problem; search for transformations that expose hidden structure.
- Base structure on the stated problem; label inference explicitly when you extend beyond the text.
- Keep each subsection concise (bullets, not essays).
- For a framework that is a poor fit, write **Not applicable** and one sentence why—do not invent structure to fill the template.
- If fewer than three representations are strong candidates, rank those that are and say why others were excluded.

## Required Workflow

### 1. Surface formulation

- Restate the problem clearly.
- What is being asked?
- What would count as a valid solution?

### 2. Core structure

Identify only structure that appears relevant to solving the problem:

- entities
- relations
- operations
- dynamics over time
- invariants
- constraints
- scarce resources
- information structure
- likely failure modes

### 3. Representation search

Consider the problem under each framework below. For each one, either complete the template or mark **Not applicable** with one sentence.

Frameworks:

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

For each framework you develop, use this template:

#### Representation: [name]

- **Entities**
- **Relations**
- **Operations**
- **Invariants**
- **What becomes easier?**
- **What becomes harder?**
- **Toolkit imported** (established methods, algorithms, or theory this view brings in)
- **One plausible solution path**

When possible, complete:

> The problem becomes easier in this representation because …

### 4. Locality analysis

For each strong candidate representation (not marked Not applicable):

- What becomes local rather than global?
- What can be checked using only a small neighborhood of information?
- What dependencies disappear?
- Which bottleneck becomes visible?

### 5. Representation ranking

Rank the top three representations (or fewer if only that many are strong). For each, explain:

- why it fits
- what toolkit it unlocks
- what key invariant, symmetry, bottleneck, or conservation law it exposes

### 6. Best representation

Identify the single most useful representation. Explain:

- why it is the most natural abstraction
- why it shortens the solution path
- what important structure becomes obvious
- what competing representations hide

### 7. Solution sketch

Using only the best representation:

- outline the solution approach
- identify the critical insight
- state what evidence would confirm this representation is correct
- state what evidence would falsify it

## Output Format

Return Markdown with headings matching sections 1–7 above. Use the representation template in section 3 for each developed framework.

## Quality Bar

- At least one representation must expose structure that was implicit in the surface formulation.
- The best representation must justify why it beats the runners-up on locality, constraints, or known theory—not on familiarity alone.
- The solution sketch must not smuggle in a different representation without saying so.
