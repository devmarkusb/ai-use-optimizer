from pathlib import Path

from promptfill.workflow import fill_prompt, initial_values, schema_for


def test_fill_prompt_success(tmp_path: Path):
    path = tmp_path / "p.md"
    path.write_text("Hello <NAME>!\n", encoding="utf-8")
    values = initial_values(schema_for(path))
    values["NAME"] = "world"
    outcome = fill_prompt(path, values)
    assert outcome.ok
    assert outcome.rendered == "Hello world!\n"
    assert outcome.missing == ()


def test_fill_prompt_missing_required(tmp_path: Path):
    path = tmp_path / "p.md"
    path.write_text(
        """---
fields:
  NAME:
    required: true
---
Hello <NAME>!
""",
        encoding="utf-8",
    )
    outcome = fill_prompt(path, {"NAME": ""})
    assert not outcome.ok
    assert "NAME" in outcome.missing


def test_fill_prompt_allows_blank_optional_placeholder(tmp_path: Path):
    path = tmp_path / "p.md"
    path.write_text("Hello <NAME>!\n", encoding="utf-8")

    outcome = fill_prompt(path, {"NAME": ""})

    assert outcome.ok
    assert outcome.rendered == "Hello !\n"
    assert outcome.missing == ()
