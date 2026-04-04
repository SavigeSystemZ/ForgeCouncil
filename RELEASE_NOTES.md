# Release Notes

Use this file for the current candidate release or milestone summary.

## Current release target

- Target label: AIAST `1.13.7`
- Intended audience: AIAST maintainers and downstream app-repo agents
- Release goal: close the downstream-proven mobile bootstrap gap by telling
  agents exactly how to turn the copied Flutter foundation into a runnable
  Android project, while keeping the isolated test-session proof flow green
- Release confidence: high after green mobile downstream proof work plus green
  maintainer and AIAST automation lanes on 2026-03-26

## User-visible changes

- Flutter Android repos now explicitly tell agents to run
  `flutter create --platforms=android .` around the copied minimal foundation
  before expecting analyze, test, or APK build commands to work.
- The shipped mobile guide and runtime mobile READMEs now reinforce that same
  bootstrap step in repo-local terms.
- Factory campaign smoke now includes the mobile repo and verifies that the
  copied mobile README and blueprint both carry the Flutter bootstrap step.

## Upgrade or migration notes

- Existing repos created before AIAST `1.13.7` should review their copied
  mobile guidance and, for Flutter Android repos, run
  `flutter create --platforms=android .` before expecting the full Flutter
  validation command set to work against the minimal foundation.

## Known limitations

- Flutter Android repos still depend on a local Flutter SDK and Android SDK to
  execute the mobile validation commands; AIAST now makes the project-generation
  step explicit, but it does not bundle those host toolchains.

## Follow-up after release

- Re-prepare the downstream test-app matrix from AIAST `1.13.7` before drawing
  conclusions from future mobile sessions.

## Rules

- Keep this aligned with `CHANGELOG.md`.
- Do not claim release readiness unless validation evidence exists.
