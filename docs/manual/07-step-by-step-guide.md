# 07 - Step-by-Step Guide: From Designs and Functionalities to Verified Apps

This guide starts from a concrete situation: **your company already has graphic designs and product-defined functionalities**, and wants to obtain Android and iOS applications ready for publication. It covers from preparation to having a verified candidate version. Publication in the stores is explained in the [chapter 08](08-publicacion-en-las-stores.md).

## 0. Overview

| Phase | Objective | Main Responsible | Result |
| --- | --- | --- | --- |
| 0 | Prepare organization, accounts and teams | Technical direction | Roles, protected repo, approved tools |
| 1 | Install and configure the harness | Harness responsible | Operational repo and validated |
| 2 | Translate designs and functionalities to harness entries | Product, design and technical responsible | Product fiche, design system and specs registered |
| 3 | Create native projects | iOS and Android developers | Two projects that compile and measure with sensors |
| 4 | Test the loop with the example feature | Harness responsible | Evidence that everything works in their infrastructure |
| 5 | Build the foundation (design system in code) | Developers with agents | Tokens, theme, navigation and localization |
| 6 | Build feature by feature | Developers with agents; people who close | `done` features with evidence |
| 7 | Cross-quality | QA, security, privacy | Quality report and risks |
| 8 | Candidate version | Release responsible | Frozen version, ready for chapter 08 |

**Cross-phase rule: An agent never decides what to build or when it is finished. These two decisions are people's; the agent proposes, implements and provides evidence.**

## Fase 0. Preparar la organización

**Objetivo:** que existan las personas, los permisos y las cuentas antes de escribir código.

1. **Nombrar roles** (ver capítulo [09](09-roles-y-gobierno.md)): responsable de producto, responsable del harness, responsable de seguridad, responsable de privacidad, gobierno de IA, responsable de release y QA.
2. **Aprobar las herramientas de IA** y el plan o tenant a usar. Anótelo en `docs/ai-governance.md` (sección 2). Decida qué clases de datos pueden entrar en un prompt (sección 3 del mismo documento).
3. **Crear el repositorio** en su plataforma de código. Active:
   - protección de la rama principal: PR obligatorio, revisión de propietarios de código, sin push forzado;
   - escaneo de secretos y protección de push, alertas de dependencias;
   - permisos de flujos de trabajo de solo lectura por defecto.
4. **Crear los equipos** que figurarán en `.github/CODEOWNERS` (por ejemplo líderes móviles, equipo iOS, equipo Android, seguridad, privacidad, gobierno de IA). Deben tener permiso de escritura.
5. **Abrir las cuentas de las stores** pronto, porque algunas verificaciones tardan: Apple Developer Program (como organización, requiere identificación legal de la empresa) y Google Play Console (cuenta de organización, con verificación). Detalle en el capítulo [08](08-publicacion-en-las-stores.md).
6. **Preparar los equipos de trabajo:** Mac con Xcode para iOS (una Mac por desarrollador iOS o un servicio de CI en macOS); JDK 17 o superior y Android Studio para Android; Python 3.9 o superior; git y make.

**Criterio de salida:** roles nombrados, repositorio protegido, herramientas de IA aprobadas, cuentas de stores en curso.

## Fase 1. Instalar y configurar el harness

**Objetivo:** un repositorio operativo y validado, aún sin código de la app.

1. Copie la plantilla como base del repositorio del proyecto y haga el primer commit.
2. Ejecute `make doctor` y resuelva los `[FAIL]`. En una máquina sin Xcode (Linux o Windows) la parte iOS aparecerá como no disponible: es normal; esa parte se verificará en una Mac o en CI.
3. Ejecute `sh init.sh` (o `make init`). Crea los ficheros de estado que falten, valida y muestra el estado.
4. Edite `harness.env`: `PROJECT_NAME`; deje `PLATFORMS="ios android"`. Las rutas de iOS se ajustan en la fase 3.
5. Edite `feature_list.json` y ponga el mismo nombre en `"project"`.
6. **Security and owners:**
   - sustituya los marcadores `@your-org/...` de `.github/CODEOWNERS` por sus equipos;
   - rellene el contacto de `SECURITY.md`.
7. **Gobierno de IA:** complete las secciones marcadas con CUSTOMIZE de `docs/ai-governance.md`.
8. Ejecute `make validate-harness`. Los avisos de marcadores sin sustituir desaparecen al completar los puntos 6 y 7.
9. Haga commit en una rama, abra un PR y compruebe que el CI ejecuta los jobs (los de Android e iOS se omiten mientras no existan los proyectos).

**Criterio de salida:** `make validate-harness` en verde; CI en verde; propietarios y contacto de seguridad definidos.

## Fase 2. Traducir diseños y funcionalidades a entradas del harness

Es la fase más importante: **la calidad de las specs y del sistema de diseño determina la calidad del resultado**. Un agente implementa fielmente lo que está escrito; lo que no esté escrito lo inventa, y eso es lo que el proceso evita.

### 2.1 Inventario y trazabilidad

Cree una tabla (en una hoja de cálculo o en el propio repositorio) que relacione cada funcionalidad de Producto con una o más features del harness:

| Funcionalidad de producto | Pantallas del diseño | Feature (`id`) | Prioridad | Plataformas | Dependencias |
| --- | --- | --- | --- | --- | --- |
| Alta de cuenta | A1, A2, A3 | `account-signup` | 1 | iOS y Android | API de identidad |

**Criterios para dividir en features:**

- Una feature debe poder entregarse y probarse **por sí sola** (un corte vertical de punta a punta).
- Si una spec supera unos 7 escenarios, es una señal de que hay que dividirla.
- Empiece por una **fundación** (tema, navegación, localización; fase 5) y por el flujo más corto de valor (un "esqueleto andante") antes de las funcionalidades secundarias.
- Las dependencias de backend se resuelven con contratos y datos simulados primero (ver 2.5).

### 2.2 Product Fiche

Rellene `docs/product.md`: qué es la app, para quién, principios, **tono de voz**, idiomas, qué **no** hace (no objetivos) y criterios de éxito. Los no objetivos son especialmente valiosos: impiden que el agente añada funcionalidades no pedidas.

### 2.3 From Graphic Designs to Design System

The designs (e.g. in a design tool) contain screens and a set of styles. The harness needs those styles as **named semantic tokens** and components as a catalog. Process:

1. **Extract styles** from the design and give them functional names, not appearance-based: `primary`, `onPrimary`, `surface`, `textSecondary`, `danger` (not `verdeClaro2`). Define each color for light and dark mode.
2. **Typography:** define roles (display, title, header, body, label, footer) and associate them with native text styles of each platform so that the user's text scaling works.
3. **Spacing, radii and elevation:** a short scale (e.g. multiples of 4) instead of loose values.
4. **Component catalog:** primary and secondary button, card, chip, text field, empty, error and loading states, etc., with their behavior and states (normal, pressed, disabled, error).
5. **Iconography and resources:** decide the origin of icons (own, or system per platform) and the delivery format. Good practice: always deliver SVG graphics; if there are bitmaps, deliver all densities that each platform requires.
6. **Fonts:** check the license for use in mobile apps before including them, and register which ones are used.
7. **App icon and launch screen:** ask design for the formats required by each platform (consult the current Apple and Android guides; they change with versions).
8. **Accessibility:** verify in the design sufficient contrast, minimum tactile target sizes and that no information depends only on color.
9. Pour everything into `docs/design-system.md`. It's the truth source for both platforms.
10. Note in `docs/parity-matrix.md` the differences the design already contemplates (e.g. back gestures or system-specific iconography). A difference without registration is a potential defect.

**Recommended text convention:** ask Product for a "text book" (a table with key, language and text, and plurals instructions) and use the same keys in both platforms, replacing points with underscores in Android. Not a harness-imposed rule; it's a convention that facilitates parity.

### 2.4 From Functionalities to Gherkin Specs

Each feature is described in a `features/NN-<id>.feature` file (NN is the priority). Use the skill `feature-spec-writer` and the guide `.agents/references/gherkin-guide.md`.

**Transformation of a user story example:**

> Historia: "Como cliente quiero recuperar mi contraseña para volver a entrar si la olvido."

```gherkin
Feature: Recuperar contraseña
  As a customer
  I want to recover my password
  So that I can sign in again if I forget it

  Background:
    Given the user is on the sign-in screen

  Scenario: Request a recovery email
    When the user asks to recover the password with a registered email
    Then the user is told that an email was sent
    And the user returns to the sign-in screen

  Scenario Outline: Reject an invalid email
    When the user asks to recover the password with the email "<email>"
    Then nothing is sent
    And a clear, calm message explains the email is not valid

    Examples:
      | email |
      |       |
      | "a@"  |

  Scenario: Service is not reachable
    Given there is no connection
    When the user asks to recover the password with a registered email
    Then the user is told the request could not be sent
    And the user can try again
```

**Quality rules (summary of Gherkin guide):**

- Describe **behavior**, not pulsations nor class names.
- Cover unlucky paths: validation, empty, error, no connection, denied permission, cancellation and interruption.
- One scenario, one behavior; between 3 and 7 steps.
- Label with `@ios` or `@android` only what really differs, and register it in the parity matrix.
- Reference texts by intention; final strings live in localization resources.
- Add an accessibility scenario when the feature incorporates new interactive interface.

**Human suspension point:** Product **reviews and approves each spec before implementing it**. An approved spec is the contract; changing it during implementation requires stopping and rewriting it (not patching the code).

### 2.5 Data and Backend

If the app consumes company services:

1. Define, with the backend team, the **contract** of each service (operations, data, errors).
2. Express that contract as a **repository interface** in the domain layer on each platform. The app depends on the interface, not the service.
3. Start with **simulated implementations** (in-memory fakes): allow testing the full flow without depending on the backend.
4. Real integration (network client, authentication, offline sync) is a technical decision: register it in an ADR (`docs/decisions/`) and respect `docs/security.md` rules (TLS, secure credential storage, no personal data in logs).
5. Keep `docs/privacy-compliance.md` data inventory updated with each new data the app collects.

### 2.6 Non-Functional Requirements

Annotate them (in specs or in `docs/product.md`) so they don't get lost: minimum OS versions, acceptable languages in target devices, acceptable performance in target devices, required accessibility, events of analytics (if applicable) and privacy and legal requirements.

### 2.7 Register Features in the Board

For each approved spec:

```bash
python3 scripts/feature.py add <id> "<Título>" --spec features/NN-<id>.feature [--priority N] [--platforms ios,android]
make status
make validate-harness
```

**Output of the phase 2:** `docs/product.md` and `docs/design-system.md` complete; all features of the first delivery with approved spec by Product and registered; initial parity matrix; agreed data contracts.

## Fase 3. Crear los proyectos nativos

Se hace una sola vez, a mano, porque las herramientas de Apple y de Google cambian sus asistentes con cada versión.

- Decide before two identifiers that **cannot be changed after publishing**:
  - the **iOS Bundle Identifier** (e.g. `com.empresa.app`), and
  - the **Android Application ID / package name** (e.g. `com.empresa.app`).

### 3.1 iOS (en `ios/`)

1. In Xcode: new App project, SwiftUI interface, Swift language. Save it in the route declared `IOS_PROJECT` (by default `ios/App/App.xcodeproj`).
2. Include a unit tests goal and an interface tests goal.
3. Recommended adjustments (detail in `.agents/references/ios-stack.md`): Swift 6 language version, default main thread actor isolation, accessible concurrency activated, activated string catalog and decided deployment destination (the default value is in `docs/stack.md`).
4. **Share the scheme** (Product, Scheme, Manage Schemes, mark "Shared"). Without shared scheme, the command line and CI may not find it.
5. Create the `ios/AGENTS.md` layers folders: `App`, `Features`, `Domain`, `Data`, `DesignSystem` and `Resources`.
6. In `harness.env`: `IOS_PROJECT`, `IOS_SCHEME`, `IOS_SRC_DIR` and a valid `IOS_DESTINATION` (use `make simulators`).
7. Verify: `make sensor-ios` must compile and run tests by default.

### 3.2 Android (en `android/`)

1. In Android Studio: new "Empty Activity" project with Compose, saved in `android/`, with the decided `package name` and `minSdk`.
2. Use Gradle with Kotlin DSL and a version catalog (`gradle/libs.versions.toml`). Take the versions from `docs/stack.md` and **verify them with the Android plugin version notes** you choose; do not copy configurations from old tutorials.
3. Add test dependencies (JUnit 4, test coroutines, Turbine, Compose tests) and state collection with lifecycle awareness.
4. Create the `android/AGENTS.md` layers folders: `features`, `domain`, `data` and `designsystem`.
5. Make commit of the Gradle `wrapper` (`gradlew` and `gradle/wrapper`).
6. In `harness.env`: adjust `ANDROID_TEST_TASK` if your module is not `:app`, and `ANDROID_SRC_DIR` if the structure differs.
7. Verify: `make sensor-android` must execute JVM tests.

### 3.3 Phase Closure

1. `make doctor` without blockers for the platforms you build on that machine.
2. `make validate-harness` in green.
3. Uncomment the Gradle and Swift entries in `.github/dependabot.yml`.
4. Open a PR and confirm that the CI executes the Android and iOS jobs.
5. If you use Dependabot, verify that `Package.resolved` is versioned (the template no longer ignores it).

**Output of the phase:** the two projects compile, their sensors run (even if with few tests) and the CI compiles them.

## Fase 4. Probar el lazo con la feature de ejemplo

**Objective:** demonstrate, in **your** infrastructure, that the process works end-to-end before building the product. It's the first time the example code compiles for real; if small API differences with your tool versions appear, they are corrected here and registered (exactly for that).

1. Copy the files of `templates/sample-feature/` to the native projects following the `README.md` of that folder.
2. Register and start the example feature:

```bash
cp templates/sample-feature/spec/01-sample-items.feature features/01-sample-items.feature
python3 scripts/feature.py add sample-items "Sample items" --spec features/01-sample-items.feature
python3 scripts/feature.py start sample-items
```

3. Run the sensors (in a Mac, both; in another machine, the Android one and leave iOS for CI or a Mac):

```bash
make sensor-ios
make sensor-android
make status        # both platforms must appear as sensor_green
```

4. Run `make gate`. In a Mac, with both sensors in green, it must end in "GATE PASSED". In a non-Mac machine the result will be "GATE PARTIAL" (iOS not verified): this is the correct behavior and demonstrates that the system does not consider good what it could not measure.
5. Test the protections (convenient that the team sees it once): try `python3 scripts/feature.py done sample-items` **without** the human flag and see that it is rejected; ask an agent to close the feature and see that the hook blocks it.
6. **It is not necessary to close the example feature.** To clean up, a person eliminates the copied example from the board and deletes the files:

```bash
python3 scripts/feature.py remove sample-items
```

If you decide to close it, it will remain in the board as history ( `done` features cannot be eliminated with the CLI).
If something had to be corrected, register it in `progress/flywheel-log.md` (template in `docs/flywheel.md`).

**Output of the phase:** sensors in green on both platforms, gate approved, team familiarized with the flow, and the CI running end-to-end.

## Fase 5. Construir la fundación (el sistema de diseño en código)

**Objective:** that both apps have the same visual language implemented before the features.

1. Create a spec `app-foundation` with scenarios like: the app opens in its initial screen; follows the system's light or dark mode; text grows with the user's font size; all text comes from localization resources; base navigation works. Pass the spec through the same process (Product approves it, it's registered, it's started).
2. In each platform, an agent implements (with the skill `design-system-parity`):
   - **Tokens** of color (light and dark), typography, spacing, radii and elevation in the design system layer (`DesignSystem` in iOS, `designsystem` in Android), with the semantic names of `docs/design-system.md`.
   - **Base components** from the catalog (buttons, cards, fields, empty, error and loading states).
   - **Resources:** icons, images, fonts, app icon and launch screen. In iOS they go to the resource catalog and project configuration; in Android, to the resource folders and manifest.
   - **Localization:** string catalog (iOS) and `strings.xml` (Android) with the keys of the text book.
   - **Base navigation** and **composition root** (`App` in iOS, `AppContainer` in Android), with simulated repositories.
3. Run `make sensor-ios` and `make sensor-android` until green, and then `make audit` (must be clean: rules are fulfilled from the beginning).
4. **Human visual review:** open the app alongside the design and compare, component by component, colors, typography, spacing and states, in light and dark mode and with text at large size. This is the starting point for no subsequent feature introduces loose values.
5. Complete and close the feature as any other (see phase 6, steps G to J).

**Output of the phase:** both apps show the same components with the same tokens; `docs/design-system.md` and the code match; the parity matrix records intentional differences.

## Fase 6. Construir feature a feature (the cycle)

It is the core of the method. It repeats for each feature, in priority order. Each step indicates who does it and what evidence it leaves.

| Step | Who | What | Evidence |
| --- | --- | --- | --- |
| A | Persona | Choose and start the feature | `python3 scripts/feature.py start <id>` and `make status` |
| B | Agente | Planificar | Plan in `progress/current.md` |
| C | Agente | Implement platform 1 and measure | Code, tests and `sensor_green` |
| D | Persona | Review platform 1 work | Code review |
| E | Agente | Implement platform 2 and measure | Code, tests and `sensor_green` |
| F | Agente | Independent validation | Validator report |
| G | Persona | Dual verification | `docs/dual-checklist.md` list |
| H | Script | Gate | `make gate` approved and registered |
| I | Persona | Close | `done` in the board |
| J | Persona | Commit, PR, merge | History and PR with evidence |

### A. Choose and start

```bash
make status
python3 scripts/feature.py start <id>
```

Only one feature can be in progress. If you have to stop due to an external dependency:
`python3 scripts/feature.py block <id> --reason "<motivo>"`; resumed with `start`.

### B. Plan (agent, skill `workflow-planner`)

Example message: *"Sigue AGENTS.md. Usa la skill workflow-planner para planificar la feature activa en ambas plataformas, pero no implements nada. Escribe el plan en progress/current.md."* The plan must divide the work into small, each verificable with a sensor, and point out the expected differences between platforms.

### C. Implement platform 1 and measure (agent)

**One platform per session.** Example message: *"Sigue AGENTS.md y ios/AGENTS.md. Implementa la feature activa solo en iOS, con pruebas, siguiendo el plan de progress/current.md. Ejecuta make sensor-ios hasta que esté en verde. Actualiza progress/current.md con el estado y las notas de traspaso."*

The agent works inside out: domain, data, state, interface. After each increment execute the sensor:

- **Red:** correct and repeat. Do not advance or declare the platform ready.
- **Green:** the sensor registers `sensor_green` in the board by itself.

If the sensor returns "not available" (code 3), the problem is the environment (e.g. missing JDK); solve with `make doctor`, don't evade.

### D. Review platform 1 (persona)

Review the change as any other, with special attention to what agents usually do bad: invented APIs, weakened tests, unwanted scope, new dependencies, hand-written design values. Run `make audit` if in doubt about layer rules. Make commit of platform 1.

### E. Implement platform 2 and measure (agent)

**New session** (clean context). Example message: *"Sigue AGENTS.md y android/AGENTS.md. Implementa la feature activa solo en Android. Usa la spec y la implementación iOS como referencia de comportamiento, no copies código. Ejecuta make sensor-android hasta verde y actualiza progress/current.md."* What is shared is the behavior and the design, not the code.

### F. Independent validation (agent)

Example message: *"Usa la skill workflow-validator sobre la feature activa. Recorre cada escenario de la spec y señala el código y la prueba que lo cubren. No ejecutes feature.py done."* A second agent (or a different session) reduces the risk that who implemented overlooks their own bias.

### G. Dual verification (persona)

With both apps open side by side, go through `docs/dual-checklist.md`: every scenario works the same, same step order, same texts and tone; empty, load and error states; permissions denied; accessibility (screen reader, large text, contrast); light and dark mode; previous data that still works (migrations). Compare with the design. Register in `docs/parity-matrix.md` each difference that is intentional. Paste the result in the PR.

### H. Gate

```bash
make gate
```

Must end in "GATE PASSED". If it's partial (some sensor not available), the feature cannot be closed: execute the missing sensors where they are available (e.g. in a Mac or CI) and repeat.

### I. Close (persona, in their terminal)

```bash
python3 scripts/feature.py done <id> --human-checklist-ok
```

It's a signed declaration: confirms that the person has reviewed the evidence. Agents cannot execute it.

### J. Commit, PR and merge

Use the PR template: evidence of sensors and gate, dual checklist, IA assistance (tool and trailer, in commit footers `AI-Assisted: <herramienta>/<modelo>`), security and privacy impact, and harness feedback (flywheel, progress notes). Code owners review. After the merge, mark the milestone in `progress/log.md`.

### Common Situations

| Situation | What to do |
| --- | --- |
| The agent deviates from the spec or rules | Correct the code; register the deviation in `progress/flywheel-log.md`; if it repeats, add a rule, scenario or stronger check (`docs/flywheel.md`) |
| The spec was bad or scope changes | Stop, rewrite the spec and obtain Product approval before following implementing |
| An error is discovered in a `done` feature | Add a reproducing scenario, register it as a new correction feature (e.g. `fix-<id>`), correct and measure; closed features are not reopened |
| A planned feature must be removed | `python3 scripts/feature.py remove <id>` (only person) and delete its spec if no longer needed |
| Two agents or people work at the same time | One branch and work tree per feature (e.g. with `git worktree`); never share a tree |
| Conflict in `feature_list.json` | Do not merge manually: take the version from the main branch and repeat the CLI and sensor commands |
| A sensor fails due to environment, not code | `make doctor`; if it's a tool version, adjust `harness.env`; do not mark by hand |
| A `make audit` violation is legitimate | Exempt that line with `audit:allow` and the reason, or decide with an ADR |

## Fase 7. Calidad transversal

Before freezing, the team reviews what unit tests do not cover. Record the result of each point.

| Area | What to check |
| --- | --- |
| Seguridad | Revise `docs/security.md`: lista MASVS, modelo de amenazas completado, `make scan-secrets` limpio, dependencias y licencias revisadas, sin depuración ni endpoints de prueba en la versión de release |
| Privacidad | `docs/privacy-compliance.md`: inventario de datos al día, manifiesto de privacidad de iOS, declaración de seguridad de datos de Android, textos de permisos, borrado de datos real |
| Accesibilidad | Pase con lector de pantalla en ambas plataformas, texto en el tamaño máximo, contraste, objetivos táctiles, reducción de movimiento |
| Pruebas de interfaz | El sensor por defecto ejecuta pruebas unitarias. Antes de publicar, ejecute además pruebas de interfaz en simulador y emulador (y valore incluirlas en el CI con un ADR) |
| Dispositivos reales | Una matriz de dispositivos y versiones de sistema representativa, incluido el dispositivo más modesto soportado |
| Rendimiento | Arranque en frío, fluidez de listas, memoria y consumo en un dispositivo modesto |
| Interrupciones | Llamadas, segundo plano, poca memoria, permisos revocados, cambio de idioma o de tamaño de texto |
| Conectividad | Sin conexión, conexión lenta, cortes a mitad de operación |
| Datos | Instalación limpia frente a actualización desde una versión anterior; migraciones |
| Localización | Todos los idiomas, textos largos, formatos de fecha y número, plurales |
| Paridad | `docs/parity-matrix.md` final: cada diferencia intencionada documentada |
| Deuda de arquitectura | `.audit-baseline` vacío o con excepciones aceptadas por escrito |
| QA exploratorio | Sesiones con objetivos concretos sobre los flujos principales |

## Fase 8. Versión candidata

**Definición de "listo para publicar"** (a nivel de proyecto). Todos los puntos deben cumplirse o tener una excepción firmada:

| Bloque | Criterio |
| --- | --- |
| Alcance | Todas las features planificadas están `done`, o las diferidas lo están por decisión escrita de Producto |
| Verificación | `make verify` en verde; CI en verde en iOS y Android; sensores en modo `test` (sin plataformas degradadas) |
| Calidad | Fase 7 completada y sus hallazgos críticos resueltos |
| Seguridad y privacidad | Puerta de seguridad de `docs/security.md` revisada y declaraciones de privacidad preparadas |
| Legal | Licencia, avisos de terceros y política de privacidad publicada |
| Contenido de las stores | Textos, capturas, iconos, categoría y datos de contacto preparados (capítulo 08) |
| Versión | Número de versión decidido y registrado en ambos proyectos |
| Trazabilidad | `progress/log.md` y `CHANGELOG` al día; etiqueta de git creada |
| Recuperación | Plan de retirada o corrección rápida acordado |

With the candidate version frozen, the release team continues with [chapter 08](08-publicacion-en-las-stores.md).

## Apéndice A. Example Messages for Agents

| Tarea | Mensaje |
| --- | --- |
| Escribir una spec | "Sigue AGENTS.md. Con docs/product.md y esta historia de usuario <texto>, escribe la spec usando la skill feature-spec-writer. No implementes." |
| Planificar | "Usa la skill workflow-planner con la feature activa y escribe el plan en progress/current.md. No escribas código." |
| Implementar | "Sigue AGENTS.md y <plataforma>/AGENTS.md. Implementa la feature activa solo en <plataforma>, con pruebas, y ejecuta el sensor hasta verde." |
| Validar | "Usa workflow-validator sobre la feature activa y entrega un informe por escenario. No cierres la feature." |
| Registrar una desviación | "Usa flywheel-recorder: registra esta desviación y proponga la regla, escenario o comprobación más fuerte que la evite." |
| Cambiar el stack | "Estamos cambiando <elemento>. Sigue docs/customizing.md: proponga el ADR y la lista de ficheros a actualizar. No toques código todavía." |

## Apéndice B. What is Produced in Each Phase

| Fase | Artefactos |
| --- | --- |
| 0 | Roles, repositorio protegido, herramientas de IA aprobadas |
| 1 | `harness.env`, `CODEOWNERS`, `SECURITY.md`, `docs/ai-governance.md` completados |
| 2 | `docs/product.md`, `docs/design-system.md`, `docs/parity-matrix.md`, specs en `features/`, tablero poblado, ADR de datos |
| 3 | Proyectos `ios/` y `android/`, `harness.env` ajustado |
| 4 | Evidencia del lazo; entradas de flywheel si hubo ajustes |
| 5 | Tokens, componentes base, recursos, localización y navegación en ambas apps |
| 6 | Features `done`, PR con evidencia, `progress/log.md` |
| 7 | Informe de calidad, `docs/security.md` y `docs/privacy-compliance.md` completados |
| 8 | Versión congelada y etiqueta |

## Apéndice C. Summary of Commands by Phase

| Fase | Comandos clave |
| --- | --- |
| 1 | `make doctor`, `sh init.sh`, `make validate-harness` |
| 2 | `python3 scripts/feature.py add ...`, `make status` |
| 3 | `make simulators`, `make sensor-ios`, `make sensor-android` |
| 4 | `python3 scripts/feature.py start`, `make gate`, `python3 scripts/feature.py remove` |
| 5 y 6 | `make sensor-ios`, `make sensor-android`, `make audit`, `make gate`, `python3 scripts/feature.py done ... --human-checklist-ok` (persona) |
| 7 y 8 | `make scan-secrets`, `make verify` |
