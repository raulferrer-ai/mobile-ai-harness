# Manual of mobile-ai-harness

Complete documentation for teams that are going to build their **iOS and Android native** applications with mobile-ai-harness, starting from graphic designs and functionalities defined by Product, until having the two apps ready for publication.

> Language: this manual is the documentation for people and is in English. The contracts that read the agents (`AGENTS.md`, skills, references) are in Spanish on purpose: it's the language in which IA tools follow instructions best. Code identifiers and commands are not translated.

## How to read it according to your role

| If you are... | Read in this order |
| --- | --- |
| Direction / sponsor | 01, 09 (section "What the company receives") and 10 (limits) |
| Producto / diseño | 01, 02, 07 (phases 2 and 3), 09 |
| Technical harness responsible | All, in order. After `docs/customizing.md` |
| iOS or Android Developer | 02, 03, 07 (phases 4 to 6), 05 |
| QA | 02, 07 (phase 6), 08, `docs/dual-checklist.md` |
| Security, privacy, legal | 09, `docs/security.md`, `docs/privacy-compliance.md`, `docs/ai-governance.md` |
| Release responsible | 07 (phase 8), 08 |

## Index

| Document | What it contains |
| --- | --- |
| [01 - Origin and philosophy](01-origen-y-filosofia.md) | The original idea, how it was developed, what problems it solves and what it does not promise |
| [02 - Concepts and glossary](02-conceptos-y-glosario.md) | The product vocabulary, with industrial quality analogies |
| [03 - How it works](03-como-funciona.md) | Harness architecture, feature life cycle and security model |
| [04 - File reference](04-referencia-de-ficheros.md) | What is each repo file, who touches it and when |
| [05 - Command reference](05-referencia-de-comandos.md) | Every command, parameter, exit code and external command that is executed |
| [06 - Configuration reference](06-referencia-de-configuracion.md) | Every `harness.env` key, each IA tool permission rule and each CI job |
| [07 - Step by step guide](07-guia-paso-a-paso.md) | From designs and functionalities to verified apps, phase by phase |
| [08 - Publication on the stores](08-publicacion-en-las-stores.md) | From the verified app to App Store and Google Play |
| [09 - Roles and governance](09-roles-y-gobierno.md) | Who does what, approvals, IA use and metrics |
| [10 - Troubleshooting and FAQ](10-solucion-de-problemas-y-faq.md) | Symptoms, causes, fixes and frequently asked questions |

## Assurance that the manual is complete

The harness itself watches this documentation: `python3 scripts/validate-harness.py` checks that each file, each `make` target, each board subcommand and each `harness.env` key appear in references 04, 05 and 06. In the template repository it runs in strict mode (`DOCS_COMPLETENESS=strict`); in client projects it remains in warning mode, so adding your own file does not block the work.

## How it is versioned

The template version is shown in `CHANGELOG.md`. This manual describes version 2.2.0.
