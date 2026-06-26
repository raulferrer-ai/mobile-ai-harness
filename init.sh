#!/usr/bin/env sh
# Idempotent bootstrap. Safe to re-run.
# Usage: sh init.sh            create missing state files, validate, print status
#        sh init.sh --check    validate only (no file creation); for CI
set -eu
cd "$(dirname "$0")"

CHECK_ONLY=0
[ "${1:-}" = "--check" ] && CHECK_ONLY=1

for tool in git python3; do
  command -v "$tool" >/dev/null 2>&1 || { echo "ERROR: required tool not found: $tool" >&2; exit 1; }
done
python3 - <<'PY' || { echo "ERROR: Python 3.9+ required" >&2; exit 1; }
import sys
sys.exit(0 if sys.version_info >= (3, 9) else 1)
PY

if [ "$CHECK_ONLY" -eq 0 ]; then
  mkdir -p .github/workflows .agents/skills .agents/references .agents/hooks \
    .claude .opencode .codex .cursor docs/decisions features progress scripts/tests android ios
  [ -f progress/current.md ] || cat > progress/current.md <<'MD'
# Current state

- Active feature: none
- Next step: write the first spec in `features/` (skill: feature-spec-writer), then `python3 scripts/feature.py add ...`
- Blockers: none

## Handoff notes
Nothing yet.
MD
  [ -f progress/log.md ] || printf '# Delivery log\n\n<!-- Newest entries first -->\n' > progress/log.md
  [ -f progress/flywheel-log.md ] || printf '# Flywheel log\n\n<!-- Newest entries first. Template: docs/flywheel.md -->\n' > progress/flywheel-log.md
  [ -f feature_list.json ] || printf '{\n  "schema_version": 2,\n  "project": "my-mobile-app",\n  "features": []\n}\n' > feature_list.json
  chmod +x init.sh scripts/*.sh 2>/dev/null || true
fi

python3 scripts/validate-harness.py

echo ""
python3 scripts/feature.py status

echo ""
echo "Sensors available on this machine:"
if [ "$(uname -s)" = "Darwin" ] && command -v xcodebuild >/dev/null 2>&1; then
  echo "  ios:     xcodebuild present"
else
  echo "  ios:     NOT available here (needs macOS + Xcode)"
fi
if command -v java >/dev/null 2>&1; then
  echo "  android: java present (gradlew is checked when the sensor runs)"
else
  echo "  android: NOT available here (needs a JDK)"
fi

if [ "$CHECK_ONLY" -eq 0 ]; then
  echo ""
  echo "Next steps:"
  echo "  1. Edit harness.env (project name, Xcode project path/scheme, simulator)."
  echo "  2. Fill docs/product.md and docs/design-system.md."
  echo "  3. Review stack defaults: docs/stack.md (change them with docs/customizing.md)."
  echo "  4. Create the native projects and prove the loop: docs/bootstrap.md (make doctor first)."
  echo "  5. Organization checklist (CODEOWNERS, branch protection, AI governance): docs/bootstrap.md section 6."
  echo "  6. Write your first spec and start: make status"
fi
