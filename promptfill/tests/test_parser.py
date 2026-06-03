from pathlib import Path

from promptfill.parser import (
    extract_placeholders,
    parse_prompt_file,
    split_front_matter,
    title_from_prompt,
)


def test_split_front_matter():
    text = "---\ntitle: Example\n---\n\n# Body\n"
    fm, body = split_front_matter(text)
    assert fm["title"] == "Example"
    assert "# Body" in body


def test_extract_placeholders_dedup_and_order():
    text = "<A> then <B> and <A> again \\<C>"
    assert extract_placeholders(text) == ["A", "B", "C"]


def test_parse_real_prompt(tmp_path: Path):
    path = tmp_path / "sample.md"
    path.write_text(
        "---\ntitle: Sample\n---\n\n## Inputs\n\n\\<PROBLEM>\n",
        encoding="utf-8",
    )
    parsed = parse_prompt_file(path)
    assert title_from_prompt(parsed) == "Sample"
    assert extract_placeholders(parsed.body) == ["PROBLEM"]
