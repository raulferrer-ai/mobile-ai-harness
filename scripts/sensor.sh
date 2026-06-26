#!/usr/bin/env sh
# Sensor runner. One implementation used by Makefile, verify-feature.sh and CI.
# Usage: sh scripts/sensor.sh <ios|android|build-ios|lint-ios|lint-android>
# Exit codes: 0 = green, 1 = red (tests/build failed), 3 = sensor unavailable here.
set -eu
cd "$(dirname "$0")/.."
# shellcheck disable=SC1091
. ./harness.env

TARGET="${1:-}"

unavailable() {
  echo "SENSOR UNAVAILABLE ($TARGET): $1" >&2
  exit 3
}

record() { python3 scripts/feature.py record-sensor "$@" || true; }

jdk_major() {
  java -version 2>&1 | awk -F'"' '/version/ { split($2, a, "."); if (a[1] == "1") print a[2]; else print a[1]; exit }'
}

need_ios() {
  [ "$(uname -s)" = "Darwin" ] || unavailable "iOS sensors need macOS"
  command -v xcodebuild >/dev/null 2>&1 || unavailable "xcodebuild not found (install Xcode)"
  [ -d "$IOS_PROJECT" ] || unavailable "$IOS_PROJECT not found (create the Xcode project or fix IOS_PROJECT in harness.env)"
}

need_android() {
  [ -f "$ANDROID_DIR/gradlew" ] || unavailable "$ANDROID_DIR/gradlew not found (create the Gradle project first)"
  command -v java >/dev/null 2>&1 || unavailable "java not found (JDK $MIN_JDK+ required)"
  major="$(jdk_major)"
  if [ -z "$major" ] || [ "$major" -lt "$MIN_JDK" ]; then
    unavailable "JDK $MIN_JDK+ required, found '${major:-unknown}'. Set JAVA_HOME."
  fi
}

case "$TARGET" in
  ios)
    need_ios
    echo "-> iOS sensor (mode=$IOS_SENSOR_MODE, destination=$IOS_DESTINATION)"
    if [ "$IOS_SENSOR_MODE" = "build" ]; then
      if xcodebuild build -project "$IOS_PROJECT" -scheme "$IOS_SCHEME" -destination "$IOS_DESTINATION" -quiet; then
        record ios --mode build
        echo "iOS build green (DEGRADED: tests did not run)"
      else
        record ios --fail
        exit 1
      fi
    else
      if xcodebuild test -project "$IOS_PROJECT" -scheme "$IOS_SCHEME" -destination "$IOS_DESTINATION" -quiet; then
        record ios --mode test
        echo "iOS sensor green"
      else
        record ios --fail
        echo "iOS sensor RED" >&2
        exit 1
      fi
    fi
    ;;
  android)
    need_android
    echo "-> Android sensor ($ANDROID_TEST_TASK, JDK $(jdk_major))"
    if (cd "$ANDROID_DIR" && sh ./gradlew "$ANDROID_TEST_TASK" --quiet); then
      record android --mode test
      echo "Android sensor green"
    else
      record android --fail
      echo "Android sensor RED" >&2
      exit 1
    fi
    ;;
  build-ios)
    need_ios
    echo "-> iOS build only (CI), destination=$IOS_CI_DESTINATION"
    xcodebuild build -project "$IOS_PROJECT" -scheme "$IOS_SCHEME" \
      -destination "$IOS_CI_DESTINATION" CODE_SIGNING_ALLOWED=NO -quiet
    ;;
  lint-ios)
    if [ -z "${IOS_LINT_CMD:-}" ]; then echo "No iOS lint configured (IOS_LINT_CMD is empty)."; exit 0; fi
    echo "-> iOS lint: $IOS_LINT_CMD"
    sh -c "$IOS_LINT_CMD"
    ;;
  lint-android)
    if [ -z "${ANDROID_LINT_TASK:-}" ]; then echo "No Android lint configured."; exit 0; fi
    need_android
    (cd "$ANDROID_DIR" && sh ./gradlew "$ANDROID_LINT_TASK" --quiet)
    ;;
  *)
    echo "Usage: sh scripts/sensor.sh <ios|android|build-ios|lint-ios|lint-android>" >&2
    exit 64
    ;;
esac
