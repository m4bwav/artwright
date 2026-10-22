#!/usr/bin/env bash
# Scaffold (runs only with `claude plugin eval --scaffold`). Written by evals/fixtures/make_fixtures.py
# --emit-scaffold; synthetic images drawn in code, museum images fetched and hash-checked.
set -euo pipefail
mkdir -p evals/fixtures/out/renders
base64 -d > evals/fixtures/out/sprite_fake.png <<'B64'
iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAABhElEQVR4nO2XMU4DQQxF9wCUlGmC
EE1SpEVCoqHMQeipUUTBkai5AwWi4ghcATRSisxoZe+PvcBmn6VfrDzeHb+Z9Xi6DsMwzLDzs8X3
xLUDAAAAcHzCb4/rSevh7lIDAgAAzByAB8TTHyT0v04BAABg4gCiCanAVBUAoxZBAAAAACEAUUBq
ggAAAAByAWQD+fx6r+SN/3h5qsaX519NGAAAmDkANWGvqKnABiQkFc3RTwEAAODEAHhAnrebSp4/
W9v1VfW98mz5008BAADgxAGUgEOVFx6qb0KWP1v3N6vqe+XZ8l8vL16bnG5DKz41yTsCAAAAAAAA
MHMAUh8wZAJKvHfOq/FyH5C9I9R4r9NLX3EAAECrAerdIApgs1hKvX+r9LuA6o8CaOXd/sK3QwAA
wJ6wVxP6JhzpA0oNsGpCq7ZGjN4JRlc8e0eETwUAAEDrA9rxarynnnO8UvGn9gHejmgVjR8gc8X2
SR0dDwAA+AmY/3g0foDMf7b4I/EY1s3bfgD55hQqTUpLVQAAAABJRU5ErkJggg==
B64
