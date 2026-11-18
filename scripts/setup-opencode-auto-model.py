#!/usr/bin/env python3
"""Configure opencode-auto-model without third-party Python dependencies.

Unrelated settings and plugin entries are preserved. JSONC comments and formatting are normalized;
a timestamped backup is created before an existing config is changed.
"""

from __future__ import annotations

import argparse
import difflib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from typing import Any, Optional

MINIMUM_VERSION = (2, 0, 31)
SCHEMA = "https://opencode.ai/config.json"
DEFAULT_LIGHT = "opencode-go/gpt-6-luna#low"
DEFAULT_STANDARD = "opencode-go/kimi-k3.1-pro#high"
DEFAULT_DEEP = "opencode-go/kimi-k3.1-pro#max"
DEFAULT_DECIDER = "opencode-go/gpt-6-luna#low"


class SetupError(Exception):
    """A safe, user-actionable setup error."""


def strip_jsonc(text: str) -> str:
    """Remove JSONC comments and trailing commas without touching string contents."""
    without_comments: list[str] = []
    in_string = False
    escaped = False
    in_line_comment = False
    in_block_comment = False
    index = 0

    while index < len(text):
        char = text[index]
        following = text[index + 1] if index + 1 < len(text) else ""

        if in_line_comment:
            if char in "\r\n":
                in_line_comment = False
                without_comments.append(char)
            else:
                without_comments.append(" ")
            index += 1
            continue

        if in_block_comment:
            if char == "*" and following == "/":
                without_comments.extend("  ")
                in_block_comment = False
                index += 2
            else:
                without_comments.append(char if char in "\r\n" else " ")
                index += 1
            continue

        if in_string:
            without_comments.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            index += 1
            continue

        if char == '"':
            in_string = True
            without_comments.append(char)
            index += 1
        elif char == "/" and following == "/":
            without_comments.extend("  ")
            in_line_comment = True
            index += 2
        elif char == "/" and following == "*":
            without_comments.extend("  ")
            in_block_comment = True
            index += 2
        else:
            without_comments.append(char)
            index += 1

    if in_string or in_block_comment:
        raise SetupError("The config contains an unterminated string or block comment.")

    source = "".join(without_comments)
    result: list[str] = []
    in_string = False
    escaped = False
    for index, char in enumerate(source):
        if in_string:
            result.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue

        if char == '"':
            in_string = True
            result.append(char)
        elif char == ",":
            lookahead = index + 1
            while lookahead < len(source) and source[lookahead].isspace():
                lookahead += 1
            if lookahead < len(source) and source[lookahead] in "}]":
                continue
            result.append(char)
        else:
            result.append(char)

    return "".join(result)


def load_config(path: Path) -> tuple[dict[str, Any], str]:
    if not path.exists():
        return {}, ""
    original = path.read_text(encoding="utf-8-sig")
    if not original.strip():
        return {}, original
    try:
        config = json.loads(strip_jsonc(original))
    except (json.JSONDecodeError, SetupError) as error:
        raise SetupError(f"Cannot parse {path}: {error}") from error
    if not isinstance(config, dict):
        raise SetupError(f"The top-level value in {path} must be an object.")
    return config, original


def is_auto_model_entry(entry: Any) -> bool:
    if isinstance(entry, str):
        return entry == "opencode-auto-model" or entry.startswith("opencode-auto-model@")
    if isinstance(entry, dict):
        package = entry.get("package")
        return isinstance(package, str) and (
            package == "opencode-auto-model" or package.startswith("opencode-auto-model@")
        )
    return False


def managed_plugin(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "package": "opencode-auto-model",
        "options": {
            "models": {
                args.light: (
                    "Quick questions, code search, explanations, formatting, renames, and small "
                    "well-defined edits"
                ),
                args.standard: "Routine features, tests, focused refactors, and debugging with clear scope",
                args.deep: (
                    "Architecture, subtle or repeated debugging, security-sensitive changes, and "
                    "ambiguous multi-file work"
                ),
            },
            "fallback": args.fallback,
            "decider": args.decider,
        },
    }


def updated_config(config: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    updated = dict(config)
    updated["$schema"] = SCHEMA
    updated["model"] = "router/auto"

    plugins = updated.get("plugins", [])
    if not isinstance(plugins, list):
        raise SetupError("The existing 'plugins' setting must be an array; refusing to replace it.")

    managed = managed_plugin(args)
    merged_plugins: list[Any] = []
    inserted = False
    for entry in plugins:
        if is_auto_model_entry(entry):
            if not inserted:
                merged_plugins.append(managed)
                inserted = True
        else:
            merged_plugins.append(entry)
    if not inserted:
        merged_plugins.append(managed)

    updated["plugins"] = merged_plugins
    return updated


def default_config_path() -> Path:
    config_home = Path(os.environ.get("XDG_CONFIG_HOME", "~/.config")).expanduser()
    config_dir = config_home / "opencode"
    jsonc_path = config_dir / "opencode.jsonc"
    json_path = config_dir / "opencode.json"
    if jsonc_path.exists() or not json_path.exists():
        return jsonc_path
    return json_path


def check_opencode_version() -> None:
    executables = [
        found
        for name in ("opencode", "opencode2", "opencode-v2", "opencode-beta")
        if (found := shutil.which(name)) is not None
    ]
    if not executables:
        print(
            "warning: no OpenCode CLI found on PATH; the plugin requires OpenCode V2 2.0.31 or later",
            file=sys.stderr,
        )
        return

    versions: list[tuple[int, int, int]] = []
    errors: list[str] = []
    for executable in dict.fromkeys(executables):
        try:
            result = subprocess.run(
                [executable, "--version"],
                check=True,
                capture_output=True,
                text=True,
                timeout=15,
            )
        except (OSError, subprocess.SubprocessError) as error:
            errors.append(f"Could not run {executable} --version: {error}")
            continue

        output = f"{result.stdout}\n{result.stderr}"
        match = re.search(r"(?<!\d)(\d+)\.(\d+)\.(\d+)(?!\d)", output)
        if match is None:
            errors.append(f"Could not parse the OpenCode version from: {output.strip()}")
            continue
        versions.append(tuple(int(part) for part in match.groups()))

    if not versions:
        raise SetupError("; ".join(errors))
    if max(versions) < MINIMUM_VERSION:
        required = ".".join(str(part) for part in MINIMUM_VERSION)
        found = ".".join(str(part) for part in max(versions))
        raise SetupError(f"OpenCode {found} is too old; opencode-auto-model requires {required} or later.")


def write_config(path: Path, content: str, existed: bool) -> Optional[Path]:
    path.parent.mkdir(parents=True, exist_ok=True)
    backup: Optional[Path] = None
    mode = 0o600
    if existed:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = path.with_name(f"{path.name}.before-auto-model-{timestamp}-{os.getpid()}.bak")
        shutil.copy2(path, backup)
        mode = path.stat().st_mode & 0o777

    temporary_name: Optional[str] = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False
        ) as temporary:
            temporary_name = temporary.name
            temporary.write(content)
        os.chmod(temporary_name, mode)
        os.replace(temporary_name, path)
    finally:
        if temporary_name is not None and os.path.exists(temporary_name):
            os.unlink(temporary_name)
    return backup


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=None, help="config file to update")
    parser.add_argument("--dry-run", action="store_true", help="print the diff without changing files")
    parser.add_argument("--light", default=DEFAULT_LIGHT, help="light model reference, including optional variant")
    parser.add_argument(
        "--standard", default=DEFAULT_STANDARD, help="standard model reference, including optional variant"
    )
    parser.add_argument("--deep", default=DEFAULT_DEEP, help="deep model reference, including optional variant")
    parser.add_argument("--fallback", default=None, help="fallback model reference (default: --standard)")
    parser.add_argument("--decider", default=DEFAULT_DECIDER, help="model used to classify the first prompt")
    args = parser.parse_args()
    if args.fallback is None:
        args.fallback = args.standard
    return args


def main() -> int:
    args = parse_args()
    try:
        check_opencode_version()
        path = args.config.expanduser() if args.config is not None else default_config_path()
        config, original = load_config(path)
        rendered = json.dumps(updated_config(config, args), indent=2, ensure_ascii=False) + "\n"
        if original == rendered:
            print(f"opencode-auto-model is already configured in {path}")
            return 0

        original_for_diff = original if not original or original.endswith("\n") else original + "\n"
        diff = "".join(
            difflib.unified_diff(
                original_for_diff.splitlines(keepends=True),
                rendered.splitlines(keepends=True),
                fromfile=str(path),
                tofile=f"{path} (configured)",
            )
        )
        if args.dry_run:
            print(diff, end="")
            return 0

        backup = write_config(path, rendered, path.exists())
        print(diff, end="")
        if backup is not None:
            print(f"Backup: {backup}")
        print(f"Configured opencode-auto-model in {path}")
        print("New sessions will default to Auto. In an existing session, run /models and select Auto.")
        print("Ensure the configured provider is connected and every referenced model and variant is available.")
        return 0
    except (OSError, SetupError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
