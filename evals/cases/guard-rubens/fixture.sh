#!/usr/bin/env bash
# Scaffold (runs only with `claude plugin eval --scaffold`). Written by evals/fixtures/make_fixtures.py
# --emit-scaffold; synthetic images drawn in code, museum images fetched and hash-checked.
set -euo pipefail
mkdir -p evals/fixtures/out/renders
curl -fsSL -A 'artwright/0.3.0 (+https://github.com/m4bwav/artwright)' -o evals/fixtures/out/cma-2006.139.jpg https://openaccess-cdn.clevelandart.org/2006.139/2006.139_web.jpg
echo '54b03bc03c745fcc3edd523b315dd9fda942c30c633988170c1cbeb24b780c5c  evals/fixtures/out/cma-2006.139.jpg' | sha256sum -c --quiet
