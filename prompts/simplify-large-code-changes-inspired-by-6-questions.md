---
title: Simplify Large Code Changes with Six Questions
type: task-prompt
purpose: Find accidental complexity in a large repository or changeset by separating independent concerns
targets:
  - ChatGPT
  - Claude
  - Codex
  - Cursor
  - Gemini
  - Generic LLM
scope:
  - code review
  - architecture
  - refactor planning
  - large diffs
recommended-stage: when a large implementation may be correct but over-entangled
---

# Simplify Large Code Changes with Six Questions

## Context

You are reviewing a large codebase or changeset for accidental complexity.

Use Rich Hickey-style decomposition questions as an analysis tool, not as a checklist to
mechanically answer for every function. The objective is to find places where independent concerns
have become entangled and decide whether the implementation can be made materially simpler.

Inspect the repository or changeset first. Build enough understanding of the relevant architecture,
data flow, state, ownership, and control flow before proposing changes.

## Task

Find the highest-value simplification candidates: places where independent concerns have been
combined unnecessarily and could be separated without losing required behavior.

For each substantial subsystem or cluster of related changes, use these questions to detect
conflation:

- What: What information, values, state, rules, or transformations actually exist?
- Who: Which component owns each piece of state, performs each decision, or has authority to mutate
  something?
- When: What depends on ordering, timing, phases, initialization, callbacks, retries, or prior
  actions?
- Where: Which concerns are tied to a particular process, object, thread, layer, storage location,
  or architectural boundary?
- Why: Which constraints are essential domain requirements, and which exist only because of the
  current implementation?
- How: Which mechanisms implement the required behavior, and are those mechanisms unnecessarily
  coupled to the semantics?

## Required Workflow

### 1. Map

Identify the major subsystems touched by the changes and the important flows between them. For a
large repository, work hierarchically rather than function by function.

### 2. Find Knots

Locate a small number of places where several independent concerns intersect. Prioritize findings by
expected simplification value, not by stylistic cleanliness.

Look especially for unnecessary combinations such as:

- state ownership plus business behavior
- identity plus value
- data plus control flow
- computation plus execution timing
- rule or policy plus mechanism
- lifecycle plus ordinary behavior
- topology or location plus semantics
- mutation plus observation
- error handling plus mainline computation
- optimization or caching plus correctness
- representation plus domain meaning

### 3. Model

For each promising knot, reconstruct the essential domain model without reference to the current
implementation. State the values, state transitions, constraints, ownership, and information flow
that are actually necessary.

### 4. Compare

Compare that model with the implementation and identify accidental machinery. Explain concrete
structural costs such as extra states, ordering constraints, duplicated knowledge, hidden
dependencies, wider interfaces, branching, synchronization, or ownership ambiguity.

### 5. Simplify

Propose the smallest high-confidence refactoring that tests the simplification. Identify behavior
that must remain invariant, estimate whether the change genuinely reduces total complexity or merely
moves it elsewhere, and flag unclear domain intent for a human decision.

## Rules

- Inspect before proposing.
- Do not attempt a wholesale rewrite merely because a cleaner architecture can be imagined.
- Do not assume more classes, layers, interfaces, patterns, or helper functions mean simpler code.
- Judge simplicity by the number of independent concepts a programmer must understand at once.
- Do not count moving code behind helpers as simplification.
- Do not count replacing explicit code with opaque generic machinery as simplification.
- Prefer removing concepts over merely shortening code.
- Do not sacrifice correctness to reduce apparent complexity.
- When analyzing a changeset, pay special attention to complexity introduced by the change itself:
  new state, branches, modes, ordering constraints, duplicated concepts, representations, lifecycle
  requirements, cross-layer knowledge, and compatibility scaffolding.

The important question throughout is not "can this code be made prettier?" but: "What independent
things have been combined here, and what would the system look like if they were allowed to vary
independently?"

## Output Format

Return Markdown with these sections:

### 1. Simplification Map

A short description of the essential model of the affected system.

### 2. Highest-Value Complexity Knots

Findings ordered by expected payoff.

### 3. Knot Analysis

For each knot:

- current entanglement
- Who/What/When/Where/Why/How dimensions involved
- simpler model
- concrete refactoring
- preserved invariants
- confidence
- unresolved questions

### 4. Necessary Complexity

Things that look complicated but should probably remain as they are, with an explanation of why
simplifying them would merely relocate or hide necessary complexity.

### 5. Overall Assessment

Estimate whether the code is close to irreducible domain complexity, moderately overcomplicated, or
structurally much more complicated than the underlying problem.
