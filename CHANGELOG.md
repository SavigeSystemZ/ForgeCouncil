# Changelog

Use this file for meaningful repo-visible change history. Keep transient task chatter in `TODO.md` or `WHERE_LEFT_OFF.md`.

## Unreleased

### Added

- `_system/KEY.md` as an exhaustive installable system key
- `bootstrap/generate-system-key.sh` as the generator for that key

### Changed

- core discovery and validation flows now treat the system key as a first-class
  installable surface
- Flutter mobile guidance now tells agents to run
  `flutter create --platforms=android .` around the copied minimal foundation
  before expecting Flutter analyze, test, or APK build commands to work
- Python starter-blueprint guidance now tells agents to use a `src/` layout or
  explicit package discovery in `pyproject.toml` inside scaffolded repos
  instead of relying on flat setuptools auto-discovery

### Fixed

- the system-key generator now resolves relative target paths correctly
- `bootstrap/validate-system.sh` now catches stale
  `_system/instruction-precedence.json.template_version` values instead of
  letting that metadata drift silently
- mobile campaign smoke now covers the copied Flutter bootstrap guidance and the
  wrapper still rewrites moved repo-local paths after staging under `apps/`

### Removed

- None recorded yet.
