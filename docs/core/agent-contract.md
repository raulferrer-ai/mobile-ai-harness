# Engineering Core — Agent Contract

## 1. Purpose

This document defines the authority boundaries between an AI agent, the Engineering Core, trusted execution and verification mechanisms, and human decision-makers.

It is a tool-agnostic contract. It does not prescribe a particular agent, model, CLI, IDE, permission syntax, or orchestration framework. Adapters translate the contract into tool-specific configuration; the Core defines the semantics that those adapters and runtime controls must preserve.

The central rule is:

> **An agent may propose and produce work. The system decides what may execute and what counts as verified. An authorized human makes the decisions reserved for human approval.**

This contract complements [the Domain Model](domain-model.md). If an implementation cannot enforce a requirement yet, it must document the limitation rather than imply that an instruction alone provides enforcement.

## 2. Scope and terminology

- **Agent:** an AI-driven process that interprets work and proposes or produces changes. Agent identity is metadata, not a required Core domain entity.
- **Harness / Core runtime:** the trusted workflow mechanisms that validate requests, manage state transitions, invoke authorized operations, and evaluate policy.
- **Execution runner:** a controlled mechanism that runs approved commands or workflows and records their results.
- **Verifier:** an authorized mechanism that executes or independently validates a defined check and produces Evidence.
- **Human approver:** a person authorized to make a decision at a defined approval point.
- **Control plane:** the policies, contracts, adapters, hooks, scripts, verifier definitions, Gate evaluator, approval mechanism, and CI configuration that govern the workflow.
- **Work plane:** the product source, tests, specifications, and other artifacts being produced or changed to fulfil a WorkItem.

An implementation may combine several roles in one program or process. It must still preserve their distinct authority.

## 3. Authority model

Authority is granted by capability and scope, not by an agent's claims, prompt text, or chosen tool.

| Actor | Authority |
| --- | --- |
| Agent | Inspect permitted context; propose plans; create and modify scoped WorkItem artifacts; request authorized operations; report observations |
| Harness / Core runtime | Validate requests; enforce state transitions and policy; create and update authoritative workflow records; invoke approved runners and verifiers; evaluate Gates |
| Execution runner | Execute approved commands within a defined scope; capture process and environment results; report execution outcomes |
| Verifier | Check identified inputs against a defined verification policy; produce authoritative Verification outcomes and Evidence |
| Human approver | Approve or reject designated decisions, including completion and other configured suspend points |
| Repository / CI governance | Enforce protected-branch, review, identity, permission, and release controls outside the agent's own authority |

An agent does not acquire a capability because it can invoke a shell command, edit a file, or persuade another agent to do so. The runtime must validate the actor, requested operation, scope, and applicable policy.

## 4. Capability contract

The following matrix defines the default Core policy. An Engineering Profile may narrow these capabilities. Expanding a capability requires an explicit policy decision and must not weaken the Core invariants.

| Capability | Agent | Harness / authorized mechanism | Human |
| --- | --- | --- | --- |
| Read permitted project context | Allowed | Allowed | Allowed |
| Read restricted or secret material | Denied by default | Only narrowly scoped services when required | According to organizational policy |
| Propose a plan or task breakdown | Allowed | May validate structure | May revise or approve |
| Edit scoped product source and tests | Allowed | May apply generated changes | Allowed |
| Create or revise a WorkItem specification | Propose changes; follow scope | Validate and record | Owns scope and acceptance decisions |
| Start or request an Execution | Request | Authorize and record | May initiate |
| Run approved development commands | Request / permitted scoped execution | Authorize and execute | May execute |
| Create authoritative Verification or Evidence | Not allowed | Authorized verifier only | May request independent verification |
| Evaluate or record a Gate result | Not allowed | Gate evaluator only | May inspect and challenge |
| Change Core policy or trusted control-plane code | Not allowed by default | Only through governed change process | Explicitly authorize and review |
| Approve WorkItem completion | Not allowed | Record a valid human decision | Authorized human only |
| Merge, tag, publish, or release | Not allowed by default | Only when explicitly authorized by release policy | Authorized human / release role |

A human may delegate operational tasks to automation, but delegation must be explicit, scoped, attributable, and represented in the applicable policy. It must not turn an ordinary agent assertion into Evidence or human approval.

## 5. Agent obligations

For every assigned WorkItem, the agent must:

1. Read the applicable project contract, Engineering Profile, WorkItem specification, and relevant policy before changing files.
2. Respect the stated scope, acceptance criteria, platform boundaries, and non-goals.
3. Ask for clarification when requirements conflict, are materially incomplete, or require an unapproved scope change.
4. Prefer the smallest coherent change that satisfies the acceptance criteria.
5. Add or update tests when required by the WorkItem or Engineering Profile; never weaken or remove a test merely to obtain a passing result.
6. Use approved commands and request authorized verification through the defined interface.
7. Report what changed, what was attempted, which checks were requested or observed, and any failures, skipped checks, or limitations.
8. Preserve diagnostic information needed for another Execution or human review.
9. Keep workflow state and evidence truthful; never claim that a check ran when it did not.
10. Stop at configured human suspend points and wait for an explicit decision.

The agent must distinguish clearly between:
- **Implemented:** the requested change has been made.
- **Attempted:** a command or check was invoked.
- **Observed:** output was received.
- **Verified:** an authorized verifier produced a passing result for the identified source snapshot.
- **Approved:** an authorized human recorded the required decision.

These terms are not interchangeable.

## 6. Prohibited agent actions

Unless a specific, separately governed policy explicitly authorizes a narrowly scoped exception, an agent must not:

### 6.1 Forge workflow state or evidence

- Directly edit authoritative WorkItem, Execution, Verification, Evidence, Gate, or Approval records.
- Set a status such as `sensor_green`, `verified`, `passed`, or `completed` by editing a file or invoking an untrusted helper.
- Fabricate, alter, replay, or misrepresent test reports, command output, timestamps, verifier identity, exit codes, snapshot identifiers, or approval records.
- Ask another agent to perform a prohibited state transition on its behalf.
- Reuse Evidence from a different source snapshot or relevant policy version.

### 6.2 Bypass verification or approval

- Bypass required verifications, Gates, reviews, or human suspend points.
- Invoke a privileged verifier in a way that bypasses its input validation or policy.
- Mark a WorkItem complete, approve its own work, or impersonate an approver.
- Merge, tag, publish, or release unless the applicable policy explicitly grants that operation through a controlled mechanism.

### 6.3 Weaken the control plane

- Change Core invariants, policy definitions, verifier implementations, Gate evaluation, approval logic, agent permissions, hooks, adapters, or CI enforcement as an incidental part of a product WorkItem.
- Disable, remove, bypass, or weaken a control to make a check pass.
- Modify protected branch settings or repository governance.
- Change a required check into an optional, skipped, degraded, or weaker check without an authorized policy decision.

Control-plane changes are legitimate engineering work only when explicitly scoped as such, reviewed under the relevant ownership policy, and verified independently.

### 6.4 Violate security or data boundaries

- Read, expose, copy, or transmit secrets, credentials, signing material, private keys, or restricted personal or customer data outside an explicitly authorized workflow.
- Send source code, logs, prompts, artifacts, or other project data to unapproved external services.
- Install dependencies, execute downloaded code, or access external networks outside the permissions and policies of the Execution environment.
- Perform destructive file, repository, infrastructure, or account operations without the required authorization.

## 7. Request and execution protocol

Agents request operations; they do not grant themselves authority.

A conforming request interface should validate, at minimum:

1. **Actor:** which agent or human initiated the request, using the identity available to the runtime.
2. **Work scope:** the WorkItem and permitted paths, resources, or targets.
3. **Operation:** the requested action and its declared purpose.
4. **Policy:** whether the operation is allowed, requires approval, or is denied.
5. **Execution context:** the runner, environment, and limits under which it may run.

For operations that execute commands, the runtime should apply least privilege, bounded execution time, controlled environment variables, and explicit network and filesystem permissions.

A request being accepted means only that the operation was authorized to run. It does not mean that it succeeded or that its result is correct.

The runner must capture the actual process outcome. When the result is used as Evidence, the authorized verifier must bind it to the source snapshot and verification policy defined in the Domain Model.

## 8. Trusted control plane

The following components are part of the control plane and require stronger protection than ordinary product files:

- Core domain contracts and policy definitions.
- State-transition and persistence code.
- Execution authorization and runner configuration.
- Verification and Evidence-generation mechanisms.
- Gate evaluation logic.
- Human approval and identity mechanisms.
- Agent adapters, permissions, hooks, and tool configuration.
- CI workflows, repository rules, branch protection, and release configuration.
- Security-sensitive configuration and secret-handling mechanisms.

Recommended controls include:

- Separate ownership and review requirements for control-plane paths.
- Protected branches and required code-owner review.
- CI checks that validate policy and adapter consistency.
- Restricted credentials and narrowly scoped execution identities.
- Isolated runners for checks that produce authoritative Evidence.
- Signed or otherwise tamper-evident records where the threat model requires them.
- Audit logs for authorization, verification, Gate evaluation, and human approval.
- A policy that prevents an agent-controlled process from rewriting the trusted verifier and then using that modified verifier to certify its own changes.

No single mechanism is sufficient in every deployment. Controls must be selected according to the threat model and the trustworthiness of the execution environment.

## 9. Human approval and suspend points

The following decisions are human-only by default:

- Acceptance or material revision of product scope and acceptance criteria.
- Changes to architecture, stack defaults, or policy where the project requires an ADR or explicit owner decision.
- Completion of a WorkItem after the required Gate has passed.
- Merge to a protected branch.
- Tagging, publishing, deployment, or release.
- Exceptions to security, privacy, licensing, or data-handling policy.
- Any action designated as a human suspend point by the Engineering Profile.

An approval must be explicit and attributable. Silence, a prompt instruction, an agent-generated checkbox, or a passing Gate is not approval.

Approval is bound to the exact Gate result and source snapshot reviewed. If relevant code or policy changes after approval, the implementation must invalidate the affected approval or require renewed review according to policy.

## 10. Failure and escalation behaviour

The agent must stop and request human input when:

- The specification conflicts with a higher-priority policy or another authoritative requirement.
- A requested operation is denied or requires approval.
- A required verifier is unavailable or cannot establish a result.
- Evidence is missing, stale, inconsistent, or cannot be tied to the source snapshot.
- A security, privacy, licensing, or data-handling concern is discovered.
- The requested change requires an unapproved control-plane modification.
- The implementation cannot meet acceptance criteria without materially expanding scope.

The system must fail closed for required controls: unavailable authorization, verifier, Evidence, or Gate evaluation must not be interpreted as success.

Incidents involving data exposure, destructive operations, or control-plane compromise must follow the project's incident process. Preserve relevant logs and execution records; do not conceal or overwrite the failure.

## 11. Adapter conformance

An Agent Adapter translates tool-specific capabilities and events into this contract. It may implement permissions, hooks, command restrictions, context loading, and user confirmations, but it must not redefine Core authority.

Every adapter should document:

- Which capabilities it can enforce directly.
- Which capabilities depend on external tool or organization settings.
- Which operations are only discouraged by instructions.
- Which controls can be bypassed by an agent with shell, filesystem, or network access.
- How human approval is requested and recorded.
- How execution and verification results reach the trusted Core runtime.

An adapter must not claim enforcement that its underlying tool cannot provide. Where an adapter is weaker than the Core policy, the deployment must compensate with external controls or mark the capability as unsupported.

### 11.1 Enforcement levels

Use these terms consistently when describing an adapter:

| Level | Meaning |
| --- | --- |
| **Enforced** | A technical control rejects the prohibited operation within the stated threat model. |
| **Externally enforced** | A repository, CI, identity, sandbox, or organization control enforces the rule outside the adapter. |
| **Guarded** | A hook or permission rule blocks common paths but can be bypassed under stated conditions. |
| **Instructed** | The agent is told not to do something, but no technical control prevents it. |
| **Unsupported** | The adapter cannot implement the required control. |

Instructions and prompt text are not enforcement. Hooks and local permissions should not be described as a security boundary unless their bypass resistance has been demonstrated.

## 12. Mapping to the current Mobile AI Harness

The current repository already expresses parts of this contract through `AGENTS.md`, `scripts/feature.py`, sensors, the Gate command, tool adapters, hooks, and human-only close instructions.

This is a conceptual mapping, not a claim that the current implementation satisfies every requirement.

| Contract requirement | Current harness mechanism | Assessment / gap |
| --- | --- | --- |
| Agent reads project rules | `AGENTS.md`, platform contracts, skills | Instructional; tool-specific loading varies |
| Scoped product changes | Agent tool permissions and repository conventions | Adapter-dependent; not a universal filesystem boundary |
| Board state transitions | `scripts/feature.py` | CLI centralizes transitions, but direct file writes remain a concern |
| Sensor execution | `scripts/sensor.sh` and Make targets | Runs checks; result trust and snapshot binding need hardening |
| Evidence integrity | Sensor records and board metadata | Insufficient until records are created through a trusted path and tied to the exact source snapshot |
| Gate evaluation | `scripts/verify-feature.sh`, `feature.py gate` | Must independently validate authoritative Evidence; must not trust caller-supplied green lists |
| Human-only close | `feature.py done`, adapter permissions, human checklist | Multiple guardrails; requires an independently enforced approval boundary |
| Control-plane ownership | CODEOWNERS, branch protection guidance, CI | Depends on repository settings being enabled and maintained |
| Adapter parity | Claude, Codex, OpenCode, Cursor and other configurations | Must be assessed per adapter; configuration syntax does not guarantee equivalent enforcement |

The current Claude configuration, for example, allows broad `python3 scripts/*` execution. This may be useful operationally, but it must not be treated as proof that privileged script operations are safely restricted. The same principle applies to broad shell permissions in other adapters.

Before the Mobile Profile claims conformance, the implementation must demonstrate that an agent cannot fabricate a passing sensor result, create valid Evidence by editing state files, pass a Gate using stale or caller-supplied statuses, or close a WorkItem without an independently recorded human decision.

## 13. Conformance checklist

An implementation claiming conformance with this contract should be able to demonstrate all of the following:

- [ ] Agent capabilities are scoped and documented.
- [ ] Agent instructions are distinguished from technical enforcement.
- [ ] Product work and control-plane changes have separate authorization paths.
- [ ] Authoritative workflow state cannot be changed through an untrusted direct-write path.
- [ ] Only an authorized verifier can create Gate-eligible Evidence.
- [ ] Evidence is bound to the exact source snapshot and relevant policy version.
- [ ] Gate evaluation independently checks required Evidence and freshness.
- [ ] Missing, skipped, unavailable, or inconclusive required checks fail closed.
- [ ] Human approval is attributable and bound to the reviewed Gate and source snapshot.
- [ ] Agents cannot approve completion or perform protected release operations by default.
- [ ] Adapter enforcement levels and bypass limitations are documented.
- [ ] CI or external governance protects the trusted control plane.
- [ ] Audit records preserve requests, executions, verification results, Gate evaluations, and approvals.

A checklist item is not satisfied by adding an instruction alone. Each item requires evidence of the corresponding technical or organizational control.

## 14. Out of scope

This contract does not define:

- A universal agent identity provider or authentication protocol.
- A specific permission language or sandbox implementation.
- A central orchestration service or multi-agent scheduling algorithm.
- A particular signing, attestation, or cryptographic record format.
- A universal approval UI.

Those mechanisms may be supplied by adapters, Engineering Profiles, or deployment-specific infrastructure. They must preserve the authority boundaries and invariants defined here.
