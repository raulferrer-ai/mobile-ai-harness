# Flywheel - from failure to rule

When an agent (or we) deviate from the spec, the design system or the Definition of Done, fixing the code is not
enough. Record the failure and turn it into guidance or, better, a sensor. That is how the harness improves.

## Entry template (copy into `progress/flywheel-log.md`, newest first)

### YYYY-MM-DD - short title
- **Symptom:** what the agent did wrong, or what slipped through review.
- **Probable cause:** ambiguous spec / missing rule / no sensor / context too large / other.
- **Code fix:** what changed in the app (brief).
- **Harness change** (strongest first):
  - [ ] New or stronger **sensor** (test, lint rule, validator check)
  - [ ] **Spec** scenario added or clarified in `features/*.feature`
  - [ ] **Rule** in `AGENTS.md` or `ios|android/AGENTS.md`
  - [ ] **Doc/skill** note
  - [ ] Nothing (justify why it does not apply)
- **Snippet:** paste the added rule/test.

## Golden rule
Same kind of failure **twice** means the harness has a hole: it must gain a rule, a scenario or a sensor.
Once can be noise.

## Preference order for the fix
1. A sensor the agent cannot ignore (test, validator, hook) beats
2. a spec scenario, which beats
3. a rule in a contract, which beats
4. prose in a doc. Prefer what can be checked mechanically.

## What is not flywheel
- Rewriting the feature without touching rules, specs or tests.
- Adding long paragraphs to `AGENTS.md` for a failure you have not seen twice (it burns context budget).
- Rules the agent cannot verify.
- Hiding the failure: a log entry is not blame, it is data.
