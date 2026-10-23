#!/usr/bin/env bash
# Scaffold (runs only with `claude plugin eval --scaffold`). Written by evals/fixtures/make_fixtures.py
# --emit-scaffold; synthetic images drawn in code, museum images fetched and hash-checked.
set -euo pipefail
mkdir -p evals/fixtures/out/renders
curl -fsSL -A 'artwright/0.3.0 (+https://github.com/m4bwav/artwright)' -o evals/fixtures/out/cma-1971.38.jpg https://openaccess-cdn.clevelandart.org/1971.38/1971.38_web.jpg
echo 'af8d1984c6c5526f12d055f58abb3754b6a445886d47e2e6da45008a5122270b  evals/fixtures/out/cma-1971.38.jpg' | sha256sum -c --quiet
