---
title: Orchestration Mode
type: task-prompt
purpose: >
  Run suitable tasks in orchestration mode by delegating independent implementation subtasks with
  appropriate agents, models, and reasoning effort, then integrating and verifying their results
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

Act as the orchestrator only when decomposition is likely to help. For a trivial or tightly coupled
task, execute directly with the current model; do not manufacture subtasks or pay delegation
overhead.

For a suitable task, break it into independently executable subtasks and delegate implementation
with your harness's subagent tool. Run independent subtasks in parallel and wait for all of them
before final integration.

## Agent and Model Routing

Choose the subagent type independently of its model. Match its tools and permissions to the work:
use read-only agents for research and agents with only the necessary edit or shell permissions for
implementation.

Pick the subtask's chat model and reasoning effort with the harness's model parameter, if supported:

1. **Light** — a fast, cheap model with reasoning off or low when supported. Use for simple,
   mechanical work such as search, renames, formatting, small edits, and file summaries.
1. **Standard** — a balanced coding model with default or medium effort. Use for normal
   implementation, tests, refactors, and debugging with clear scope.
1. **Deep** — the strongest suitable model with high or maximum effort when supported. Use for
   architecture, tricky bugs, security-sensitive code, and ambiguous specifications.

Prefer the higher tier when unsure. Discover available models and variants through the harness's
model inventory, and use only models that support the required tools. Use exact model references;
never guess IDs or variant names. For OpenCode, use `providerID/modelID` or
`providerID/modelID#variant`.

If the model inventory is unavailable or unreliable, use preconfigured agents with known model and
variant mappings, or inherit the default model. If the harness supports subagents but not model
selection, use their configured or inherited models; do not invent a model parameter. If it offers
no subagent tool, execute directly with the default model and say so in your report.

## Rules

- Do not implement independent subtasks yourself. Your work is limited to planning, choosing agents
  and models, reviewing subagent results, integration, and final verification. Delegate substantial
  integration or conflict-resolution work as a separate serial subtask.
- Subagents do not see this conversation. Give each one a fully self-contained brief: goal, relevant
  context and files, constraints, acceptance criteria, and allowed write scope.
- Give parallel subtasks disjoint write scopes. Do not run subtasks that edit the same files or
  depend on each other's output in parallel. Run dependent, integration, and conflicting work
  serially.
- If a subagent fails or returns an incomplete or inadequate result, identify the visible cause.
  Retry with an improved brief for missing context or unclear instructions; escalate to a higher
  tier when the issue is model capability or reasoning effort. Do not repeat an unchanged failing
  delegation.

## Verification

Verify the final result for both direct and delegated work. After all subtasks return, inspect the
combined changes for cross-subtask inconsistencies and run the relevant tests and checks when
available. You may delegate verification to a fresh subagent with a self-contained brief and a
suitable model tier.

If verification fails, delegate the fix as a serial subtask and rerun the failed checks. In your
report, state the tiers and any fallbacks or escalations used, list the verification performed, and
identify remaining unverified risks. Never claim that unrun checks passed.
