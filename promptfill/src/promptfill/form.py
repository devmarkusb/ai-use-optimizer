"""Interactive terminal form for placeholder values."""

from __future__ import annotations

import sys

from promptfill.schema import FieldSpec, fields_with_defaults, fields_to_prompt


def read_multiline(prompt_label: str) -> str:
    print(f"{prompt_label} (multiline; end with a single '.' on its own line):")
    lines: list[str] = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line == "." and lines:
            break
        if line == "." and not lines:
            return ""
        lines.append(line)
    return "\n".join(lines)


def read_single(prompt_label: str, required: bool) -> str:
    while True:
        try:
            value = input(f"{prompt_label}: ").strip()
        except EOFError:
            value = ""
        if value or not required:
            return value
        print("  (required — enter a value or Ctrl-C to cancel)")


def collect_values(schema: list[FieldSpec]) -> dict[str, str]:
    values: dict[str, str] = {}
    for field in fields_with_defaults(schema):
        values[field.name] = field.default or ""

    for field in fields_to_prompt(schema):
        label = field.display_label
        if field.required:
            label = f"{label} *"
        if field.multiline:
            value = read_multiline(label)
        else:
            value = read_single(label, field.required)
        values[field.name] = value
    return values


def collect_values_noninteractive(
    schema: list[FieldSpec],
    preset: dict[str, str],
) -> dict[str, str]:
    """Apply preset overrides; use defaults for the rest."""
    values: dict[str, str] = {}
    for field in schema:
        if field.name in preset:
            values[field.name] = preset[field.name]
        elif field.default is not None:
            values[field.name] = field.default
        else:
            values[field.name] = ""
    return values


def is_tty() -> bool:
    return sys.stdin.isatty() and sys.stdout.isatty()
