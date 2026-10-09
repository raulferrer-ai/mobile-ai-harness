---
name: git-governance
description: Keep commits, branches and the working tree clean, scoped and verified, with no IDE artifacts or secrets. Use when preparing commits, branches or snapshots.
---

# Git Governance

## Summary
Every commit contains only intentional, verified files and tells a clear story.

## When to use
- Creating commits, branches, PR descriptions or release snapshots.
- Cleaning local editor or build artifacts.

## Steps
1. `git status` and `git diff`: review every modified and untracked file.
2. Run `make clean-ide` if OS/IDE artifacts appear; confirm `.gitignore` covers them.
3. Run `make validate-harness`; run the relevant sensor(s) for code changes.
4. Commit in small, scoped units with imperative messages that name the feature id when relevant.
5. Add an `AI-Assisted: <tool>/<model>` trailer to commits an agent materially produced (`docs/ai-governance.md`).
6. Fill the PR template (`.github/pull_request_template.md`) with evidence, not claims.

## Gotchas
- Never commit `.env*`, signing material, `google-services.json`, `xcuserdata/`, `.idea/` or build output.
- Never use `--no-verify`, force-push or hard resets without explicit human approval.
- Merge, tag and release are human decisions.
