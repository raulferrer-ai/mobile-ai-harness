# Contributing

This repository is built with AI coding agents *and* people under one process. Humans and agents follow the same rules.

1. Read `AGENTS.md` and the platform contract for the code you touch.
2. Work from a spec: `features/*.feature` (new behaviour needs a spec first).
3. One feature at a time, one platform per agent session; use `make status`.
4. Verify with the sensors and the gate (`make sensors`, `make gate`); never weaken a test to pass.
5. Open a PR using the template: evidence (not claims), the dual checklist, and the AI-assistance disclosure.
6. Code owners (`.github/CODEOWNERS`) review; changes to contracts, scripts, hooks or CI need the owners named there.
7. Follow `docs/ai-governance.md` for anything involving AI tools, data you may share with them, and attribution.

Security issues: see `SECURITY.md`. Stack or architecture changes: `docs/customizing.md` (ADR required).
