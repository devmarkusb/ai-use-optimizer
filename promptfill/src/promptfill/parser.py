"""Parse Markdown prompt files: front matter, body, placeholders."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

# Conservative: uppercase identifiers only; optional backslash escape before <
PLACEHOLDER_RE = re.compile(r"\\?<([A-Z][A-Z0-9_]*)>")


@dataclass(frozen=True)
class ParsedPrompt:
    path: Path
    front_matter: dict[str, Any]
    body: str
    raw: str


def split_front_matter(text: str) -> tuple[dict[str, Any], str]:
    """Split YAML front matter from Markdown body."""
    if not text.startswith("---"):
        return {}, text
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return {}, text
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, text
    fm_text = "".join(lines[1:end])
    body = "".join(lines[end + 1 :])
    if not fm_text.strip():
        return {}, body
    data = yaml.safe_load(fm_text)
    if not isinstance(data, dict):
        return {}, body
    return data, body


def extract_placeholders(text: str) -> list[str]:
    """Return placeholder names in first-seen order (deduplicated)."""
    seen: set[str] = set()
    names: list[str] = []
    for match in PLACEHOLDER_RE.finditer(text):
        name = match.group(1)
        if name not in seen:
            seen.add(name)
            names.append(name)
    return names


def parse_prompt_file(path: Path) -> ParsedPrompt:
    raw = path.read_text(encoding="utf-8")
    front_matter, body = split_front_matter(raw)
    return ParsedPrompt(path=path, front_matter=front_matter, body=body, raw=raw)


def title_from_prompt(parsed: ParsedPrompt) -> str:
    title = parsed.front_matter.get("title")
    if isinstance(title, str) and title.strip():
        return title.strip()
    return parsed.path.stem.replace("-", " ").title()


def remaining_placeholders(text: str) -> list[str]:
    return extract_placeholders(text)
