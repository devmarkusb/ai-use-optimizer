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

Review the current branch as a pull request to `origin/main`. Fetch first if needed so `origin/main`
is current. Scope the change with the merge-base diff (`origin/main...HEAD`).

## Goal

Explain what changed and why, find real bugs, fix comment regressions in touched code, judge whether
the diff is minimal repo-fit work or unnecessary AI-generated churn, and stress-test the author's
defense of the riskiest decisions.

## Task

### Part I — Correctness and intent

1. Model behavior from the diff and nearby context—read changed code plus enough context to judge
   behavior, not every unchanged file.
1. Find bugs, regressions, and behavioral surprises—not style unless it hides a defect. Separate
   confirmed defects from hypotheses; mark uncertainty explicitly. Give the smallest verification
   step per finding.
1. Fix unambiguous comment regressions locally; keep edits minimal and do not refactor unrelated
   code. For moved or extracted code, compare source and destination hunks for comment changes, not
   just changed executable behavior.
1. Explain the change in plain language.

### Part II — Fit and minimalism ("AI slop")

Would an experienced maintainer say this belongs here?

1. Architecture and naming match the repo?
1. Abstraction boundaries: for every new or modified function, type, module, and public interface,
   do names, comments, and signatures describe the abstraction itself—not its current caller? Per
   function: does the name describe **how it works** or **who currently uses it**? Could it be
   reused in another project with the same name? Should caller-specific or business terminology move
   to the call site?
1. Reuses existing utilities, error handling, logging, and ownership patterns? Search the repo for
   what the branch reinvents.
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

- **Adversarial reviewer:** ask specific, high-pressure questions about concrete risks this branch
  actually introduces. Prefer **why** and **what happens if** over factual trivia answerable from
  the diff alone; target reasoning, tradeoffs, and system understanding. Escalate difficulty when
  the diff looks superficially correct.
- **Author/respondent:** answer each question as the person or agent responsible for the change. If
  you authored or proposed it, answer from your actual rationale, implementation, and verification
  work; otherwise answer only from the diff and repository evidence, clearly labeling assumptions,
  unknowns, and evidence gaps.

Typical probe dimensions (pick only the ones that matter): control flow, data flow, state,
concurrency, lifecycle; system/API/ownership contracts; alternatives, tradeoffs, failure modes,
silent behavior changes; ops (deploy, rollback, migrations, observability); performance,
security/trust boundaries, maintainability; test blind spots, hidden coupling, unjustified
assumptions.

## Rules

- Evidence from diff and repo beats generic advice; do not invent repo requirements. Infer broader
  system context when the branch is small, but label inference clearly.
- Comment fixes must match post-change behavior. Pure moves must preserve comments exactly; if
  executable code did not change, comment text, placement, and presence should not change either. If
  behavior changed, restore or adjust comments that still explain non-obvious behavior, invariants,
  constraints, compatibility, lifecycle, or edge cases.
- Lead with the risky core; scale detail to diff size.
- Name specific simplifications and reuse targets—not vague "could be cleaner."
- Caller-centric names, comments, or interfaces at abstraction boundaries are slop unless the
  boundary is intentionally caller-specific; prefer moving business terminology to the call site.
- Put each substantive point in one primary section. Use brief cross-references instead of repeating
  the same issue across `Bugs and Risks`, `Slop Assessment`, and `Adversarial Defense Q&A`.
- Adversarial answers must be concrete and falsifiable. Separate evidence from inference with labels
  such as `Evidence`, `Inference`, `Assumption`, `Unknown`, or `Not verified` where the distinction
  matters. Do not inflate weak defenses: if a defense depends on missing tests, missing context,
  unverified behavior, or an assumption, say so plainly, name the consequence, and state what
  evidence would close the gap.

## Output Format

Return Markdown with exactly these sections:

### Brief Summary

Two to four plain-language sentences: what changed and why it matters. Keep it high-level; do not
restate individual findings.

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

Open todos only: each item names a concrete repo path, function, type, or pattern the branch should
call or align with but does not, what in the diff should change, and why. No praise, no "already
correct" notes, no filler—an empty section (`None.`) is expected when reuse is already correct.

### Adversarial Defense Q&A

Start with `Defense strength: Weak | Mixed | Strong` plus `Review difficulty: Low | Medium | High`.

Then a one-line **Problem index** so failures are visible without reading every answer:

- If any pair exposes a real bug, serious mistake, or material undefended gap:\
  `**PROBLEM INDEX:** #N, #M — <shortest label per item>`\
  (use the same numbers as the Q&A list; bold the whole line)
- If none: `**PROBLEM INDEX:** None.`

Then give **3–5** numbered pairs (hard cap **7**; go above 5 only when distinct high-severity risks
each need their own question). Prefer fewer sharp questions over covering every risk dimension;
merge related risks into one pair. Empty padding to hit a count is a quality failure. Each pair:

```markdown
N. **Q:** ...
   **A:** ...
```

When the answer exposes a real bug, serious mistake, or material undefended gap (not a minor
uncertainty):

1. Prefix the item with a bold alert on its own line so skimming works:\
   `**⚠ DEFENSE FAILED — <Critical|High|Medium>: <one-line consequence>**`
1. Keep `**Q:**` / `**A:**` immediately under that alert; in `**A:**`, state the gap, consequence,
   and what evidence would close it.
1. Ensure the item number appears in the **Problem index**.

If the defense holds, write a normal pair with no alert line and no Problem-index entry. Minor
residual risk or a labeled `Unknown` without a concrete failure mode is not a defense failure. If a
question overlaps with a bug or slop finding, reference that item number and add only the new
defense-specific evidence, assumption, or uncertainty.

## Quality Bar

- Bug findings are actionable; Brief Summary stands alone.
- Slop items reference this repo—not generic clean-code advice. Flagged caller-centric naming cites
  the function or interface and a concrete reuse or call-site alternative.
- If the change is sound and minimal, say so in narrative or slop-risk sections; do not invent nits.
- Adversarial questions target concrete risks from this branch; answers cite files, tests, commands,
  contracts, or runtime behavior where available and name concrete failure scenarios, not vague
  "what if it breaks."
- Defense failures are skimmable: a reader spots every serious problem from the **PROBLEM INDEX**
  and `⚠ DEFENSE FAILED` lines without reading the held defenses.
