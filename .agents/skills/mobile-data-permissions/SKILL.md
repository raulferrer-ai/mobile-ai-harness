---
name: mobile-data-permissions
description: Handle local persistence, migrations, media, runtime permissions and scheduled reminders on iOS and Android. Use when touching storage, photos, notifications or other OS capabilities.
---

# Mobile Data and Permissions

## Summary
Reliable local data and OS capabilities with explicit failure and denied states, using the stack in `docs/stack.md`.

## When to use
- Implementing or changing entities, repositories, migrations, media handling, permissions, notifications or background work.

## Steps
1. Model entity <-> domain mapping at the repository boundary; entities never leave the data layer.
2. Plan schema versioning and a migration for every schema change from the first release; test it.
3. Wrap OS capabilities (permissions, notifications, camera/photos, clock) behind interfaces.
4. Handle not-determined, denied and restricted states with a usable fallback and clear copy.
5. Make scheduling deterministic: reschedule/cancel when items change or are deleted, and after device restarts where relevant.
6. Delete associated files and reminders when deleting an item; process and downscale media before storing.
7. Test planners, mappers, repositories and migrations with fast tests (`mobile-testing-harness`).

## Gotchas
- Orphaned reminders and stale media files after delete or edit.
- Assuming a permission is granted, or requesting it out of context.
- Platform specifics (exact alarms, background limits) live in the references; read them before designing.
