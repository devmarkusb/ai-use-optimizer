---
title: Code Review
type: task-prompt
purpose: Review the current branch as a PR with bug, comment, repo-fit, and defense checks
targets:
  - ChatGPT
  - Claude
  - Codex
  - Cursor
  - Gemini
  - Generic LLM
scope:
  - code review
  - pull requests
  - diffs
  - brownfield
---

# Code Review

## Context

Review the current branch as a pull request to `origin/main`. Fetch if needed. Scope the change with
the merge-base diff (`origin/main...HEAD`).

## Goal

Explain what changed and why, find real bugs, fix comment regressions in touched code, judge whether
the diff is minimal repo-fit work or unnecessary AI-generated churn, and stress-test the author's
defense of the riskiest decisions.

Include a **Grill me** adversarial self-interrogation forcing defense of design and implementation
decisions. It should test whether the author actually understands the change and its surroundings,
not whether the diff looks fine on a quick read. Expose both the strongest defense of the branch and
the places where that defense is weak, uncertain, or unsupported by the repository evidence.

## Task

### Part I — Correctness and intent

1. Model behavior from the diff and nearby context.
1. Find bugs, regressions, and behavioral surprises—not style unless it hides a defect.
1. Fix comment regressions locally using the rules below; keep edits minimal.
1. Explain the change in plain language.

### Part II — Fit and minimalism ("AI slop")

Would an experienced maintainer say this belongs here?

1. Architecture and naming match the repo?
1. Reuses existing utilities, error handling, logging, and ownership patterns?
1. Minimal change—no unnecessary layers, classes, or files?
1. New or modified functions with no callers in the repo (search references; note uncertainty for
   dynamic dispatch, plugins, or intentional public API)?
1. Lifecycle, threading, performance, exception-safety, and ABI/API compatibility considered?
1. Tests assert observable behavior, not implementation details?
1. Overall: "This fits here"?

### Part III — Adversarial defense

Act in two roles for the riskiest parts of the branch. This is a defense of design and
implementation decisions, not a second conventional review:

- **Adversarial reviewer:** ask specific, high-pressure questions about the change.
- **Author/respondent:** answer each question as the person or agent responsible for the change.

If you authored or proposed the change, answer from your actual rationale, implementation details,
and verification work. If you did not author it, answer only from the diff and repository evidence;
clearly label assumptions, unknowns, and evidence gaps.

Probe whether the defense covers:

- the code and control flow
- data flow, state management, concurrency, races, and lifecycle behavior
- surrounding system contracts, API boundaries, and ownership boundaries
- realistic alternatives and tradeoffs
- failure modes, error handling, edge cases, and silent behavior changes
- operational consequences, including deploy, rollback, migrations, incidents, observability, and
  debugging
- performance, scalability, threading, and exception safety
- security and trust boundaries
- maintainability and future evolution
- test coverage, testing blind spots, and verification gaps
- hidden coupling, accidental risk, and unjustified assumptions

## Required Workflow

1. Fetch first if needed so `origin/main` is current.
1. Diff scope: `origin/main...HEAD`.
1. Read changed code plus enough context to judge behavior—not every unchanged file.
1. For moved or extracted code, compare the source and destination hunks for comment changes, not
   just changed executable behavior.
1. Separate confirmed defects from hypotheses; mark uncertainty explicitly.
1. Fix unambiguous comment issues; do not refactor unrelated code.
1. Give the smallest verification step per bug finding.
1. For Part II, search the repo for callers of new or touched functions; cite concrete repo files,
   patterns, or utilities to reuse.
1. For Part III, ask only questions tied to concrete risk in this branch. Pair every question with a
   direct answer.
1. Infer broader system context when the branch is small, but label inference clearly.

## Rules

- Evidence from diff and repo beats generic advice.
- Each bug: file, line range, failure scenario, minimal fix, verification step.
- Comment fixes must match post-change behavior.
- Pure moves must preserve comments exactly; if executable code did not change, comment text,
  placement, and presence should not change either. If behavior changed, restore or adjust comments
  that still explain non-obvious behavior, invariants, constraints, compatibility, lifecycle, or
  edge cases.
- Lead with the risky core; scale detail to diff size.
- Name specific simplifications and reuse targets—not vague "could be cleaner."
- Do not invent repo requirements.
- Answers in the adversarial section must be concrete and falsifiable.
- Separate evidence from inference. Use labels such as `Evidence`, `Inference`, `Assumption`,
  `Unknown`, or `Not verified` where that distinction matters.
- Do not inflate weak defenses. If a defense depends on missing tests, missing context, unverified
  behavior, or an assumption, say so plainly.
- When an answer exposes a real gap, name the consequence and the evidence that would close the gap.
- Prefer **why** and **what happens if** over factual trivia answerable from the diff alone.
- Target reasoning, tradeoffs, and system understanding, not syntax.
- Challenge assumptions aggressively, especially when the branch appears superficially correct.

## Output Format

Return Markdown with exactly these sections:

### Brief Summary

Two to four plain-language sentences: what changed and why it matters.

### What It Does and Why

Short narrative of behavior, motivation, and how touched pieces interact.

### Bugs and Risks

Numbered list. Per item: **File / lines**, **Severity** (`Critical`/`High`/`Medium`/`Low`),
**Issue**, **Why it matters**, **Suggested fix** (minimal), **How to verify**. Say "None found." if
empty.

### Comment Fixes

Per item: **File / lines**, **Before**, **After**, **Reason**. Say "None." if empty.

### Slop Assessment

#### Slop risks

Concrete churn, over-abstraction, unused never-called functions, or convention mismatches.

#### Concrete simplifications

Specific deletions, inlines, or rewrites without losing behavior.

#### Existing code to reuse

Repo paths, functions, types, or patterns to align with or call.

#### Requires human confirmation

Product intent, compatibility, rollout, or ownership the diff cannot settle.

### Adversarial Defense Q&A

Start with `Defense strength: Weak`, `Defense strength: Mixed`, or `Defense strength: Strong`, plus
`Review difficulty: Low`, `Review difficulty: Medium`, or `Review difficulty: High`.

Then give 8–15 numbered `Q:` and `A:` pairs. Start with the highest-risk implementation choices,
then cover core defense, deep dives into architecture/data flow/concurrency/failure handling,
realistic alternatives, production readiness, and red-team failure scenarios. Escalate difficulty
when the diff appears superficially correct.

### Weakest Defenses

The 3–5 questions whose answers most reduce confidence in the branch. For each, name the missing
evidence, unproven assumption, or unresolved risk, plus the evidence or test that would close the
gap. Say "None material." only when the branch is low-risk and well-supported.

## Do Not

- Line-by-line walkthroughs when a risk-focused read suffices.
- Findings on formatting, rename-only hunks, or boilerplate unless they hide defects.
- Rewrites beyond comment clarity or confirmed bugs.
- Confident language that hides uncertainty.
- Large refactors when a minimal fix works.
- Review arbitrary text, a detached file, or a supplied folder as a substitute for the
  `origin/main...HEAD` branch diff.
- Turn the adversarial section into generic interview filler or conventional nit comments.

## Quality Bar

- Bug findings are actionable; Brief Summary stands alone.
- Slop items reference this repo—not generic clean-code advice.
- If the change is sound and minimal, say so; do not invent nits.
- Adversarial questions must target concrete risks from the branch and answers must cite files,
  tests, commands, contracts, or runtime behavior where available.
- At least one adversarial question must cover each major risk area surfaced earlier in the review.
- Red-team and Weakest Defenses content must name concrete failure scenarios, not vague "what if it
  breaks."
