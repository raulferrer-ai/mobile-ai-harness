#!/usr/bin/env sh
# Toolchain diagnostic for this machine. Exit 1 if a blocker is found for a platform you can build here.
# Usage: sh scripts/doctor.sh
set -eu
cd "$(dirname "$0")/.."
# shellcheck disable=SC1091
. ./harness.env

BLOCKERS=0
ok()   { printf '  [ok]    %s\n' "$1"; }
warn() { printf '  [warn]  %s\n' "$1"; }
bad()  { printf '  [FAIL]  %s\n' "$1"; BLOCKERS=$((BLOCKERS + 1)); }

echo "Core"
command -v git >/dev/null 2>&1 && ok "git $(git --version | awk '{print $3}')" || bad "git not found"
command -v make >/dev/null 2>&1 && ok "make present" || bad "make not found"
if command -v python3 >/dev/null 2>&1; then
  if python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)'; then
    ok "python3 $(python3 -c 'import platform; print(platform.python_version())')"
  else
    bad "python3 3.9+ required"
  fi
else
  bad "python3 not found"
fi

echo "Android"
if command -v java >/dev/null 2>&1; then
  major="$(java -version 2>&1 | awk -F'"' '/version/ { split($2, a, "."); if (a[1] == "1") print a[2]; else print a[1]; exit }')"
  if [ -n "$major" ] && [ "$major" -ge "$MIN_JDK" ]; then ok "JDK $major (needs $MIN_JDK+)"; else bad "JDK $MIN_JDK+ required, found '${major:-unknown}'"; fi
else
  bad "java not found (JDK $MIN_JDK+ required for the Android sensor)"
fi
[ -f "$ANDROID_DIR/gradlew" ] && ok "$ANDROID_DIR/gradlew present" || warn "$ANDROID_DIR/gradlew missing (create the Android project: docs/bootstrap.md)"
[ -n "${ANDROID_HOME:-${ANDROID_SDK_ROOT:-}}" ] && ok "Android SDK path is set" || warn "ANDROID_HOME/ANDROID_SDK_ROOT not set (Android Studio sets sdk.dir in local.properties)"

echo "iOS"
if [ "$(uname -s)" = "Darwin" ]; then
  if command -v xcodebuild >/dev/null 2>&1; then
    ok "$(xcodebuild -version 2>/dev/null | head -1)"
    command -v swift >/dev/null 2>&1 && ok "$(swift --version 2>&1 | head -1)"
    n="$(xcrun simctl list devices available 2>/dev/null | grep -c 'iPhone' || true)"
    [ "${n:-0}" -gt 0 ] && ok "$n iPhone simulator(s) available (IOS_DESTINATION=$IOS_DESTINATION)" || warn "no iPhone simulators found: install a runtime in Xcode"
  else
    bad "xcodebuild not found (install Xcode and run xcode-select)"
  fi
  [ -d "$IOS_PROJECT" ] && ok "$IOS_PROJECT present" || warn "$IOS_PROJECT missing (create the Xcode project: docs/bootstrap.md)"
else
  warn "not macOS: the iOS sensor cannot run here (use a Mac or CI)"
fi

echo ""
if [ "$BLOCKERS" -gt 0 ]; then
  echo "doctor: $BLOCKERS blocker(s) found."
  exit 1
fi
echo "doctor: no blockers."
