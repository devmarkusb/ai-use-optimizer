---
title: Code Review
type: task-prompt
purpose: Review the current branch as a PR with bug, comment, repo-fit, and adversarial defense checks
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

Identify every abstraction boundary in touched code (functions, types, modules, public APIs). At
each boundary, verify that names, comments, and interfaces describe the abstraction itself—not its
current caller.

1. Architecture and naming match the repo?
1. Abstraction boundaries: for every new or modified function and public interface, do names,
   comments, and signatures describe the abstraction—not the current caller? Per function:
   - Does the name describe **how it works** or **who currently uses it**?
   - Could this function be reused in another project with the same name?
   - Should any business or caller-specific terminology move to the call site instead?
1. Reuses existing utilities, error handling, logging, and ownership patterns?
1. Minimal change—no unnecessary layers, classes, or files?
1. New or modified functions with no callers in the repo (search references; note uncertainty for
   dynamic dispatch, plugins, or intentional public API)?
1. Lifecycle, threading, performance, exception-safety, and ABI/API compatibility considered?
1. Tests assert observable behavior, not implementation details?
1. Overall: "This fits here"?

### Part III — Adversarial defense

Act in two roles for the **few highest-risk** parts of the branch. This is a defense of design and
implementation decisions, not a second conventional review and not a checklist tour of every risk
category:

- **Adversarial reviewer:** ask specific, high-pressure questions about the change.
- **Author/respondent:** answer each question as the person or agent responsible for the change.

If you authored or proposed the change, answer from your actual rationale, implementation details,
and verification work. If you did not author it, answer only from the diff and repository evidence;
clearly label assumptions, unknowns, and evidence gaps.

Prefer depth over breadth. Ask only about concrete risks this branch actually introduces. Typical
probe dimensions (pick the ones that matter; do not invent a Q&A for each):

- control flow, data flow, state, concurrency, races, lifecycle
- system/API/ownership contracts; caller-centric abstractions
- alternatives, tradeoffs, failure modes, silent behavior changes
- ops (deploy, rollback, migrations, incidents, observability)
- performance, security/trust boundaries, maintainability
- test blind spots, hidden coupling, unjustified assumptions

## Required Workflow

1. Fetch first if needed so `origin/main` is current.
1. Diff scope: `origin/main...HEAD`.
1. Read changed code plus enough context to judge behavior—not every unchanged file.
1. For moved or extracted code, compare the source and destination hunks for comment changes, not
   just changed executable behavior.
1. Separate confirmed defects from hypotheses; mark uncertainty explicitly.
1. Fix unambiguous comment issues; do not refactor unrelated code.
1. Give the smallest verification step per bug finding.
1. For Part II, identify abstraction boundaries in touched code and flag caller-centric naming,
   comments, or interfaces; search the repo for callers of new or touched functions. Cite concrete
   repo paths, patterns, or utilities in `Existing code to reuse instead of the reinvention` only
   when the branch reinvents or diverges from them—never to praise correct reuse.
1. For Part III, ask only questions tied to concrete risk in this branch. Default to **3–5**
   `Q:`/`A:` pairs; go above 5 only when distinct high-severity risks each need their own question;
   never exceed **7**. Pair every question with a direct answer. If the answer exposes a gap, name
   it in that answer instead of repeating it elsewhere, and mark the pair so a skim finds it (see
   Output Format).
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
- `Existing code to reuse instead of the reinvention` is an open-todo list only: each item is a
  missed reuse opportunity with a concrete repo path or symbol. No praise, no "already correct"
  notes, no filler. Say `None.` when the branch does not reinvent existing code.
- Caller-centric names, comments, or interfaces at abstraction boundaries are slop unless the
  boundary is intentionally caller-specific; prefer moving business terminology to the call site.
- Do not invent repo requirements.
- Put each substantive point in one primary section. Use brief cross-references instead of repeating
  the same issue across `Bugs and Risks`, `Slop Assessment`, and `Adversarial Defense Q&A`.
- Answers in the adversarial section must be concrete and falsifiable.
- Separate evidence from inference. Use labels such as `Evidence`, `Inference`, `Assumption`,
  `Unknown`, or `Not verified` where that distinction matters.
- Do not inflate weak defenses. If a defense depends on missing tests, missing context, unverified
  behavior, or an assumption, say so plainly.
- When an answer exposes a real gap, name the consequence and the evidence that would close the gap.
- Prefer **why** and **what happens if** over factual trivia answerable from the diff alone.
- Target reasoning, tradeoffs, and system understanding, not syntax.
- Challenge assumptions aggressively, especially when the branch appears superficially correct.
- Part III stays short: few sharp questions on the riskiest decisions, not a tour of every probe
  dimension. When a defense fails, mark it loudly (`PROBLEM INDEX` + `⚠ DEFENSE FAILED`) so the
  failure is obvious on a skim.

## Output Format

Return Markdown with exactly these sections:

### Brief Summary

Two to four plain-language sentences: what changed and why it matters. Keep it high-level; do not
restate individual bug, slop, or adversarial findings.

### What It Does and Why

Short narrative of behavior, motivation, and how touched pieces interact. Do not preview detailed
findings that belong in later sections.

### Bugs and Risks

Numbered list. Per item: **File / lines**, **Severity** (`Critical`/`High`/`Medium`/`Low`),
**Issue**, **Why it matters**, **Suggested fix** (minimal), **How to verify**. Say "None found." if
empty.

### Comment Fixes

Per item: **File / lines**, **Before**, **After**, **Reason**. Say "None." if empty.

### Slop Assessment

#### Slop risks

Concrete churn, over-abstraction, caller-centric naming at abstraction boundaries, unused
never-called functions, or convention mismatches. Say `None.` if empty.

#### Concrete simplifications

Specific deletions, inlines, or rewrites without losing behavior. Say `None.` if empty.

#### Existing code to reuse instead of the reinvention

Open todos only: repo paths, functions, types, or patterns the branch should call or align with but
does not. Each item names what to reuse, what in the diff should change, and why. No praise for
correct reuse; do not list utilities already used properly. Do not invent items to fill the section.
Say `None.` if empty.

### Adversarial Defense Q&A

Start with `Defense strength: Weak`, `Defense strength: Mixed`, or `Defense strength: Strong`, plus
`Review difficulty: Low`, `Review difficulty: Medium`, or `Review difficulty: High`.

Then a one-line **Problem index** so failures are visible without reading every answer:

- If any pair exposes a real bug, serious mistake, or material undefended gap:\
  `**PROBLEM INDEX:** #N, #M — <shortest label per item>`\
  (use the same numbers as the Q&A list; bold the whole line)
- If none: `**PROBLEM INDEX:** None.`

Then give **3–5** numbered pairs (hard cap **7**). Prefer fewer sharp questions over covering every
risk dimension. Start with the highest-risk implementation choices; escalate difficulty when the
diff looks superficially correct. Do not pad with low-value or checklist questions.

Each pair uses this shape:

```markdown
N. **Q:** ...
   **A:** ...
```

When the answer exposes a real bug, serious mistake, or material undefended gap (not a minor
uncertainty):

1. Prefix the item with a bold alert on its own line so skimming works:\
   `**⚠ DEFENSE FAILED — <Critical|High|Medium>: <one-line consequence>**`
1. Keep `**Q:**` / `**A:**` immediately under that alert.
1. In `**A:**`, state the gap, consequence, and what evidence would close it.
1. Ensure the item number appears in the **Problem index**.

If the defense holds, write a normal `**Q:**` / `**A:**` with no alert line and do not list it in
the Problem index. Minor residual risk or labeled `Unknown` without a concrete failure mode is not a
defense failure.

If a question overlaps with a bug or slop finding, reference that item number and add only the new
defense-specific evidence, assumption, or uncertainty.

## Quality Bar

- Bug findings are actionable; Brief Summary stands alone.
- Slop items reference this repo—not generic clean-code advice.
- Caller-centric abstraction naming must cite the function or interface and a concrete reuse or
  call-site alternative when flagged.
- If the change is sound and minimal, say so in narrative or slop-risk sections; do not invent nits.
  An empty `Existing code to reuse instead of the reinvention` (`None.`) is expected when reuse is
  already correct—do not pad it with praise or restatements of what already matches the repo.
- Adversarial questions must target concrete risks from the branch and answers must cite files,
  tests, commands, contracts, or runtime behavior where available.
- Cover major risk areas surfaced earlier only when each still needs a distinct defense question;
  merge related risks into one Q&A instead of one question per earlier finding.
- Prefer 3–5 adversarial pairs; never exceed 7. Empty padding to hit a count is a quality failure.
- Adversarial Defense Q&A content must name concrete failure scenarios, not vague "what if it
  breaks."
- Defense failures must be skimmable: bold **PROBLEM INDEX** plus a bold `⚠ DEFENSE FAILED` line on
  each failing pair; a reader should spot every serious problem without reading the held defenses.
