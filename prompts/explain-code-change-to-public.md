---
title: Explain Code Change to Public
type: task-prompt
purpose: >
  Write a public walkthrough of the current branch as it exists, and separately record
  simplification candidates found while explaining
targets:
  - ChatGPT
  - Claude
  - Codex
  - Cursor
  - Gemini
  - Generic LLM coding agents
scope:
  - branch walkthrough
  - public documentation
  - explanation-driven design review
recommended-stage: when a branch is ready to explain but should not be rewritten in the same pass
---

# Explain Code Change to Public

## Context

You are explaining a branch so a public reader can understand the problem, the solution, the
architecture, and the important flows. Reconstructing that explanation is also a design review: if
something is hard to explain for reasons that look intrinsic to the implementation rather than the
problem, record it. Do not mix those observations into the architecture narrative, and do not
implement follow-up simplifications in this pass.

## Goal

Produce a walkthrough of the branch **as it currently exists**, plus separate simplification
findings and, where warranted, small planning documents. Keep explanation, diagnosis, and proposed
redesign distinct.

## Required Workflow

1. Inspect the branch (diff, nearby code, tests, history as needed).
1. Reconstruct the simplest conceptual explanation of the problem, solution, architecture, and
   important flows.
1. While reconstructing, notice implementation-intrinsic complexity. Do not silently fix it.
1. Write the public walkthrough describing the current design.
1. Record meaningful simplification findings separately. For substantial High or Medium confidence
   findings, add focused planning documents.
1. Lightly annotate the walkthrough where a finding affects a described part. Do not rewrite the
   architecture as if the simplification had already happened.
1. Stop. Human review decides which candidates to pursue; implementation and walkthrough updates
   come later.

## Walkthrough

Write `docs/branch-review/README.md` unless the user names another path. Aim it at a public reader
who does not have the session context.

Cover:

- the problem
- the solution
- architecture as it currently exists
- important flows

Use diagrams when they make the current structure clearer. Mark places that may disappear if a
recorded follow-up is accepted, for example:

> Simplification candidate: this intermediate representation may not be necessary. See
> `simplify-intermediate-representation.md`.

## Explanation-driven design review

Treat explaining as review. Typical signals that complexity is in the implementation, not the
problem:

- a concept needs many qualifications or exceptions to explain
- two mechanisms seem to solve essentially the same problem
- an abstraction exists mainly to compensate for another abstraction
- control flow is hard to summarize because responsibility is scattered
- several layers only forward or translate information
- state or ownership is harder than the domain appears to require
- a supposedly important component disappears in a conceptual description
- substantial code seems incidental to the actual solution
- a design decision cannot be justified by a real constraint
- the implementation model differs substantially from the simplest conceptual model
- code added by the branch no longer appears necessary after later changes
- the same invariant is enforced in several places
- a special case could plausibly disappear under a better representation

Classify each finding as one of:

1. **Clearly unnecessary** — can be removed or simplified with very high confidence while preserving
   intended behavior.
1. **Likely simplification opportunity** — a materially simpler design appears possible, but
   implementation or validation is still needed.
1. **Questionable design** — something looks suspicious, but intent or constraints are too unclear
   to recommend a change confidently.

## Simplification findings

Add this section to the walkthrough. Include only meaningful findings; do not manufacture entries.

```markdown
## Potential simplifications discovered while explaining

### <short name>

**Current situation**
What makes the present design unnecessarily difficult to explain or reason about.

**Suspected simpler model**
The simpler conceptual structure that may replace it.

**Why this seems possible**
Evidence from the branch, surrounding code, tests, or architecture.

**Confidence**
High | Medium | Low

**Impact**
Delete code | simplify design | reduce state | remove indirection | unify mechanisms | other

**Needs validation**
What must be checked before changing it.
```

## Planning documents

For every substantial High or Medium confidence finding, add a sibling file such as
`docs/branch-review/simplify-<topic>.md`. Keep it at design level. Do not implement it.

Each planning document must include:

- **Observation** — what explaining the branch surfaced
- **Current model** — relevant structure and why it is complicated
- **Proposed model** — simpler target; use a Mermaid diagram when the structural difference matters
- **Expected simplification** — qualitative: components, states, branches, duplicated logic,
  interfaces, conversions, ownership, code volume. Do not invent LOC estimates unless they can be
  derived reasonably
- **Behavioral invariants** — what must remain true
- **Validation** — tests, comparisons, benchmarks, or manual checks for equivalence
- **Implementation sketch** — short sequence of changes
- **Risks / unresolved questions** — anything that blocks high confidence

## Output Format

Return:

1. Path to the walkthrough.
1. Paths to any planning documents, or `None.`
1. A one-paragraph public summary of the branch as it exists.
1. Finding count by confidence (High / Medium / Low), or `None.`
