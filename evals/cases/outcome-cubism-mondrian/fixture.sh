#!/usr/bin/env bash
# Scaffold (runs only with `claude plugin eval --scaffold`). Written by evals/fixtures/make_fixtures.py
# --emit-scaffold; synthetic images drawn in code, museum images fetched and hash-checked.
set -euo pipefail
mkdir -p evals/fixtures/out/renders
curl -fsSL -A 'artwright/0.1.0 (+https://github.com/m4bwav/artwright)' -o evals/fixtures/out/cma-1967.215.jpg https://openaccess-cdn.clevelandart.org/1967.215/1967.215_web.jpg
echo '79f82c7e28afc064bd19199dd6883d90d3bb42af26cd61517b6cd28e27dbe58e  evals/fixtures/out/cma-1967.215.jpg' | sha256sum -c --quiet
