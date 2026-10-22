#!/usr/bin/env bash
# Scaffold (runs only with `claude plugin eval --scaffold`). Written by evals/fixtures/make_fixtures.py
# --emit-scaffold; synthetic images drawn in code, museum images fetched and hash-checked.
set -euo pipefail
mkdir -p evals/fixtures/out/renders
base64 -d > evals/fixtures/out/renders/render_05.png <<'B64'
iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAACAklEQVR4nO3SsVEDUQwEUBdASEgJ
BBRCSw5pkICQEmgBOrA9YzSr9b2d2fROX3qnk4iIiIiIiIjIjXl+evm91PT/p5t+3/T/1w8IQDjp
AQEIJz0gAOGkBwQgnPSAAISTHhCAcNIDAhAe4PP8erHTB7j2/+mm3zcOBIDd7wMAAAAAAAAAAAAA
AAAAAPhnAPcCmX7g9IG2zzd+YAB2z5e+PwAAPPaCt8+Xvj8AADz2grfPl74/AAA89oK3zxc/8LUH
Ti8wDWD7+wAAAAAAAAAAAAAAAAAAAAAAYBMABUABUAAUAAVAAVAAFIBb+/3zdbHbvw/A8gMBAAAA
AAAAAAAAAAAAAAAcDEAayHaA6fePHxgAAAAAAAAAAAAAAAAAAACAQwG4NsDH+1u00/O1vx+A5d8H
YPmB2t8PwPLvA7D8QO3vB2D59wFYfqD29wOw/PsAKAAKgAKgACgACoACoAAoAAqAAqAAKAAKgAKg
hwOQ/v/2+QAAAAAAAAAAAAAAAAAAAAAAoAlAeoHpAwEAAAAAAAAAAAAAAAAAAAAAwCYA9wJJL2C6
6fnHDwzA7vnT9wcAgO4Fts+fvj8AAHQvsH3+9P0BAKB7ge3zn9rTvoD2+eNpX2D7/PG0L7B9/nja
F9g+fzztC2yfP572BbbPH0/7Atvnj6d9ge3zi4iIiIiIiMhx8gceYz0xKpjmlAAAAABJRU5ErkJg
gg==
B64
