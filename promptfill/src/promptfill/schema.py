"""Infer fill schema from placeholders and optional front matter fields."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from promptfill.parser import ParsedPrompt, extract_placeholders


@dataclass(frozen=True)
class FieldSpec:
    name: str
    field_type: str = "string"
    multiline: bool = False
    required: bool = False
    default: str | None = None
    label: str | None = None

    @property
    def display_label(self) -> str:
        return self.label or self.name.replace("_", " ").title()


def _coerce_field_meta(name: str, meta: Any) -> FieldSpec:
    if meta is None:
        return FieldSpec(name=name)
    if isinstance(meta, str):
        return FieldSpec(name=name, default=meta)
    if not isinstance(meta, dict):
        return FieldSpec(name=name)
    field_type = str(meta.get("type", "string"))
    multiline = bool(meta.get("multiline", field_type in ("markdown", "text", "multiline")))
    required = bool(meta.get("required", False))
    default = meta.get("default")
    default_str = str(default) if default is not None else None
    label = meta.get("label")
    label_str = str(label) if label is not None else None
    return FieldSpec(
        name=name,
        field_type=field_type,
        multiline=multiline,
        required=required,
        default=default_str,
        label=label_str,
    )


def infer_schema(parsed: ParsedPrompt) -> list[FieldSpec]:
    """Build ordered field list from body placeholders plus front matter fields."""
    names = extract_placeholders(parsed.body)
    fm_fields = parsed.front_matter.get("fields")
    meta_by_name: dict[str, Any] = {}
    if isinstance(fm_fields, dict):
        meta_by_name = fm_fields

    # Preserve placeholder order; append front-matter-only fields not in body
    ordered: list[str] = list(names)
    for key in meta_by_name:
        if key not in ordered:
            ordered.append(str(key))

    return [_coerce_field_meta(n, meta_by_name.get(n)) for n in ordered]


def fields_with_defaults(schema: list[FieldSpec]) -> list[FieldSpec]:
    return [f for f in schema if f.default is not None]


def fields_to_prompt(schema: list[FieldSpec]) -> list[FieldSpec]:
    return [f for f in schema if f.default is None]
