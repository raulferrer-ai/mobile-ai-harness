# Security

How this project handles security. Owners: see `.github/CODEOWNERS`. Reporting: `SECURITY.md`.
Skill for day-to-day work: `mobile-security-privacy`. This document is a **template**: complete the marked sections
and align it with your organization's policies, which take precedence.

## 1. Baseline: OWASP MASVS
Use the OWASP Mobile Application Security Verification Standard (MASVS) as the checklist vocabulary. Per release,
confirm each group applies and note the evidence (test, config, review):
| MASVS group | What to confirm |
| --- | --- |
| STORAGE | Sensitive data only in Keychain / Keystore-backed storage; excluded from backups where required; no secrets in logs |
| CRYPTO | Platform crypto APIs only; no custom algorithms; no hardcoded keys |
| AUTH | Tokens short-lived and refreshable; biometric/passcode gates where the data warrants it; secure sign-out |
| NETWORK | TLS only; no disabled certificate validation; pinning only if the threat model justifies it |
| PLATFORM | Minimal permissions; validated deep links/intents; exported components reviewed; no sensitive data on the clipboard or in screenshots/app switcher where relevant |
| CODE | Dependencies reviewed and pinned; debug code, logging and test endpoints removed from release; input validation |
| RESILIENCE | Decide deliberately whether root/jailbreak detection or obfuscation is required (usually a risk-based decision, not default) |
| PRIVACY | Data minimization, purpose limitation, user control; see `docs/privacy-compliance.md` |

## 2. Threat model (fill in per project)
Keep it to one page and update it when scope changes.
- **Assets:** <!-- what is worth protecting: user data, credentials, content, reputation -->
- **Actors:** <!-- curious user, malicious app on the device, network attacker, lost/stolen device, insider -->
- **Entry points:** <!-- UI input, deep links, files/media import, network APIs, notifications, backups -->
- **Trust boundaries:** <!-- device <-> backend, app <-> OS services, app <-> third-party SDKs -->
- **Top threats and mitigations:** <!-- table: threat | impact | mitigation | residual risk | owner -->
- **Out of scope / accepted risks:** <!-- with owner and date of acceptance -->

## 3. Secrets and signing
- Secrets never live in the repo. Local values in git-ignored files; CI values in the CI secret store.
- Signing keys, certificates and provisioning profiles live in the organization's secret manager or a managed signing service.
- `make scan-secrets` (also in CI and the gate) blocks known secret patterns and forbidden file types. It complements
  your organization's secret scanning and push protection; enable those too.
- A committed secret is **compromised**: rotate first, then clean up.

## 4. Supply chain
- **Pin and review.** Every dependency has a reason in the PR. Commit lock/resolution data:
  `Package.resolved` for SwiftPM; Gradle dependency locking or dependency verification for Gradle.
- **Automate updates** with Dependabot (`.github/dependabot.yml`) and review them like any other change.
- **Review dependencies in PRs** (dependency review in CI) and check licenses against your company policy.
- **SBOM:** produce a software bill of materials for each release if your organization or customers require it
  (choose the generator that matches your build tooling and record it in an ADR).
- **CI hygiene:** least-privilege workflow permissions (already `contents: read`), pin third-party actions to a
  commit SHA if your policy requires it, no secrets exposed to pull requests from forks.
- **AI-suggested dependencies** are treated like any other new dependency: verify the package exists, is maintained
  and is the one intended (typosquatting and hallucinated package names are real risks).

## 5. Release security gate (human)
Before each store submission: MASVS checklist reviewed, `make validate-harness` green, no debug flags, dependency and
license review done, privacy declarations current, release notes free of sensitive detail.

## 6. Incident basics
Contact path in `SECURITY.md`. For a leaked secret or a vulnerability: contain (rotate/disable), assess impact, fix,
release, record a post-mortem as an entry in `progress/flywheel-log.md` and, when it generalizes, a new rule or sensor.
