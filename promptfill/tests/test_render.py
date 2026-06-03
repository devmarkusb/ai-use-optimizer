from pathlib import Path

from promptfill.parser import parse_prompt_file, remaining_placeholders
from promptfill.render import apply_values


def test_apply_values_replaces_escaped_and_plain(tmp_path: Path):
    path = tmp_path / "p.md"
    path.write_text("Line \\<A> and <B> end\n", encoding="utf-8")
    parsed = parse_prompt_file(path)
    out = apply_values(parsed, {"A": "one", "B": "two"})
    assert out == "Line one and two end\n"
    assert remaining_placeholders(out) == []


def test_missing_required_values():
    from promptfill.render import missing_required_values

    assert missing_required_values({"NEED"}, {"NEED": ""}) == ["NEED"]
    assert missing_required_values({"NEED"}, {"NEED": "ok"}) == []
