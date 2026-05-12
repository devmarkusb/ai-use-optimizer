# Agent instructions — AI Use Optimizer

Canonical instructions for AI coding agents (Cursor, Claude Code, and other `AGENTS.md`-compatible tools). Tool-specific files in this repo should stay thin and point here.

## 1. Project overview

Private collection of **reusable prompts and documentation** for working with LLMs: meta-prompts (e.g. Prompt Architect), task prompts (e.g. AI Repo Setup), and a root `README.md` that describes how to use them. **No application runtime, package manager, or compiled code.** Not a monorepo.

## 2. Build commands

None. There is no build system or compiled output.

## 3. Test commands

None configured. No test runner or CI in this repository.

## 4. Formatting and linting

No repository-level formatter, linter, or pre-commit configuration. **Unverified:** if you add a stack later, document exact commands here after they exist in the repo.

## 5. Architecture and important directories

| Path | Role |
|------|------|
| `README.md` | Human-facing index: tools, when to use which prompt, maintenance notes. |
| `prompts/` | Authoritative prompt sources (`*.md`, `*.prompt.md`). YAML-style front matter appears in some files—preserve it. |
| `.idea/` | JetBrains IDE metadata (gitignored in part elsewhere; see `.gitignore`). |

## 6. Coding conventions

- Match the tone and structure of existing prompts: clear headings, scoped “when to use / when not” sections where appropriate.
- Prefer small, justified edits over large rewrites unless the user asks for a redesign.
- Keep `README.md` aligned with real files under `prompts/` when adding or renaming prompts.

## 7. Testing expectations

No automated tests. For prompt changes, sanity-check that `README.md` links and file paths still match the tree.

## 8. Files and directories agents must not edit without explicit approval

- **Secrets and local env:** `.env`, `*.pem`, keychains, credential stores (none are expected here; do not introduce them casually).
- **`.idea/`** — IDE-specific; avoid churn unless the user explicitly wants IDE config updates.
- **Lockfiles and vendored trees** — not present; if added later, treat edits as high-risk unless requested.
- **Downstream consumers** — this repo is a source library; do not assume deployment or migration duties without instruction.

## 9. Security and privacy constraints

- Do not add MCP servers, API keys, tokens, or webhook URLs to versioned config.
- Prompts may be pasted into external tools; avoid embedding real credentials or private URLs in examples.

## 10. Review checklist before final response

- [ ] Paths and commands stated match the actual repository (no invented `npm test` / `pytest` unless added to the repo).
- [ ] `README.md` still describes all first-class prompts if any were added, moved, or renamed.
- [ ] No unnecessary duplication between `AGENTS.md`, `CLAUDE.md`, and `.cursor/rules/`.
- [ ] Diff stays focused; no large generic boilerplate.
