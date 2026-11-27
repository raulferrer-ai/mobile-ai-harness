# 01 - Origin and Philosophy

## 1. The Original Idea

Building an app for two platforms is usually solved with one of two strategies: a single codebase that is multiplatform (Flutter, React Native, Kotlin Multiplatform) or two native teams that coordinate manually. Each has a cost. The first cedes control over the native experience and depends on a framework. The second duplicates effort and usually ends up with two products that resemble each other less and less.

The hypothesis that gave rise to mobile-ai-harness was different:

> With AI agents writing code, what is worth **sharing across platforms is product knowledge**, not UI code interface. If the two native implementations start from the same specifications, the same visual language and the same "done" criterion, they can evolve separately without diverging.

For that hypothesis to work, an **harness** (literally "harness") was needed: the set of contracts, specifications, automatic checks and human decision points that surround the agent and make their work verifiable. An agent without a harness produces code that looks correct; an agent with a harness produces code whose correctness can be demonstrated.

## 2. How it was Developed

The harness was not designed in abstraction. It arose from a real project, **Leafly**: a plant care app, native in iOS (SwiftUI) and Android (Jetpack Compose), built as a case study of *harness engineering* applied to dual native development. Leafly is not oriented to the stores; it exists to learn and document. Each version of the harness is the response to observed failures in the previous project.

| Stage | What was Built | What was Learned |
| --- | --- | --- |
| Leafly v1.0 (harness MVP) | Rules in `AGENTS.md`, Gherkin specifications, feature list, progress notes and a "gate" verification script before closing a feature | Saying "done" is not the same as demonstrating it: the agent could consider a platform good without evidence |
| Leafly v2.0 (Loop mode) | The "build, measure, correct" loop: a platform is not considered done until its sensor is green; explicit work graph; fault recording (flywheel) | Rules written in prose are forgotten; those that become automatic checks are fulfilled |
| mobile-ai-harness v1 | Extraction of the generic: binderless contracts, adapters for various IA tools, ten skills | Compared to Leafly, defects appeared: a parity document that was a copy, hooks whose patterns never matched, hand-written project routes, a gate that turned green if the toolchain was missing |
| mobile-ai-harness v2.0 | Reconstruction: state machine board, single configuration (`harness.env`), centralized sensors, modifiable default stack, 14 skills | A "ready to use" template needs explicit default decisions and an orderly way to change them |
| mobile-ai-harness v2.1 | Security and supply chain, AI governance, startup guide, vertical example, architecture auditor | For a large company, missing security controls, IA usage traceability and a way to test the loop in their machine |
| mobile-ai-harness v2.2 | This manual and its automatic completeness check | Documentation also degrades; it's convenient for a script to warn when it becomes incomplete |

### First Real Test of the Template: Migrate Leafly

The v2.1 template was applied to Leafly itself (12 finished features with the previous harness). Without running a single compilation, the architecture auditor found what no test had seen: 25 hardcoded color literals on two Android screens that were bypassing the design system tokens, although those features had passed their sensors and their gate. That illustrates the purpose well: **tests check that the code works; the harness additionally checks that the code complies with project rules**.

### Design Decisions and Why

| Decision | Why |
| --- | --- |
| Text pointers (`CLAUDE.md`, `GEMINI.md`) instead of symbolic links | Symbolic links fail on Windows and some CI; a three-line file works everywhere |
| Line-budgeted contracts | Instructions that are always loaded consume the agent's working memory; extensive content goes to documents and is loaded on demand |
| Skills loaded on demand | The agent reads a procedure only when the task requires it |
| Sensors are executed by a script, not the agent | Who produces the result cannot be the one who certifies the result |
| Closing a feature is a human decision | A responsible person needs to sign off; the agent prepares the evidence |
| The board is a state machine with CLI | Avoids impossible states or gained without evidence |
| A single configuration file (`harness.env`) | Changing project doesn't require editing scripts |
| "Not available" is never "green" | If it couldn't be measured, it can't be asserted to be correct |
| Guards and permissions as guardrails, not as a wall | Honestly warn: an agent with terminal access can cause damage; real defense is review and CI validation |
| Explicit default values and changable with record (ADR) | Any technical decision can change, but never in silence |
| Mechanical audits of written rules | A rule that no one checks is a suggestion |
| Documentation verified by script | Incomplete documentation is a risk equal to a missing test |

## 4. What it Concretely Serves For

For a company that already has **graphic designs** and **product-defined functionalities**, the harness converts those inputs into two native applications via a repeatable process:

1. Functionalities are written as verifiable specifications (Gherkin).
2. Designs are converted into a design system with tokens that both platforms implement.
3. Each functionality is implemented platform by platform, with tests, under sensor control.
4. A person verifies parity and closes the functionality with evidence.
5. At the end there are two verified apps, with full traceability of what was done and who approved it.

## 5. What it Is Not, and What It Does Not Promise

- **It is not an application framework.** It does not provide libraries or UI: it provides process, rules and checks.
- **It does not replace people.** Product, design, QA, security and the person who closes each feature remain indispensable.
- **It does not guarantee that the code is correct.** It guarantees that it is measured, that what is auditable is audited and that there is a record. Quality depends on the specifications and the tests written.
- **It does not automate publishing.** It delivers verified apps; signing, uploading and publishing is a company process (see `docs/manual/08-publication-en-las-stores.md`). That automation is planned for a future version.
- **It does not include backend, crash reporting, analytics or task manager integration** (Jira, Azure DevOps).
- **It is not a multiplatform UI framework.** By design they are two native codebases.

- Its example code did not compile within the template. The vertical slice of `templates/sample-feature/` is verified the first time it runs on the team's machine (step 4 of the guide).

## 6. When it is Convenient and When it Is Not

| Convenient | Not Convenient |
| --- | --- |
| Native iOS + Android apps with small or medium teams using IA agents | Single-codebase multiplatform by business decision |
| The company needs traceability of what changed, how it was verified and who approved | Dishposable prototypes without quality requirements |
| Real parity between platforms is desired | Games or apps with their own graphics engines |
| There is a design system and product specifications | Projects without any prior product definition |
