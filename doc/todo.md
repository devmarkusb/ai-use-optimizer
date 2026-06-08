# Code Semantic Digest — Research Notes & Future Tooling

Related prompt: [`prompts/code-semantic-digest.md`](../prompts/code-semantic-digest.md)

This document captures open questions and roadmap ideas that emerged from deep research into formal
behavioral specification languages (109-agent study, June 2026). The prompt is the immediate
deliverable; everything below is future work.

---

## What the prompt deliberately defers

The prompt asks an LLM to extract contracts and render them in the notation. It does not validate
that the contracts are consistent, type-check them against the source, generate tests from them, or
enforce them at runtime. All of that is deferred to the tooling tiers below.

---

## Tooling roadmap

The dream notation is technically achievable at DSL tier — not a full type-theoretic compiler — but
requires more than prompt engineering alone (LLM + Dafny as intermediate = 88% vs 86% baseline;
marginal gain confirmed by adversarial verification against 2025 POPL paper).

### Tier 1 — AI prompt (now)

`prompts/code-semantic-digest.md`. Works today. The LLM extracts contracts and renders them in the
notation. No tooling required.

**Ceiling:** LLM hallucinations, no consistency check, no diff between spec versions, no
mechanical use of the output.

### Tier 2 — DSL + language server

Define a formal grammar for the notation (tree-sitter or ANTLR). Ship a VS Code extension with:

- syntax highlighting
- spec linting (duplicate operation names, malformed blocks, missing `[inferred]` discipline)
- spec-to-stub generation (generate empty implementation signatures from `Operation` declarations)
- spec diff (compare contract versions across branches)

This tier makes specs first-class artifacts: version-controlled, diffable, lintable, and
reviewable.

**Open question:** Is there an existing LSP-ready grammar toolkit (tree-sitter, ANTLR, Langium)
that could host this notation as a VS Code extension with real-time linting and AI-assisted stub
generation, without needing a full type-theoretic verifier backend?

### Tier 3 — AI code action for extraction

Wire a VS Code code action to the language server: select a C++ class or function, invoke "Extract
Semantic Digest," and the extension calls an LLM with the source and produces a draft contract
block for the spec file. Human reviews and accepts.

This closes the loop between source and spec without requiring a full AST analysis backend.

### Tier 4 — Test skeleton generation from `fails:` blocks

Each named `fails:` block describes an observable post-failure state. That structure is sufficient
to generate:

- property-based test stubs (precondition → trigger → assert post-failure state)
- fuzz targets seeded from `requires:` negations
- contract conformance test runners

**Open question:** Can `fails:` semantics be given a rigorous operational definition without full
algebraic effects machinery — for example, by treating each named failure mode as a tagged
exceptional postcondition with an implicit "no normal return" constraint, using JML's
`exceptional_behavior` as the semantic anchor? (JML's `signals (E e) P` + `signals_only` is the
closest prior art.)

### Tier 5 — Lightweight static conformance

Check that the implementation does not obviously violate its spec:

- operations declared `ensures: result != null` should have a return-type non-null check
- `fails:` blocks without a corresponding catch or error path in the implementation flagged as
  spec/code drift

This is "documentation linting," not formal verification. No proof obligations. No alias analysis.

**Open question:** What is the minimal subset of frame condition semantics that can be statically
approximated without full alias analysis — specifically, could a restricted ownership model
(Rust-style or a simplified capability type) make side-effect declarations in `ensures:` both
declarative and mechanically checkable at DSL tier?

### Tier 6 — Full compiler (research-grade, long horizon)

Static verification of `ensures:` side-effect declarations (e.g., `inventory.reserved_for(result)`)
requires alias analysis. JML's own designers acknowledged this is non-trivial and conservative
(CHASE tool, VMCAI 2003). This tier is a research project, not an engineering project.

**Do not attempt until Tier 2–5 provide empirical signal on adoption and value.**

---

## The genuinely novel part of this notation

Every existing behavioral specification language — JML, Dafny, Design by Contract (Eiffel), F*,
Why3, OCL, TLA+, Alloy — treats contract violations as bugs. Precondition violations are client
bugs; postcondition violations are supplier bugs. There is no semantic slot for correct named
program outcomes that are not bugs.

The `fails:` block is architecturally new. It names domain failure modes (`OutOfStock`,
`PaymentRejected`) as first-class program states with their own postcondition sets. This was
confirmed by adversarial verification against the official Eiffel documentation (verbatim: *"A
run-time assertion violation is the manifestation of a bug"*) and against the algebraic
specification literature (Bidoit 1984, ICALP: equations alone cannot capture error introduction,
propagation, and recovery — declaration-level constructs are required).

JML's `signals (E e) P` comes closest but maps to Java exception class names, not human-readable
domain labels, and requires proof obligations the dream notation deliberately avoids.

---

## Closest existing foundation

If a Tier 2+ DSL is ever built, build on JML's semantic model:

- `requires:` ← JML `requires`
- `ensures:` ← JML `ensures` (normal behavior)
- `fails: X:` ← JML `exceptional_behavior` + `signals (X e)` + `signals_only X`
- `invariant:` ← JML `invariant`

Strip Java coupling, strip proof obligations, replace exception class names with domain labels,
add human-readable indented syntax.

---

## Open research questions (from the June 2026 study)

1. **`fails:` operational semantics.** Can the `fails:` block be given a rigorous definition
   without algebraic effects — e.g., as a tagged exceptional postcondition with implicit
   `ensures false` for normal return? JML `exceptional_behavior` is the anchor.

2. **LSP grammar toolkit.** Which of tree-sitter, ANTLR, or Langium best hosts this notation
   for a VS Code extension with real-time linting + AI code action, without a full type-theoretic
   backend?

3. **Lightweight frame conditions.** Can side-effect declarations (`ensures: inventory.reserved`)
   be statically approximated using a restricted ownership model (Rust-style borrowing or a
   simplified capability discipline) instead of full alias analysis?

4. **Industry empirical validation.** Has any team deployed a human-readable behavioral
   specification language — even informally — and measured whether it improved downstream test
   coverage or reduced integration bugs? No confirmed evidence of this exists in the literature.

---

## Research methodology note

Findings above marked as confirmed survived a 3-vote adversarial verification pass (need ≥2/3
votes to survive). Of 25 claims tested, 5 were confirmed and 20 were killed. The tooling roadmap
above is based only on confirmed claims plus sound inferences from them.
