---
title: Explain Code Level 3
type: task-prompt
purpose: Explain subsystem dynamics through lifecycle, mutation, failure, and dependency views
targets:
  - ChatGPT
  - Claude
  - Codex
  - Cursor
  - Generic LLM coding agents
scope:
  - code understanding
  - system dynamics
  - brownfield code
---

# Explain Code Level 3

## Task

Explain the dynamic behavior of this subsystem.

## Output Format

Produce seven views:

1. Lifecycle Picture: states, transitions, and who triggers each transition.
1. Mutation Picture: which objects may modify which other objects. Distinguish owns, mutates, reads,
   observes, and caches.
1. Failure Picture: failure modes. For each, include trigger, detection, recovery, and resulting
   state.
1. Ownership Picture: ownership, including lifetime, borrowing, shared ownership, invalidation, and
   caching.
1. Consistency Picture: object invariants, cross-module invariants, persistence invariants, and
   concurrency assumptions.
1. Dependency Picture: the dependency graph, separated into internal modules, external libraries,
   and external systems. Identify boundaries and list side effects.
1. Edit Impact Picture: for each major component, what is likely affected, what is unlikely
   affected, and what hidden coupling exists.

End with:

1. Unknown Boundaries: "Things this analysis cannot know."
1. Next Files To Inspect: if any lifecycle, mutation, failure, ownership, consistency, dependency,
   or edit-impact behavior depends on uninspected code, list the smallest useful files or
   directories to inspect next.

For each next file or directory, include:

- path
- suspected responsibility
- uncertainty it would resolve
- which picture it affects

## Rules

- Be explicit whenever behavior depends on code outside the inspected files.
- Never invent details.
