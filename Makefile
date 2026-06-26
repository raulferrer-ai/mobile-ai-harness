# Standard entry points for humans and agents. Configuration lives in harness.env.
include harness.env

.DEFAULT_GOAL := help
.PHONY: help init validate-harness test-harness scan-secrets doctor sensor-ios sensor-android sensors \
        build-ios lint-ios lint-android gate verify status simulators clean-ide

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## ' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "  make %-18s %s\n", $$1, $$2}'
	@echo ""
	@echo "Human-only (not Make targets on purpose): dual checklist, 'feature.py done', merge, tag."

init: ## Bootstrap and validate the harness (idempotent)
	sh init.sh

validate-harness: ## Validate structure, schemas, links, budgets and scan for secrets
	python3 scripts/validate-harness.py
	python3 .agents/hooks/check-contract-size.py
	python3 scripts/scan-secrets.py

scan-secrets: ## Scan the repo for secrets and forbidden files
	python3 scripts/scan-secrets.py

doctor: ## Check this machine's toolchain (Xcode, JDK, Python, simulators)
	sh scripts/doctor.sh

test-harness: ## Run the harness' own unit tests
	python3 -m unittest discover -s scripts/tests -v

status: ## Show the feature board and what to do next
	python3 scripts/feature.py status

sensor-ios: ## iOS sensor (tests on a simulator)
	sh scripts/sensor.sh ios

sensor-android: ## Android sensor (JVM unit tests)
	sh scripts/sensor.sh android

sensors: sensor-ios sensor-android ## Both platform sensors

build-ios: ## iOS build only, no signing (used by CI)
	sh scripts/sensor.sh build-ios

lint-ios: ## Optional iOS lint (IOS_LINT_CMD)
	sh scripts/sensor.sh lint-ios

lint-android: ## Optional Android lint (ANDROID_LINT_TASK)
	sh scripts/sensor.sh lint-android

gate: ## Dual gate for the in_progress feature (or FEATURE=<id>)
	sh scripts/verify-feature.sh $(FEATURE)

verify: validate-harness test-harness gate ## Harness checks, then the gate

simulators: ## List available iOS simulators
	xcrun simctl list devices available

clean-ide: ## Remove local IDE/OS artifacts
	find . -path ./.git -prune -o \( -name '*.xcuserstate' -o -name '.DS_Store' -o -name 'Thumbs.db' \) -exec rm -f {} +
