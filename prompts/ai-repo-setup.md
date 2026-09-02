---
title: AI Repo Setup
type: task-prompt
purpose: Repository AI-agent bootstrap and normalization
targets:
  - Codex
  - Claude Code
  - Cursor
  - Generic LLM coding agents
scope:
  - brownfield
  - post-bootstrap greenfield
recommended-stage: after initial repo scaffold exists
---

# AI Repo Setup

## Context

This prompt is intended for:

- existing repositories
- or freshly bootstrapped repositories that already contain an initial project structure and build
  system, tests, formatter, CI skeleton, and first README

It is not intended for completely empty directories.

## Goal

Bring this repository to a current, maintainable AI-agent setup. First inspect the repository, then
generate only the configuration that is justified by the actual project structure, tooling, language
stack, and risk profile.

## Instructions

Set up a minimal, high-signal agent configuration for Cursor, Claude Code, Codex, Gemini, and other
AGENTS.md-compatible tools.

Prefer one canonical source of truth. Use tool-specific files only as thin adapters.

**When re-running later:** If the tree or tooling changed a lot, re-inspect from scratch, update
`AGENTS.md` and adapters to match reality, merge with existing files, and preserve bespoke sections
unless they are clearly obsolete—do not replace wholesale without diffing against what was there.

### Inspect before editing

Before proposing or editing configuration, inspect the repository for:

- language stack and framework conventions
- build system and package manager
- test commands and existing CI
- formatter, linter, static analysis, and pre-commit hooks
- generated, vendored, third-party, migration, lock, and build-output paths
- monorepo boundaries and directory-specific conventions
- security-sensitive areas such as credentials, deployment, infrastructure, payments, auth, or data
  migrations
- existing AI config files such as `AGENTS.md`, `CLAUDE.md`, `.cursor/rules`, `.claude`,
  `.mcp.json`, `.github/copilot-instructions.md`, `GEMINI.md`, `.windsurfrules`,
  `.codex/config.toml`, `SKILL.md` or legacy `.cursorrules`

If the repository already has useful AI configuration, preserve it and reduce duplication instead of
replacing it blindly.

### Output files

Create or update only the files that are useful for this repository:

- `AGENTS.md` as the primary portable instruction file
- `CLAUDE.md` if Claude Code needs a dedicated entry point
- `.cursor/rules/*.mdc` only for Cursor-specific scoping or rule metadata
- `.claude/settings.json`, `.claude/agents`, `.claude/commands`, or `.claude/skills` only when there
  is a clear workflow that benefits from them
- `.mcp.json` only when MCP servers are actually needed and safe to configure

Do not add large generic templates. Do not add rules that merely restate obvious software
engineering principles.

### `AGENTS.md` content

Keep `AGENTS.md` concise and operational. Include only repository-specific instructions under these
headings where applicable:

1. Project overview
1. Build commands
1. Test commands
1. Formatting and linting
1. Architecture and important directories
1. Coding conventions
1. Testing expectations
1. Files and directories agents must not edit without explicit approval
1. Security and privacy constraints
1. Review checklist before final response

Use exact commands discovered from the repository. If a command cannot be verified, mark it as
unverified rather than inventing it.

Always include Git/remote workflow constraints in `AGENTS.md`:

- **Never push without approval:** do not run `git push`, force-push, or any equivalent flow (`gh`,
  IDE sync, etc.) that publishes local commits to a remote unless the user explicitly requests it.

### Layering and scoping

Use the following layering model:

- global user config: personal preferences and tool permissions only
- repository root config: shared project rules
- nested config: only for monorepo subtrees with genuinely different build/test/style rules
- session prompt: task-specific intent only

If this is a monorepo, prefer additional nested `AGENTS.md` files only when subdirectories have
materially different toolchains or rules.

### Cursor

If Cursor project rules are needed, create `.cursor/rules/*.mdc` as thin wrappers around the
canonical repo instructions.

Do not duplicate the whole `AGENTS.md` into Cursor rules. Use Cursor rules for:

- path-scoped behavior via globs
- always-apply project constraints
- Cursor-specific interaction preferences

### Claude Code

If Claude Code is used, make `CLAUDE.md` refer to `AGENTS.md` and include only Claude-specific
additions.

Use `.claude/settings.json` only for permissions, hooks, environment, or MCP configuration that
should be versioned for this repository. Do not store secrets.

Use `.claude/agents`, `.claude/commands`, or `.claude/skills` only for repeatable workflows that are
specific enough to be worth maintaining.

### MCP

Configure MCP only when it provides concrete value. Prefer a small allowlisted set of servers.

Before adding an MCP server, explain:

- what capability it adds
- whether it needs network, filesystem, browser, database, or credential access
- what permissions it requires
- why it belongs in repo config instead of user config

Do not add broad filesystem, browser, GitHub, database, or shell access by default.

### Safety constraints

Do not push to any remote without explicit user approval. Local git work (status, diff, commit when
requested) is fine; publishing commits always requires the user to ask.

Do not edit:

- secrets or local environment files
- production deployment config
- database migrations
- generated code
- vendored dependencies
- lockfiles
- CI release workflows

unless explicitly requested or clearly necessary. If such a change is necessary, explain the risk
before editing.

## Deliverables

Return:

1. A short assessment of the current repository state
1. The files created or changed
1. The rationale for each file
1. Any commands discovered for build/test/lint
1. Any remaining unknowns or assumptions
1. A short maintenance policy explaining what should stay global, repo-local, nested, or
   task-specific

## Quality bar

The final setup should be small, current, and easy to maintain. Prefer 200 lines of precise
repo-specific configuration over 2,000 lines of generic boilerplate.
