# Prompt Architect

`prompt-architect.system.md` is a reusable meta prompt for turning rough ideas into high-quality prompts for ChatGPT, Codex, Claude, Gemini, Cursor, and generic LLMs.

It is not meant to solve the original task directly. Its job is to produce a better prompt.

## Files

```text
prompts/
  prompt-architect.system.md
  README.md
```

For Cursor-specific use, you may also keep a copy at:

```text
.cursor/rules/prompt-architect.mdc
```

## How To Use

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

### Quick Start

1. Open ChatGPT, Claude, or another LLM.
2. Paste the contents of `prompt-architect.system.md`.
3. Then send your rough request.

## Recommended Request Format

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

## Modes

### BASIC

Use for quick improvements.

Best for:
- simple writing prompts
- small code prompts
- quick research prompts
- rewriting unclear requests

### DETAIL

Use when quality matters and the task is underspecified.

Best for:
- professional writing
- technical design
- analysis
- research
- prompts that need clarifying questions

### PRODUCTION

Use when the prompt will be reused.

Best for:
- Cursor rules
- Claude project instructions
- Custom GPT instructions
- agent prompts
- team prompt libraries
- automation workflows

## Maintenance Workflow

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
