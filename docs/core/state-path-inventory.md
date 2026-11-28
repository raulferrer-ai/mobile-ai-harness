# IC-001 — Authoritative State Path Inventory

## 1. Scope and method

This inventory maps the repository paths that can create, mutate, consume, or invalidate feature-board state and the controls that currently surround them.

It is based on static inspection of the repository at the \`feat/engineering-core\` branch. It is not a runtime penetration test, a test execution report, or proof of the effective GitHub branch-protection configuration.

The primary state file is \`feature_list.json\`. The relevant state includes:

- Feature lifecycle: \`planned\`, \`in_progress\`, \`blocked\`, \`done\`.
- Per-platform lifecycle: \`pending\`, \`in_progress\`, \`sensor_green\`, \`done\`.
- Sensor metadata under \`features[].sensors\`.
- Gate metadata under \`features[].gate\`.
- Completion metadata: \`verified\`, \`completed_at\`, and \`blocked_reason\`.

## 2. State mutation inventory

| Path / entry point | State affected | Mutation or authority | Static finding |
| --- | --- | --- | --- |
| \`scripts/feature.py save()\` | Entire feature board | Writes \`feature_list.json\` | Central persistence helper, but no caller identity, authorization token, or trusted-process check |
| \`feature.py add\` | Feature collection | Adds a planned feature | Validates basic input and schema-related constraints |
| \`feature.py start\` | Feature status | Sets \`in_progress\` | Enforces one active feature and validates the spec |
| \`feature.py platform\` | Platform status | Sets manual states | Rejects direct \`sensor_green\`, but only for this one CLI path |
| \`feature.py record-sensor\` | Platform status, sensor metadata, Gate | Sets \`sensor_green\`, records timestamp and mode; failure removes sensor metadata and invalidates Gate | **Critical:** directly callable; no proof that a sensor command ran and no actor authorization |
| \`feature.py gate\` | Gate metadata | Writes Gate from \`--sensors\` argument | **Critical:** trusts caller-supplied platform names; does not independently require matching sensor records or successful executions |
| \`feature.py done\` | Feature and platform completion | Sets platforms to \`done\`, feature to \`done\`, \`verified=true\`, and timestamp | Requires a boolean CLI flag, Gate coverage, and green platform states; does not authenticate a human |
| \`feature.py block\` | Feature status, Gate | Sets \`blocked\`, reason, clears Gate | No actor authorization |
| \`feature.py import-legacy\` | Entire feature board | Replaces board with converted legacy data | Writes state through the same save path; no actor authorization |
| \`scripts/sensor.sh record()\` | Sensor state via CLI | Calls \`feature.py record-sensor\` | Runs after sensor success/failure, but the record operation itself is not restricted to this caller |
| \`scripts/verify-feature.sh\` | Sensor state and Gate | Runs checks, collects exit codes, invokes Gate | Normal workflow orchestrator; Gate still trusts the supplied list rather than independently resolving evidence |
| Direct filesystem writes | Entire feature board | Any process with write access can edit JSON | CLI convention and editor hooks do not prevent shell/Python/file API writes |
| \`scripts/tests/test_feature_cli.py\` | Test fixture state | Exercises the CLI and board | Existing happy-path test calls \`record-sensor\` directly and then records Gate; it does not execute real platform checks |

## 3. Read and decision paths

| Path | Reads | Decision made | Gap |
| --- | --- | --- | --- |
| \`feature.py validate()\` | Board, configured platforms | Checks schema and internal consistency | Structural consistency is not provenance or authenticity |
| \`feature.py cmd_gate()\` | Feature platforms, caller-provided \`--sensors\`, sensor metadata | Checks that supplied names cover feature platforms; labels non-test modes degraded | Does not prove a corresponding sensor execution occurred or that its result is current |
| \`feature.py cmd_done()\` | Feature status, Gate, platform statuses | Allows closure if Gate covers platforms and each platform is \`sensor_green\` | All prerequisites can currently be created by untrusted CLI calls; human flag is not authenticated |
| \`verify-feature.sh\` | Sensor process exit codes and feature platform list | Stops on failed or unavailable checks; calls Gate on complete run | Good orchestration path, but it does not make the underlying state-writing commands privileged |
| \`validate-harness.py\` | Board and repository files | Validates structure, configuration, and board invariants | Does not validate sensor provenance, source snapshot, Gate freshness, or approval identity |

## 4. Agent invocation and adapter controls

### 4.1 Claude Code

File: \`.claude/settings.json\`

- Allows \`Bash(python3 scripts/*)\` and \`Bash(sh scripts/*)\`.
- Denies the direct \`Edit\` operation on \`feature_list.json\`.
- Denies a command pattern for \`feature.py done*\`.
- Installs a destructive-command hook and a sensitive-path edit hook.

**Assessment:** broad script execution permits direct calls to \`record-sensor\`, \`gate\`, \`block\`, and other CLI commands. The edit restriction applies to the editor tool, not arbitrary shell-based file writes. The hooks are guardrails and do not authenticate the actor.

### 4.2 OpenCode

File: \`.opencode/opencode.json\`

- Allows all Bash commands by default.
- Denies selected destructive commands and a \`feature.py done*\` pattern.

**Assessment:** direct \`record-sensor\` and \`gate\` invocation is allowed by the default Bash rule. The configuration does not establish a trusted verifier boundary or human identity.

### 4.3 Codex

File: \`.codex/config.toml\`

- Uses \`workspace-write\` sandbox mode.
- Uses \`on-request\` approval policy.
- Defines no repository-specific command deny list or sensor/Gate authorization hook.

**Assessment:** the workspace sandbox is not a command-level authorization model for the feature CLI. A process permitted to write within the workspace can potentially modify the board or invoke its scripts, subject to the actual runtime sandbox.

### 4.4 Cursor

File: \`.cursor/hooks.json\`

- Installs a \`beforeShellExecution\` hook for \`block-destructive.py\`.

**Assessment:** the hook targets destructive command patterns. It does not deny direct sensor recording or caller-supplied Gate evaluation. Its effectiveness depends on the tool invoking the hook for the operation.

### 4.5 Shared hooks

Files:

- \`.agents/hooks/block-destructive.py\`
- \`.agents/hooks/guard-sensitive-paths.py\`

The destructive hook blocks selected shell patterns and the textual patterns \`feature.py done\` and \`--human-checklist-ok\`. The sensitive-path hook blocks editor operations targeting the board and selected secret/local files.

**Assessment:** both scripts explicitly describe themselves as guardrails, not security boundaries. The shell hook is a pattern matcher, not a command parser or authenticated authorization service. The edit hook only protects operations that pass through it. Neither prevents a process from importing Python modules, writing the JSON through another program, or invoking an alternate path.

## 5. CI and repository governance

### 5.1 CI workflow

File: \`.github/workflows/ci.yml\`

The workflow runs harness validation and unit tests, secret scanning, and conditionally runs Android tests or an iOS build when platform projects are present.

Observations:

- The harness CI job validates structure and runs the existing unit tests.
- Android checks run when \`android/gradlew\` exists.
- iOS CI currently runs a build, not the full iOS test sensor.
- Missing platform projects cause the corresponding job step to skip rather than fail.
- The workflow does not currently establish a separate trusted identity for Evidence creation or bind Gate records to a source snapshot.
- CI is triggered on pushes to \`main\` and pull requests; branch-specific protection and required status settings are external repository configuration.

### 5.2 CODEOWNERS

File: \`.github/CODEOWNERS\`

The file declares ownership patterns for scripts, adapters, hooks, workflow configuration, and governance documents. It still contains \`@your-org/*\` placeholders.

**Assessment:** the file expresses intended review ownership, but placeholder owners do not establish effective review. Whether code-owner review is required depends on active branch-protection/ruleset settings, which this static inventory has not verified.

## 6. Existing tests and coverage gaps

File: \`scripts/tests/test_feature_cli.py\`

Existing tests cover:

- Basic feature creation and start transitions.
- Manual rejection of \`sensor_green\` through the \`platform\` command.
- Completion requiring the human flag, Gate, and green platform states.
- Gate coverage for required platform names.
- Gate invalidation after a failed sensor record.
- Structural validation of a hand-edited completed feature.

Critical gaps:

1. \`test_full_happy_path\` calls \`record-sensor ios\` and \`record-sensor android\` directly. It then calls Gate with a caller-provided list. No platform test/build command is executed.
2. There is no negative test asserting that direct \`record-sensor\` success is rejected.
3. There is no negative test asserting that Gate rejects fabricated platform names or missing sensor records.
4. There is no test that modifies relevant source after a sensor result and expects the result/Gate to become stale.
5. There is no test proving that a human approval came from an authenticated human identity.
6. There is no test that an agent cannot write or replace the board through a shell-based alternate path.

The existing test suite therefore verifies the intended CLI sequence, but currently codifies an unsafe shortcut as a valid happy path.

## 7. Findings and severity

### F-001 — Agent-callable sensor certification

**Severity:** Critical  
**Evidence:** \`feature.py cmd_record_sensor()\`; \`sensor.sh record()\`; Claude and OpenCode adapter permissions; existing CLI tests.

The \`record-sensor\` command changes platform state to \`sensor_green\` and creates sensor metadata without requiring an execution identifier, verifier identity, captured exit status, or proof of a test run. The same command is exposed to agents through broad script permissions.

**Impact:** an agent can manufacture the state required by \`done\` without executing the platform check.

### F-002 — Caller-controlled Gate inputs

**Severity:** Critical  
**Evidence:** \`feature.py cmd_gate()\`; \`verify-feature.sh\`.

Gate evaluation receives \`--sensors\` from its caller and checks only that the supplied set covers the configured platforms. It does not independently load and validate trusted verification records.

**Impact:** a caller can record a Gate for platform names without demonstrating that the corresponding sensors passed.

### F-003 — Direct board mutation is not prevented by the CLI convention

**Severity:** High  
**Evidence:** \`feature.py save()\`; Claude editor restrictions; shared edit hook; Codex workspace-write; OpenCode Bash allow-all.

The CLI is described as the sanctioned board writer, but the board is a normal workspace file. Adapter restrictions cover selected tool operations, not all processes that can write it.

**Impact:** an agent or process with workspace write access can bypass CLI invariants by editing the JSON through shell, Python, or another available file operation.

### F-004 — Human approval is represented by a caller-supplied flag

**Severity:** High  
**Evidence:** \`feature.py cmd_done()\`; \`block-destructive.py\`; adapter-specific deny patterns.

The \`--human-checklist-ok\` flag is a boolean argument. It does not contain an authenticated approver identity or an independently verifiable approval record. Adapter-level command pattern blocks are not universal and can be bypassed by alternate invocation paths.

**Impact:** the local CLI cannot distinguish a human invocation from an agent invocation that supplies the same flag.

### F-005 — Existing happy-path tests bypass real verification

**Severity:** High  
**Evidence:** \`scripts/tests/test_feature_cli.py::test_full_happy_path\`.

The test records sensor success directly and treats that as sufficient to proceed to Gate and completion.

**Impact:** the tests protect the current behavior rather than the intended trust boundary, and can give false confidence about verification.

### F-006 — No source snapshot or policy binding in sensor records

**Severity:** High  
**Evidence:** sensor metadata written by \`cmd_record_sensor()\` contains only timestamp and mode.

There is no source revision/tree digest, check-definition version, verifier identity/version, or policy/profile version in the sensor record.

**Impact:** a result cannot be shown to apply to the code or policy currently being evaluated; stale results cannot be detected reliably.

### F-007 — Control-plane governance is not demonstrated

**Severity:** Medium / unresolved  
**Evidence:** CODEOWNERS placeholders; no branch-protection/ruleset inspection in this task.

The repository contains intended ownership patterns, but the owners remain placeholders and enforcement settings have not been verified.

**Impact:** the repository-level review boundary cannot yet be claimed as active.

## 8. State-path summary

| State / decision | Current writer | Current validator | Can an agent reach the path? | Trust assessment |
| --- | --- | --- | --- | --- |
| Feature creation/start/block | \`feature.py\` | CLI invariants | Yes, through allowed scripts or workspace access | Workflow validation only; no authenticated actor |
| \`sensor_green\` | \`record-sensor\` | No independent verifier check | Yes | **Untrusted** |
| Sensor metadata | \`record-sensor\` | None beyond reading fields | Yes | **Untrusted** |
| Gate result | \`feature.py gate\` | Caller-supplied sensor coverage | Yes | **Untrusted** |
| \`done\` / \`verified\` | \`feature.py done\` | Gate + platform status + CLI flag | Tool-dependent; alternate invocation remains possible | **Untrusted as human approval** |
| Structural board validity | \`feature.py\`, direct file write | \`feature.py validate\`, CI validator | Yes | Integrity check, not provenance |
| CI test/build result | GitHub Actions | Workflow runner | External CI identity | More trustworthy execution context, but not yet bound to Gate Evidence |

## 9. IC-001 conclusion

IC-001 static inventory is complete for the currently identified feature-board, sensor, Gate, completion, adapter, hook, test, and CI paths.

The most important distinction is:

- \`sensor.sh\` is a legitimate route that runs platform checks and then records a result.
- \`feature.py record-sensor\` is a separate, directly invocable state-writing route that does not prove a check ran.
- \`feature.py gate\` accepts caller-provided status names instead of deriving its decision from trusted verification records.
- The current adapter restrictions do not consistently close those routes.

No implementation has been changed as part of this inventory.

## 10. Required next step — IC-002

Create adversarial regression tests before changing verifier or Gate behavior.

The initial test set must demonstrate that the current implementation permits, or explicitly rejects, each of these attempts:

1. Directly call \`record-sensor\` without running a platform check.
2. Call \`gate\` with all configured platform names when no trusted sensor records exist.
3. Supply a sensor name that is not configured for the feature.
4. Modify \`feature_list.json\` through a shell/Python path despite editor-hook restrictions.
5. Reuse a passing sensor record after changing relevant source.
6. Close a feature by supplying the human flag without authenticated human approval.

Record current vulnerable behavior as reproducible regression cases; then change the expected result to rejection as each P0 fix is implemented.

## 11. Related documents

- [Implementation Roadmap](implementation-roadmap.md)
- [Architecture](architecture.md)
- [Domain Model](domain-model.md)
- [Agent Contract](agent-contract.md)
- [AI Governance](../ai-governance.md)
- [Feature Workflow](../workflow.md)
