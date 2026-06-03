"""Command-line interface for promptfill."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from promptfill import __version__
from promptfill.clipboard import ClipboardError, copy_to_clipboard
from promptfill.discover import (
    find_prompts_dir,
    load_prompt_catalog,
    resolve_prompt_path,
)
from promptfill.form import collect_values, collect_values_noninteractive, is_tty
from promptfill.parser import parse_prompt_file
from promptfill.render import (
    apply_values,
    missing_required_values,
    unresolved_required,
)
from promptfill.schema import infer_schema


def _pick_prompt(catalog: list[tuple[Path, str]]) -> Path | None:
    if not catalog:
        print("No prompt files found.", file=sys.stderr)
        return None
    print("Select a prompt:\n")
    for i, (_, title) in enumerate(catalog, start=1):
        print(f"  {i:2}. {title}")
    print()
    while True:
        try:
            choice = input("Number (or q): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return None
        if choice in ("q", "quit", ""):
            return None
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(catalog):
                return catalog[idx - 1][0]
        print("  Invalid selection — try again.")


def _cmd_list(prompts_dir: Path) -> int:
    catalog = load_prompt_catalog(prompts_dir)
    if not catalog:
        print(f"No .md files in {prompts_dir}")
        return 1
    for path, title in catalog:
        print(f"{title}\t{path.name}")
    return 0


def _cmd_fill(
    prompts_dir: Path,
    selector: str | None,
    *,
    no_clipboard: bool,
    dry_run: bool,
    preset: dict[str, str],
) -> int:
    catalog = load_prompt_catalog(prompts_dir)
    path: Path | None
    if selector:
        path = resolve_prompt_path(prompts_dir, selector)
        if path is None:
            print(f"Prompt not found: {selector}", file=sys.stderr)
            return 1
    else:
        if not is_tty():
            print("No prompt specified and stdin is not a TTY.", file=sys.stderr)
            return 1
        path = _pick_prompt(catalog)
        if path is None:
            return 0

    parsed = parse_prompt_file(path)
    schema = infer_schema(parsed)

    if not schema:
        rendered = parsed.body
        values = {}
    elif preset or not is_tty():
        values = collect_values_noninteractive(schema, preset)
        rendered = apply_values(parsed, values)
    else:
        print(f"\nFilling: {path.name}\n")
        values = collect_values(schema)
        rendered = apply_values(parsed, values)

    required = {f.name for f in schema if f.required}
    empty_required = missing_required_values(required, values)
    unresolved = unresolved_required(rendered, required)

    if empty_required or unresolved:
        problems = empty_required or unresolved
        print(
            "Refusing output — unresolved required placeholders: "
            + ", ".join(f"<{n}>" for n in problems),
            file=sys.stderr,
        )
        return 2

    if dry_run:
        print(rendered, end="" if rendered.endswith("\n") else "\n")
        return 0

    if not no_clipboard:
        try:
            copy_to_clipboard(rendered)
            print(f"Copied to clipboard ({len(rendered)} chars) from {path.name}")
        except ClipboardError as exc:
            print(str(exc), file=sys.stderr)
            return 3

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="promptfill",
        description="Fill <PLACEHOLDER> values in Markdown prompts and copy to clipboard.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument(
        "--prompts-dir",
        type=Path,
        help="Directory of prompt .md files (default: auto-detect ./prompts)",
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="fill",
        help="list | fill | <stem> (shorthand for fill)",
    )
    parser.add_argument(
        "selector",
        nargs="?",
        help="Prompt filename, stem, or path (fill only)",
    )
    parser.add_argument(
        "--no-clipboard",
        action="store_true",
        help="Do not copy result to clipboard",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print rendered prompt to stdout instead of clipboard",
    )
    parser.add_argument(
        "--set",
        action="append",
        metavar="NAME=VALUE",
        default=[],
        help="Preset field value (repeatable)",
    )
    return parser


def _parse_preset(pairs: list[str]) -> dict[str, str]:
    preset: dict[str, str] = {}
    for item in pairs:
        if "=" not in item:
            raise ValueError(f"Invalid --set value (expected NAME=VALUE): {item}")
        name, _, value = item.partition("=")
        name = name.strip()
        if not name:
            raise ValueError(f"Invalid --set value: {item}")
        preset[name] = value
    return preset


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    prompts_dir = args.prompts_dir
    if prompts_dir is None:
        found = find_prompts_dir()
        if found is None:
            print(
                "Could not find prompts/ directory. "
                "Use --prompts-dir or set PROMPTFILL_PROMPTS_DIR.",
                file=sys.stderr,
            )
            return 1
        prompts_dir = found
    else:
        prompts_dir = prompts_dir.expanduser().resolve()
        if not prompts_dir.is_dir():
            print(f"Not a directory: {prompts_dir}", file=sys.stderr)
            return 1

    command = args.command or "fill"
    selector = args.selector

    if command == "list":
        return _cmd_list(prompts_dir)

    if command == "fill":
        try:
            preset = _parse_preset(args.set or [])
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 1
        return _cmd_fill(
            prompts_dir,
            selector,
            no_clipboard=args.no_clipboard,
            dry_run=args.dry_run,
            preset=preset,
        )

    # Shorthand: `promptfill project-start` → fill by stem
    try:
        preset = _parse_preset(args.set or [])
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return _cmd_fill(
        prompts_dir,
        command,
        no_clipboard=args.no_clipboard,
        dry_run=args.dry_run,
        preset=preset,
    )


if __name__ == "__main__":
    raise SystemExit(main())
