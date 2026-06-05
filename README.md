# AI Use Optimizer

[![CI](https://github.com/devmarkusb/ai-use-optimizer/actions/workflows/ci.yml/badge.svg)](https://github.com/devmarkusb/ai-use-optimizer/actions/workflows/ci.yml)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/devmarkusb/ai-use-optimizer/blob/main/.pre-commit-config.yaml)
[![Dependabot](https://img.shields.io/badge/dependabot-enabled-025e8c?logo=dependabot&logoColor=white)](https://github.com/devmarkusb/ai-use-optimizer/blob/main/.github/dependabot.yml)
[![Security](https://img.shields.io/badge/security-gitleaks%20%7C%20pip--audit%20%7C%20zizmor-6e4c7b)](https://github.com/devmarkusb/ai-use-optimizer/blob/main/.github/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

Reusable prompts for working with LLMs. Each file under `prompts/` is meant to be pasted as-is; this
README adds chooser notes only where helpful. Licensed under the [MIT License](./LICENSE).

## Contents

- [Introduction](#introduction)
- [Development](#development)
- [Tools](#tools)
- [Prompt style guide](#prompt-style-guide)
- [Prompt Architect](#prompt-architect)
- [Interview Me](#interview-me)
- [AI Repo Setup](#ai-repo-setup)

## Introduction

Practical helpers for ChatGPT, Claude, Cursor, Codex, Gemini, or your own automation—not one-off
viral tricks. New prompts can be added without rewriting the repo.

## Development

Markdown in `README.md`, `AGENTS.md`, `CLAUDE.md`, `promptfill/README.md`, and `prompts/**/*.md`
uses a **100-column** wrap and lint via [pre-commit](https://pre-commit.com) (local on commit and in
CI).

**Prerequisites:** [uv](https://docs.astral.sh/uv/) (`brew install uv` on macOS).

```bash
uv sync
uv run pre-commit install
uv run pre-commit run --all-files   # check or fix
```

`mdformat` reflows prose; `markdownlint-cli2` enforces `.markdownlint-cli2.jsonc`. See
`.pre-commit-config.yaml` and `.mdformat.toml`.

**CI** (`.github/workflows/ci.yml`): pre-commit (Markdown, gitleaks, actionlint), lychee link check,
README prompt index guard, **promptfill** pytest (`promptfill/`), pip-audit (root and promptfill),
zizmor. Dependabot (`.github/dependabot.yml`) proposes weekly GitHub Actions and uv dependency
updates (root dev tools and `promptfill/`).

**promptfill** (`promptfill/`): CLI to pick a prompt, fill `<PLACEHOLDER>` values, and copy the
rendered text to the clipboard (Espanso-friendly). See `promptfill/README.md`. From `promptfill/`:
`uv sync && uv run pytest`.

## Tools

Pick by goal; paste the prompt file. **More** links to short README notes when they exist (not a
second copy of the prompt).

| You want to…                                                                                    | Prompt                                     | More                                  |
| ----------------------------------------------------------------------------------------------- | ------------------------------------------ | ------------------------------------- |
| Improve wording before you send a request                                                       | `prompts/prompt-architect.system.md`       | [Prompt Architect](#prompt-architect) |
| Turn a manual workflow into questions before delegating or automating                           | `prompts/interview-me.md`                  | [Interview Me](#interview-me)         |
| Rethink a hard problem via multiple formal representations                                      | `prompts/find-the-right-representation.md` | —                                     |
| Shorten prose or code without changing meaning or behavior                                      | `prompts/shorten-and-simplify.md`          | —                                     |
| Derive an evidence-based dev spec from an existing codebase                                     | `prompts/reverse-engineer-dev-spec.md`     | —                                     |
| Stress-test a PR, diff, or design by grilling the author on decisions and failure modes         | `prompts/grill-me.md`                      | —                                     |
| Triage a PR or diff to the few spots a human must read before merge                             | `prompts/human-code-review.md`             | —                                     |
| Add or normalize agent config in an existing repo (`AGENTS.md`, Cursor rules, Claude Code, MCP) | `prompts/ai-repo-setup.md`                 | [AI Repo Setup](#ai-repo-setup)       |
| Bootstrap a new codebase from an empty or nearly empty repo                                     | `prompts/project-start.md`                 | —                                     |

Greenfield: run `prompts/project-start.md` first; use `prompts/ai-repo-setup.md` after the repo has
real tooling. Architect shapes *prompts*; Interview Me extracts workflow detail; AI Repo Setup
shapes *repo agent config*.

## Prompt style guide

Use when adding or updating prompts in `prompts/`.

- Files: `<slug>.md` (task) or `<slug>.system.md` (system/meta). No `.prompt.md` suffix.
- YAML front matter: `title`, `type`, `purpose`, `targets`, `scope`; optional `version`,
  `last-reviewed`, `recommended-stage` when useful.
- H1 matches `title`; prefer sections such as `Context`, `Goal`, `Task`, `Instructions`,
  `Required Workflow`, `Rules`, `Output Format`, `Deliverables`, and `Quality Bar`.
- Short, direct instructions; concrete `Use`, `Avoid`, `Do not` over persona language.
- Explicit constraints: inputs, outputs, limits, stop conditions, safety, success criteria,
  verification.
- Self-contained and pasteable—no README required to run a prompt.
- No generic boilerplate, unsupported claims, hidden chain-of-thought, or tricks without a real
  failure mode.
- On add/rename: add a row to **Tools** with literal `prompts/<slug>.md` (or `.system.md`). CI fails
  if a prompt file is not indexed.
- README **More** sections only for chooser disambiguation or repo-specific notes—never duplicate
  the prompt body.

## Prompt Architect

`prompts/prompt-architect.system.md` improves the *prompt* you paste elsewhere, not the original
task. The file is self-contained (**Starter response**, **Intake behavior**, **Operating modes**).

**Use** when a prompt has a fuzzy goal, weak structure, or unclear success criteria. **Skip** when
the prompt is final and you want execution, or for repo agent layout
([AI Repo Setup](#ai-repo-setup)).

Paste or **@** the file (system or first message in Cursor); use the starter form or a rough
request. Optional: `.cursor/rules/prompt-architect.mdc`.

**Maintenance:** review the file every 1–3 months or after a major model release; prefer small
edits, `CHANGELOG.md`, and provider-backed changes—not viral prompt tricks.

## Interview Me

`prompts/interview-me.md` asks clarification questions before an agent reproduces or automates a
workflow (rules and output format are in the file).

**Use** when a task is easy to demo but hard to specify. **Skip** when the task is fully specified,
or for prompt rewriting ([Prompt Architect](#prompt-architect)).

Paste the file, describe the task with any relevant artifacts, then answer the questions for the
next agent.

## AI Repo Setup

`prompts/ai-repo-setup.md` runs inside a target repo: inspect tree and tooling, then add minimal
justified agent files (`AGENTS.md`, thin adapters). Task, constraints, and deliverables are in the
prompt—not for arbitrary prompt wording ([Prompt Architect](#prompt-architect)).

**Use** on brownfield code or greenfield repos that already have build, tests, formatter, CI, and
README. **Skip** for empty dirs or idea-only bootstrap—use `prompts/project-start.md` first.

Open the target repo, attach `prompts/ai-repo-setup.md` (e.g. `@prompts/ai-repo-setup.md`),
optionally ask for assessment before large edits. One session with full tree access; review diffs.
