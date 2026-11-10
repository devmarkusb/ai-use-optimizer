---
title: Orchestration Mode
type: task-prompt
purpose: >
  Run a task in orchestration mode by delegating all implementation subtasks to subagents and
  assembling their results
targets:
  - Claude Code
  - Codex
  - Cursor
  - OpenCode
  - Generic LLM coding agents with a subagent tool
scope:
  - multi-agent delegation
  - task orchestration
---

# Orchestration Mode

## Task

You are the orchestrator for the current task. Break it into independent subtasks and delegate each
one with your harness's subagent tool. Pick the subagent model per subtask by passing a `model`
parameter, if the harness supports it:

1. **Light** — fast, cheap models. Simple, mechanical work (search, renames, formatting, small
   edits, summarizing files)
1. **Standard** — balanced default models. Normal implementation, tests, refactors, debugging with
   clear scope
1. **Deep** — the strongest reasoning models. Hard reasoning (architecture, tricky bugs,
   security-sensitive code, ambiguous specs)

Map each tier to the closest model the harness actually offers (for example haiku / sonnet / opus in
Claude Code). Prefer the higher tier when unsure.

Run independent subtasks in parallel.

## Rules

- Do not do implementation work yourself. Your own work is limited to planning, choosing models,
  reviewing subagent results, and putting them together.
- Subagents do not see this conversation. Give each one a fully self-contained brief: goal, relevant
  files, constraints, acceptance criteria.
- If the harness offers no subagent tool or no model choice, proceed without it: run the task
  directly with the default model and say so in your report.
- After all subtasks return, verify the combined result (or delegate verification to a fresh
  subagent) before reporting.
