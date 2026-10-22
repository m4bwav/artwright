#!/usr/bin/env bash
# Scaffold (runs only with `claude plugin eval --scaffold`). Written by evals/fixtures/make_fixtures.py
# --emit-scaffold; synthetic images drawn in code, museum images fetched and hash-checked.
set -euo pipefail
mkdir -p evals/fixtures/out/renders
base64 -d > evals/fixtures/out/renders/render_01.png <<'B64'
iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAACJUlEQVR4nO3YsU0EQRAEwA8AE5MQ
MAiElDBJEAOTEEgBJAL4FxqWveuulsbkb3q2LC4XEREREREREZE/yv3dw9e1Wf33q5Peb5z0A6X3
Gyf9QOn9xkk/UHq/cdIPlN5vnPQDpfcbJ/1A6f3GST9Qer/LtMDby+PVWf33+i1O+oHS+42TfqD0
fuOkHyi93zjpB0rvN076gdL7jZN+oPR+46QfKL3fONOCq+fWfmfff/f7AwDAuQ949v13vz8AAJz7
gGfff/f7AwDAuQ949v13vz8AAMwOmP5Aq++z+/0BAAAAAAAAAAAAAAAAAAAAyAJw9Adon+VAADj2
AFA+AJQPAOUDQPkAUD4AlM/h/0+wGtDH5/vVOfrvT++3/IEBAAAAAAAAAAAAAAAAAAAAAOAXAFYf
aPr7R98PAAAAAAAAAAAAAAAAAAAAAAD+E8CtBV6fn8zGWQ4EgGMPAOUDQPkAUD4AlA8A5QNA+QBQ
PgCUDwDlA0D5AFA+AJQPAOUDQPksBwBI+QMDAAAAAAAAAAAAAAAAAAAAAMA/Arj1++3f3/3+AADQ
/QC7v7/7/QEAoPsBdn9/9/sDAED3A+z+/u73ByAdwOqC0wOs/v7R91sO5OgFAQAAAAAAAAAAAAAA
AAAAADgVgGkB+wFgPwDsB4D9ALAfAPYDwH4A2O/vAEwL7l7QfuUF7FdewH7lBexXXsB+5QXsV17A
fuUF7CciIiIiIiIicvnJN96F6ldoAXlhAAAAAElFTkSuQmCC
B64
