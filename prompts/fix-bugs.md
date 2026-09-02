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

## Context

You are performing a repository-wide correctness audit of an AI-developed codebase that has evolved
rapidly. The human maintainer no longer trusts that all implemented behavior is correct.

## Goal

Infer what the system is supposed to do, find as many real correctness bugs as reasonably possible,
fix bugs whose intended behavior is sufficiently clear, surface cases where correctness depends on
an ambiguous product or design decision, and leave the repository in a measurably more trustworthy
state. Avoid speculative rewrites.

## Ground truth hierarchy

Do not assume the current implementation is correct. Infer intended behavior in this priority order:

1. explicit requirements, specifications, design/architecture documents, ADRs, README files
1. externally visible API contracts and documented invariants
1. tests that clearly encode intentional behavior
1. call-site expectations and cross-component invariants
1. comments
1. current implementation

Treat tests as evidence, not absolute truth—a test may encode an existing bug. When sources
disagree, do not silently choose one; record the conflict.

## Required Workflow

### 1. Understand the system before editing

Inspect the repository broadly and build a concise semantic model: major components and
responsibilities, important data structures and invariants, state machines and legal transitions,
ownership and lifetime assumptions, persistence and serialization contracts, concurrency model,
error-handling model, external API/protocol contracts, security boundaries, and cross-module
assumptions.

Compare available design documentation against the actual implementation and note drift. Focus on
semantics and invariants relevant to correctness, not trivial code structure.

### 2. Construct a bug-search map

Before fixing individual issues, identify where bugs are most likely to exist. Prioritize:

- duplicated implementations of the same concept; inconsistent implementations of equivalent paths
- code added recently or repeatedly modified; TODO/FIXME/workaround/hack comments
- error handling, cleanup paths, partial failures, retry/idempotency behavior
- boundary conditions: empty/null/zero/maximum inputs, overflow, truncation, signedness, conversions
- ownership, lifetime, dangling references, resource leaks
- concurrency: races, locking, atomics, reentrancy
- state: invalid transitions, caching and stale-state bugs
- persistence: schema/version compatibility, serialization/deserialization asymmetry, malformed
  input
- contracts: API pre/postconditions, disagreement between callers and callees
- code whose complexity is disproportionate to its apparent responsibility; branches that appear
  unreachable or untested
- behavior described in design documents but not enforced in code

Look for bugs across component boundaries, not only inside individual functions.

### 3. Actively try to falsify the implementation

For every important subsystem, ask: What must always be true? Where is that invariant established,
and where can it be violated? What does this code assume about its callers, and is that actually
guaranteed? What happens at boundaries, after partial failure, when operations repeat, or when
execution is interrupted? Can two independently reasonable components disagree about representation
or state?

Search for concrete counterexamples. Prefer evidence-producing methods where practical: run existing
tests, add focused regression tests, enable compiler warnings, run sanitizers/static
analysis/correctness linters, use property-based or fuzz tests where they have high leverage, check
round-trip properties and invariants before/after transformations. Target these runs; do not run
expensive tools blindly across the whole repository.

Make several passes with different failure models (specification drift; invariants and state;
ownership/lifetime/concurrency; boundaries and partial failure; cross-component contracts; test and
assertion gaps; suspicious complexity and duplication). Update the bug-search map after each pass
and go deeper where findings cluster. Finish with a regression review of your own fixes.

### 4. Classify every suspected bug before changing code

- **A. Confirmed bug** — strong evidence that current behavior violates an intended invariant or
  explicit contract (contradicts specification or clearly intentional tests, demonstrably violates
  an invariant, undefined behavior, wrong result for a concrete input, leak/corruption, race,
  invalid lifetime, objectively incompatible caller/callee contracts). Action: fix it, add or
  improve a regression test where appropriate, verify the fix.
- **B. Highly probable bug** — evidence strongly suggests a defect, but intent is not formally
  documented. Action: investigate nearby code, callers, history, tests, and docs; if one
  interpretation overwhelmingly fits the system, fix it and clearly record the assumption; otherwise
  escalate to the human.
- **C. Ambiguous behavior / design question** — two or more behaviors are plausible and choosing one
  would encode a product or architecture decision. Action: do not guess; formulate a precise
  question for the human (see below).
- **D. Suspicious but unproven** — looks wrong but lacks evidence. Action: do not "fix" it merely
  because it looks odd; attempt to construct a failing case or targeted test, then upgrade to A/B/C
  or leave it documented as unresolved.
- **E. Non-bug** — do not report stylistic preferences, personal design taste, or hypothetical
  improvements as bugs.

## Confidence discipline

For every bug you propose fixing, state a confidence level:

- 99%+: effectively certain; strong specification/invariant/runtime evidence
- 90–99%: highly probable
- 70–90%: plausible but needs judgment
- below 70%: do not modify behavior without human confirmation

The number is a forcing function to distinguish evidence from intuition, not a calibrated
probability. Do not inflate confidence.

## Human-interaction rule

Do not stop for minor questions. Ask the human only when behavior is genuinely ambiguous, the answer
materially affects correctness or architecture, or choosing incorrectly could corrupt data, break
compatibility, change externally visible behavior, or create significant rework. Batch independent
questions and provide enough analysis for a quick answer, using this format:

```text
Question: [precise decision]
Evidence: [what the repo/docs imply]
Option A: [behavior and consequence]
Option B: [behavior and consequence]
Recommendation: [your best judgment]
Can work continue without this answer? [yes/no and why]
```

## Fixing rules

- Prefer the smallest change that restores the intended invariant; preserve unrelated behavior.
- Avoid broad refactoring unless the bug cannot be fixed safely otherwise; do not "clean up" large
  areas opportunistically.
- Add regression coverage for significant defects.
- Preserve public APIs unless changing them is necessary for correctness.
- Do not hide failures to make tests pass, weaken assertions or tests unless the assertion/test
  itself is demonstrably wrong, or silently change semantics based on preference.
- If architectural complexity repeatedly causes defects, record it separately as a structural risk
  rather than turning the audit into a redesign.

## Verification

After fixes: rebuild affected targets, run relevant then broader tests, run applicable
sanitizers/static analysis, inspect the resulting diff, and look specifically for bugs introduced by
your fixes. Verify regression tests fail before the fix and pass afterward when practical. Do not
declare success solely because the test suite passes.

## Stopping condition

Stop when all high-risk subsystems have received at least one serious correctness pass, available
automated checks pass or remaining failures are explained, all high-confidence bugs are fixed,
ambiguous high-impact issues are surfaced to the human, and another pass produces predominantly
low-confidence or duplicate findings. Do not claim the repository is bug-free.

## Final report

1. **Executive assessment** — overall confidence in the codebase; areas now robust, areas still
   risky, major sources of uncertainty.
1. **Bugs fixed** — per significant bug: location, symptom, root cause, evidence, confidence, fix,
   regression test or verification.
1. **Human decisions required** — only unresolved issues needing semantic/product/design judgment.
1. **Suspicious unresolved areas** — potential issues that could not be confirmed.
1. **Verification performed** — commands, tests, sanitizers, static analysis, fuzzing, other checks.
1. **Residual risk** — what classes of bugs could still reasonably remain and why.
1. **Recommended next highest-value checks** — only checks that materially increase confidence.

## Core principle

Your job is not to make the code look better. It is to construct and test a model of what the system
must do, systematically search for violations of that model, repair violations when intent is clear,
and surface uncertainty when human judgment is genuinely required.
