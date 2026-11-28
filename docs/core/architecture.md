# Engineering Core — Architecture

## 1. Purpose

This document defines the logical architecture, responsibilities, boundaries, interfaces, dependency direction, and initial implementation strategy of the Engineering Core.

The Core is a tool-agnostic engineering control system for agent-assisted software development. It coordinates work, validates workflow transitions, invokes trusted verification, records Evidence, evaluates policy, and preserves human accountability.

The first reference implementation targets dual-native iOS and Android development. Mobile is an Engineering Profile and reference implementation, not a dependency of the Core.

This is a logical architecture, not a mandate to introduce a distributed system, service, database, or user interface.

## 2. Architectural goals

The architecture must:

1. Keep domain concepts and workflow rules independent of programming languages, platforms, frameworks, and agent vendors.
2. Make authoritative state transitions explicit and validated.
3. Separate agent-produced work from trusted verification and Gate evaluation.
4. Bind verification and approval to an exact source snapshot and relevant policy version.
5. Support multiple Agent Adapters without allowing adapters to redefine Core semantics.
6. Support Engineering Profiles that supply stack-specific checks and policies.
7. Preserve an auditable history of Executions, Verifications, Evidence, Gate evaluations, and Approvals.
8. Start with a repository-local implementation that can evolve without premature infrastructure.
9. Make trust assumptions and enforcement limitations visible rather than hiding them behind prompts or configuration.

## 3. Architectural principles

### 3.1 Policy and domain before tools

Core domain types and use cases must not import or depend on Codex, Claude Code, Cursor, OpenCode, Xcode, Gradle, Flutter, Spring, or other vendor/platform SDKs.

Tool-specific behavior belongs in adapters. Stack-specific checks belong in Engineering Profiles.

### 3.2 One authoritative path for state changes

Agents and adapters must not write authoritative workflow state directly. State transitions go through Core operations that validate current state, actor authority, scope, and policy.

The persistence mechanism is not itself the authority boundary. File permissions, process isolation, trusted execution, and repository/CI controls determine who can alter authoritative records.

### 3.3 Separate work from control

The architecture distinguishes:

- **Work plane:** product source, tests, specifications, and outputs being changed to fulfil a WorkItem.
- **Control plane:** Core contracts, policy, transition logic, trusted runners, verifiers, Gate evaluation, approval recording, and enforcement configuration.

An ordinary product WorkItem must not silently grant authority to modify the control plane.

### 3.4 Verification is a trusted operation

An Agent Adapter may request a check, but the Verification subsystem determines whether it is authorized, executes or independently validates it, captures the actual outcome, and binds Evidence to the source snapshot.

A prompt, hook, local status flag, or agent-authored report is not sufficient to establish trusted verification.

### 3.5 Explicit ports, replaceable adapters

The Core defines the interfaces it needs. Infrastructure and tool integrations implement those interfaces. Adapters may be replaced without changing domain rules.

### 3.6 Fail closed for required controls

If authorization, required Evidence, source identity, policy, or a verifier is unavailable or cannot be trusted, the relevant operation must not succeed by default.

## 4. Logical architecture

The Core is organized into six logical areas:

1. Domain Model
2. Application / Workflow Engine
3. Policy and Gate Evaluation
4. Verification and Evidence
5. Ports and Adapters
6. Persistence and Audit

Engineering Profiles and Agent Adapters integrate at defined boundaries. They are not additional domain authorities.

\`\`\`mermaid
flowchart TB
    Agent[AI Agent] --> AA[Agent Adapter]
    Human[Human] --> HA[Approval Interface]
    AA --> APP[Application / Workflow Engine]
    HA --> APP
    APP --> DOMAIN[Domain Model]
    APP --> POLICY[Policy & Gate Evaluation]
    APP --> VERIFY[Verification & Evidence]
    POLICY --> PORTS[Core Ports]
    VERIFY --> PORTS
    APP --> PORTS
    PORTS --> STORE[Persistence & Audit Adapter]
    PORTS --> RUNNER[Trusted Execution Runner]
    PORTS --> PROFILE[Engineering Profile Adapter]
    PORTS --> SCM[Source Snapshot Adapter]
    PROFILE --> CHECKS[Profile-defined Checks]
    RUNNER --> CHECKS
\`\`\`

The diagram is logical. A first implementation may package these areas in one repository and one process, but must preserve their contracts and trust distinctions.

## 5. Component responsibilities

### 5.1 Domain Model

Owns the technology-independent concepts and invariants defined in [domain-model.md](domain-model.md):

- WorkItem
- Execution
- Artifact
- Verification
- Evidence
- Gate
- Approval

Responsibilities:

- Define valid states and transitions.
- Define relationships and identity requirements.
- Enforce domain invariants that do not require external infrastructure.
- Represent outcomes explicitly, including failed, blocked, stale, inconclusive, and rejected states.

The Domain Model must not execute shell commands, read Git repositories, load agent configuration, or depend on a storage format.

### 5.2 Application / Workflow Engine

Coordinates use cases and is the authoritative entry point for state-changing operations.

Initial use cases include:

- Create or register a WorkItem.
- Validate and start an Execution.
- Record permitted progress and execution lifecycle events.
- Request a Verification.
- Record a trusted Verification result.
- Request and perform Gate evaluation.
- Submit a WorkItem for human approval.
- Record an authorized Approval decision.
- Complete or block a WorkItem.
- Invalidate affected Gate and Approval results when relevant inputs change.

The Workflow Engine validates actor, capability, scope, current state, and policy; coordinates domain objects and ports; rejects invalid transitions; and appends attributable records.

It does not treat an agent request as proof that an operation succeeded. It also does not implement tool-specific permissions itself: the execution environment and adapters provide authenticated actor context and enforce the boundaries available to them.

### 5.3 Policy and Gate Evaluation

Owns policy interpretation and Gate decisions.

Responsibilities:

- Load the applicable, versioned policy.
- Determine required Verification conditions for a WorkItem and Engineering Profile.
- Retrieve authoritative Evidence through a port.
- Check Evidence integrity, provenance, source-snapshot identity, and freshness.
- Evaluate every required condition.
- Produce a Gate result with per-condition outcomes and references to the Evidence considered.
- Mark or treat prior results as stale when relevant source or policy inputs change.

The evaluator must not accept a caller-supplied list of green statuses as authoritative input. It obtains Evidence from the trusted Evidence store or verifier interface.

Policy definitions may be expressed in configuration, but policy parsing and evaluation semantics belong to the Core. A profile may add requirements; it may not weaken mandatory Core invariants.

### 5.4 Verification and Evidence

Coordinates trusted checks and creates authoritative Verification and Evidence records.

Responsibilities:

- Accept Verification requests from authorized use cases.
- Resolve the applicable check definition from policy and profile.
- Establish the source snapshot to be checked.
- Invoke an authorized runner or independent verifier.
- Capture the real process outcome and relevant metadata.
- Persist immutable Evidence through the trusted persistence path.
- Return a Verification result to the Workflow Engine.

A verifier must not rely on an agent-authored result file as proof that a command ran. It must either execute the check itself in a controlled context or independently validate a trustworthy attestation from an authorized execution system.

If the verifier cannot establish the input snapshot or integrity of the execution, it must return a non-passing outcome.

### 5.5 Ports and Adapters

Ports are interfaces owned by the Core. Adapters provide concrete integrations.

The initial port set should remain small:

| Port | Responsibility |
| --- | --- |
| WorkItemRepository | Load and persist WorkItem state through validated Core operations |
| ExecutionRepository | Append and retrieve Execution records |
| EvidenceRepository | Store and retrieve authoritative, append-only Evidence |
| GateRepository | Store and retrieve Gate evaluation history |
| ApprovalRepository | Store and retrieve attributable human decisions |
| PolicyProvider | Load versioned Core and profile policies |
| SourceSnapshotProvider | Identify the exact source tree or immutable revision |
| ExecutionRunner | Execute an authorized, bounded command and capture process results |
| VerificationProvider | Resolve and run or independently validate a defined check |
| ActorContextProvider | Supply authenticated actor and capability context |
| Clock | Provide timestamps for deterministic testing and consistent records |
| AuditSink | Append security- and workflow-relevant events |

These are conceptual boundaries, not a requirement to create one class or file per port. Combine ports where it simplifies the first implementation without merging trust responsibilities.

Adapters include:

- Agent Adapters: Codex, Claude Code, Cursor, OpenCode, and others.
- Source-control adapters: initially Git.
- Execution adapters: local runner and, later, isolated CI runner.
- Persistence adapters: initially repository-local files.
- Profile adapters: Mobile first; backend or web later.
- Human approval adapter: initially an explicit CLI or repository review action.

An adapter translates external behavior. It must not own domain policy or bypass the Workflow Engine.

### 5.6 Persistence and Audit

The first implementation may use repository-local files.

Persistence must preserve:

- Stable identifiers and explicit relationships.
- Validated state transitions.
- Append-only Execution and Verification history.
- Immutable Evidence records.
- Versioned policy references.
- Source-snapshot binding.
- Gate evaluation history.
- Human Approval identity, scope, and decision.
- Attributable audit events.

Separate mutable work artifacts from authoritative records. The fact that a record is stored in Git does not make it trustworthy: an agent able to edit both the record and verifier can fabricate a consistent-looking history.

For the initial local implementation, document trust assumptions and protect control-plane paths. For stronger assurance, move authoritative verification and record creation to an isolated runner or CI identity that the agent cannot modify or impersonate.

## 6. Engineering Profiles

An Engineering Profile supplies technology- and project-specific engineering requirements to the generic Core.

A profile may define:

- Supported platforms and build targets.
- Architecture and coding conventions.
- Required test suites and verification commands.
- Static analysis and lint rules.
- Build matrix and supported toolchain versions.
- Acceptance checks and quality thresholds.
- Required artifacts and release constraints.
- Profile-specific human suspend points.

A profile must not redefine:

- Core entity semantics.
- Evidence immutability and provenance.
- Source-snapshot binding.
- Gate evaluation integrity.
- Human approval requirements.
- Core state-transition invariants.

The first profile is **Mobile**, covering the dual-native iOS and Android workflow. Flutter may be included as a project technology where relevant, but it is not a Core dependency.

A later Backend profile should use the same Core contracts while defining Java/Spring Boot-specific builds, tests, and quality checks. This second profile is an important test of whether the Core is genuinely technology-agnostic.

## 7. Agent Adapters

Agent Adapters expose the Core workflow to individual coding tools.

Their responsibilities are limited to:

- Loading relevant project and task context.
- Translating tool actions into Core requests.
- Applying tool-specific permission configuration.
- Communicating authorization failures and required human decisions.
- Returning Core outcomes to the agent.
- Preserving tool/session metadata where required.

Adapters must not:

- Implement their own competing WorkItem state machine.
- Create authoritative Evidence.
- Set Gate outcomes.
- Impersonate human approval.
- Expand capabilities beyond the active policy.
- Claim technical enforcement where the tool only supports instructions.

Adapters should publish an enforcement assessment using the levels defined in [agent-contract.md](agent-contract.md): Enforced, Externally enforced, Guarded, Instructed, or Unsupported.

## 8. Key workflows

### 8.1 Work execution and verification

\`\`\`mermaid
sequenceDiagram
    participant A as Agent
    participant D as Agent Adapter
    participant W as Workflow Engine
    participant R as Trusted Runner / Verifier
    participant E as Evidence Store
    participant G as Gate Evaluator
    A->>D: Request work operation
    D->>W: Authorized Core request
    W->>W: Validate state, scope, capability
    W-->>D: Execution created / operation accepted
    A->>A: Implement scoped changes
    A->>D: Request Verification
    D->>W: Verification request
    W->>R: Dispatch authorized check
    R->>R: Establish snapshot and execute check
    R->>E: Persist authoritative Evidence
    E-->>W: Evidence reference and outcome
    W-->>D: Verification result
    A->>D: Request Gate evaluation
    D->>W: Gate request
    W->>G: Evaluate current Evidence and policy
    G-->>W: Gate result
    W-->>D: Gate outcome
    D-->>A: Report result
\`\`\`

The agent's implementation session is not the trusted verifier. The runner must inspect or execute against the exact source snapshot being evaluated.

### 8.2 Human approval and completion

\`\`\`mermaid
sequenceDiagram
    participant A as Agent
    participant W as Workflow Engine
    participant G as Gate Evaluator
    participant H as Human
    participant P as Approval Provider
    A->>W: Request review
    W->>G: Confirm current passing Gate
    G-->>W: Gate result and source snapshot
    W->>H: Present changes, Evidence, and Gate
    H->>P: Approve or reject
    P->>W: Attributable decision bound to Gate and snapshot
    W->>W: Validate decision and current state
    alt Approved and still current
        W->>W: Complete WorkItem
    else Rejected or stale
        W->>W: Return to in_progress or require reevaluation
    end
\`\`\`

Merge, release, and deployment remain separate delivery workflows governed by project policy.

## 9. Dependency rules

Dependencies point inward:

\`\`\`mermaid
flowchart LR
    PROFILE[Engineering Profiles] --> APP[Application]
    ADAPTERS[External Adapters] --> PORTS[Core Ports]
    INFRA[Infrastructure Adapters] --> PORTS
    APP --> DOMAIN[Domain Model]
    APP --> PORTS
    POLICY[Policy Evaluation] --> DOMAIN
    VERIFY[Verification] --> DOMAIN
\`\`\`

Normative rules:

1. Domain Model depends on no adapter, infrastructure, profile, or agent SDK.
2. Application use cases depend on Domain Model and Core-owned ports.
3. Policy and Gate evaluation depend on domain concepts and policy interfaces, not on agent-specific status files.
4. Verification depends on Core contracts and ports; concrete command execution is supplied by a runner adapter.
5. Agent Adapters depend on Core request interfaces, never the reverse.
6. Engineering Profiles provide policy and check definitions through declared extension points; they do not fork Core behavior.
7. Persistence adapters implement repository ports; domain and application layers do not depend on file formats or storage vendors.
8. No adapter may bypass authorization or write authoritative records through a parallel path.

## 10. Initial deployment topology

The first implementation should be a **modular, repository-local application**.

It may consist of a small Core package or set of modules, a CLI entry point, repository-local configuration and profile definitions, file-based state and append-only records, a local execution adapter, and CI integration for checks requiring a more trusted environment.

Do not introduce a central service, database, GUI, message broker, or distributed agent orchestrator at this stage.

This is a deployment choice, not a permanent architectural constraint. Ports should allow later replacement of local persistence and execution with a service or isolated CI runner without changing domain semantics.

### 10.1 Trust limitation of local execution

A local CLI running under the same user account and filesystem permissions as an agent cannot, by itself, guarantee that the agent is unable to modify its scripts, state files, or outputs.

Therefore:

- Local hooks and command restrictions are defense in depth, not a strong security boundary.
- Control-plane files require protected ownership and review.
- Authoritative checks should progressively move to CI or another isolated runner when the threat model requires it.
- A local Evidence record must clearly state its trust level and execution provenance.
- The system must not claim stronger guarantees than its runtime can demonstrate.

## 11. Initial module layout

The following is a proposed logical layout, not a requirement to create every directory immediately:

\`\`\`text
core/
  domain/
    work_item
    execution
    artifact
    verification
    evidence
    gate
    approval
  application/
    commands
    queries
    workflow
  policy/
    policy_model
    gate_evaluator
  verification/
    verification_service
    evidence_validation
  ports/
    repositories
    execution
    source_snapshot
    identity
    audit
  adapters/
    persistence/
    source_control/
    execution/
    agents/
      codex/
      claude/
      cursor/
      opencode/
  profiles/
    mobile/
      profile
      checks
      policies
    backend/
      profile
      checks
      policies
  cli/
  tests/
    conformance/
\`\`\`

The existing repository structure need not be reshaped all at once. Extract responsibilities from current scripts only when a clear boundary and a testable contract exist.

## 12. Incremental implementation roadmap

### Phase 0 — Contract baseline

- Keep the Domain Model and Agent Contract as normative references.
- Define this architecture and record unresolved decisions.
- Identify current scripts and files by responsibility.
- Document existing enforcement and trust limitations.

**Exit condition:** every existing workflow responsibility has an identified target component; no code has been moved speculatively.

### Phase 1 — Harden the current Mobile implementation

- Prevent agents from directly manufacturing authoritative sensor status.
- Make the Gate independently inspect actual verifier results.
- Bind every result to an exact commit or deterministic working-tree snapshot.
- Ensure relevant source changes invalidate prior Gate results.
- Protect control-plane paths and test prohibited operations.
- Demonstrate real iOS and Android builds/tests in the reference project where toolchains permit.

**Exit condition:** negative conformance tests show that known self-certification and stale-evidence paths are rejected. Runtime validation is reported separately from static review.

### Phase 2 — Extract the minimal Core

- Introduce Core domain types and validated transition operations.
- Define the first Core ports.
- Move WorkItem and Execution lifecycle logic behind the Workflow Engine.
- Preserve current CLI behavior through a compatibility adapter where practical.
- Add conformance tests for state transitions and authorization.

**Exit condition:** the current Mobile workflow uses Core operations rather than independently mutating authoritative state.

### Phase 3 — Formalize Mobile Profile

- Move platform checks and acceptance requirements into the Mobile Profile.
- Define the iOS/Android verification matrix.
- Verify the profile against the Leafly reference project.
- Document which controls are enforced locally and which rely on CI or human governance.

**Exit condition:** Mobile-specific requirements are profile configuration, not hidden assumptions in Core domain logic.

### Phase 4 — Validate generality with Backend

- Add a Java/Spring Boot Backend Profile.
- Reuse the same WorkItem, Execution, Evidence, Gate, and Approval contracts.
- Add backend build, test, and static-analysis checks without adding backend concepts to the Core.
- Record any abstraction that fails and justify changes to the Core.

**Exit condition:** the same Core workflow supports a materially different technology stack without a Core fork.

### Phase 5 — Reassess deployment and extension needs

Only after the local modular implementation has been validated, assess whether remote execution, centralized persistence, multi-project coordination, or a UI is justified by concrete requirements.

**Exit condition:** each infrastructure addition has a demonstrated use case and a documented architectural decision.

## 13. Architectural decisions and deferred questions

The following decisions are established for the initial implementation:

| Decision | Initial choice | Rationale |
| --- | --- | --- |
| Core scope | Tool- and technology-agnostic | Prevents Mobile assumptions from becoming domain rules |
| First profile | Dual-native Mobile | Provides the initial reference implementation |
| Deployment | Repository-local modular application | Lowest operational complexity while contracts mature |
| Persistence | File-based initially | Reuses repository workflow; trust limitations are explicit |
| Execution | Local runner initially, isolated CI where required | Supports incremental hardening |
| Agent integration | Replaceable adapters | Avoids vendor coupling |
| Central service / database / GUI | Deferred | No demonstrated need at this stage |

Questions to resolve through implementation evidence or ADRs:

- What exact snapshot algorithm covers tracked, untracked, ignored, generated, and submodule content?
- Which Evidence fields must be cryptographically signed, and by which identity?
- Which checks can safely run locally, and which require isolated CI?
- How will human identity and approval be authenticated in a repository-local workflow?
- What is the smallest stable machine-readable profile and policy schema?
- How should concurrent Executions and worktrees be represented without state conflicts?
- Which compatibility period is required for the existing CLI and adapters?

Do not prematurely standardize these details before testing the first implementation.

## 14. Architecture conformance criteria

The implementation conforms to this architecture only to the extent that it demonstrates:

- Core domain and application logic have no dependency on agent vendors or project technology stacks.
- All authoritative state transitions pass through validated Core operations.
- Agent Adapters cannot create authoritative Verification, Evidence, Gate, or Approval outcomes.
- Verification and Evidence are tied to the exact source snapshot and applicable policy.
- Gate evaluation independently validates Evidence and freshness.
- Human Approval is attributable and bound to the reviewed Gate and snapshot.
- Engineering Profiles add stack-specific requirements without changing Core invariants.
- Persistence and execution mechanisms can be replaced through Core-owned interfaces.
- Trust assumptions and adapter enforcement levels are documented.
- Negative conformance tests reject prohibited operations.

Documentation alone does not establish architectural conformance. Each criterion requires implementation evidence and tests appropriate to the stated threat model.

## 15. Related documents

- [Domain Model](domain-model.md)
- [Agent Contract](agent-contract.md)
- [AI Governance](../ai-governance.md)
- [Feature Workflow](../workflow.md)
