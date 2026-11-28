# 08 - Publication on the Stores

This chapter continues where the step-by-step guide ends [07](07-guia-paso-a-paso.md): you have a **verified candidate version** of the two apps and want to publish them in App Store and Google Play.

## 0. Scope and Warnings

- **The harness delivers verified code, not automated publishing.** Signing, uploading and publishing is a process of your company. Release automation (CI signing, automatic upload, environments) is not part of this version.
- The policies and assistants of Apple and Google **change frequently**. Everything marked as **[Verificar]** depends on norms you must contrast with the official documentation valid on the day of publication.
- Official reference documentation: *App Store Connect Help* and *App Review Guidelines* (https://developer.apple.com/app-store/review/guidelines/), *Google Play Console Help* (https://support.google.com/googleplay/android-developer) and *Sign your app* (https://developer.android.com/studio/publish/app-signing).
- Publication secrets (store signing keys, passwords, store API keys) **must never go to the repo**. `make scan-secrets` and the hooks exist to avoid it, but custody is your organization's responsibility.

## 1. Common Preparation for Both Platforms

| Element | What to decide or prepare | Responsible |
| --- | --- | --- |
| Version policy | Visible version number (e.g. `1.0.0`) and increasing internal build number. Keep the same visible version on both platforms | Release |
| Branch and tag | Release branch and git tag over the candidate version (human decision) | Technical responsible |
| Release notes | Text for users, by language | Product |
| Privacy policy | Public URL, coherent with `docs/privacy-compliance.md` | Legal and privacy |
| Support contact | URL or email that will appear in the fiches | Product |
| Legal identity | Company data for developer accounts | Legal |
| Fiche resources | Icon, screens by required screen size, texts, category | Design and Product |
| Retirement plan | What to do if a serious failure appears after publication | Release and technical responsible |
| Data inventory | Must coincide with both stores' privacy declarations | Privacy |

## 2. iOS: App Store

### 2.1 Accounts and Registrations

1. **Apple Developer Program** as organization (requires legal entity identification) and access to **App Store Connect**.
2. Assign roles in App Store Connect according to the principle of least privilege.
3. Register the **Bundle Identifier** and the capabilities the app needs (notifications, etc.).
4. **Signing:** the simplest is automatic Xcode signing with the company team. For CI, use an App Store Connect API key stored in the company's secret manager, never in the repo.

### 2.2 Project Settings

- **Version and build:** the marketing version and the build number are adjusted in the Xcode project; the build number must increase with each upload.
- **Visible name, app icon and launch screen** according to current Apple guidelines.
- **Usage texts** of each permission the app requests (camera, photos, notifications, location...), clear and localized.
- **App Privacy manifest** of the app and of third-party SDKs that require it.
- **Compliance with export (encryption):** respond with the legal team if the app uses encryption; it can be declared in the project configuration so the question doesn't repeat on each upload.
- **Required SDK:** Apple publishes each year a date from which uploads must compile with the current SDK. The baseline of `docs/stack.md` indicates the one that was verified. **[Verificar]** the current date.

### 2.3 Generate and Upload the Build

1. In Xcode, select the scheme and "Any iOS Device" destination and use **Product > Archive** (Release configuration).
2. In the **Organizer**, run **Validate App** and correct the warnings.
3. **Distribute App** towards App Store Connect. Alternative via command line: `xcodebuild archive` and then `xcodebuild -exportArchive` with an export options file; consult `xcodebuild` help and Apple's documentation for the current options.
4. Wait for App Store Connect to process the build.

### 2.4 TestFlight

- **Internal tests:** team members, available as soon as processing ends.
- **External tests:** require a prior beta review (Beta App Review) and test information.
- Collect feedback and failures; each correction goes through the normal harness process (correction feature, sensors, gate, human close) and generates a new build.

### 2.5 App Store Connect Fiche

Create the app record (name, primary language, Bundle ID, SKU) and complete: description, keywords, support URL and privacy policy, required-size screenshots, category, **age classification**, price and availability, **App Privacy** (must coincide with `docs/privacy-compliance.md`) and **information for the reviewer** (contact, **demo account if there is login**, and notes about hard-to-test functions.

### 2.6 Submit for Review and Publication

1. Associate the build to the version and submit for review.
2. Common reasons for rejection: unexpected failures or closures, metadata that does not match real behavior, missing demo account, inconsistent privacy declarations, unclear permission texts, incomplete functions. Respond from the App Store Connect resolution center.
3. Choose the launch mode: manual, automatic or **staggered** (recommended for the first version).

## 3. Android: Google Play

### 3.1 Accounts and Registrations

1. **Google Play Console** as organization account (with company verification). **[Verificar]** additional Google tests that may be imposed according to the account type before allowing production publication.
2. Create the app (name, language, type, free or paid, declaration). The **package name is definitive**.

### 3.2 Signing

1. Use **Play App Signing**: Google custodies the final signing key and you sign the uploads with an **upload key**.
2. Generate the upload key (a *keystore*) on a secure team device and save it, along with its passwords, in the company's secret manager, with backup and responsible persons defined.
3. Configure the release signature reading data from a local file ignored by git (`keystore.properties`) or from CI variables. **Never** write it in `build.gradle.kts`.
4. If the upload key is lost there is a Google recovery procedure, but it delays publication.

### 3.3 Project Settings

- **versionCode** (integer increasing with each upload) and **versionName** (visible version).
- **Code and resource reduction (R8)** activated in release; thoroughly test the release version because reduction can break code that uses reflection. Keep necessary preservation rules.
- **Permissions** minimum and justified in the manifesto.
- **Target SDK level:** Google requires a minimum that increases each year. **[Verificar]** the current requirement.

### 3.4 Generate the Build

From the Android project folder (the same way the harness invokes Gradle):

```bash
cd android
sh ./gradlew :app:bundleRelease        # generates the AAB to upload to Play
sh ./gradlew :app:assembleRelease      # optional: APK for manual tests
```

The AAB remains in `app/build/outputs/bundle/release/`. Test the signed release version on real devices before uploading. Adjust the module name if yours is not `app`.

### 3.5 Test and Production Tracks

1. Upload the AAB first to **Internal tests** and review the **pre-launch report** that Play generates.
2. Advance to **Closed tests** and, if applicable, **Open tests**.
3. Complete the **app content declarations**: data security (must coincide with `docs/privacy-compliance.md`), content classification, target audience, ads and those that apply to your sector.
4. Complete the **fiche**: short and long descriptions, icon and function graph in the sizes that Play indicates, screenshots, category, privacy policy URL and contact.

### 3.6 Production

Create the production version with notes by language and use a **staggered deployment** (a percentage of users that expands). Monitor Play Console stability metrics (crashes and blocks). Stop the deployment if serious problems appear.

## 4. Unified Release Procedure

| Stage | Actions | Responsible |
| --- | --- | --- |
| 1. Congelation | Phase 8 of the guide completed; git tag; versions fixed | Technical responsible |
| 2. Firmadas compilaciones | iOS: archivo y validación. Android: AAB firmado | Release |
| 3. Pruebas internas | TestFlight interno y pista interna de Play; humo en dispositivos reales | QA |
| 4. Beta | TestFlight externo y pruebas cerradas de Play; recogida de fallos | QA and Product |
| 5. Cierre de la beta | Correcciones por el proceso del harness; compilaciones nuevas | Equipo |
| 6. Fichas y declaraciones | Textos, capturas, privacidad y contenido en ambas stores | Product and privacy |
| 7. Envío a revisión | iOS y Android | Release |
| 8. Publicación escalonada | Porcentajes progresivos en ambas | Release |
| 9. Vigilancia | Estabilidad, valoraciones y soporte durante los primeros días | Release and support |
| 10. Registro | `progress/log.md`, `CHANGELOG`, etiqueta final | Technical responsible |

## 5. After Publication

- **Urgent corrections:** treated as a correction feature (spec with the scenario that reproduces the failure, implementation, sensors, gate, human close) followed by a patch version with higher build number.
- **Annual platform updates:** Apple and Google publish new versions each year. Review `docs/stack.md`, update versions with an ADR and verify with `make sensors` after each step.
- **Dependencies:** attend Dependabot PR with the same review as any other change.
- **Security:** repeat the security door of `docs/security.md` before each relevant release.

## 5. What the Harness Still Does Not Cover (and What to Do While Waiting)

| Necessity | Situation | Recommendation |
| --- | --- | --- |
| Automated signing and upload | Not included | Manual process of this chapter; automate with your chosen tools and register an ADR |
| Environments (development, pre-production, production) | Not included | Define per-environment configuration in an ADR before integrating a real backend |
| Function flags and forced updates | Not included | Evaluate if the business requires it; ADR |
| Failure reports and analytics | Not included | Choose an approved tool, review its privacy impact and register an ADR |
| Task manager (Jira, Azure DevOps) | Not integrated | The harness board coexists with the task manager; use the feature identifier as cross-reference |

## 6. Final Publication Checklist

**Both platforms**

- [ ] Candidate version verified and tagged; `make verify` in green
- [ ] Privacy declarations coherent with `docs/privacy-compliance.md`
- [ ] Privacy policy and support contact published
- [ ] Screens, icons, texts and release notes prepared in all languages
- [ ] Retirement plan agreed; responsible persons assigned for vigilance

**iOS**

- [ ] Bundle ID, capabilities, permission texts and correct privacy manifest
- [ ] Archive validated in the Organizer; processed compilation; TestFlight tested
- [ ] Age classification, App Privacy, reviewer information and demo account completed

**Android**

- [ ] Upload key custodied; Play App Signing active; no secrets in the repo
- [ ] `versionCode` and `versionName` correct; release version tested with R8 on real devices
- [ ] Pre-launch report reviewed; data security and security declarations completed
- [ ] Staggered deployment configured

## 7. What the Harness Still Does Not Cover (and What to Do While Waiting)

(Repeated from section 6 for convenience)

| Necessity | Situation | Recommendation |
| --- | --- | --- |
| Automated signing and upload | Not included | Manual process of this chapter; automate with your chosen tools and register an ADR |
| Environments (development, pre-production, production) | Not included | Define per-environment configuration in an ADR before integrating a real backend |
| Function flags and forced updates | Not included | Evaluate if the business requires it; ADR |
| Failure reports and analytics | Not included | Choose an approved tool, review its privacy impact and register an ADR |
| Task manager (Jira, Azure DevOps) | Not integrated | The harness board coexists with the task manager; use the feature identifier as cross-reference |
