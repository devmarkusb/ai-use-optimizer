---
title: Overnight Agent — Sleep / Consolidation Mode
type: task-prompt
purpose: >
  Run an unattended overnight investigation and deliver a dense morning report that deepens
  understanding of a repository or problem instead of maximizing code written
targets:
  - Claude Code
  - Codex
  - Cursor
  - Generic LLM coding agents
scope:
  - unattended research
  - investigation
  - consolidation
recommended-stage: when leaving an agent alone for an extended session on a problem or repository area
---

# Overnight Agent — Sleep / Consolidation Mode

## Context

You have an extended unattended work session. Your purpose is not to maximize the amount of code
written. It is to wake me up with a substantially better understanding of this repository/problem
than I had before, including discoveries I would probably not have made during a normal interactive
session.

## Inputs

Investigate:

\<PROBLEM / AREA / QUESTION>

Treat my current understanding and assumptions as hypotheses, not facts:

\<OPTIONAL: CURRENT MODEL / SUSPICIONS / IDEAS>

## Goal

Work independently on the investigation above. Prefer discovering that my assumptions are wrong over
confirming them. The morning report, not the amount of work performed, is the measure of success.

## Required Workflow

### 1. Investigate–consolidate cycles

Run an iterative research loop:

1. Inspect the relevant system.
1. Build a model of how it actually works.
1. Identify uncertainties, contradictions, accidental complexity, duplication, suspicious
   abstractions, and unexplained behavior.
1. Form concrete hypotheses.
1. Find evidence that could falsify each important hypothesis.
1. Run safe experiments where useful.
1. Update your model.
1. Ask: "What important thing am I still missing?"
1. Explore the most promising unanswered question.
1. Repeat.

Do not stop merely because you have produced a plausible explanation. Actively search for evidence
against your current conclusions.

**Representation search.** Periodically reconsider whether you are looking at the problem through
the wrong abstraction. Where useful, model it as one or more of:

- data flow / information flow
- dependency graph
- state machine
- constraint system
- ownership / resource flow
- transformations between representations
- invariants and pre/postconditions
- performance/cost model
- historical/accidental architecture versus essential architecture

Prefer the representation that makes the system simplest to explain.

**Consolidation.** After a substantial investigation phase, stop exploring temporarily and ask:

- What have I actually established? What is merely inferred?
- Which assumptions were falsified?
- Which facts explain several observations at once?
- Can the current model be made substantially simpler?
- Are two apparently different mechanisms actually the same mechanism?
- Is some complexity accidental and removable?
- What would an expert reviewing this investigation challenge?
- What experiment would most reduce remaining uncertainty?

Then begin another investigation cycle based on the consolidated model. Do several such cycles
rather than one enormous linear exploration.

### 2. Experiments

You may read arbitrary repository files and history, search code and documentation, inspect tests,
compile, run existing tests and benchmarks, create temporary analysis scripts, inspect generated
artifacts, perform static analysis, and make temporary experimental modifications when necessary to
test a hypothesis.

Prefer experiments over speculation whenever reasonably cheap. Record enough information that
important results are reproducible.

## Deliverables

Maintain these files under `overnight/`:

- `WORKLOG.md` — significant observations, hypotheses, experiments, results, rejected explanations,
  and unresolved questions. Keep evidence separate from interpretation; do not dump every command
  into this file.
- `FINDINGS.md` — only promote findings here once they have survived reasonable attempts at
  falsification. For every important finding include: finding, why it matters, evidence, confidence,
  remaining uncertainty.
- `OPPORTUNITIES.md` — code or design that appears unnecessarily complicated, duplicated, obsolete,
  or removable. Do NOT silently refactor it; record it here instead. For each opportunity describe:
  current situation, why it appears unnecessary or overly complicated, proposed simplification,
  expected benefit, risk, evidence needed before changing it.

The primary deliverable is `MORNING.md` (see Output Format).

## Rules

### Safety

This session is unattended. Do NOT:

- modify production/external systems
- deploy anything
- push commits
- force-push
- delete important data
- modify credentials or secrets
- send messages
- make network-side changes
- perform irreversible actions

Treat destructive shell commands and broad filesystem operations as prohibited. Repository
modifications should be experimental unless explicitly authorized.

### Do not optimize for activity

Do not manufacture work to fill the available time. If investigation reaches diminishing returns,
spend the remaining effort on:

- challenging conclusions
- simplifying the resulting model
- reproducing important findings
- checking edge cases
- looking for counterexamples
- inspecting relevant history
- identifying missing tests
- finding opportunities to delete or simplify code
- improving the morning report

It is better to establish five important facts with strong evidence than produce fifty speculative
observations.

## Output Format

`overnight/MORNING.md` is written for a human who has just returned and wants the highest
information density possible. Structure it as **Morning Report** with these sections:

- **Executive summary** — the 5–10 things worth knowing.
- **Mental model** — the simplest accurate explanation of how the relevant system works. Include
  diagrams where they materially improve understanding.
- **What surprised me** — results that were unexpected, contradicted assumptions, or substantially
  changed the model.
- **Strong findings** — important conclusions and their evidence.
- **Things I tried that were wrong** — rejected hypotheses and why they failed. Keep this section;
  do not hide failed attempts.
- **Simplification opportunities** — things that may be deletable, mergeable, generalizable, or
  conceptually simpler than the current implementation suggests.
- **Risks / bugs** — potential correctness, performance, maintainability, or architectural problems
  discovered. Separate demonstrated bugs from suspicions.
- **Remaining uncertainty** — important questions that remain unresolved.
- **Recommended next investigations** — a small set of experiments or decisions with high expected
  information value. Do not create a giant generic TODO list.
- **Suggested changes** — only changes justified by the investigation. For each: what, why, expected
  benefit, risk, confidence.
- **Appendix: evidence** — commands, measurements, code locations, commits, tests, or other material
  needed to verify important conclusions.

## Quality Bar

Before finishing:

1. Re-read `MORNING.md`.
1. Challenge every major conclusion.
1. Remove weak or redundant observations.
1. Clearly distinguish fact, inference, and speculation.
1. Check whether a simpler explanation fits the evidence.
1. Verify important measurements where practical.
1. Ensure the report explains why, not merely what.
1. Make the executive summary understandable without reading the worklog.
