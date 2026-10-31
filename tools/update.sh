#!/bin/sh
# Full refresh of ScannersDB: download the upstream lists, add new networks, rebuild the lists and README tables,
# check everything. Nothing is committed; read the import report and `git diff --stat` before committing.
set -eu
cd "$(dirname "$0")/.."
python3 tools/import_sources.py --apply
python3 tools/export.py
python3 tools/readme_table.py
python3 tools/test_data.py
echo
echo "Import report: ${SCDB_CACHE:-$HOME/.cache/scannersdb}/review.md"
git status --short -- data README.md 2>/dev/null | head -20 || true
