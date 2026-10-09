---
name: mobile-security-privacy
description: Apply mobile security and privacy basics: secrets, secure storage, data minimization, logging, permissions and network safety. Use when handling credentials, personal data, networking or logging.
---

# Security and Privacy

## Summary
Keep secrets out of the repo, personal data minimal and out of logs, and sensitive data in secure storage.

## When to use
- Adding networking, authentication, analytics, logging, backups, deep links or any personal data.

## Steps
0. Read `docs/security.md` (MASVS checklist, supply chain) and `docs/privacy-compliance.md` (data inventory) when the change touches data, networking or dependencies.
1. Never commit secrets or signing material; use local config files that are git-ignored and CI secrets.
2. Store tokens and credentials in the Keychain (iOS) / encrypted storage with the Keystore (Android), never in plain preferences.
3. Collect the least data needed; declare purpose in permission strings; request permissions in context.
4. Keep personal data and tokens out of logs, crash reports and analytics.
5. Use TLS only; do not disable certificate validation; validate inputs, including deep-link and intent data.
6. Decide backup behavior for sensitive files (exclude from cloud backup where appropriate).
7. When in doubt about legal/privacy obligations, escalate to the human; do not guess.

## Gotchas
- Debug builds and test fixtures that contain real data or keys.
- Leaving verbose logging enabled in release builds.
- Third-party SDKs: every dependency is an attack and privacy surface; justify and review it.
