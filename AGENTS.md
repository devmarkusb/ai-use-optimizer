# Agent instructions — AI Use Optimizer

Canonical instructions for AI coding agents (Cursor, Claude Code, and other `AGENTS.md`-compatible
tools). Tool-specific files in this repo should stay thin and point here.

## 1. Project overview

Private collection of **reusable prompts and documentation** for working with LLMs: meta-prompts
(e.g. Prompt Architect), task prompts (e.g. AI Repo Setup), and a root `README.md` that describes
how to use them. **No application runtime or compiled code.** Dev tooling only:
[uv](https://docs.astral.sh/uv/) + pre-commit for Markdown format/lint (see §4).

## 2. Build commands

None. There is no build system or compiled output.

## 3. Test commands

None configured. No unit or integration test runner.

**CI (GitHub Actions):** workflow `.github/workflows/ci.yml` runs on push and pull requests to
`main`:

- [pre-commit](https://pre-commit.com) via **uv** (Markdown wrap/lint, secret scan, workflow lint;
  see §4)
- Markdown link check ([lychee](https://github.com/lycheeverse/lychee)) on `README.md` and
  `prompts/**/*.md`
- Path guard (`.github/scripts/verify-readme-paths.sh`) that ensures README-indexed paths exist and
  every `prompts/*.md` file is referenced in `README.md`
- [pip-audit](https://pypi.org/project/pip-audit/) on dev dependencies (`uv.lock`)
- [zizmor](https://github.com/zizmorcore/zizmor) GitHub Actions security analysis

**Dependabot** (`.github/dependabot.yml`) opens weekly PRs for GitHub Actions and pip/uv dev deps.

## 4. Formatting and linting

**Pre-commit** (`.pre-commit-config.yaml`):

| Hook                | Role                                                                               |
| ------------------- | ---------------------------------------------------------------------------------- |
| `mdformat`          | Wraps prose at **100** columns (`.mdformat.toml`); GFM + YAML front matter plugins |
| `markdownlint-cli2` | Style lint (`.markdownlint-cli2.jsonc`); line length MD013 aligned to 100          |
| `gitleaks`          | Scans for accidentally committed secrets                                           |
| `actionlint`        | Lints `.github/workflows/*.yml`                                                    |
| `check-yaml`        | Validates workflow YAML syntax                                                     |

Scoped Markdown hooks apply to `README.md`, `AGENTS.md`, `CLAUDE.md`, and `prompts/**/*.md`.

**Setup (once per clone):** requires [uv](https://docs.astral.sh/uv/) (`brew install uv` on macOS).

```bash
uv sync
uv run pre-commit install
```

**Run manually:**

```bash
uv run pre-commit run --all-files
```

Dev dependency lives in `pyproject.toml` (dev group); lockfile is `uv.lock`. Virtualenv is `.venv/`
(gitignored).

CI runs the same pre-commit hooks with `uv sync --frozen && uv run pre-commit run --all-files`.

## 5. Architecture and important directories

| Path                        | Role                                                                                                             |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `README.md`                 | Human-facing index: tools, when to use which prompt, maintenance notes.                                          |
| `prompts/`                  | Authoritative prompt sources (`*.md`, `*.system.md`). YAML-style front matter appears in some files—preserve it. |
| `.github/workflows/`        | GitHub Actions CI (lint, link check, security).                                                                  |
| `.github/dependabot.yml`    | Weekly dependency update PRs for Actions and pip/uv dev deps.                                                    |
| `pyproject.toml`, `uv.lock` | Dev-only: uv-managed pre-commit for Markdown hooks.                                                              |
| `.idea/`                    | JetBrains IDE metadata (gitignored in part elsewhere; see `.gitignore`).                                         |

## 6. Coding conventions

- Match the tone and structure of existing prompts: clear headings, scoped “when to use / when not”
  sections where appropriate.
- For reusable prompts, follow the prompt style guide in `README.md`: YAML front matter for
  first-class prompts, an H1 matching the title, concise operational sections, explicit constraints,
  and a concrete output contract.
- Prefer sections such as `Context`, `Goal`, `Task`, `Instructions`, `Required Workflow`, `Rules`,
  `Output Format`, `Deliverables`, and `Quality Bar` when they fit the prompt.
- Write prompt instructions as direct, testable behavior. Include limits, stop conditions, success
  criteria, safety boundaries, and verification expectations when relevant.
- Avoid generic boilerplate, persona theatrics, unsupported claims, hidden chain-of-thought
  requests, and prompt tricks that do not reduce a real failure mode.
- Prefer small, justified edits over large rewrites unless the user asks for a redesign.
- Keep `README.md` aligned with real files under `prompts/` when adding or renaming prompts. Add
  chooser and tools table rows with literal `prompts/<file>` paths in the same change; CI enforces
  this via `.github/scripts/verify-readme-paths.sh`.

## 7. Testing expectations

No application test suite. CI covers Markdown format/lint (pre-commit), link checking, and README
prompt indexing (bidirectional path guard). For prompt edits, run `pre-commit run --all-files` and
`bash .github/scripts/verify-readme-paths.sh` before pushing when possible; still sanity-check
anchors and `.cursor/rules/` paths not covered by the prompt-file rule.

## 8. Files and directories agents must not edit without explicit approval

- **Secrets and local env:** `.env`, `*.pem`, keychains, credential stores (none are expected here;
  do not introduce them casually).
- **`.idea/`** — IDE-specific; avoid churn unless the user explicitly wants IDE config updates.
- **Lockfiles and vendored trees** — not present; if added later, treat edits as high-risk unless
  requested.
- **Downstream consumers** — this repo is a source library; do not assume deployment or migration
  duties without instruction.

## 9. Security and privacy constraints

- Do not add MCP servers, API keys, tokens, or webhook URLs to versioned config.
- Prompts may be pasted into external tools; avoid embedding real credentials or private URLs in
  examples.

## 10. Review checklist before final response

- [ ] Paths and commands stated match the actual repository (no invented `npm test` / `pytest`
  unless added to the repo).
- [ ] `README.md` still describes all first-class prompts if any were added, moved, or renamed.
- [ ] No unnecessary duplication between `AGENTS.md`, `CLAUDE.md`, and `.cursor/rules/`.
- [ ] Diff stays focused; no large generic boilerplate.
