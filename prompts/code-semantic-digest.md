---
title: Code Semantic Digest
type: task-prompt
purpose: Extract per-operation behavioral contracts from source files for fast code comprehension
targets:
  - Claude Code
  - ChatGPT
  - Claude
  - Codex
  - Cursor
  - Gemini
  - Generic LLM
scope:
  - code reading
  - semantic analysis
  - brownfield
---

# Code Semantic Digest

## Context

You are reading source code on behalf of a human who needs to reason about it quickly—not review it
for bugs, not summarize its architecture.

You will receive one or more source files or a folder path.

## Goal

For each significant component, extract the minimum behavioral contracts a human needs to hold in
their head to reason correctly about the code. Surface only what cannot be confidently inferred from
names and types alone.

Do not produce an architecture overview, a code review, or an implementation walkthrough.

## Output Notation

Express all contracts in the following notation. Emit it directly—do not wrap it in Markdown prose
paragraphs.

```text
Component <Name>

[invariant:
    <property that holds across all operations on this component>]

Operation <name>(<param>: <Type>, ...) -> <ReturnType>

[requires:
    <non-obvious precondition the caller must satisfy>]

[ensures:
    <non-obvious guarantee on result or observable state after normal return>]

[fails:
    <FailureName>:
        <observable state after this exit path>]
```

Each block is optional. Omit any block that would be empty or trivially obvious from the name and
types.

Notation semantics:

- `requires:` — preconditions the caller must satisfy that the type system does not enforce. Include
  ownership and lifetime assumptions, thread-safety requirements, ordering constraints, and implicit
  valid ranges.
- `ensures:` — observable guarantees the operation provides on a normal return. Include state
  mutations, output properties, and guarantees the return type alone does not capture.
- `fails:` — named legitimate exit paths that are correct program outcomes, not defect reports. Each
  named block describes observable state after that path. Only include failure modes where state
  differs materially between paths; do not enumerate every catchable exception class.
- `invariant:` — structural property that holds before and after every operation on this component.
  Place at component level, before the first `Operation`.
- Append `[inferred]` to any individual line whose claim is not directly confirmed by code or
  assertions. Do not invent semantics not supported by the code.

**Reference example:**

```text
Component OrderService

Operation submit(cart: Cart, user: User) -> Order

requires:
    user.authenticated
    cart.items.count > 0

ensures:
    result.state == Created
    inventory.reserved_for(result) [inferred]
    audit_log.contains(OrderSubmitted(result.id))

fails:
    OutOfStock:
        no order created
        no payment captured
    PaymentRejected:
        order.state == Created
        inventory not reserved
```

## Required Workflow

1. Scan the provided code. Identify components and their significant public operations.
1. For each operation, determine what the caller must guarantee that the parameter types alone do
   not enforce. That yields `requires:` entries.
1. For each operation, determine what the caller knows about state and output after a normal return
   that the return type alone does not capture. That yields `ensures:` entries.
1. For each operation, identify named exit paths other than normal return and how observable state
   differs for each. That yields `fails:` entries. Only include paths where the post-failure state
   is distinct and the caller must handle it differently.
1. For each component, identify any structural property that holds before and after every operation.
   That yields `invariant:` entries.
1. Skip operations where all blocks would be empty or trivially obvious. Prioritize operations where
   the gap between what the name implies and what the code actually does is largest.

## Rules

- Emit contracts only for operations where the behavior is not obvious from the name and types.
- Do not summarize implementation steps. Contracts describe what, not how.
- Do not diagnose bugs or suggest improvements.
- Do not produce a component inventory or architecture section.
- Base every claim on observable behavior in the code, tests, or assertions. Label inference
  explicitly.
- `fails:` blocks describe correct named outcomes, not defect reports. Focus on cases where the
  caller must branch on the specific failure to handle state correctly.
- If the entire provided code is trivial enough that no non-obvious contracts exist, say so in one
  sentence.

## Do Not

- Answer this prompt with architecture prose, implementation walkthroughs, or conventional
  summaries.
- Emit prose paragraphs in place of notation blocks.
- List every possible exception in `fails:`; only name modes with distinct observable states.
- Diagnose bugs, propose fixes, or recommend refactors.
- Invent contracts not supported by the code.

## Quality Bar

- Every contract line must be falsifiable—a reader should be able to point to code that confirms or
  contradicts it.
- `fails:` blocks must describe observable post-failure state, not just name exception types.
- A reader who only reads the output should be able to reason correctly about calling conventions,
  ownership, and failure handling for any operation covered.
- If nothing non-obvious exists in the provided code, the correct output is one sentence saying so.
