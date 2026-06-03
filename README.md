# AI Use Optimizer

[![CI](https://github.com/devmarkusb/ai-use-optimizer/actions/workflows/ci.yml/badge.svg)](https://github.com/devmarkusb/ai-use-optimizer/actions/workflows/ci.yml)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/devmarkusb/ai-use-optimizer/blob/master/.pre-commit-config.yaml)
[![Dependabot](https://img.shields.io/badge/dependabot-enabled-025e8c?logo=dependabot&logoColor=white)](https://github.com/devmarkusb/ai-use-optimizer/blob/master/.github/dependabot.yml)
[![Security](https://img.shields.io/badge/security-gitleaks%20%7C%20pip--audit%20%7C%20zizmor-6e4c7b)](https://github.com/devmarkusb/ai-use-optimizer/blob/master/.github/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

This repository collects reusable tools for improving how you work with large language models. Each
tool lives in its own area of the repo with its own files and usage notes.

## Contents

- [Introduction](#introduction)
- [Development](#development)
- [Choosing a prompt](#choosing-a-prompt)
- [Tools in this repository](#tools-in-this-repository)
- [Prompt style guide](#prompt-style-guide)
- [Prompt Architect](#prompt-architect)
  - [When to use](#when-to-use-prompt-architect)
  - [Files](#files)
  - [How to use](#how-to-use)
    - [Quick start](#quick-start)
  - [Recommended request format](#recommended-request-format)
  - [Modes](#modes)
    - [BASIC](#basic)
    - [DETAIL](#detail)
    - [PRODUCTION](#production)
  - [Maintenance workflow](#maintenance-workflow)
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

The goal is practical, maintainable helpers you can copy into ChatGPT, Claude, Cursor, Codex,
Gemini, or your own automation—not one-off viral tricks. New optimizers can be added alongside
existing ones without rewriting the whole repo.

This repository is licensed under the [MIT License](./LICENSE).

## Development

Markdown in `README.md`, `AGENTS.md`, `CLAUDE.md`, and `prompts/**/*.md` is kept readable with a
**100-column** wrap and lint checks. [pre-commit](https://pre-commit.com) runs locally on commit and
in CI.

**Prerequisites:** [uv](https://docs.astral.sh/uv/) (`brew install uv` on macOS).

**One-time setup:**

```bash
uv sync
uv run pre-commit install
```

**Check or fix everything:**

```bash
uv run pre-commit run --all-files
```

`mdformat` reflows wrapped paragraphs; `markdownlint-cli2` enforces the rules in
`.markdownlint-cli2.jsonc` (line length, heading style, and similar). Config:
`.pre-commit-config.yaml`, `.mdformat.toml`.

**CI on GitHub** (`.github/workflows/ci.yml`, same checks you can run locally plus):

- pre-commit (Markdown, gitleaks secret scan, actionlint on workflows)
- lychee link check on docs
- README path guard
- pip-audit on dev dependencies
- zizmor workflow security analysis

Dependabot (`.github/dependabot.yml`) proposes weekly updates for GitHub Actions and uv dev deps.

## Choosing a prompt

| You want to…                                                                                       | Start with                                                                                                    |
| -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Improve wording of a request before you send it                                                    | [Prompt Architect](#prompt-architect)                                                                         |
| Turn a manual workflow into questions before delegating or automating it                           | [Interview Me](#interview-me)                                                                                 |
| Rethink a hard problem by trying multiple formal representations                                   | `prompts/find-the-right-representation.md`                                                                    |
| Add or normalize AI agent config in an existing repo (`AGENTS.md`, Cursor rules, Claude Code, MCP) | [AI Repo Setup](#ai-repo-setup)                                                                               |
| Bootstrap a new codebase from an empty or nearly empty repo                                        | `prompts/project-start.md` (greenfield scaffold; run **before** AI Repo Setup if you later want agent config) |

Prompt Architect, Interview Me, and AI Repo Setup solve different problems: one shapes *prompts*,
one extracts missing workflow details, and one shapes *repository agent configuration*.

## Tools in this repository

| Tool                              | Role                                                                                                                                          |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **Prompt Architect**              | Meta-prompt that turns rough ideas into stronger prompts for any supported target.                                                            |
| **Interview Me**                  | Task prompt that asks targeted clarification questions before an agent reproduces or automates a workflow.                                    |
| **Find the Right Representation** | Task prompt that searches formal representations (graphs, constraints, optimization, and others) to expose structure before solving.          |
| **AI Repo Setup**                 | Task prompt for inspecting a real repo and creating minimal, justified `AGENTS.md`-style agent setup (Cursor, Claude Code, compatible tools). |

More tools may be added here over time.

## Prompt style guide

Use this style when adding or updating reusable prompts in `prompts/`.

- Name files under `prompts/` as `<slug>.md` for task prompts and `<slug>.system.md` for system or
  meta prompts. Do not use a `.prompt.md` suffix—the directory already signals purpose.
- Start first-class prompts with YAML front matter: `title`, `type`, `purpose`, `targets`, and
  `scope`; add fields such as `version`, `last-reviewed`, or `recommended-stage` only when they are
  useful.
- Use an H1 that matches the title, then prefer clear sections such as `Context`, `Goal`, `Task`,
  `Instructions`, `Required Workflow`, `Rules`, `Output Format`, `Deliverables`, and `Quality Bar`.
- Write operational instructions in short, direct sentences. Prefer concrete `Use`, `Avoid`, and
  `Do not` rules over broad persona language.
- Make constraints explicit: inputs, outputs, limits, stop conditions, safety boundaries, success
  criteria, and verification expectations.
- Keep prompts pasteable and self-contained. Do not require the user to read the README to run a
  prompt.
- Avoid generic boilerplate, unsupported claims, hidden chain-of-thought requests, and prompt tricks
  that do not reduce a real failure mode.
- When a prompt becomes a first-class tool, document when to use it, when not to use it, its file
  path, and the expected result in this README.

## Prompt Architect

`prompt-architect.system.md` is a reusable meta prompt for turning rough ideas into high-quality
prompts for ChatGPT, Codex, Claude, Gemini, Cursor, and generic LLMs.

It is not meant to solve the original task directly. Its job is to produce a better prompt.

### When to use Prompt Architect

Use it when you have a fuzzy goal, weak structure, or unclear success criteria for a prompt you will
paste elsewhere. Typical cases: drafting Cursor rules, agent instructions, repeated team prompts,
research or writing briefs, or coding requests where you want the *prompt* tightened before
execution.

Skip it when you already have a precise, final prompt and want the model to execute the task
immediately, or when you need repository-specific agent file layout (use
[AI Repo Setup](#ai-repo-setup) instead).

### Files

```text
prompts/
  prompt-architect.system.md
```

For Cursor-specific use, you may also keep a copy at:

```text
.cursor/rules/prompt-architect.mdc
```

### How to use

`prompt-architect.system.md` is a meta prompt.

It does not solve tasks directly. It generates better prompts.

Workflow:

```text
Your rough idea
    ↓
Prompt Architect optimizes it
    ↓
You receive a production-grade prompt
    ↓
Use that prompt in ChatGPT / Claude / Cursor / Codex
```

#### Quick start

1. Open ChatGPT, Claude, or another LLM.
1. Paste the contents of `prompt-architect.system.md`.
1. If the chatbot responds, it should show the ready line, the starter form, and the short field
   guide (see **Starter response** in `prompt-architect.system.md`).
1. Then send your rough request in plain language, or fill in and send the starter form.

In Cursor, you can paste the file contents into the system or first user message, or use **@** to
reference `prompts/prompt-architect.system.md` in chat so the model loads it as context.

### Recommended request format

This structure is optional and is embedded in `prompt-architect.system.md`. Use it when you want a
cleaner start; otherwise send a messy paragraph and let Prompt Architect infer the pieces.

```text
Target: ChatGPT | Codex | Claude | Claude Code | Gemini | Cursor | Generic
Mode: BASIC | DETAIL | PRODUCTION

Goal:
[The outcome the final prompt should cause. One or two sentences is enough.]

Context:
[Facts the target model must know or respect: audience, domain, constraints, inputs, files, examples, non-goals.]

Output:
[What the final answer should look like: format, length, tone, sections, schema, files, acceptance criteria.]

Rough prompt:
[Your messy draft, notes, bullets, or pasted instruction. Leave blank if Goal and Context already cover it.]
```

Field guide:

- **Goal** is the desired result of running the final prompt.
- **Context** is background, constraints, and source material the target model would not otherwise
  know.
- **Output** is the expected shape of the answer or deliverable.
- **Rough prompt** is any existing wording you want improved; it can be incomplete or duplicated
  elsewhere.

### Modes

#### BASIC

Use for quick improvements.

Best for:

- simple writing prompts
- small code prompts
- quick research prompts
- rewriting unclear requests

#### DETAIL

Use when quality matters and the task is underspecified.

Best for:

- professional writing
- technical design
- analysis
- research
- prompts that need clarifying questions

#### PRODUCTION

Use when the prompt will be reused.

Best for:

- Cursor rules
- Claude project instructions
- Custom GPT instructions
- agent prompts
- team prompt libraries
- automation workflows

### Maintenance workflow

Review `prompt-architect.system.md` every 1–3 months, or immediately after a major model release.
Use your favorite AI agent for that, perhaps even with the help of `prompt-architect.system.md`
itself.

Prefer small, justified edits over complete rewrites.

Keep a `CHANGELOG.md`.

Perhaps even add tests before changing the meta-prompt.

Do not chase every viral prompt trick.

Prefer updates backed by:

1. official provider documentation
1. repeatable tests
1. measurable improvement
1. clear reduction in failure modes

## Interview Me

`prompts/interview-me.md` is a task prompt for extracting the missing operational details behind a
task, workflow, or action before an agent reproduces or automates it.

It does not automate the workflow and does not propose a solution. Its job is to ask the questions
that make the next prompt, specification, script, or handoff safer and more complete.

### When to use Interview Me

Use it when a task is easy to demonstrate manually but hard to specify. Typical cases: recurring
browser or IDE workflows, repository maintenance routines, data cleanup, tool handoffs, manual
checklists, or automation candidates.

It is especially useful before writing a task prompt, runbook, standard operating procedure, or
agent instruction.

### When not to use Interview Me

Skip it when the task is already fully specified and you want execution now, or when you want a
rough request rewritten into a stronger prompt rather than interviewed. Use
[Prompt Architect](#prompt-architect) for prompt rewriting.

### Interview Me file

```text
prompts/
  interview-me.md
```

### How to use Interview Me

1. Paste or attach `prompts/interview-me.md` in ChatGPT, Claude, Cursor, Codex, Gemini, or another
   LLM.
1. Describe the task you just performed, plan to perform, or want an agent to reproduce. Include
   relevant files, screenshots, commands, tools, inputs, outputs, and constraints when available.
1. Answer the questions. Use the answers as context for the agent that will implement, automate, or
   document the workflow.

### What Interview Me should produce

You should get a numbered list of at most 10 clarification questions focused on correctness, safety,
repeatability, tools, inputs, outputs, dependencies, edge cases, failure handling, permissions, and
success criteria.

If the workflow is already sufficiently specified, it should stop early instead of inventing
unnecessary questions.

## AI Repo Setup

`prompts/ai-repo-setup.md` is a **task** prompt for an AI coding agent. You run it *inside* a
repository (or with the repo open in the IDE) so the agent can inspect the tree, tooling, and CI,
then add or update only the agent-oriented files that make sense—usually starting with a concise
`AGENTS.md` and thin tool-specific adapters.

It is not a meta-prompt for wording arbitrary requests; for that, use
[Prompt Architect](#prompt-architect).

### When to use AI Repo Setup

Use it on **brownfield** codebases, or on **greenfield repos that already have** a scaffold: build
system, tests, formatter, CI skeleton, and a first README. Typical triggers: onboarding a team to
Cursor or Claude Code, standardizing on `AGENTS.md`, removing duplicated or stale
`.cursorrules`-style content, or after a major stack change when agent instructions should track
reality.

### When not to use AI Repo Setup

Do not use it for **completely empty** directories or when you still need to **create the project
from an idea**—use `prompts/project-start.md` first, then return here once the repo exists and has
real tooling to inspect.

### File location

```text
prompts/
  ai-repo-setup.md
```

### How to use AI Repo Setup

1. Open the **target repository** in Cursor (or another agent that can read the tree and edit
   files).
1. Attach or paste `prompts/ai-repo-setup.md` (for example `@prompts/ai-repo-setup.md` in Cursor
   chat).
1. Ask the agent to follow the prompt and report the assessment and file list before large edits if
   you want an extra checkpoint.

Prefer a **single session** with full repo access so inspection steps (package manager, CI, linters)
are accurate. Review diffs carefully: the prompt intentionally avoids secrets, lockfiles, and
release workflows unless you explicitly expand scope. You can **re-run** the same prompt after large
refactors or stack changes; say in chat if specific sections must stay, and check the diff so custom
agent text is not dropped by mistake.

### What you should get

The agent should return a short repo assessment, a list of created or changed files with rationale,
discovered build or test or lint commands (marked **unverified** when not run), unknowns, and a
brief maintenance policy for global versus repo-local config. The on-disk result should stay **small
and specific**—not a large generic template dump.
