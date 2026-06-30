---
title: Grill Me
type: task-prompt
purpose: Adversarial self-interrogation forcing defense of design and implementation decisions
targets:
  - ChatGPT
  - Claude
  - Codex
  - Cursor
  - Gemini
  - Generic LLM
scope:
  - code review
  - design review
  - pull requests
---

# Grill Me

## Context

You are conducting a deep technical design and implementation review of a code change, design, or
proposed addition. The respondent is the author of the change, which may be a human developer or an
AI coding agent, and must defend every significant decision.

You will receive one or more of: source files, a git diff, a pull request, a branch, a design
document, or a combination.

## Goal

Generate and answer a structured interrogation that tests whether the author actually understands
the change and its surroundings—not whether the diff looks fine on a quick read.

The output should expose both the strongest defense of the change and the places where that defense
is weak, uncertain, or unsupported by the provided material.

## Task

Act in two roles:

- **Adversarial reviewer:** ask specific, high-pressure questions about the change.
- **Author/respondent:** answer each question as the person or agent responsible for the change.

If you authored or proposed the change, answer from your actual rationale, implementation details,
and verification work. If you did not author it, answer only from the provided material and clearly
label assumptions, unknowns, and evidence gaps.

Infer the system beyond the diff when the change is small. If the change appears correct on the
surface, escalate difficulty rather than stopping early.

Probe whether the author's defense covers:

- the code and control flow
- the surrounding system and contracts
- realistic alternatives and tradeoffs
- failure modes and edge cases
- operational consequences (deploy, rollback, migrations, incidents)
- performance and scalability
- security and trust boundaries
- maintainability and future evolution
- accidental risk and unjustified assumptions

## Rules

- Pair every question with an answer.
- Answers must be direct, concrete, and falsifiable.
- Separate evidence from inference. Use labels such as `Evidence`, `Inference`, `Assumption`,
  `Unknown`, or `Not verified` where that distinction matters.
- Do not inflate weak answers. If a defense depends on missing tests, missing context, unverified
  behavior, or an assumption, say so plainly.
- When an answer exposes a real gap, name the consequence and the evidence that would close the gap.
- Focus on the highest-leverage questions.
- Prefer **why** and **what happens if** over factual trivia answerable from the diff alone.
- Escalate difficulty across sections.
- Target reasoning, tradeoffs, and system understanding—not syntax.
- Challenge assumptions aggressively.
- Look for hidden coupling, races, state management, API contracts, error handling, observability
  gaps, deployment and migration risks, testing blind spots, and scalability limits.
- If the change is small, infer the broader system and question that context.
- If the code appears correct, become more adversarial rather than ending early.

## Output Format

Return Markdown with exactly these sections and headings:

Within each Q&A section, use numbered `Q:` and `A:` pairs.

### Executive Assessment

Brief summary of:

- what this change appears to do
- areas most likely to hide risk
- strength of the author's current defense: `Weak`, `Mixed`, or `Strong`
- estimated review difficulty: `Low`, `Medium`, or `High`

### Core Defense Q&A

10–20 question-and-answer pairs every competent author should be able to handle.

### Deep Dive Q&A

Question-and-answer pairs requiring strong understanding of architecture, data flow, concurrency,
failure handling, operational behavior, and performance.

### Alternative Design Q&A

Question-and-answer pairs that force justification of the chosen approach versus realistic
alternatives.

### Production Readiness Q&A

Question-and-answer pairs about monitoring, rollback, deployment, migrations, incident response, and
debugging.

### Red-Team Q&A

Question-and-answer pairs intended to expose weaknesses in the design or implementation.

### Weakest Defenses

The 3–5 questions whose answers most reduce confidence in the change, with the specific missing
evidence, unproven assumption, or unresolved risk for each.

## Do Not

- Provide conventional code-review comments (nits, style, line-by-line critique).
- Turn the response into a patch plan unless the user explicitly asks for fixes.
- Pretend the change is safer, more tested, or better understood than the provided evidence
  supports.

## Quality Bar

- Questions and answers must be specific to the provided material or defensibly inferred context—not
  generic interview filler.
- At least one question per major risk area surfaced in the Executive Assessment.
- Red-Team and Weakest Defenses sections must name concrete failure scenarios, not vague “what if it
  breaks.”
- Strong answers must cite concrete implementation details, tests, commands, files, contracts, or
  runtime behavior where available.
