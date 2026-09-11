#!/usr/bin/env sh
# Dual gate: the last automated lock before a feature can be closed.
# Usage: sh scripts/verify-feature.sh [feature-id]     (default: the in_progress feature)
# Env:   SKIP_SENSORS="ios"   skip a platform explicitly (result is PARTIAL, exit 3, no gate recorded)
# Exit:  0 passed | 1 failed | 3 partial (a sensor was unavailable or skipped)
set -eu
cd "$(dirname "$0")/.."
# shellcheck disable=SC1091
. ./harness.env

FEATURE_ID="${1:-}"
SKIP_SENSORS="${SKIP_SENSORS:-}"

step() { printf '\n==> %s\n' "$1"; }

step "1/5 Harness integrity and contract budgets"
python3 scripts/validate-harness.py
python3 .agents/hooks/check-contract-size.py
python3 scripts/scan-secrets.py

step "2/5 Forbidden local IDE / OS artifacts"
if find . -path ./.git -prune -o \( -name '*.xcuserstate' -o -name '.DS_Store' -o -name 'Thumbs.db' \) -print | grep -q .; then
  echo "ERROR: forbidden IDE/OS files found. Run: make clean-ide" >&2
  exit 1
fi
echo "clean"

step "3/5 Resolve feature"
if [ -z "$FEATURE_ID" ]; then
  FEATURE_ID="$(python3 scripts/feature.py next --active-only)"
fi
if [ -z "$FEATURE_ID" ]; then
  echo "No in_progress feature. Harness checks passed; nothing else to verify."
  exit 0
fi
echo "feature: $FEATURE_ID"

step "4/5 Spec sanity"
python3 scripts/feature.py check "$FEATURE_ID"

step "5/5 Platform sensors"
PASSED=""
FAILED=""
PARTIAL=""
for p in $(python3 scripts/feature.py platforms "$FEATURE_ID"); do
  case " $SKIP_SENSORS " in
    *" $p "*) echo "SKIPPED (explicit): $p"; PARTIAL="$PARTIAL $p"; continue ;;
  esac
  rc=0
  sh scripts/sensor.sh "$p" || rc=$?
  case "$rc" in
    0) PASSED="$PASSED,$p" ;;
    3) PARTIAL="$PARTIAL $p" ;;
    *) FAILED="$FAILED $p" ;;
  esac
done
PASSED="${PASSED#,}"

printf '\n============================================\n'
if [ -n "$FAILED" ]; then
  echo "GATE FAILED. Red sensor(s):$FAILED. Fix and re-run. Do NOT mark the feature done."
  exit 1
fi
if [ -n "$PARTIAL" ]; then
  echo "GATE PARTIAL. Not verified:$PARTIAL. The feature cannot be closed until every platform runs its sensor."
  exit 3
fi
python3 scripts/feature.py gate "$FEATURE_ID" --sensors "$PASSED"
echo "GATE PASSED for $FEATURE_ID."
echo "Next (HUMAN): complete docs/dual-checklist.md, then run in your own terminal:"
echo "  python3 scripts/feature.py done $FEATURE_ID --human-checklist-ok"
