"""Shared fill workflow for CLI and desktop GUI."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from promptfill.clipboard import copy_to_clipboard
from promptfill.discover import find_prompts_dir, load_prompt_catalog, resolve_prompt_path
from promptfill.form import collect_values_noninteractive
from promptfill.parser import parse_prompt_file
from promptfill.render import apply_values, missing_required_values, unresolved_required
from promptfill.schema import FieldSpec, infer_schema


@dataclass(frozen=True)
class FillOutcome:
    ok: bool
    rendered: str
    missing: tuple[str, ...]
    source: Path | None = None


def resolve_prompts_dir(prompts_dir: Path | None = None) -> Path:
    if prompts_dir is not None:
        resolved = prompts_dir.expanduser().resolve()
        if not resolved.is_dir():
            raise FileNotFoundError(f"Not a directory: {resolved}")
        return resolved
    found = find_prompts_dir()
    if found is None:
        raise FileNotFoundError(
            "Could not find prompts/ directory. "
            "Use --prompts-dir or set PROMPTFILL_PROMPTS_DIR."
        )
    return found


def catalog_for(prompts_dir: Path) -> list[tuple[Path, str]]:
    return load_prompt_catalog(prompts_dir)


def schema_for(path: Path) -> list[FieldSpec]:
    return infer_schema(parse_prompt_file(path))


def initial_values(schema: list[FieldSpec], preset: dict[str, str] | None = None) -> dict[str, str]:
    return collect_values_noninteractive(schema, preset or {})


def fill_prompt(path: Path, values: dict[str, str]) -> FillOutcome:
    parsed = parse_prompt_file(path)
    schema = infer_schema(parsed)
    rendered = apply_values(parsed, values) if schema else parsed.body
    required = {field.name for field in schema if field.required}
    missing = missing_required_values(required, values) or unresolved_required(rendered, required)
    return FillOutcome(
        ok=not missing,
        rendered=rendered,
        missing=tuple(missing),
        source=path,
    )


def copy_rendered(text: str) -> None:
    copy_to_clipboard(text)


def resolve_selector(prompts_dir: Path, selector: str) -> Path | None:
    return resolve_prompt_path(prompts_dir, selector)
