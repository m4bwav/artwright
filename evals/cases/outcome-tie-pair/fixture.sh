#!/usr/bin/env bash
# Scaffold (runs only with `claude plugin eval --scaffold`). Written by evals/fixtures/make_fixtures.py
# --emit-scaffold; synthetic images drawn in code, museum images fetched and hash-checked.
set -euo pipefail
mkdir -p evals/fixtures/out/renders
curl -fsSL -A 'artwright/0.3.0 (+https://github.com/m4bwav/artwright)' -o evals/fixtures/out/cma-1930.189.jpg https://openaccess-cdn.clevelandart.org/1930.189/1930.189_web.jpg
echo 'b0f546cc1972fb8e7ef84d21eb7d30805de189297a22a248b1ecaf11c5b5468d  evals/fixtures/out/cma-1930.189.jpg' | sha256sum -c --quiet
curl -fsSL -A 'artwright/0.3.0 (+https://github.com/m4bwav/artwright)' -o evals/fixtures/out/cma-1940.1002.jpg https://openaccess-cdn.clevelandart.org/1940.1002/1940.1002_web.jpg
echo 'cf8c01bdc069c8d8dd79028fc55e74c58032eb09e7982fd95d38b7d3fd8ddbe9  evals/fixtures/out/cma-1940.1002.jpg' | sha256sum -c --quiet
