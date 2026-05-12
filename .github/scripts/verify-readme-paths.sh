#!/usr/bin/env bash
# Fail if README.md references repo paths that are not files in the tree.
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$root"
mapfile -t paths < <(
  grep -oE 'prompts/[a-zA-Z0-9._-]+(\.md|\.prompt\.md)|\.cursor/rules/[a-zA-Z0-9._-]+\.mdc' README.md |
    sort -u
)
if ((${#paths[@]} == 0)); then
  echo "verify-readme-paths: no paths matched in README.md" >&2
  exit 1
fi
missing=0
for p in "${paths[@]}"; do
  if [[ ! -f "$p" ]]; then
    echo "verify-readme-paths: README.md references missing file: $p" >&2
    missing=1
  fi
done
if ((missing)); then
  exit 1
fi
echo "verify-readme-paths: OK (${#paths[@]} path(s) from README.md exist)"
