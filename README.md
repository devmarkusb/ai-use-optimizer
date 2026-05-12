# AI Use Optimizer

This repository collects reusable tools for improving how you work with large language models. Each tool lives in its own area of the repo with its own files and usage notes.

## Contents

- [Introduction](#introduction)
- [Choosing a prompt](#choosing-a-prompt)
- [Tools in this repository](#tools-in-this-repository)
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
- [AI Repo Setup](#ai-repo-setup)
  - [When to use](#when-to-use-ai-repo-setup)
  - [When not to use](#when-not-to-use-ai-repo-setup)
  - [File location](#file-location)
  - [How to use](#how-to-use-ai-repo-setup)
  - [What you should get](#what-you-should-get)

## Introduction

The goal is practical, maintainable helpers you can copy into ChatGPT, Claude, Cursor, Codex, Gemini, or your own automation—not one-off viral tricks. New optimizers can be added alongside existing ones without rewriting the whole repo.

## Choosing a prompt

| You want to… | Start with |
|----------------|------------|
| Improve wording of a request before you send it | [Prompt Architect](#prompt-architect) |
| Add or normalize AI agent config in an existing repo (`AGENTS.md`, Cursor rules, Claude Code, MCP) | [AI Repo Setup](#ai-repo-setup) |
| Bootstrap a new codebase from an empty or nearly empty repo | `prompts/project-start.prompt.md` (greenfield scaffold; run **before** AI Repo Setup if you later want agent config) |

Prompt Architect and AI Repo Setup solve different problems: one shapes *prompts*, the other shapes *repository agent configuration*.

## Tools in this repository

| Tool | Role |
|------|------|
| **Prompt Architect** | Meta-prompt that turns rough ideas into stronger prompts for any supported target. |
| **AI Repo Setup** | Task prompt for inspecting a real repo and creating minimal, justified `AGENTS.md`-style agent setup (Cursor, Claude Code, compatible tools). |

More tools may be added here over time.

## Prompt Architect

`prompt-architect.system.md` is a reusable meta prompt for turning rough ideas into high-quality prompts for ChatGPT, Codex, Claude, Gemini, Cursor, and generic LLMs.

It is not meant to solve the original task directly. Its job is to produce a better prompt.

### When to use Prompt Architect

Use it when you have a fuzzy goal, weak structure, or unclear success criteria for a prompt you will paste elsewhere. Typical cases: drafting Cursor rules, agent instructions, repeated team prompts, research or writing briefs, or coding requests where you want the *prompt* tightened before execution.

Skip it when you already have a precise, final prompt and want the model to execute the task immediately, or when you need repository-specific agent file layout (use [AI Repo Setup](#ai-repo-setup) instead).

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

It does not solve tasks directly.
It generates better prompts.

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
2. Paste the contents of `prompt-architect.system.md`.
3. Then send your rough request.

In Cursor, you can paste the file contents into the system or first user message, or use **@** to reference `prompts/prompt-architect.system.md` in chat so the model loads it as context.

### Recommended request format

Use this structure (or don't):

```text
Target: ChatGPT | Codex | Claude | Claude Code | Gemini | Cursor | Generic
Mode: BASIC | DETAIL | PRODUCTION

Goal:
[What you want the final prompt to achieve]

Context:
[Audience, domain, constraints, inputs, project details]

Output:
[Desired format, length, style, schema, or deliverable]

Rough prompt:
[Your current draft, if any]
```

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
Use your favorite AI agent for that, perhaps even with the help of `prompt-architect.system.md` itself.

Prefer small, justified edits over complete rewrites.

Keep a `CHANGELOG.md`.

Perhaps even add tests before changing the meta-prompt.

Do not chase every viral prompt trick.

Prefer updates backed by:
1. official provider documentation
2. repeatable tests
3. measurable improvement
4. clear reduction in failure modes

## AI Repo Setup

`prompts/ai-repo-setup.prompt.md` is a **task** prompt for an AI coding agent. You run it *inside* a repository (or with the repo open in the IDE) so the agent can inspect the tree, tooling, and CI, then add or update only the agent-oriented files that make sense—usually starting with a concise `AGENTS.md` and thin tool-specific adapters.

It is not a meta-prompt for wording arbitrary requests; for that, use [Prompt Architect](#prompt-architect).

### When to use AI Repo Setup

Use it on **brownfield** codebases, or on **greenfield repos that already have** a scaffold: build system, tests, formatter, CI skeleton, and a first README. Typical triggers: onboarding a team to Cursor or Claude Code, standardizing on `AGENTS.md`, removing duplicated or stale `.cursorrules`-style content, or after a major stack change when agent instructions should track reality.

### When not to use AI Repo Setup

Do not use it for **completely empty** directories or when you still need to **create the project from an idea**—use `prompts/project-start.prompt.md` first, then return here once the repo exists and has real tooling to inspect.

### File location

```text
prompts/
  ai-repo-setup.prompt.md
```

### How to use AI Repo Setup

1. Open the **target repository** in Cursor (or another agent that can read the tree and edit files).
2. Attach or paste `prompts/ai-repo-setup.prompt.md` (for example `@prompts/ai-repo-setup.prompt.md` in Cursor chat).
3. Ask the agent to follow the prompt and report the assessment and file list before large edits if you want an extra checkpoint.

Prefer a **single session** with full repo access so inspection steps (package manager, CI, linters) are accurate. Review diffs carefully: the prompt intentionally avoids secrets, lockfiles, and release workflows unless you explicitly expand scope.

### What you should get

The agent should return a short repo assessment, a list of created or changed files with rationale, discovered build or test or lint commands (marked **unverified** when not run), unknowns, and a brief maintenance policy for global versus repo-local config. The on-disk result should stay **small and specific**—not a large generic template dump.
