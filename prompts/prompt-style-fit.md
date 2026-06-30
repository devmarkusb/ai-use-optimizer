---
title: Prompt Style Fit
type: task-prompt
purpose: >
  Bring one or more raw or newly added prompt files into this repo's style without bloating them
targets:
  - Codex
  - Claude Code
  - Cursor
  - Generic LLM coding agents
scope:
  - prompt maintenance
  - repo hygiene
recommended-stage: when adding rough prompts under prompts/
---

# Prompt Style Fit

## Context

You are working in this repository. One or more raw or newly added prompt files need to match the
local prompt style without turning small ideas into large frameworks.

## Inputs

- `PROMPT_FILES`: one or more paths to new or rough prompt files. Treat a single `PROMPT_FILE` as a
  one-file batch.
- Optional user intent notes, either global or per file.

## Task

Normalize each file in `PROMPT_FILES` for this repository. Preserve each original job, make every
prompt self-contained and pasteable, and keep each diff small.

## Required Workflow

1. Read all `PROMPT_FILES`, `README.md`'s prompt style guide, and 1-3 nearby prompts with similar
   scope. For batches, reuse nearby examples when they fit multiple files.
1. For each prompt file, state the original job in one sentence and use it as that file's scope
   guard.
1. Process files one at a time so each prompt stays internally coherent.
1. Add or repair only the style elements the file actually needs: front matter, H1, concise task
   wording, necessary rules, and an output contract if the prompt depends on one.
1. Preserve each original behavior unless it is unsafe, ambiguous, or conflicts with repo style.
1. Remove bloat: generic persona language, broad checklists, speculative capabilities, redundant
   sections, and constraints that do not reduce a real failure mode.
1. Add or update `README.md` Tools rows with literal `prompts/<file>.md` paths. Add README More
   sections only when chooser guidance is genuinely useful.
1. Run `uv run pre-commit run --files README.md PROMPT_FILES...` and
   `bash .github/scripts/verify-readme-paths.sh` when the tools are available.

## Rules

- Do not solve or redesign any prompt's underlying task.
- Do not expand a small raw prompt into a full operating manual.
- If a raw prompt is tiny, the final prompt should usually stay compact after front matter.
- Do not edit files unrelated to the target prompts and their required README rows.
- If preserving intent and matching style conflict, stop and ask for the user's preference.

## Output Format

Return a short summary with:

- files changed
- original intent preserved, grouped per prompt when multiple files were changed
- bloat removed or avoided
- checks run
