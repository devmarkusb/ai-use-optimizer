# AI Use Optimizer

[![CI](https://github.com/devmarkusb/ai-use-optimizer/actions/workflows/ci.yml/badge.svg)](https://github.com/devmarkusb/ai-use-optimizer/actions/workflows/ci.yml)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/devmarkusb/ai-use-optimizer/blob/main/.pre-commit-config.yaml)
[![Dependabot](https://img.shields.io/badge/dependabot-enabled-025e8c?logo=dependabot&logoColor=white)](https://github.com/devmarkusb/ai-use-optimizer/blob/main/.github/dependabot.yml)
[![Security](https://img.shields.io/badge/security-gitleaks%20%7C%20pip--audit%20%7C%20zizmor-6e4c7b)](https://github.com/devmarkusb/ai-use-optimizer/blob/main/.github/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

Reusable prompts and docs for working with LLMs. Each tool lives under `prompts/` with usage notes
here. Licensed under the [MIT License](./LICENSE).

## Contents

- [Introduction](#introduction)
- [Development](#development)
- [Choosing a prompt](#choosing-a-prompt)
- [Tools in this repository](#tools-in-this-repository)
- [Prompt style guide](#prompt-style-guide)
- [Prompt Architect](#prompt-architect)
  - [When to use](#when-to-use-prompt-architect)
  - [How to use](#how-to-use-prompt-architect)
  - [Maintenance](#maintenance)
- [Interview Me](#interview-me)
  - [When to use Interview Me](#when-to-use-interview-me)
  - [When not to use Interview Me](#when-not-to-use-interview-me)
  - [Interview Me file](#interview-me-file)
  - [How to use Interview Me](#how-to-use-interview-me)
  - [What Interview Me should produce](#what-interview-me-should-produce)
- [AI Repo Setup](#ai-repo-setup)
  - [When to use](#when-to-use-ai-repo-setup)
  - [When not to use](#when-not-to-use-ai-repo-setup)
  - [File location](#file-location)
  - [How to use](#how-to-use-ai-repo-setup)
  - [What you should get](#what-you-should-get)

## Introduction

Practical helpers you can paste into ChatGPT, Claude, Cursor, Codex, Gemini, or your own
automation—not one-off viral tricks. New tools can be added alongside existing ones without
rewriting the repo.

## Development

Markdown in `README.md`, `AGENTS.md`, `CLAUDE.md`, and `prompts/**/*.md` uses a **100-column** wrap
and lint via [pre-commit](https://pre-commit.com) (local on commit and in CI).

**Prerequisites:** [uv](https://docs.astral.sh/uv/) (`brew install uv` on macOS).

```bash
uv sync
uv run pre-commit install
uv run pre-commit run --all-files   # check or fix
```

`mdformat` reflows prose; `markdownlint-cli2` enforces `.markdownlint-cli2.jsonc`. See
`.pre-commit-config.yaml` and `.mdformat.toml`.

**CI** (`.github/workflows/ci.yml`): pre-commit (Markdown, gitleaks, actionlint), lychee link check,
README prompt index guard, pip-audit, zizmor. Dependabot (`.github/dependabot.yml`) proposes weekly
GitHub Actions and uv dev dependency updates.

## Choosing a prompt

| You want to…                                                                                    | Start with                                                                               |
| ----------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Improve wording before you send a request                                                       | [Prompt Architect](#prompt-architect)                                                    |
| Turn a manual workflow into questions before delegating or automating                           | [Interview Me](#interview-me)                                                            |
| Rethink a hard problem via multiple formal representations                                      | `prompts/find-the-right-representation.md`                                               |
| Shorten prose or code without changing meaning or behavior                                      | `prompts/shorten-and-simplify.md`                                                        |
| Derive an evidence-based dev spec from an existing codebase                                     | `prompts/reverse-engineer-dev-spec.md`                                                   |
| Add or normalize agent config in an existing repo (`AGENTS.md`, Cursor rules, Claude Code, MCP) | [AI Repo Setup](#ai-repo-setup)                                                          |
| Bootstrap a new codebase from an empty or nearly empty repo                                     | `prompts/project-start.md` (run **before** AI Repo Setup if you later want agent config) |

Architect shapes *prompts*; Interview Me extracts workflow detail; AI Repo Setup shapes *repo agent
config*. Other task prompts cover representation search, compression, brownfield specs, and
greenfield bootstrap.

## Tools in this repository

| Tool                                           | Role                                                                                                         |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| **Prompt Architect**                           | Meta-prompt: rough ideas → stronger prompts for any supported target.                                        |
| **Interview Me**                               | Task prompt: clarification questions before an agent reproduces or automates a workflow.                     |
| **Find the Right Representation**              | Task prompt: search formal representations (graphs, constraints, optimization, etc.) before solving.         |
| **Shorten and Simplify**                       | Task prompt: shorten text or code while preserving meaning, behavior, and constraints.                       |
| **Reverse-Engineer Development Specification** | Brownfield task prompt: evidence-based engineering spec from the current codebase.                           |
| **Project Start**                              | Greenfield task prompt: bootstrap stack, structure, tooling, and README (not full agent config).             |
| **AI Repo Setup**                              | Task prompt: inspect a repo and add minimal `AGENTS.md`-style setup (Cursor, Claude Code, compatible tools). |

More tools may be added over time.

## Prompt style guide

Use when adding or updating prompts in `prompts/`.

- Files: `<slug>.md` (task) or `<slug>.system.md` (system/meta). No `.prompt.md` suffix.
- YAML front matter: `title`, `type`, `purpose`, `targets`, `scope`; optional `version`,
  `last-reviewed`, `recommended-stage` when useful.
- H1 matches `title`; prefer sections such as `Context`, `Goal`, `Task`, `Instructions`,
  `Required Workflow`, `Rules`, `Output Format`, `Deliverables`, `Quality Bar`.
- Short, direct instructions; concrete `Use`, `Avoid`, `Do not` over persona language.
- Explicit constraints: inputs, outputs, limits, stop conditions, safety, success criteria,
  verification.
- Self-contained and pasteable—no README required to run a prompt.
- No generic boilerplate, unsupported claims, hidden chain-of-thought, or tricks without a real
  failure mode.
- On add/rename: update **Choosing a prompt** and **Tools in this repository** with literal
  `prompts/<slug>.md` (or `.system.md`). CI fails if a prompt file is not indexed.
- First-class tools: document when to use, when not, path, and expected result here.

## Prompt Architect

Meta-prompt: `prompts/prompt-architect.system.md`. It improves the *prompt* you will paste
elsewhere—not the original task. The file is self-contained (starter form, field guide, target and
mode handling, intake rules). See **Starter response**, **Intake behavior**, and **Operating modes**
in the file; you do not need this README to use it.

### When to use Prompt Architect

Use when a prompt has a fuzzy goal, weak structure, or unclear success criteria—e.g. Cursor rules,
agent instructions, team prompts, or coding requests you want tightened before execution.

Skip when the prompt is final and you want execution now, or when you need repo agent layout (use
[AI Repo Setup](#ai-repo-setup)).

### How to use Prompt Architect

1. Paste or **@** `prompts/prompt-architect.system.md` (system or first message in Cursor).
1. Use the model’s starter form, or send a rough request in plain language.

Optional persistent copy: `.cursor/rules/prompt-architect.mdc`

### Maintenance

Review `prompts/prompt-architect.system.md` every 1–3 months or after a major model release. Prefer
small edits; keep `CHANGELOG.md`; add tests before large changes. Prefer updates backed by provider
docs, repeatable tests, measurable improvement, and fewer failure modes—not viral prompt tricks.

## Interview Me

`prompts/interview-me.md` asks targeted questions about a task or workflow before an agent
reproduces or automates it—not automation or solutions.

### When to use Interview Me

When a task is easy to demo but hard to specify: recurring browser/IDE workflows, repo maintenance,
data cleanup, handoffs, checklists, automation candidates. Useful before a task prompt, runbook,
SOP, or agent instruction.

### When not to use Interview Me

Skip when the task is fully specified and you want execution, or when you want prompt rewriting—use
[Prompt Architect](#prompt-architect).

### Interview Me file

`prompts/interview-me.md`

### How to use Interview Me

1. Paste `prompts/interview-me.md` in your LLM.
1. Describe the task (performed, planned, or to automate); include files, screenshots, commands,
   tools, I/O, and constraints when available.
1. Answer questions; use answers for the implementing agent.

### What Interview Me should produce

At most 10 numbered clarification questions (correctness, safety, repeatability, tools, I/O,
dependencies, edge cases, failures, permissions, success criteria). Stop early if already specified.

## AI Repo Setup

`prompts/ai-repo-setup.md` is a **task** prompt for a coding agent inside a repo: inspect tree,
tooling, and CI; add or update only justified agent files—usually `AGENTS.md` plus thin adapters.
Not for arbitrary prompt wording ([Prompt Architect](#prompt-architect)).

### When to use AI Repo Setup

**Brownfield** codebases or **greenfield repos with** build, tests, formatter, CI, and README—e.g.
onboarding Cursor/Claude Code, standardizing `AGENTS.md`, cleaning stale `.cursorrules`, or after a
stack change.

### When not to use AI Repo Setup

Not for empty dirs or creating a project from an idea—use `prompts/project-start.md` first, then
return when tooling exists.

### File location

`prompts/ai-repo-setup.md`

### How to use AI Repo Setup

1. Open the target repo in an agent with tree access.
1. Attach `prompts/ai-repo-setup.md` (e.g. `@prompts/ai-repo-setup.md` in Cursor).
1. Optionally ask for assessment and file list before large edits.

Use one session with full repo access; review diffs (prompt avoids secrets, lockfiles, releases
unless expanded). Re-run after large refactors; say in chat if sections must stay.

### What you should get

Short repo assessment; created/changed files with rationale; build/test/lint commands
(**unverified** if not run); unknowns; brief global vs repo-local maintenance policy. On-disk output
stays small and specific—not a template dump.
