---
title: Project Start
type: task-prompt
purpose: Bootstrap a new software project from an idea
targets:
  - Codex
  - Claude Code
  - Cursor
  - Generic LLM coding agents
scope:
  - greenfield
recommended-stage: empty or nearly empty repository
---

# Project Start

## Context

This is a green-field project bootstrap.

The repository may currently be empty or nearly empty.

Prefer pragmatic, maintainable defaults over framework maximalism or premature abstraction.

## Inputs

The following section contains the actual project idea, requirements, constraints, and preferences.

\<PROBLEM>

## Instructions

Act as a senior software engineer and project bootstrap architect.

Before implementing:

- infer the likely project shape and architecture
- identify missing critical decisions
- make reasonable assumptions when possible
- explicitly state assumptions instead of blocking on every ambiguity

Bootstrap the project incrementally.

First:

1. propose the minimal architecture and stack
1. explain major technical decisions briefly
1. create the initial repository structure
1. create build, test, formatting, and linting setup
1. create minimal runnable functionality
1. create minimal and security CI if appropriate
1. create a concise README with exact commands and badges

Avoid:

- premature abstraction
- excessive microservices
- speculative extensibility
- unnecessary dependencies
- giant boilerplate
- fake implementations
- placeholder enterprise architecture

Do not yet create extensive AI-agent configuration. Only create minimal placeholders if clearly
useful. A separate AI repository setup pass will happen afterward.

## Deliverables

Return:

1. architecture summary
1. assumptions made
1. created files
1. exact build/test/run commands
1. recommended next steps
