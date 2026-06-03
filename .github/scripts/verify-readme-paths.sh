#!/usr/bin/env bash
# README ↔ prompts/ consistency:
# - Every path like prompts/*.md or .cursor/rules/*.mdc in README.md must exist.
# - Every prompts/*.md file must appear in README.md (chooser and/or tools tables).
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$root"

mapfile -t readme_paths < <(
  grep -oE 'prompts/[a-zA-Z0-9._-]+(\.md|\.prompt\.md)|\.cursor/rules/[a-zA-Z0-9._-]+\.mdc' README.md |
    sort -u
)
if ((${#readme_paths[@]} == 0)); then
  echo "verify-readme-paths: no paths matched in README.md" >&2
  exit 1
fi

missing_files=0
for p in "${readme_paths[@]}"; do
  if [[ ! -f "$p" ]]; then
    echo "verify-readme-paths: README.md references missing file: $p" >&2
    missing_files=1
  fi
done
if ((missing_files)); then
  exit 1
fi

mapfile -t prompt_files < <(find prompts -maxdepth 1 -type f -name '*.md' | sort)
if ((${#prompt_files[@]} == 0)); then
  echo "verify-readme-paths: no prompt files under prompts/" >&2
  exit 1
fi

unindexed=0
for p in "${prompt_files[@]}"; do
  if ! grep -Fq "$p" README.md; then
    echo "verify-readme-paths: README.md does not index prompt file: $p" >&2
    echo "  Add a row to Choosing a prompt and Tools in this repository with the path prompts/$(basename "$p")." >&2
    unindexed=1
  fi
done
if ((unindexed)); then
  exit 1
fi

echo "verify-readme-paths: OK (${#readme_paths[@]} README path(s), ${#prompt_files[@]} prompt(s) indexed)"
