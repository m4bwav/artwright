#!/usr/bin/env bash
# Scaffold (runs only with `claude plugin eval --scaffold`). Written by evals/fixtures/make_fixtures.py
# --emit-scaffold; synthetic images drawn in code, museum images fetched and hash-checked.
set -euo pipefail
mkdir -p evals/fixtures/out/renders
curl -fsSL -A 'artwright/0.1.0 (+https://github.com/m4bwav/artwright)' -o evals/fixtures/out/cma-1958.21.jpg https://openaccess-cdn.clevelandart.org/1958.21/1958.21_web.jpg
echo 'b8508d3dafd5c7e5abbf7acd8223654326918d5b6941f560d575d9c762d0fda0  evals/fixtures/out/cma-1958.21.jpg' | sha256sum -c --quiet
