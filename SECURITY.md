# Security policy

> Template: replace the placeholders and align with your organization's security process.

## Reporting a vulnerability
Do not open a public issue. Report privately to **<security-contact@your-company.example>** (or through your
organization's internal channel), including steps to reproduce, affected versions and impact.
Expected response: acknowledgement within <N> business days. <!-- CUSTOMIZE per company policy -->

## Scope
The mobile apps in `ios/` and `android/`, their build/CI configuration and this harness (scripts, hooks, contracts).

## Supported versions
<!-- CUSTOMIZE: which released versions receive security fixes. -->

## Handling secrets
If a secret was committed, treat it as compromised: **rotate it first**, then remove it from the tree and, if your
policy requires, from history. Details: `docs/security.md`.

## Related documents
- `docs/security.md` - threat model, mobile security checklist, supply chain rules
- `docs/privacy-compliance.md` - privacy and store compliance
- `docs/ai-governance.md` - rules for AI-assisted development
