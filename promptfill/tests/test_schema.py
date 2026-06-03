from pathlib import Path

from promptfill.parser import parse_prompt_file
from promptfill.schema import infer_schema


def test_infer_schema_from_front_matter(tmp_path: Path):
    path = tmp_path / "p.md"
    path.write_text(
        """---
title: T
fields:
  PROBLEM:
    type: markdown
    multiline: true
    required: true
  AUDIENCE:
    type: string
    default: Generic LLM
---
\\<PROBLEM>
<AUDIENCE>
""",
        encoding="utf-8",
    )
    parsed = parse_prompt_file(path)
    schema = infer_schema(parsed)
    names = [f.name for f in schema]
    assert names == ["PROBLEM", "AUDIENCE"]
    assert schema[0].multiline is True
    assert schema[0].required is True
    assert schema[1].default == "Generic LLM"
