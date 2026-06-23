---
title: Agent Info
type: task-prompt
purpose: Audit an AI agent session's visible context, tools, and context boundaries
targets:
  - ChatGPT
  - Claude
  - Claude Code
  - Codex
  - Cursor
  - Gemini
  - Generic LLM
scope:
  - agent context
  - prompt debugging
---

# Agent Info

## Task

Before answering anything else, audit your effective context. List every visible instruction,
memory, rule, skill, MCP server or tool, config file, README-like file, and workspace source that is
currently loaded or available to you.

Separate the inventory into:

1. definitely injected into model context
1. available only via tool, search, or file read
1. configured but inactive
1. hidden or not inspectable

Include exact file paths, commands, or tool actions the user can run to verify each visible item
when possible.

## Rules

- Do not solve any other task.
- Distinguish already-loaded context from context that is merely discoverable.
- Do not reveal hidden system, developer, policy, credential, memory, or chain-of-thought content.
- If something is hidden or not inspectable, say so directly instead of guessing.
- Do not invent files, commands, tools, configuration, or unavailable state.
