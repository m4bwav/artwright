#!/usr/bin/env bash
# Runs artwright eval cases under WSL2, Linux or macOS. Native Windows has no sandbox backend, so `claude plugin eval`
# refuses cases that grant Bash there (L-001). From PowerShell:
#   wsl -d Ubuntu -- bash /mnt/<drive>/<path>/artwright/scripts/eval-wsl.sh "action-*" [extra plugin-eval options]
# Results: evals/results/<timestamp>/ and evals/cases/results/<glob>.json (both git-ignored).
# Harness: a pinned 2.1.281 copy when present (2.1.307 makes every Bash path read-only in eval runs); CLAUDE=... overrides.
set -u
CLAUDE="${CLAUDE:-$HOME/.local/bin/claude}"
PINNED="$HOME/.local/share/claude-pinned/claude-2.1.281"
[ "$CLAUDE" = "$HOME/.local/bin/claude" ] && [ -x "$PINNED" ] && CLAUDE="$PINNED"
echo "harness: $("$CLAUDE" --version 2>/dev/null | head -1)"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT" || exit 1
GLOB="${1:-*}"
shift || true
OUT="evals/cases/results/$(printf '%s' "$GLOB" | tr -c 'A-Za-z0-9-' '_').json"
"$CLAUDE" plugin eval . --trust-plugin --ablation none --model sonnet --case "$GLOB" -j 3 --scaffold \
  --allow-tools Bash Write Edit Read Glob Grep Skill --no-publish --json "$OUT" "$@" 2>&1 | tail -4
echo "json: $OUT"
