# 10 - Troubleshooting and FAQ

## 1. How to Diagnose

1. `make doctor` for the environment.
2. `make validate-harness` for the repo.
3. `make status` for the features state.
4. Read the message: scripts indicate what's missing and how to correct it.

## 2. Environment and Sensors

| Symptom or message | Cause | What to do |
| --- | --- | --- |
| "SENSOR UNAVAILABLE (ios): iOS sensors need macOS" | The machine is not a Mac | Run the iOS sensor on a Mac or in CI; on this machine use `make sensor-android` |
| "xcodebuild not found" | Xcode not installed or not selected | Install Xcode and run `xcode-select` toward it |
| "ios/App/App.xcodeproj not found" | `IOS_PROJECT` does not match the real project | Adjust `IOS_PROJECT` in `harness.env` |
| `xcodebuild` not find the destination or the simulator | `IOS_DESTINATION` names a simulator that does not exist | `make simulators` and correct the name |
| `xcodebuild` not find the scheme | The scheme is not shared or `IOS_SCHEME` is incorrect | Share it in Xcode (Manage Schemes) and review `IOS_SCHEME` |
| "android/gradlew not found" | The Gradle project does not exist or `ANDROID_DIR` is incorrect | Create the project (phase 3) or correct `ANDROID_DIR` |
| "JDK 17+ required, found ..." | Old JDK or `JAVA_HOME` points to another | Install the required JDK and define `JAVA_HOME` |
| Gradle does not download dependencies | No network or company proxy | Configure the proxy in Gradle or use the company internal repository |
| The Android sensor fails by a non-existent task | `ANDROID_TEST_TASK` does not correspond to your module | Adjust the task (e.g. another module or variant) |
| The iOS sensor is in red by non-existent tests | Newly created project without tests | Add the first feature's tests |
| `make` ends with code 2 although the script indicates another | `make` returns 2 on any recipe failure | Execute the script directly to see its original code |
| Result "PARTIAL" in the gate | A sensor was not available or omitted | Run the missing sensors where they are available; do not close with partial |

## 3. Board and Process

| Symptom or message | Cause | What to do |
| --- | --- | --- |
| "ERROR: ... is already in_progress" | There's already a feature in progress | Finish or block the current one |
| "sensor_green is written only by a passing sensor" | Attempted to mark by hand | Run the corresponding sensor |
| "closing a feature is a HUMAN decision" | `done` was executed without the flag | A person completes the dual checklist and executes it with the flag |
| "no recorded gate covering every platform" | Missing the gate, or a subsequent sensor invalidated it | Run `make gate` again with both sensors in green |
| "spec ... still contains '@template-placeholder'" | Copied the template without completing it | Complete the spec and delete that line |
| "spec ... no 'Scenario:' found" | The spec has no scenarios | Add at least one |
| A sensor green stops being so after touching code | Normal functioning: a new result invalidates the gate | Re-measure and pass the gate again |
| Conflict of fusion in `feature_list.json` | Two branches modified the board | Take the main branch version and repeat the CLI and sensor commands |
| I cannot eliminate a `done` feature | It's project history | Create a correction feature; closed features are not reopened |

## 4. Validation and Quality

| Symptom or message | Cause | What to do |
| --- | --- | --- |
| "missing required file" | Missing a template file | Restore it from the template |
| "exceeds its budget" | A contract exceeds the maximum lines | Move detail to `docs/` or to `.agents/references/` |
| "broken link" o "references missing path" | A document mentions a non-existent route | Correct the route or create the file |
| "mentions unknown make target" | A document cites a non-existent command | Correct the document or add the target |
| "frontmatter name must equal folder name" | A skill does not match its folder | Align both |
| "skills/README.md does not list skill" | Outdated index | Add the skill to the index |
| Avisos de "not documented in docs/manual" | You added own files, commands or keys | Documéntelos en los capítulos 04, 05 o 06, o deje el modo `warn` |
| "SECRET SCAN FAILED" | A secret pattern or prohibited file type | **Rote el secreto** (ya está comprometido), elimínelo y, si es un falso positivo, use `secrets:allow` en la línea o `.secrets-allowlist` |
| "ARCHITECTURE AUDIT FAILED" | A layer or style rule is broken | Correct; if legitimate, exempt the line with `audit:allow` and the reason; in an existing project, register the debt with `--update-baseline` |
| "forbidden IDE/OS files found" | There are `xcuserstate`, `.DS_Store` or similar | `make clean-ide`; if they were versioned, `git rm -r --cached` |

## 5. Agents and Tools

| Symptom | Probable cause | What to do |
| --- | --- | --- |
| A hook blocks a legitimate action | The rule is stricter than its necessity | Ask a person to execute that action; if it repeats, value adjusting the rule with owners approval |
| The agent ignores a rule | Rule too long, ambiguous or not checkable | Register it in the flywheel and convert the rule into a scenario or an automatic check |
| The agent changes or deletes a test to pass the sensor | Serious deviation | Revert, register it and reinforce the review; contracts expressly prohibit it |
| The agent invents functions of a library | Hallucination | Always compile and test; review new dependencies |
| The agent loses the thread in long sessions | Saturated context | Short sessions per platform; use `progress/current.md` for handover |
| The hooks don't execute in a tool | That tool does not support them | Trust the validator, the CI and the review (hooks are guardrails, not a wall) |
| iOS CI job fails by the simulator | The name does not exist in the executor | Consult the job list printed and adjust `IOS_DESTINATION` |

## 6. Frequently Asked Questions

**¿Puede usarse para una sola plataforma?** Sí. Define `PLATFORMS` with a single one in `harness.env`; features can only point to it. Detail in `docs/customizing.md`.

**¿Puedo cambiar el stack (base de datos, navegación, inyección, pruebas)?** Sí, todo lo de los contratos es un valor por defecto. El procedimiento es: ADR, actualizar contrato, `docs/stack.md` y referencia, y validar (`docs/customizing.md`).

**¿Sirve con Flutter, React Native o Kotlin Multiplatform?** No: the design is based on two native codebases. Adapting it would require rewriting architecture and contracts.

**¿Qué herramientas de IA admite?** Cualquier que lea `AGENTS.md`. Hay adaptadores para Claude Code, Codex, Cursor, OpenCode y Gemini. The permissions and hooks vary according to what each one supports.

**¿Necesito usar las 14 skills?** El agente carga solo las que necesita. Si elimina una, actualice el índice y el manual.

**¿Garantiza que el código sea correcto?** No. Garantiza medición, auditoría de lo auditable, trazabilidad y decisión humana. The quality depends on the specs and the tests written.

**¿Quién responde si un fallo llega a producción?** Las personas que aprobaron: cerrar una feature es una decisión humana registrada. The harness aporta la evidencia de qué se verificó y qué no.

**¿Funciona en Windows?** Los scripts usan `sh`, `make` y Python 3. Se espera que funcionen con WSL o Git Bash, pero **no se han probado en Windows nativo**. iOS exige siempre una Mac.

**¿Cuánto tiempo lleva el arranque?** Depende de su organización (cuentas, aprobaciones, diseños). No se ofrecen cifras fiables que las respalden.

**¿Qué hago si el CI no puede ejecutar pruebas iOS?** El job de CI compila (`make build-ios`), pero cerrar una feature exige el sensor iOS en verde en alguna máquina (`make sensor-ios` en una Mac o en un CI con simuladores).

**¿Por qué `IOS_DIR` no hace nada?** Es una clave que el validador exige pero que ningún script usa todavía; se conserva por coherencia con `ANDROID_DIR`.

**¿Cómo actualizo la plantilla?** Ver el capítulo 09, sección 10.

**¿Puedo ejecutar varios agentes a la vez?** Sí, con ramas y directorios de trabajo separados (por ejemplo `git worktree`), una feature por agente, sin compartir árbol.

**¿Cómo añado una skill, un comando o una regla?** Skill: skill `harness-maintainer` and update the index. Command or key: add it and document it in chapters 05 or 06. Rule: in the corresponding contract, within the line budget, and better if it's checkable by a script.

## 7. Known Limits

| Limit | Consequence |
| --- | --- |
| El corte vertical de ejemplo no se compiló dentro de la plantilla | Se verifica en la fase 4 de su infraestructura |
| El sensor por defecto ejecuta pruebas unitarias, no de interfaz | Añada pruebas de interfaz antes de publicar (fase 7) y valore incluirlas en el CI con un ADR |
| Las reglas del auditor se basan en líneas de código | Detectan lo evidente; no sustituyen la revisión |
| Hooks y permisos son barandillas | No impiden a un usuario malicioso con terminal; la defensa real es la revisión y la protección de rama |
| `CODEOWNERS` requiere protección de rama | Sin ella, la revisión de propietarios no es obligatoria |
| Windows nativo no probado | Use WSL o Git Bash, o un CI Linux |
| Sin automatización de releases, entornos, interruptores de funciones ni informes de fallos | Ver capítulo 08, sección 6 |
