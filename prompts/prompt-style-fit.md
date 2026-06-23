---
title: Prompt Style Fit
type: task-prompt
purpose: Bring a raw or newly added prompt file into this repo's style without bloating it
targets:
  - Codex
  - Claude Code
  - Cursor
  - Generic LLM coding agents
scope:
  - prompt maintenance
  - repo hygiene
recommended-stage: when adding a rough prompt under prompts/
---

# Prompt Style Fit

## Context

You are working in this repository. A raw or newly added prompt file needs to match the local prompt
style without turning a small idea into a large framework.

## Inputs

- `PROMPT_FILE`: path to the new or rough prompt file.
- Optional user intent notes.

## Task

Normalize `PROMPT_FILE` for this repository. Preserve the original job, make it self-contained and
pasteable, and keep the diff small.

## Required Workflow

1. Read `PROMPT_FILE`, `README.md`'s prompt style guide, and 1-3 nearby prompts with similar scope.
1. State the prompt's original job in one sentence and use it as the scope guard.
1. Add or repair only the style elements the file actually needs: front matter, H1, concise task
   wording, necessary rules, and an output contract if the prompt depends on one.
1. Preserve the original behavior unless it is unsafe, ambiguous, or conflicts with repo style.
1. Remove bloat: generic persona language, broad checklists, speculative capabilities, redundant
   sections, and constraints that do not reduce a real failure mode.
1. Add or update the `README.md` Tools row with the literal `prompts/<file>.md` path. Add a README
   More section only when chooser guidance is genuinely useful.
1. Run `uv run pre-commit run --files README.md PROMPT_FILE` and
   `bash .github/scripts/verify-readme-paths.sh` when the tools are available.

## Rules

- Do not solve or redesign the prompt's underlying task.
- Do not expand a small raw prompt into a full operating manual.
- If the raw prompt is tiny, the final prompt should usually stay compact after front matter.
- Do not edit unrelated files.
- If preserving intent and matching style conflict, stop and ask for the user's preference.

## Output Format

Return a short summary with:

- files changed
- original intent preserved
- bloat removed or avoided
- checks run
