# Engineering Core — Implementation Roadmap

## 1. Purpose

This roadmap turns the [Architecture](architecture.md), [Domain Model](domain-model.md), and [Agent Contract](agent-contract.md) into an incremental, testable implementation plan.

The objective is not to extract abstractions as quickly as possible. It is to establish trustworthy workflow behavior in the existing harness, then extract the smallest reusable Core that the implementation has demonstrated it needs.

All work described here is performed on the \`feat/engineering-core\` branch until a separately reviewed integration decision is made.

## 2. Delivery principles

1. **Fix trust before abstraction.** Do not extract a Core around state transitions that can still be forged.
2. **Tests prove rejection as well as acceptance.** Every security-sensitive capability needs negative tests for unauthorized paths.
3. **Evidence must be independently established.** Agent declarations and editable status files are not authoritative results.
4. **Bind results to exact inputs.** A passing check is valid only for the source snapshot and policy it actually verified.
5. **Preserve the current workflow where possible.** Prefer incremental changes and compatibility over a repository-wide rewrite.
6. **Keep the implementation honest.** Distinguish implemented, locally guarded, CI-enforced, and not-yet-enforced controls.
7. **One coherent change per task.** Each task should have a bounded scope, explicit acceptance criteria, and its own reviewable commit or pull request unit.

## 3. Priority model

- **P0 — Trust blocker:** must be addressed before treating Gate results as authoritative.
- **P1 — Reference implementation:** required to demonstrate the Mobile workflow end to end.
- **P2 — Core extraction:** required to establish reusable domain and application boundaries.
- **P3 — Generality:** required to validate a second Engineering Profile and broader adoption.

A task is complete only when its acceptance criteria are met and the relevant evidence is available. A documentation update alone does not satisfy an implementation task.

## 4. Phase 0 — Baseline and threat model

### IC-001 — Inventory authoritative state paths

**Priority:** P0  
**Type:** Analysis

Trace every code path that can create, update, read, or invalidate:

- Sensor results and \`sensor_green\` state.
- Feature/work-item state.
- Gate results.
- Human completion flags.
- Verification output and logs.

Inspect CLI commands, imported functions, scripts, Make targets, hooks, adapter permissions, and CI workflows. Record which actor can invoke each path and whether the path validates authority or merely trusts caller-supplied values.

**Acceptance criteria:**

- A path inventory identifies each writer and reader of authoritative state.
- Every state mutation is mapped to its entry point and authorization check.
- Direct agent-invocable paths are explicitly identified.
- The inventory distinguishes enforcement from instruction or convention.

### IC-002 — Establish adversarial regression tests

**Priority:** P0  
**Type:** Test

Create tests that reproduce the known classes of failure before changing implementation.

At minimum, test whether an agent or untrusted process can:

- Invoke a sensor-recording helper without running the underlying check.
- Supply or modify a green sensor result.
- Call Gate evaluation with caller-selected sensor statuses.
- Reuse a previous passing result after relevant source changes.
- Modify a result record or verifier output and have it accepted.
- Mark work complete without a current passing Gate and valid human approval.

Tests must exercise public command/script entry points where possible, not only private helper functions.

**Acceptance criteria:**

- Each attack scenario has a reproducible test.
- Tests fail against the vulnerable behavior or clearly document an existing mitigation.
- Test output identifies the attempted bypass and expected rejection.
- No test treats a prompt or agent instruction as a security boundary.

### IC-003 — Document the current trust boundary

**Priority:** P0  
**Type:** Documentation

Record the current execution model: which processes run as the agent's user, which files the agent can edit, which scripts the agent can invoke, and which CI or repository controls are outside the agent's authority.

**Acceptance criteria:**

- The threat model names the untrusted actor and protected assets.
- Local guardrails are not described as strong isolation if the agent can modify or invoke around them.
- Remaining limitations and accepted risks are explicit.

## 5. Phase 1 — Harden verification and Gate

### IC-010 — Remove agent authority to certify sensor outcomes

**Priority:** P0  
**Type:** Security implementation

Replace any agent-writable sensor status path with a trusted verification operation.

The agent may request a sensor run. It must not be able to create authoritative success by invoking a record-only command, setting a flag, editing a status file, or supplying a claimed exit code.

**Acceptance criteria:**

- No agent-accessible command can directly set an authoritative sensor to green.
- The trusted operation executes the configured check or validates a trusted execution attestation.
- The actual process exit status is captured by the trusted mechanism.
- Missing, skipped, malformed, or inconclusive results cannot be interpreted as passing.
- Regression tests from IC-002 reject direct certification attempts.

### IC-011 — Make Gate evaluation independently derive its inputs

**Priority:** P0  
**Type:** Security implementation

Change Gate evaluation so it retrieves authoritative Verification/Evidence records from the trusted source and derives sensor outcomes itself.

It must not accept a caller-provided list of green sensors or trust mutable board fields as proof that checks ran.

**Acceptance criteria:**

- Gate evaluation resolves required checks from policy/profile configuration.
- It loads the corresponding trusted verification records.
- It checks verifier identity/version, outcome, required metadata, and source binding.
- Missing or invalid Evidence results in a non-passing Gate.
- A caller cannot obtain a passing Gate by supplying fabricated statuses.
- Existing CLI behavior is retained only where it does not weaken these rules.

### IC-012 — Define and implement source snapshot identity

**Priority:** P0  
**Type:** Security implementation / design

Define the exact source content covered by a verification.

Prefer an immutable Git commit when the checked tree is exactly represented by that commit. For uncommitted work, define a deterministic snapshot procedure that covers all relevant tracked changes and untracked files. Document treatment of ignored files, generated outputs, submodules, and external dependencies.

Do not use a branch name or mutable working-tree path as the snapshot identity.

**Acceptance criteria:**

- The snapshot procedure is documented and deterministic.
- The snapshot identifier is collision-resistant.
- Evidence records the snapshot identifier and the procedure/version used.
- Changes to relevant tracked or untracked inputs produce a different snapshot identity.
- Tests cover staged, unstaged, untracked, deleted, renamed, and submodule changes where applicable.
- The implementation explicitly documents excluded content and why it is excluded.

### IC-013 — Bind Evidence and Gate to snapshot and policy

**Priority:** P0  
**Type:** Security implementation

Every authoritative verification result must identify the exact source snapshot, check definition, verifier identity/version, execution outcome, and relevant policy/profile version.

Gate evaluation must use only Evidence that matches the current snapshot and applicable policy.

**Acceptance criteria:**

- Evidence is append-only; reruns create new records.
- A Gate result records the snapshot and policy version it evaluated.
- Evidence from another snapshot cannot satisfy the current Gate.
- A relevant policy change invalidates the affected Gate.
- A source change after verification makes the prior Gate stale.
- A stale Gate cannot close a WorkItem.

### IC-014 — Protect the verification control plane

**Priority:** P0  
**Type:** Security implementation / repository governance

Identify control-plane paths, including verifier implementations, Gate evaluation, state-transition logic, adapters, permissions, hooks, and CI workflows.

Apply repository ownership/review protections and CI checks where available. Do not rely solely on local file permissions when the agent runs under the same account.

**Acceptance criteria:**

- Control-plane paths are listed and covered by ownership/review policy.
- Changes to these paths receive the required human review.
- CI validates relevant policy and workflow configuration.
- The documented threat model distinguishes local protections from externally enforced controls.
- An agent cannot silently weaken a control and use the modified control to certify the same change.

### IC-015 — Make human approval attributable and snapshot-bound

**Priority:** P0  
**Type:** Workflow/security implementation

Ensure the human completion step records an attributable decision tied to the exact passing Gate and source snapshot.

A command-line flag supplied by an agent must not be treated as proof of human approval unless the execution identity and approval mechanism establish that the decision came from an authorized human.

**Acceptance criteria:**

- Approval records identify approver, decision, timestamp, WorkItem, Gate result, and source snapshot.
- Rejection returns the WorkItem to the appropriate active state.
- Approval cannot be reused after relevant source or policy changes.
- Completion is rejected without a valid current Gate and authorized approval.
- The trust level of local approval is documented; stronger identity enforcement is delegated to repository/CI governance where needed.

### IC-016 — Run adversarial regression suite

**Priority:** P0  
**Type:** Test / verification

Run the IC-002 attack scenarios against the hardened implementation.

**Acceptance criteria:**

- Every previously reproducible bypass is rejected.
- Positive tests demonstrate legitimate sensor execution, Evidence creation, Gate passage, and human closure.
- Test reports are generated by the test runner, not authored by the agent.
- Results identify the exact source revision or snapshot tested.
- Any unresolved bypass blocks Phase 1 completion.

**Phase 1 exit condition:** the harness cannot accept agent-authored sensor success or caller-supplied green flags as authoritative Evidence; Gate freshness and approval binding are tested; remaining trust limitations are explicit.

## 6. Phase 2 — Prove the Mobile reference implementation

### IC-020 — Establish the real iOS verification path

**Priority:** P1  
**Type:** Integration verification

Run the required iOS build and test workflow using the actual project and supported toolchain.

**Acceptance criteria:**

- The workflow identifies the Xcode/toolchain version and target.
- Build and required tests execute through the trusted verification path.
- Exit status and relevant logs are captured as Evidence.
- The Evidence is bound to the exact source snapshot.
- Unavailable platform infrastructure is reported as blocked, never green.

### IC-021 — Establish the real Android verification path

**Priority:** P1  
**Type:** Integration verification

Run the required Android build and test workflow using the actual project and supported toolchain.

**Acceptance criteria:**

- The workflow identifies the JDK, Gradle, Android Gradle Plugin, SDK, and target configuration as applicable.
- Build and required tests execute through the trusted verification path.
- Exit status and relevant logs are captured as Evidence.
- The Evidence is bound to the exact source snapshot.
- Unavailable platform infrastructure is reported as blocked, never green.

### IC-022 — Validate dual-platform Gate and human review

**Priority:** P1  
**Type:** End-to-end verification

Demonstrate the full feature lifecycle using the Mobile profile: WorkItem, Execution, iOS and Android checks, Evidence, Gate, human review, and closure.

**Acceptance criteria:**

- Both platform verifications are required by policy.
- A failure or missing result on either platform prevents Gate passage.
- A source change after either check invalidates the affected result and Gate.
- Human approval is a separate step after Gate passage.
- The complete history can be inspected and traced to its source snapshot.

### IC-023 — Validate with Leafly

**Priority:** P1  
**Type:** Reference implementation

Apply the hardened Mobile workflow to the Leafly reference project, subject to availability of its source and platform toolchains.

**Acceptance criteria:**

- Profile requirements are exercised against a real project.
- Any project-specific assumptions are documented outside the generic Core.
- Build/test limitations are reported accurately.
- Reusable profile requirements are separated from Leafly-specific configuration.

**Phase 2 exit condition:** a real dual-native project can complete the workflow with independently verified platform results and a snapshot-bound human approval.

## 7. Phase 3 — Extract the minimal Engineering Core

Do not begin this phase until Phase 1 exit criteria are satisfied.

### IC-030 — Define executable Core contracts

**Priority:** P2  
**Type:** Design / tests

Translate the Domain Model into executable types, transition rules, and contract tests without selecting unnecessary infrastructure.

**Acceptance criteria:**

- WorkItem, Execution, Verification, Evidence, Gate, and Approval semantics are represented.
- Valid and invalid transitions have tests.
- Domain code has no agent-vendor or mobile-framework dependencies.
- Failure, blocked, stale, inconclusive, and rejected states are explicit.

### IC-031 — Introduce the Workflow Engine

**Priority:** P2  
**Type:** Implementation

Move authoritative state transitions behind Core application operations.

**Acceptance criteria:**

- State changes pass through validated use cases.
- Actor capability, scope, current state, and policy are checked.
- No adapter writes authoritative state through a parallel path.
- Existing CLI entry points delegate to Core operations where practical.

### IC-032 — Define minimal Core ports

**Priority:** P2  
**Type:** Design / implementation

Introduce only the ports needed by demonstrated workflows: repositories, policy provider, source snapshot provider, execution runner, verification provider, actor context, clock, and audit sink.

**Acceptance criteria:**

- Ports are owned by the Core.
- Infrastructure implementations depend inward on port contracts.
- Domain logic does not depend on file formats, shell commands, or Git libraries.
- No port is introduced without a concrete use case and test.

### IC-033 — Move Gate and Evidence semantics into Core

**Priority:** P2  
**Type:** Implementation

Implement snapshot-aware Evidence validation and policy-driven Gate evaluation behind Core interfaces.

**Acceptance criteria:**

- Gate evaluation cannot receive trusted status as an arbitrary caller payload.
- Evidence provenance and freshness are checked centrally.
- Policy versions are explicit.
- Gate outcomes are reproducible from recorded inputs and policy.

### IC-034 — Add Core conformance tests

**Priority:** P2  
**Type:** Test

Build a reusable test suite for state transitions, actor authority, Evidence provenance, snapshot freshness, Gate evaluation, and human approval.

**Acceptance criteria:**

- Positive and negative cases cover every Core invariant.
- Tests can run without Xcode, Android SDK, Flutter, or an agent CLI.
- The suite is reusable by future Engineering Profiles and adapters.

**Phase 3 exit condition:** the current Mobile workflow uses a small, tested Core implementation; adapters and storage can change without rewriting domain rules.

## 8. Phase 4 — Formalize profiles and adapters

### IC-040 — Extract the Mobile Engineering Profile

**Priority:** P3  
**Type:** Profile implementation

Move Mobile-specific build targets, platform checks, architecture rules, and quality requirements into a versioned profile.

**Acceptance criteria:**

- Core contains no iOS/Android-specific acceptance rules.
- The profile declares required checks and their parameters.
- Profile validation rejects missing or malformed requirements.
- The Mobile reference workflow still passes its conformance suite.

### IC-041 — Add Agent Adapter conformance tests

**Priority:** P3  
**Type:** Adapter/test

Test each supported agent adapter against the Agent Contract.

**Acceptance criteria:**

- Each adapter maps operations to the same Core semantics.
- Prohibited state/evidence operations are rejected or externally blocked.
- Enforcement levels are documented accurately.
- Adapter-specific instructions are not counted as technical enforcement.
- Unsupported capabilities are explicit rather than silently emulated.

### IC-042 — Add a Backend Engineering Profile

**Priority:** P3  
**Type:** Generality validation

Add a Java/Spring Boot profile as a second, materially different implementation.

**Acceptance criteria:**

- Backend build, test, and static-analysis checks are profile-defined.
- The same Core workflow and domain contracts are reused.
- No backend-specific concepts are added to the Core without a demonstrated cross-profile need.
- Core conformance tests pass independently of backend toolchains.
- Any abstraction failure is documented and resolved deliberately.

**Phase 4 exit condition:** at least two materially different profiles use the same Core contracts without a Core fork.

## 9. Phase 5 — Reassess deployment

### IC-050 — Review operational requirements

**Priority:** P3  
**Type:** Architecture decision

Evaluate whether real usage justifies isolated remote runners, centralized persistence, multi-project coordination, or a user interface.

**Acceptance criteria:**

- Each proposed infrastructure component addresses a demonstrated constraint.
- Security, operational cost, and maintenance implications are documented.
- A local modular implementation remains viable unless evidence supports a change.
- Any new deployment model preserves the Core domain and trust invariants.

## 10. Dependency order

The critical path is:

\`\`\`mermaid
flowchart TD
    A[IC-001 State-path inventory] --> B[IC-002 Adversarial tests]
    B --> C[IC-010 Trusted sensor execution]
    C --> D[IC-011 Independent Gate evaluation]
    D --> E[IC-012 Snapshot identity]
    E --> F[IC-013 Evidence and Gate binding]
    F --> G[IC-014 Control-plane protection]
    G --> H[IC-015 Human approval binding]
    H --> I[IC-016 Adversarial regression suite]
    I --> J[IC-020/021 Real platform verification]
    J --> K[IC-022/023 Mobile end-to-end]
    K --> L[IC-030/034 Core extraction]
    L --> M[IC-040/041 Profiles and adapters]
    M --> N[IC-042 Backend profile]
    N --> O[IC-050 Deployment reassessment]
\`\`\`

Tasks within a phase may be split into smaller changes, but a downstream task must not be treated as complete while its prerequisite trust condition remains unresolved.

## 11. Definition of done

Every implementation task must include:

- A clear problem statement and bounded scope.
- Relevant acceptance criteria.
- Tests for expected behavior.
- Negative tests for security-sensitive behavior.
- A record of commands actually executed and their outcomes.
- The exact commit or source snapshot tested.
- Documentation updates where contracts or trust assumptions change.
- Human review for control-plane changes.

A task is **not done** merely because:

- An agent reports success.
- A status file says green.
- A command was attempted but its exit status was not captured.
- A Gate was evaluated against stale or unverifiable Evidence.
- A local instruction says an operation is prohibited.
- A document describes a control that is not implemented.

## 12. Current execution rule

Work begins with **IC-001**, followed by **IC-002**. Do not modify verifier or Gate behavior until the existing paths and bypasses have been mapped and captured in regression tests.

After IC-002, implement one P0 task at a time, rerunning the relevant regression suite after each change. Keep changes on \`feat/engineering-core\` and do not merge to the default branch without an explicit review decision.

## 13. Related documents

- [Architecture](architecture.md)
- [Domain Model](domain-model.md)
- [Agent Contract](agent-contract.md)
- [Feature Workflow](../workflow.md)
- [AI Governance](../ai-governance.md)
