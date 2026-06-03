# promptfill

Local CLI that turns Markdown prompts with `<PLACEHOLDER>` fields into a filled prompt on your
clipboard. Prompt files stay in the parent repo’s `prompts/` directory;
[Espanso](https://espanso.org/) (or any launcher) only starts the tool.

## Placeholder convention

Use uppercase angle-bracket tokens in the prompt body:

```markdown
<PROBLEM>
<CONTEXT>
<AUDIENCE>
```

Existing files may escape `<` for Markdown formatters (`\<PROBLEM>`); promptfill treats both forms
the same.

Optional YAML front matter adds field metadata when inference is not enough:

```yaml
---
title: Find the Right Representation
fields:
  PROBLEM:
    type: markdown
    multiline: true
    required: true
  AUDIENCE:
    type: string
    default: Generic LLM
---
```

If a name appears in the body, it becomes a field automatically. Repeated tokens share one value.

## Install

From the repository root (requires [uv](https://docs.astral.sh/uv/)):

```bash
cd promptfill
uv sync
uv run promptfill list
```

## Usage

| Command                                              | Action                                |
| ---------------------------------------------------- | ------------------------------------- |
| `promptfill`                                         | Picker → interactive fill → clipboard |
| `promptfill list`                                    | Titles and filenames                  |
| `promptfill project-start`                           | Fill by stem (no picker)              |
| `promptfill fill project-start`                      | Same, explicit subcommand             |
| `promptfill --dry-run find-the-right-representation` | Print result, no clipboard            |
| `promptfill --set PROBLEM='fix bug' project-start`   | Preset fields (non-interactive)       |

Environment:

- `PROMPTFILL_PROMPTS_DIR` — override auto-detected `prompts/` directory

## Espanso

Copy `examples/espanso-promptfill.yml` into your Espanso match folder (wherever that lives). Set an
**absolute path to this repo’s root** (the directory that contains `prompts/` and `promptfill/`),
not only `promptfill/`. Example:

```text
/Users/user/dev/ai-use-optimizer
```

Typical flow:

1. `;pf` opens Terminal: `cd <repo_root> && uv run --directory promptfill promptfill`
1. Pick a prompt, answer prompts, result on clipboard

Keep Espanso as a thin launcher; all parsing and forms live in promptfill.

## Tests

```bash
cd promptfill
uv sync
uv run pytest
```

CI runs the same (`uv sync --frozen && uv run pytest` in `.github/workflows/ci.yml`).

## Roadmap (not in MVP)

- Desktop UI (Tauri/React) and Android
- Editor or browser context injection
- Conditional sections and team sync

The MVP validates: placeholder-first prompts, fast fill, safe output (no leftover required
`<TOKENS>`), and Espanso as entry point only.
