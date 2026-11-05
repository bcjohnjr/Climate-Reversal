#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
test ! -e .git || { echo 'Already a git repository; refusing to overwrite history' >&2; exit 1; }
python3 scripts/fetch_pinned_sources.py
python3 scripts/verify_archive.py
git init -b main
git remote add origin https://github.com/bcjohnjr/Climate-Reversal.git
git add -A
git commit -m 'Archive pinned climate model code, original V67 results, figures and published supplementary tables'
git push -u origin main
printf '\nPublished to https://github.com/bcjohnjr/Climate-Reversal\n'
