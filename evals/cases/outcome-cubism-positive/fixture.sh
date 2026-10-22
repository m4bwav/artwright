#!/usr/bin/env bash
# Scaffold (runs only with `claude plugin eval --scaffold`). Written by evals/fixtures/make_fixtures.py
# --emit-scaffold; synthetic images drawn in code, museum images fetched and hash-checked.
set -euo pipefail
mkdir -p evals/fixtures/out/renders
curl -fsSL -A 'artwright/0.1.0 (+https://github.com/m4bwav/artwright)' -o evals/fixtures/out/cma-2026.37.jpg https://openaccess-cdn.clevelandart.org/2026.37/2026.37_web.jpg
echo '6068ee295ad619357929200f1a586a45089d1f3c2097d190d09222fb08ebaa01  evals/fixtures/out/cma-2026.37.jpg' | sha256sum -c --quiet
