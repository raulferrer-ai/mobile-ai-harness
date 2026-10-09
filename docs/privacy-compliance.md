# Privacy and store compliance

> Template and checklist, **not legal advice**. Have legal/privacy owners confirm what applies to your product,
> markets and data. Owners: `.github/CODEOWNERS`.

## 1. Data inventory (maintain from day one)
| Data | Purpose | Where stored | Leaves device? | Retention | Legal basis / consent |
| --- | --- | --- | --- | --- | --- |
| <!-- e.g. photos --> | | | | | |

Rule: if it is not in the inventory, the app does not collect it. Features that add data must update this table in the same PR.

## 2. Apple
- **Privacy manifest** (`PrivacyInfo.xcprivacy`) for the app and for third-party SDKs that require one: declare data
  collected, tracking, and the reasons for any "required reason" APIs you use.
- **App Privacy details** (nutrition labels) in App Store Connect must match the inventory above.
- **Usage description strings** in the app's Info settings for every protected resource you request (camera, photos,
  notifications context, location...), written in plain language and localized.
- Re-check Apple's current submission requirements before each release (SDK requirements change yearly; see the
  baseline in `docs/stack.md`).

## 3. Google Play
- **Data safety** form must match the inventory and the actual behavior of the app and its SDKs.
- Declare permissions minimally; justify sensitive ones; provide an in-app explanation before requesting.
- Keep target API level and other Play policy requirements current; check the Play Console policy center before each release.

## 4. Data protection (GDPR-style principles)
Data minimization, purpose limitation, storage limitation, user access/export/deletion paths, a privacy notice,
processor agreements for every third-party SDK or backend that handles personal data, and a breach procedure.
Features must make deletion real: deleting an item removes its files, reminders and derived data (skill: `mobile-data-permissions`).

## 5. Accessibility as compliance
In many markets accessibility for consumer digital services is a legal requirement (for example the European
Accessibility Act, applicable since June 2025 to many services). Treat `docs/dual-checklist.md` accessibility checks as
evidence and keep an accessibility statement if your legal team requires one.

## 6. Third-party SDKs
Each SDK needs: purpose, data it collects, privacy manifest/Data safety impact, license, owner. No SDK is added without
a note in the PR and an update to the inventory.

## 7. Release checklist (human)
- [ ] Inventory updated; store declarations match it
- [ ] Privacy manifest and usage strings current; permissions minimal
- [ ] SDK list reviewed; licenses approved
- [ ] Deletion and export paths work
- [ ] Accessibility evidence recorded
