---
title: Extract Application IR
type: task-prompt
purpose: Normalize an existing codebase into a language-independent semantic intermediate representation
targets:
  - ChatGPT
  - Claude
  - Claude Code
  - Codex
  - Cursor
  - Gemini
  - Generic LLM
scope:
  - brownfield
  - reverse engineering
  - semantic modeling
---

# Extract Application IR

## Context

You are given an existing codebase. Your job is to reconstruct its semantic intermediate
representation: the canonical, implementation-independent description of what the system *is* and
*does*.

Treat the repository as evidence, not as the shape the IR must keep. The IR should contain enough
semantic information for documentation, UML, tests, APIs, database schemas, or another
implementation to be generated later without consulting the original source.

## Goal

Extract the complete semantic model of the application.

Preserve externally observable semantics. Omit implementation details unless they encode semantics.
Prefer stable concepts over implementation artifacts.

## Evidence Rules

- Base every statement on repository evidence: source code, tests, assertions, schemas, migrations,
  API contracts, configuration, documentation, naming, and comments.
- For every non-trivial claim, assign confidence: `High`, `Medium`, or `Low`.
- Distinguish confirmed facts from inference. Mark inferred concepts with `[inferred]` and state
  uncertainty explicitly.
- Never invent business semantics.

## Required Workflow

1. Map the repository evidence relevant to domain concepts, behavior, persistence, integration,
   configuration, and operations.
1. Extract the **Domain Layer**: what exists.
1. Extract the **Behavior Layer**: what the application does.
1. Extract the **Operational Layer**: software semantics that affect behavior or correctness.
1. Normalize synonymous concepts and implementation-specific entry points into semantic objects.
1. Check that cross-references are consistent, duplicate semantics are removed, and non-trivial
   claims carry confidence and inference markers.

## IR Layers

The resulting IR consists of exactly three semantic layers.

### 1. Domain Layer

Describe what exists:

- entities
- value objects
- enumerations
- relationships and cardinalities
- identity and ownership
- aggregates
- lifecycles and state machines
- invariants
- derived properties

Ignore databases and APIs unless they encode domain semantics.

### 2. Behavior Layer

Describe what the application does:

- commands
- queries
- operations
- workflows
- state transitions
- preconditions and postconditions
- side effects
- events
- failure modes
- retry semantics
- consistency guarantees

Express behavior declaratively. Do not describe implementation steps unless they are externally
observable.

### 3. Operational Layer

Describe software semantics:

- persistence
- transactions and isolation assumptions
- authorization and authentication
- external systems
- messaging and event streams
- cache semantics
- indexes and search
- versioning and replication
- scheduling
- observability and audit
- deployment assumptions

Include only semantics observable from the repository.

## Normalization Rules

- Normalize synonymous concepts. For example, `CustomerService`, `CustomerManager`, and
  `CustomerFacade` may all become `Service Customer` when the evidence supports that semantic role.
- Normalize CRUD handlers, REST controllers, GraphQL resolvers, and RPC endpoints into semantic
  operations.
- Recover implicit semantics where justified: ownership, invariants, transactional boundaries,
  bounded contexts, aggregate roots, event producers, and consistency assumptions.
- Reference semantic objects by name. Do not duplicate the same semantics in multiple places.
- Prefer semantic names such as `Entity Booking`, `Command ConfirmBooking`, and
  `publishes BookingConfirmed` over implementation names such as `class Booking`,
  `BookingService::confirm()`, or `KafkaProducer::publish(...)`.

## Ignore

Do not emit these unless they carry business or correctness semantics:

- call graphs
- include graphs
- inheritance trees
- helper classes
- utility functions
- implementation patterns
- framework plumbing
- dependency injection
- templates
- macros
- generated code

## Output Format

Produce one normalized textual Application IR. Use structured notation only, not explanatory prose.
Omit empty fields.

Use this shape:

```text
Application <Name>

Domain Layer

Bounded Context <Name>
confidence: High|Medium|Low
evidence:
    <path or artifact>

Entity <Name>
identity:
    <Identity>
owns:
    <Entity>[*]
references:
    <Entity>
invariants:
    <invariant> [inferred]
derived:
    <property>
confidence: High|Medium|Low
evidence:
    <path or artifact>

Behavior Layer

Command <Name>
requires:
    <precondition>
writes:
    <semantic object or property>
ensures:
    <postcondition>
publishes:
    <Event>
fails:
    <FailureMode>
confidence: High|Medium|Low
evidence:
    <path or artifact>

Query <Name>
reads:
    <semantic object or property>
returns:
    <result>
confidence: High|Medium|Low
evidence:
    <path or artifact>

Operational Layer

Repository <Name>
stores:
    <Entity>
transaction:
    <semantics>
confidence: High|Medium|Low
evidence:
    <path or artifact>

External System <Name>
operations:
    <Operation>
failure modes:
    <FailureMode>
confidence: High|Medium|Low
evidence:
    <path or artifact>
```

## Quality Bar

- The IR is language independent, framework independent, implementation independent, deterministic,
  internally consistent, human readable, and machine parseable.
- Every non-trivial semantic claim is supported by evidence, confidence, and inference status.
- A reader can use the IR to regenerate documentation, UML, tests, APIs, database schemas, or
  another implementation without consulting the original source.
- The output models semantics rather than implementation structure.
