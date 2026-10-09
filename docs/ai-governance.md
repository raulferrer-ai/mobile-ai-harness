# AI governance for development

Rules for using AI coding agents on this project. This is a **template**: your organization's AI, security and legal
policies take precedence; fill in the marked sections with the approved decisions. Owners: `.github/CODEOWNERS`.

## 1. Principles
1. **Humans are accountable.** An agent proposes; a person reviews, approves and owns every change that merges.
2. **Evidence over claims.** Sensors, the gate and review are the proof, never the agent's statement.
3. **Least privilege.** Agents get the minimum tools, paths and data needed for the task.
4. **Transparency.** AI assistance is disclosed and traceable.
5. **The harness is the control system.** Changing contracts, hooks, scripts or CI is a governed decision, not an agent shortcut.

## 2. Approved tools and models <!-- CUSTOMIZE -->
Only tools on this list may be used with this repository. Each entry names the approved plan/tenant (for example an
enterprise agreement with data-retention and no-training terms) and the owner.
| Tool | Approved use | Plan / tenant | Data classes allowed | Owner |
| --- | --- | --- | --- | --- |
| <!-- Claude Code --> | | | | |
| <!-- Codex / Cursor / OpenCode / Gemini --> | | | | |

## 3. Data classification: what may enter a prompt or context
| Class | Examples | Allowed in AI tools |
| --- | --- | --- |
| Public | Open-source code, public docs | Yes |
| Internal | This repository's source, specs, designs | Only with approved tools in 2. |
| Confidential | Unreleased roadmap, customer-identifiable data, credentials, signing material, production logs | **No**, unless explicitly approved and sanitized |
Technical enforcement already present: `.aiexclude`, `.cursorignore`, Claude permission denies and hooks keep secrets and
signing files out of agent reach. They are guardrails, not guarantees; people must not paste restricted data either.

## 4. Review requirements
- Every PR is reviewed by a human code owner; AI-authored changes get the same scrutiny as any other, with extra attention to:
  invented APIs or packages, weakened tests, security-sensitive code, license-encumbered snippets and unrequested scope.
- Changes to `AGENTS.md`, platform contracts, `.agents/`, `scripts/`, tool adapters, `.github/` and `harness.env` require the owners in
  `.github/CODEOWNERS`. Enable branch protection with "Require review from Code Owners".
- Closing a feature is human-only (`docs/workflow.md`).

## 5. Disclosure and traceability
- The PR template includes an **AI assistance** section: tools used, what they did, what the human verified.
- Commits materially produced by an agent carry a trailer, for example `AI-Assisted: <tool>/<model>`, so history can be audited.
- `progress/log.md` records milestones with evidence; `progress/flywheel-log.md` records deviations and the controls added.
- Keep tool-side logs/transcripts according to your organization's retention policy <!-- CUSTOMIZE -->.

## 6. Intellectual property and licensing
- Do not accept large verbatim snippets of unknown origin; ask the agent for the source or rewrite.
- New dependencies follow the supply-chain rules in `docs/security.md` and the company license policy.
- Decide ownership/attribution rules for AI-generated code with legal <!-- CUSTOMIZE -->.

## 7. Agent permissions model
| Capability | Default |
| --- | --- |
| Read/edit source, run `make` and project scripts | Allowed |
| Network access, package installation | Only as needed and permitted by the tool's sandbox/policy |
| Destructive git/file operations | Blocked by hooks and permissions; human approval required |
| Secrets, signing material | Never |
| Closing features, merging, tagging, releasing | Human only |
Prefer your tools' organization-level managed settings (where available) over per-repo files, so policy cannot be
loosened locally; the per-repo adapters then act as defense in depth.

## 8. Incidents
If an agent leaked data, executed something destructive, or introduced a vulnerability: stop the session, contain
(rotate secrets, revert), notify the owners in `SECURITY.md`, then record the lesson (`docs/flywheel.md`) and add a
control (rule, hook, validator check or CI gate).

## 9. Multiple agents and automation
Parallel agents must not share one working tree. Use separate branches/worktrees, one feature per agent, and let the
board (`scripts/feature.py`) arbitrate; do not hand-merge `feature_list.json` conflicts, re-run the CLI instead.
Unattended agents (CI bots, scheduled runs) need their own owner, scoped credentials and the same review rules.

## 10. Review cadence
Review this document, the approved-tools list and the hook/permission rules each quarter and after any incident.
