---
title: Fix Bugs
type: task-prompt
purpose: Audit an AI-developed codebase for real correctness bugs, fix clear ones, and surface ambiguity
targets:
  - Codex
  - Claude Code
  - Cursor
  - Generic LLM coding agents
scope:
  - brownfield
  - correctness
  - whole-repository
---

# Fix Bugs

You are performing a repository-wide correctness audit of an AI-developed codebase.

The repository has evolved rapidly over several weeks. There is a large amount of code, and the
human maintainer no longer trusts that all implemented behavior is correct.

Your objective is:

1. infer what the system is supposed to do,
1. find as many real correctness bugs as reasonably possible,
1. fix bugs when the intended behavior is sufficiently clear,
1. avoid speculative rewrites,
1. explicitly identify cases where correctness depends on an ambiguous product/design decision,
1. leave the repository in a measurably more trustworthy state.

## Ground truth hierarchy

Do not assume the current implementation is correct.

Infer intended behavior using this priority order:

1. explicit requirements, specifications, design documents, architecture documents, ADRs, README
   files
1. externally visible API contracts and documented invariants
1. tests that clearly encode intentional behavior
1. call-site expectations and cross-component invariants
1. comments
1. current implementation

Treat tests as evidence, not absolute truth. A test may encode an existing bug.

When sources disagree, do not silently choose one. Record the conflict.

## Phase 1 — Understand the system before editing

Inspect the repository broadly before making fixes.

Build a concise semantic model containing:

- major components and their responsibilities
- important data structures and invariants
- state machines and legal transitions
- ownership and lifetime assumptions
- persistence and serialization contracts
- concurrency model
- error-handling model
- external API/protocol contracts
- security boundaries
- important numerical or domain constraints
- assumptions made between modules

Read the available technical/design documentation and compare it against the actual implementation.

Identify areas where the implementation appears to have drifted from the design.

Do not spend effort documenting trivial code structure. Focus on semantics and invariants relevant
to correctness.

## Phase 2 — Construct a bug-search map

Before fixing individual issues, identify where bugs are most likely to exist.

Prioritize:

- duplicated implementations of the same concept
- code paths added recently or repeatedly modified
- TODO/FIXME/workaround/hack comments
- error handling and cleanup paths
- boundary conditions
- empty/null/zero/maximum cases
- integer overflow, truncation, signedness, conversions
- ownership, lifetime, dangling references, resource leaks
- concurrency, races, locking, atomics, reentrancy
- invalid state transitions
- caching and stale-state bugs
- persistence/schema/version compatibility
- parsing and malformed input
- serialization/deserialization asymmetry
- retry/idempotency behavior
- partial failures
- exception/error propagation
- API preconditions and postconditions
- disagreement between callers and callees
- code whose complexity is disproportionate to its apparent responsibility
- branches that appear unreachable or insufficiently tested
- behavior described in design documents but not enforced in code

Look for bugs across component boundaries, not only inside individual functions.

## Phase 3 — Actively try to falsify the implementation

Do not merely review code stylistically.

For every important subsystem, ask:

- What must always be true?
- Where is that invariant established?
- Where can it be violated?
- What assumptions does this function make about its callers?
- Are those assumptions actually guaranteed?
- What happens at boundaries and degenerate inputs?
- What happens after partial failure?
- What happens when operations are repeated?
- What happens when execution is interrupted?
- Can two independently reasonable components disagree about representation or state?
- Does the implementation match the design documentation in all semantically important cases?

Search for concrete counterexamples.

Prefer evidence-producing methods where practical:

- run existing tests
- add focused regression tests
- enable compiler warnings
- run sanitizers
- run static analysis
- run linters that can detect correctness issues
- use property-based or fuzz tests where they have high leverage
- test boundary values and invalid inputs
- compare alternate implementations when two paths should be equivalent
- check round-trip properties
- check invariants before and after transformations

Do not run expensive tools blindly across the entire repository when a targeted run would be more
informative.

## Phase 4 — Classify every suspected bug

For each finding, classify it before changing code.

### A. Confirmed bug

Use this classification when there is strong evidence that current behavior violates an intended
invariant or explicit contract.

Examples of strong evidence:

- contradicts specification
- demonstrably violates an invariant
- causes undefined behavior
- produces an incorrect result for a concrete input
- contradicts clearly intentional tests or API guarantees
- leaks/corrupts resources or state
- creates a race or invalid lifetime
- caller and callee contracts are objectively incompatible

Action:

- fix it
- add or improve a regression test where appropriate
- verify the fix

### B. Highly probable bug

Use this when evidence strongly suggests a defect, but intent is not formally documented.

Action:

- investigate nearby code, callers, history if available, tests, and docs
- if one interpretation overwhelmingly fits the system, fix it and clearly record the assumption
- otherwise escalate to the human

### C. Ambiguous behavior / design question

Use this when two or more behaviors are plausible and choosing one would encode a product or
architecture decision.

Action:

- do not guess
- formulate a precise question for the human
- include:
  - the relevant code/design context
  - the competing interpretations
  - consequences of each
  - your recommended interpretation, if any
  - whether work can safely continue without the answer

### D. Suspicious but unproven

Use this for code that looks wrong but lacks enough evidence.

Action:

- do not “fix” it merely because it looks odd
- attempt to construct a failing case
- add a targeted test if useful
- either upgrade it to A/B/C or leave it documented as unresolved

### E. Non-bug

Do not report stylistic preferences, personal design taste, or hypothetical improvements as bugs.

## Confidence discipline

For every bug you propose fixing, state a confidence level:

- 99%+: effectively certain; strong specification/invariant/runtime evidence
- 90–99%: highly probable
- 70–90%: plausible but needs judgment
- below 70%: do not modify behavior without human confirmation

The numeric confidence is not meant as mathematically calibrated probability. It is a forcing
function to distinguish evidence from intuition.

Do not inflate confidence.

## Human-interaction rule

Do not stop for minor questions.

Ask the human only when:

- behavior is genuinely ambiguous,
- the answer materially affects correctness or architecture,
- choosing incorrectly could corrupt data, break compatibility, change externally visible behavior,
  or create significant rework.

Batch independent questions together when possible.

For each question, provide enough analysis that the human can answer quickly.

Use this format:

Question: [precise decision]

Evidence: [what the repo/docs imply]

Option A: [behavior and consequence]

Option B: [behavior and consequence]

Recommendation: [your best judgment]

Can work continue without this answer? [yes/no and why]

## Fixing rules

When fixing bugs:

- prefer the smallest change that restores the intended invariant
- preserve unrelated behavior
- avoid broad refactoring unless the bug cannot be fixed safely otherwise
- do not “clean up” large areas opportunistically
- add regression coverage for significant defects
- preserve public APIs unless changing them is necessary for correctness
- do not hide failures merely to make tests pass
- do not weaken assertions or tests unless you can establish that the assertion/test itself is wrong
- do not silently change semantics based on personal preference

If you encounter architectural complexity that repeatedly causes defects, record it separately as a
structural risk rather than turning the bug audit into a redesign.

## Multi-pass strategy

Do not perform only one linear code review.

Use several passes with different failure models.

At minimum:

Pass 1: specification and design drift Pass 2: invariants and state transitions Pass 3: ownership,
lifetime, resources, concurrency Pass 4: boundary values, malformed inputs, partial failure Pass 5:
cross-component contract mismatches Pass 6: tests, assertions, and missing adversarial coverage Pass
7: suspicious complexity, duplication, and inconsistent implementations Pass 8: regression review of
your own fixes

After each pass, update your internal list of high-risk areas.

Continue deeper where findings cluster.

## Verification

After fixes:

- rebuild the affected targets
- run relevant tests
- run broader tests where practical
- run applicable sanitizers/static analysis
- inspect the resulting diff
- look specifically for bugs introduced by your fixes
- verify regression tests fail before the fix when practical and pass afterward
- verify behavior against the inferred system model

Do not declare success solely because the test suite passes.

## Stopping condition

Stop when:

- all high-risk subsystems have received at least one serious correctness pass,
- currently available automated checks pass or remaining failures are explained,
- all high-confidence discovered bugs have been fixed,
- ambiguous high-impact issues have been surfaced to the human,
- another review pass is producing predominantly low-confidence or duplicate findings.

Do not claim that the repository is bug-free.

## Final report

Produce:

1. Executive assessment

State:

- overall confidence in the codebase
- areas that now appear robust
- areas that remain risky
- major sources of uncertainty

1. Bugs fixed

For each significant bug:

- location
- symptom
- root cause
- evidence
- confidence
- fix
- regression test or verification

1. Human decisions required

Only unresolved issues requiring semantic/product/design judgment.

1. Suspicious unresolved areas

Potential issues that could not be confirmed.

1. Verification performed

Commands, tests, sanitizers, static analysis, fuzzing, or other checks.

1. Residual risk

Explain what classes of bugs could still reasonably remain and why.

1. Recommended next highest-value checks

List only checks that materially increase confidence.

## Core principle

Your job is not to make the code look better.

Your job is to construct and test a model of what the system must do, systematically search for
violations of that model, repair violations when intent is clear, and surface uncertainty when human
judgment is genuinely required.
