# promptfill

Local CLI and desktop app that turns Markdown prompts with `<PLACEHOLDER>` fields into a filled
prompt on your clipboard. Prompt files stay in the parent repo’s `prompts/` directory;
[Espanso](https://espanso.org/) (or any launcher) can open the GUI with `;p`.

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
Fields are optional by default; add `required: true` when a field must be filled before output.

## Install

From the repository root (requires [uv](https://docs.astral.sh/uv/)):

```bash
cd promptfill
uv sync
uv run promptfill list
```

**Desktop GUI:** requires Python with tkinter (included with python.org installers on Windows; macOS
system Python; on Debian/Ubuntu install `python3-tk`). The window uses a bundled app icon
(`src/promptfill/assets/icon.png`). **Enter** copies, closes the window, and pastes back into the
app that was focused when launched (macOS/Linux X11/Windows; needs Automation/Accessibility
permission on macOS). **Shift+Enter** inserts a newline in a field. **Tab** and **Shift+Tab** move
through placeholder fields.

## Usage

| Command                                              | Action                               |
| ---------------------------------------------------- | ------------------------------------ |
| `promptfill gui`                                     | Desktop app: pick prompt, fill, copy |
| `promptfill`                                         | Terminal picker → fill → clipboard   |
| `promptfill list`                                    | Titles and filenames                 |
| `promptfill project-start`                           | Fill by stem (no picker)             |
| `promptfill fill project-start`                      | Same, explicit subcommand            |
| `promptfill --dry-run find-the-right-representation` | Print result, no clipboard           |
| `promptfill --set PROBLEM='fix bug' project-start`   | Preset fields (non-interactive)      |

Environment:

- `PROMPTFILL_PROMPTS_DIR` — override auto-detected `prompts/` directory

## Espanso

Use Espanso with the `;p` shortcut, or copy `examples/espanso-promptfill.yml` into your Espanso
match folder. Set **absolute path to this repo’s root** (the directory that contains `prompts/` and
`promptfill/`).

Typical flow:

1. `;p` opens the promptfill desktop window (no terminal)
1. Pick a prompt, fill fields, **Copy to clipboard**

## Tests

```bash
cd promptfill
uv sync
uv run pytest
```

CI runs the same (`uv sync --frozen && uv run pytest` in `.github/workflows/ci.yml`).

## Roadmap

- Editor or browser context injection
- Conditional sections and team sync
- Optional native shell (Tauri) if tkinter is not enough

The MVP validates: placeholder-first prompts, fast fill, safe output for required `<TOKENS>`,
desktop GUI on macOS/Linux/Windows, and Espanso as a thin launcher.
