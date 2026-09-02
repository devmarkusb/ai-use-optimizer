---
title: Simplify Large Code Changes
type: task-prompt
purpose: Diagnose whether a large AI-assisted implementation can be replaced by a smaller coherent design
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
  - redesign
  - large diffs
recommended-stage: after a large implementation is believed correct but may be overbuilt
---

# Simplify Large Code Changes

## Context

You are reviewing a feature that evolved through many iterations of AI-assisted development. The
current implementation is believed to be correct, tested, and reasonably clean locally, but it has
grown to a suspiciously large number of lines of new code.

The user suspects the same required behavior may admit a substantially smaller implementation,
possibly by an order of magnitude. Do not assume that suspicion is correct. Your job is to determine
whether it is.

## Goal

Independently derive the smallest conceptually coherent implementation of the required behavior,
using the existing implementation only as evidence about requirements, edge cases, constraints, and
semantics.

Do not refactor, clean up, or edit code yet. Report the redesign case first and wait for approval.

## Core Principle

Separate:

1. essential problem complexity,
1. accidental complexity introduced by the current design,
1. complexity caused by requirements that may be unnecessary or overgeneralized.

Do not preserve an abstraction, subsystem, type hierarchy, layer, cache, intermediate
representation, configuration mechanism, compatibility mechanism, or extension point merely because
it exists. Every major piece of machinery must justify its existence from actual required semantics.

## Required Workflow

### 1. Recover the real problem

Inspect the repository, tests, call sites, history or diff if available, and current implementation.

Construct a compact semantic specification:

- What externally observable behavior must exist?
- What inputs, outputs, state, and side effects exist?
- What invariants must hold?
- What edge cases are actually required?
- What performance requirements are real?
- What compatibility constraints are real?
- Which behavior is explicitly tested?
- Which behavior is merely an artifact of the current implementation?

Express the problem independently of the current architecture. Do not propose code changes yet.

### 2. Find the irreducible model

Ask: "If this functionality did not exist and I had to implement it today from the semantic
specification alone, what representation would make the problem almost trivial?"

Look for opportunities to replace machinery with a better representation:

- control flow to data
- implicit relationships to a graph
- temporal coupling to an explicit state machine
- procedural validation to constraints
- duplicated special cases to one general rule
- object hierarchies to values and composition
- distributed mutable state to explicit state transformation
- repeated computation paths to a shared semantic operation
- multiple representations to one canonical representation
- framework or layer machinery to direct functions and data structures

Search for the smallest set of concepts from which the required behavior follows naturally.

### 3. Account for complexity

Explain where the current size comes from. When counting LOC, count code files only for the main
implementation estimate. Separate production/source code from tests, generated files, fixtures,
documentation, build/config files, and diagnostics unless one of those artifacts is itself the
feature being simplified.

Group substantial portions into categories such as:

- essential domain logic
- duplicated semantics
- adapters and conversions
- abstraction scaffolding
- defensive machinery
- generalized infrastructure
- compatibility code
- state synchronization
- caching or performance machinery
- error handling
- tests, debugging, or diagnostics
- generated or repetitive code

For each major subsystem, answer: "What requirement would become impossible or materially worse if
this subsystem disappeared?"

Look especially for large subsystems, abstractions, compatibility paths, or generalized mechanisms
that serve only one narrow or marginal use case. If deleting them would lose behavior that is rarely
used, weakly justified, or plausibly acceptable to drop, call that out explicitly as a tradeoff
instead of preserving the machinery by default.

If there is no strong answer, treat it as accidental complexity. Also identify complexity
amplification: early design decisions that force downstream types, adapters, branches,
synchronization rules, or special cases.

### 4. Design independently

Design the implementation you would choose if the current implementation did not constrain you.

Prefer:

- few concepts
- few representations
- explicit data
- pure transformations where practical
- direct control and data flow
- composition
- reuse of existing repository facilities
- deletion over abstraction

Large-scale replacement is allowed if it produces a materially simpler system without losing
required behavior. Do not optimize for preserving the current diff, and do not introduce a new
framework merely to eliminate the old one.

### 5. Try to falsify the redesign

Before recommending a simpler design, aggressively search for reasons it cannot work. Compare it
against:

- every required behavior
- important tests
- edge cases
- performance constraints
- lifetime or ownership requirements
- concurrency
- compatibility
- failure handling

Distinguish genuine irreducible complexity, complexity that only exists because of the current
architecture, and speculative future requirements.

If the current size is substantially justified, say so. Prefer a correct conclusion that the code
cannot be radically reduced over an unjustified simplification.

## Rules

- Follow semantics, not existing architecture.
- Treat tests as evidence, not necessarily as the complete specification.
- Trace abstractions down to the requirement that supposedly necessitates them.
- Prefer removing concepts over merely shortening code.
- Do not count moving code behind helpers, or replacing explicit code with opaque generic machinery,
  as simplification.
- Do not sacrifice correctness merely to reduce LOC.
- Do not assume the user's belief that the implementation should be 10x smaller is correct.

The goal is not minimum LOC. The goal is minimum conceptual machinery required by the actual
problem.

## Output Format

Return Markdown with exactly these sections:

### 1. Semantic Core

The smallest precise description of what the feature actually does.

### 2. Complexity Diagnosis

Why the current implementation requires approximately its current size. Identify the largest sources
of accidental complexity and their root causes.

### 3. Minimal Architecture

Describe the independently derived design. Make its central representation and invariants explicit.

### 4. Deletion Map

For each major existing subsystem, choose **KEEP**, **COLLAPSE**, **REPLACE**, or **DELETE** with a
short justification. For **COLLAPSE** or **DELETE** candidates, name any marginal behavior that
would be lost and whether the tradeoff appears acceptable, uncertain, or unacceptable.

### 5. Estimated Implementation Size

Give a realistic range, not false precision.

Example:

```text
current: ~20k LOC
plausible redesign: 3-5k LOC
lower bound: ~2k LOC
```

Explain what prevents further reduction.

### 6. Semantic Equivalence Risks

List anything the redesign might accidentally lose.

### 7. Verdict

Choose one:

- **A.** The implementation is fundamentally justified at roughly its current complexity.
- **B.** Moderate simplification is possible.
- **C.** A substantially smaller architecture is possible.
- **D.** The current architecture is solving a harder problem than the actual requirements require.

State why.
