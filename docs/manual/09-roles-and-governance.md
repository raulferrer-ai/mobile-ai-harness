# 09 - Roles and Governance

## 1. What the Company Receives

| Delivery | Content |
| --- | --- |
| Template repository (version 2.2.0) | Contracts, 14 skills, references, hooks, scripts, CI, security privacy and IA governance cuts, vertical example |
| This manual | Ten chapters plus index, in `docs/manual/`, with the mechanical guarantee that it covers all files, commands and keys |
| The harness own tests | 38 automatic tests executable with `make test-harness` |
| First application on a real project (Leafly, case study) | Migration prepared and audited; native sensors **were not executed** in the preparation environment |
| Native code of the vertical slice and adjustments to Xcode and Gradle projects | **Not compiled by the template**: verified in your infrastructure in phase 4 of the guide |
| Security, privacy and IA governance | Templates and checklists: must be completed and approved by their responsible; not legal advice |

**Real verification state (without adornments):**

| Element | State |
| --- | --- |
| Scripts, board, hooks, validator, scanner, audit and manual check | Tested with automatic tests |
| First application on a real project (Leafly, case study) | Migration prepared and audited; native sensors **were not executed** in the preparation environment |
| Native code of the vertical slice and project adjustments for Xcode and Gradle | **Not compiled by the template**: verified in your infrastructure in the guide's phase 4 |
| Security, privacy and IA governance | Templates and checklists: must be completed and approved by their responsible; not legal advice |

**What the company must provide:** defined designs and functionalities; developer accounts for both stores; teams with Xcode and Android Studio or CI in macOS; approved IA tools; people in the roles of this chapter; and the security, privacy and legal decisions own to their sector.

## 2. Roles

| Rol | Responsibilities | Decide |
| --- | --- | --- |
| Producto | Funcionalidades, specs, tono, no objetivos, aceptación de cada spec y de la versión | Qué se construye y su prioridad |
| Diseño | Sistema de diseño, componentes, recursos, revisión visual de cada feature | Cómo debe verse y comportarse la interfaz |
| Responsable del harness | Configuración, contratos, skills, scripts, CI, actualizaciones de la plantilla, flywheel | Cambios en el proceso (con propietarios) |
| Desarrollador iOS o Android | Dirige a los agentes, revisa el código, mantiene la plataforma | Detalles de implementación dentro de los contratos |
| QA | Lista dual, pruebas exploratorias, dispositivos reales, calidad transversal | Si una feature cumple su calidad |
| Seguridad | `docs/security.md`, revisión de dependencias, modelo de amenazas, incidentes | Riesgos aceptables y excepciones de seguridad |
| Privacidad y legal | `docs/privacy-compliance.md`, declaraciones de las stores, licencias | Qué datos se recogen y bajo qué condiciones |
| Gobierno de IA | `docs/ai-governance.md`, herramientas aprobadas, clasificación de datos | Qué herramientas y datos se permiten |
| Release | Cuentas, firma, compilaciones, envío a las stores, despliegue | Cuándo y cómo se publica |
| Persona que cierra (rol por feature) | Ejecuta la lista dual y el cierre humano | Si la evidencia basta para cerrar |

In small teams, one person can cover several roles; what should not happen is that **the same person implements and closes without review** nor that an agent closes.

## 3. Responsibility Matrix

R = executes, A = approves, C = consultated, I = informed.

| Actividad | Producto | Diseño | Harness | Desarrollo | QA | Seguridad | Release |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Escribir y aprobar una spec | A | C | I | R | C | I | I |
| Sistema de diseño | C | A y R | I | R | C | I | I |
| Registrar y arrancar una feature | I | I | R | R | I | I | I |
| Implementar y medir | I | I | I | R | I | I | I |
| Revisión del código | I | I | C | R y A | C | C | I |
| Lista dual y cierre | A | C | I | C | R | I | I |
| Cambiar el stack o el proceso (ADR) | I | I | R | C | I | C | A |
| Cambiar permisos de agentes | I | I | R | I | I | C | A y gobierno de IA |
| Puerta de seguridad de release | I | I | I | C | C | A y R | R |
| Envío a las stores | A | C | I | C | C | C | R |

## 4. Human Approval Points

| Punto | Quién decide | Documento |
| --- | --- | --- |
| Aprobar una spec | Producto | Fase 2 de la guía |
| Cambiar alcance durante una feature | Producto | `docs/workflow.md` |
| Lista dual | QA y quien cierra | `docs/dual-checklist.md` |
| Cerrar una feature | Persona que cierra | `scripts/feature.py` (human closure) |
| Eliminar una feature | Producto y responsable técnico | `scripts/feature.py` (elimination command) |
| Merge | Propietarios de código | `.github/CODEOWNERS` |
| Cambiar contratos, hooks, scripts o CI | Propietarios del harness y gobierno de IA | `.github/CODEOWNERS` |
| Cambiar el stack | Responsable del harness y seguridad | `docs/customizing.md` |
| Publicar | Release y Producto | Capítulo 08 |

## 5. IA Use Rules: Team Rules

The detail is in `docs/ai-governance.md`. Operational summary:

1. Only approved tools, with the approved plan or tenant.
2. **Never** confidential data in a prompt: credentials, signing material, client data, non-published plans.
3. Every agent contribution is reviewed by a person with the same exigency as any other.
4. IA assistance is disclosed in the PR and, for material changes, in the commit footer.
5. An agent never closes nor eliminates features, nor edits the board, nor touches secrets.
6. Changes to the own harness require owners approval.
7. Parallel agents use separate branches and work trees.
8. An incident (data leakage, destructive action, vulnerability) is contained, communicated to security and converted into a rule or check (flywheel).

## 6. Incorporating a New Person

| Order | Action |
| --- | --- |
| 1 | Read chapters 01 to 03 of this manual |
| 2 | Install tools and run `make doctor` and `sh init.sh` |
| 3 | Read `AGENTS.md` and the contract of your platform |
| 4 | Run `make status` and read `progress/current.md` |
| 5 | Work a small feature with an agent, accompanied by an experienced person |
| 6 | Review another person's feature using the dual checklist |

## 7. Government Pace

| Frequency | Activity |
| --- | --- |
| Every feature | Evidence, dual checklist, human closure, deviation registration |
| Every week | Review of `progress/flywheel-log.md`: what rules, scenarios or checks to add |
| Every month | Review of the `.audit-baseline` debt and pending dependencies |
| Every trimestre and after any incident | Review of `docs/ai-governance.md`, approved tools and hook and permission rules |
| Every release | Security door, privacy and chapter 08 |
| Every year or major platform change | Update the `docs/stack.md` baseline with an ADR |

## 8. Suggested Indicators

No universal target figures; measure your own trend:

- Features closed per period and time between start and close.
- Proportion of features whose gate passes the first time.
- Sensors in red per feature and most frequent causes.
- Flywheel entries and how many became an automatic check.
- Evolution of `.audit-baseline` violations (should decrease).
- Defects discovered after close and after publication, and why they weren't detected before.
- Registered parity divergences and their age.

## 9. Audit Evidences

Everything remains in the repository and in your code platform: the board (who and when closed each feature, with what gate), the specs (what was requested), the PRs (review, IA disclosure), `progress/log.md` and `progress/flywheel-log.md`, the ADRs (decisions), the results of CI and the git history with IA assistance footers.

## 10. Update the Template

When a new version exists, compare by areas:

- `scripts/` and `.agents/hooks/` (adopt the new)
- `docs/workflow.md` and `docs/flywheel.md` (adopt)
- `harness.env` (merge: conserve your values and add the new keys; the validator names the ones that falter)
- Platform contracts and `docs/stack.md` (manual merge: contain your decisions)
- Execute `make validate-harness` and `make test-harness` after each update.
