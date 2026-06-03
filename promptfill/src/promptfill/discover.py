"""Discover prompt files and repository prompts directory."""

from __future__ import annotations

import os
from pathlib import Path

from promptfill.parser import ParsedPrompt, parse_prompt_file, title_from_prompt


def find_prompts_dir(start: Path | None = None) -> Path | None:
    """Resolve prompts directory: env, then walk up from cwd."""
    env = os.environ.get("PROMPTFILL_PROMPTS_DIR")
    if env:
        path = Path(env).expanduser().resolve()
        if path.is_dir():
            return path
    base = (start or Path.cwd()).resolve()
    for candidate in [base, *base.parents]:
        prompts = candidate / "prompts"
        if prompts.is_dir() and any(prompts.glob("*.md")):
            return prompts
    return None


def list_prompt_files(prompts_dir: Path) -> list[Path]:
    files = sorted(prompts_dir.glob("*.md"), key=lambda p: p.name.lower())
    return [p for p in files if p.is_file()]


def load_prompt_catalog(prompts_dir: Path) -> list[tuple[Path, str]]:
    catalog: list[tuple[Path, str]] = []
    for path in list_prompt_files(prompts_dir):
        parsed = parse_prompt_file(path)
        catalog.append((path, title_from_prompt(parsed)))
    return catalog


def resolve_prompt_path(prompts_dir: Path, selector: str) -> Path | None:
    """Resolve filename, stem, or path."""
    direct = Path(selector).expanduser()
    if direct.is_file():
        return direct.resolve()

    for candidate in (
        prompts_dir / selector,
        prompts_dir / f"{selector}.md",
    ):
        if candidate.is_file():
            return candidate.resolve()

    stem = selector.removesuffix(".md")
    for path in list_prompt_files(prompts_dir):
        if path.stem == stem:
            return path
    return None
