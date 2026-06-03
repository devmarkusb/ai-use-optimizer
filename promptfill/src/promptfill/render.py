"""Replace placeholders and validate output."""

from __future__ import annotations

import re

from promptfill.parser import PLACEHOLDER_RE, ParsedPrompt, remaining_placeholders

# Match literal <NAME> or escaped \<NAME>
def _replacement_pattern(name: str) -> re.Pattern[str]:
    return re.compile(rf"\\?<({re.escape(name)})>")


def apply_values(parsed: ParsedPrompt, values: dict[str, str]) -> str:
    """Return body with all known placeholders substituted."""
    result = parsed.body
    for name, value in values.items():
        result = _replacement_pattern(name).sub(value, result)
    return result


def missing_required_values(
    schema_names_required: set[str],
    values: dict[str, str],
) -> list[str]:
    """Required fields with no non-empty value."""
    return sorted(
        n for n in schema_names_required if not str(values.get(n, "")).strip()
    )


def unresolved_required(rendered: str, required_names: set[str]) -> list[str]:
    """Required placeholder names still present in rendered text."""
    still = set(remaining_placeholders(rendered))
    return sorted(still & required_names)
