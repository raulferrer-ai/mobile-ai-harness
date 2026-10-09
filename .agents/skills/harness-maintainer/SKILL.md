---
name: harness-maintainer
description: Evolve the harness itself: add or prune skills, scripts and contracts, refresh the version baseline, keep budgets and portability. Use when changing anything under the harness files.
---

# Harness Maintainer

## Summary
Keep the harness lean, portable, symlink-free, consistent and self-validating.

## When to use
- Adding or editing skills, scripts, hooks, docs, budgets or CI.
- Refreshing `docs/stack.md` versions or applying a stack change (`docs/customizing.md`).

## Steps
1. Check whether an existing skill, doc or script already covers the need; extend before adding.
2. Skills: valid frontmatter (`name` equals folder), within `BUDGET_SKILL`, tech-light, linking to references; list it in `.agents/skills/README.md`.
3. Contracts stay within their budgets (`harness.env`); move detail to `docs/` or `.agents/references/`.
4. Scripts: POSIX `sh` or Python 3 standard library only; read configuration from `harness.env`.
5. Prefer a mechanical check in `scripts/validate-harness.py` over prose rules; add a test in `scripts/tests/`.
6. Refreshing versions: verify each component against official release pages, update the baseline table and date.
7. Changes to contracts, hooks, scripts or CI need the owners in `.github/CODEOWNERS` (`docs/ai-governance.md`).
8. Run `make validate-harness` and `make test-harness`; append to `progress/log.md`.

## Gotchas
- No symlinks, no duplicated large references across skills (drift).
- Do not weaken a guardrail to make a task pass; propose the change to the human.
- Never copy versions from memory or old tutorials.
