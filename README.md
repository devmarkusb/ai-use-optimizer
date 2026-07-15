# AI Use Optimizer

[![CI](https://github.com/devmarkusb/ai-use-optimizer/actions/workflows/ci.yml/badge.svg)](https://github.com/devmarkusb/ai-use-optimizer/actions/workflows/ci.yml)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/devmarkusb/ai-use-optimizer/blob/main/.pre-commit-config.yaml)
[![Dependabot](https://img.shields.io/badge/dependabot-enabled-025e8c?logo=dependabot&logoColor=white)](https://github.com/devmarkusb/ai-use-optimizer/blob/main/.github/dependabot.yml)
[![Security](https://img.shields.io/badge/security-gitleaks%20%7C%20pip--audit%20%7C%20zizmor-6e4c7b)](https://github.com/devmarkusb/ai-use-optimizer/blob/main/.github/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

Reusable prompts for working with LLMs. Top-level files under `prompts/` are meant to be pasted
as-is; archived research prompts live under `prompts/archived/`. This README adds chooser notes only
where helpful. Licensed under the [MIT License](./LICENSE).

## Contents

- [Introduction](#introduction)
- [Development](#development)
- [Tools](#tools)
- [Prompt style guide](#prompt-style-guide)
- [Prompt Style Fit](#prompt-style-fit)
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

| You want to…                                                                                       | Prompt                                     | More                                  |
| -------------------------------------------------------------------------------------------------- | ------------------------------------------ | ------------------------------------- |
| Improve wording before you send a request                                                          | `prompts/prompt-architect.system.md`       | [Prompt Architect](#prompt-architect) |
| Bring a raw new prompt into this repo's style without bloating it                                  | `prompts/prompt-style-fit.md`              | [Prompt Style Fit](#prompt-style-fit) |
| Pause an uncertain agent after hard work and make it ask missing intent/context questions          | `prompts/interview-me.md`                  | [Interview Me](#interview-me)         |
| Rethink a hard problem via multiple formal representations                                         | `prompts/find-the-right-representation.md` | —                                     |
| Solve a difficult problem systematically with Polya-style heuristics                               | `prompts/how-to-solve-it.md`               | —                                     |
| Shorten scoped prose or code (one file/selection) without changing meaning or behavior             | `prompts/shorten-and-simplify.md`          | —                                     |
| Audit an AI agent session's visible context, tools, and context boundaries                         | `prompts/agent-info.md`                    | —                                     |
| Ground factual answers in cited sources, uncertainty, and contradicting evidence                   | `prompts/sources-please.md`                | —                                     |
| Sanity-check a conversation for unsupported claims, contradictions, sycophancy, and overconfidence | `prompts/verify.md`                        | —                                     |
| Review a branch PR for bugs, intent, comment fixes, repo-fit, and adversarial defense              | `prompts/code-review.md`                   | —                                     |
| Explain a code subtree at a quick intuition level                                                  | `prompts/explain-code-level-1.md`          | —                                     |
| Explain code as an architectural mental model                                                      | `prompts/explain-code-level-2.md`          | —                                     |
| Explain subsystem behavior through lifecycle, mutation, failure, and dependency views              | `prompts/explain-code-level-3.md`          | —                                     |
| Review code architecture for contracts, flows, risks, and unknown boundaries                       | `prompts/explain-code-level-4.md`          | —                                     |
| Add or normalize agent config in an existing repo (`AGENTS.md`, Cursor rules, Claude Code, MCP)    | `prompts/ai-repo-setup.md`                 | [AI Repo Setup](#ai-repo-setup)       |
| Bootstrap a new codebase from an empty or nearly empty repo                                        | `prompts/project-start.md`                 | —                                     |
| Fix failing CI across one or more repositories with minimal, verified changes                      | `prompts/fix-my-ci-runs.md`                | —                                     |
| Trim a messy diff to the smallest coherent patch that still achieves the intended change           | `prompts/cleanup-code-changes.md`          | —                                     |

Greenfield: run `prompts/project-start.md` first; use `prompts/ai-repo-setup.md` after the repo has
real tooling. Architect shapes *prompts*; Interview Me pauses an active agent to extract missing
intent or context; AI Repo Setup shapes *repo agent config*.

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
- On add/rename of a first-class prompt: add a row to **Tools** with literal `prompts/<slug>.md` (or
  `.system.md`). CI fails if a top-level prompt file is not indexed.
- README **More** sections only for chooser disambiguation or repo-specific notes—never duplicate
  the prompt body.

## Prompt Style Fit

`prompts/prompt-style-fit.md` normalizes a rough prompt file that already lives in this repo. It is
for repo fit, not for broad prompt redesign.

Use it after adding a raw file under `prompts/`:

```text
@prompts/<new-prompt>.md @prompts/prompt-style-fit.md
```

The workflow tells the agent to read the target file, this README's style guide, and a few nearby
prompts; keep the final prompt compact; update the Tools row; and run the focused Markdown and path
checks.

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

`prompts/interview-me.md` pauses an agent after a difficult task, confidence wobble, or circular
debugging session and makes it ask the user for missing intent or context that would change the
result.

**Use** when an agent says it is done but you suspect it misunderstood the goal, missed context,
made unverified assumptions, optimized for the wrong process or tradeoff, or needs user answers
before continuing. **Skip** when you want a separate transcript sanity check ([Verify](#tools)),
branch code review with adversarial defense ([Code Review](#tools)), or prompt rewriting
([Prompt Architect](#prompt-architect)).

Paste the file into the active agent session after your challenge, for example: "Are you really
confident? This took a long time. If you are missing context or have open questions, ask me now."
Answer the questions before asking the agent to continue.

## AI Repo Setup

`prompts/ai-repo-setup.md` runs inside a target repo: inspect tree and tooling, then add minimal
justified agent files (`AGENTS.md`, thin adapters). Task, constraints, and deliverables are in the
prompt—not for arbitrary prompt wording ([Prompt Architect](#prompt-architect)).

**Use** on brownfield code or greenfield repos that already have build, tests, formatter, CI, and
README. **Skip** for empty dirs or idea-only bootstrap—use `prompts/project-start.md` first.

Open the target repo, attach `prompts/ai-repo-setup.md` (e.g. `@prompts/ai-repo-setup.md`),
optionally ask for assessment before large edits. One session with full tree access; review diffs.
