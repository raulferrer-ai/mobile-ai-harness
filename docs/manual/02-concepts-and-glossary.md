# 02 - Concepts and Glossary

## 1. Central Idea in a Sentence

An **IA agent** writes code; a **harness** wraps it with rules, automatic tests and human decision points so that every change is **verifiable**. People decide what to build and when it is done; the harness makes that decision evidence-based.

## 2. Glossary

| Term | Definition | Where it Lives | Quality Analogy |
| --- | --- | --- | --- |
| Harness | Set of contracts, specifications, checks and human decision points that surround the agent | Entire repository | Quality management system |
| Agent | IA tool that reads the repository, edits files and executes commands (Claude Code, Codex, Cursor, OpenCode, Gemini) | Outside the repo | Worker with work instructions |
| Contract | Rule file that the agent reads on start. There is a root one and one per platform | `AGENTS.md`, `ios/AGENTS.md`, `android/AGENTS.md` | Quality manual |
| Pointer | Short file that redirects another agent toward the contract | `CLAUDE.md`, `GEMINI.md` | Referral to the manual |
| Skill | Brief procedure that the agent loads only when the task requires it | `.agents/skills/<nombre>/SKILL.md` | Standardized work procedure (PNT/SOP) |
| Reference | Technical document with patterns and examples per platform | `.agents/references/` | Technical instruction method |
| Line-budgeted contract | Maximum allowed lines for files that are always loaded | `harness.env` (BUDGET_*) | Manual page limit |
| Spec | Behavior description of a functionality in Gherkin language (Given/When/Then) | `features/*.feature` | Product specification or analytical method |
| Feature | Delivery unit: a functionality with its spec, its state and its evidence | `feature_list.json` | Lot or batch |
| Board | Record of all features and their state. Only modified with a tool | `feature_list.json` | Batch record |
| Feature state | `planned`, `in_progress`, `blocked` or `done` | Board | Batch state |
| Platform state | Per platform: `pending`, `in_progress`, `sensor_green` or `done` | Board | Each production line state |
| Sensor | Automatic check (compile and run tests) of a platform. Its result is written by the script | `scripts/sensor.sh` | Process control (IPC) |
| Loop | Implement, measure with the sensor, correct, until green cycle | (`AGENTS.md`) | In-line measurement adjustment cycle |
| Gate | Automatic final check of a feature: validations, secrets, architecture and sensors of all its platforms | `scripts/verify-feature.sh` | Batch release essay |
| Partial Gate | Gate in which some sensor could not execute. It does not register and does not allow closing | Gate exit code (code 3) | Incomplete batch: non-releasable lot |
| Legacy Gate (legacy) | Mark for features closed with a previous harness; accepted by trust | `feature_list.json` | Historical lot accepted by prior record |
| Work Graph | Diagram of the steps and routes a feature advances through | `docs/workflow.md` | Process flow diagram |
| Human Suspension Point | Step where the agent must stop and a person decides | `docs/workflow.md` | Release/approval point |
| Human Close | Order that marks a feature as done; only executed by a person | `scripts/feature.py done` | Batch release by qualified person |
| Dual Checklist | Human review that iOS and Android behave the same | `docs/dual-checklist.md` | Final inspection |
| Definition of Done (DoD) | Conditions to consider a feature done (dual) | `AGENTS.md` | Batch acceptance criteria |
| Flywheel (flywheel) | Custom of converting every deviation into a rule, scenario or sensor | `docs/flywheel.md` | Corrective and preventive action (CAPA) |
| ADR | Brief record of a technical decision: context, decision, consequences | `docs/decisions/` | Change control |
| Hook | Script that executes before an agent action and can block it | `.agents/hooks/` | Security interlock |
| Guardrail | Barrier that prevents accidents. Not an infallible security frontier | Hooks and permissions | Machine guard |

## 3. The Four Planes of the Harness

To orient oneself, it is convenient to see the harness as four planes that cooperate:

| Plane | Question it Answers | Pieces |
| --- | --- | --- |
| Contract | What rules does the agent follow? | `AGENTS.md`, platform contracts, skills, references |
| Process | What is built and in what order? | Specs, board, work graph, dual checklist |
| Control | How is it checked? | Sensors, gate, audit, secret scanner, validator, hooks, permissions, CI |
| State | Where are we? | `progress/`, `feature_list.json`, records |

## 4. Who Does What (Summary)

| Actor | Does | Does Not Do |
| --- | --- | --- |
| Agent | Plans, implements, writes tests, executes sensors, updates handover notes | Closes features, edits the board by hand, touches secrets, executes destructive commands, decides scope or stack changes |
| Person | Defines specs, reviews, executes dual checklist, closes features, does merge and publishes | Delegates closing to the agent |
| Script | Measures, records results and validates invariants | Interprets or decides |
