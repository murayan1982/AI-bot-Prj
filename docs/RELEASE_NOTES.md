# Release Notes

Current release: v2.7.0

## v2.7.0 - Documentation Structure and Release Packaging Cleanup

### Summary

This release cleans up documentation structure and release packaging rules before larger v3.0 runtime work.

v2.7.0 focuses on:

- keeping `README.md` as the first-time user entry point
- clarifying the role of public docs
- using `docs/RELEASE_NOTES.md` as the current release notes file on `main`
- preserving historical release notes through Git tags and GitHub Releases
- preventing public docs from referencing internal release checklist files
- preparing clearer release package rules

### Added

- Added `docs/release_package_policy.md` to define public release package include / exclude rules.
- Added `scripts/check_release_package.py` for release documentation sanity checks.

### Changed

- Updated documentation policy so `main` only keeps release notes for the current public version.
- Replaced version-specific release notes references with the stable `docs/RELEASE_NOTES.md` path.
- Removed public documentation references to internal release checklist files.
- Clarified that old release notes are preserved by Git tags and GitHub Releases.
- Clarified that release checklist files are internal working files and should not be referenced by public docs.
- Clarified that local build scripts and generated release archives are maintainer-side artifacts and are not Git-managed.
- Updated v3.0 roadmap documentation to match the current release notes policy.

### Documentation policy

`main` is not treated as a full historical archive for release notes.

Historical release information is preserved by:

- Git tags
- GitHub Releases

The current release notes should live at:

```text
docs/RELEASE_NOTES.md
```

Version-specific release note files should not be accumulated on `main` unless there is a specific reason.

### Release checklist policy

Release checklist files are internal working files.

They may be used during release preparation, but public documentation should not depend on them.

Rules:

- Do not link to release checklist files from `README.md`.
- Do not link to release checklist files from public docs.
- Do not include release checklist files in public release packages.
- Keep required public verification steps directly in this release notes file.

### Verification

Run the standard checks before tagging the release:

```powershell
python -m compileall -q .
python scripts/check_release_package.py
python scripts/smoke_public_facade.py
python examples/app_error_handling.py
python examples/public_text_chat.py
python examples/minimal_app_text_chat.py
```

### Notes for GitHub Release

When publishing the release, copy the relevant contents of this file into the GitHub Release page.

After the next version starts, this file may be updated for the next current release.  
Past release details are preserved by the corresponding Git tag and GitHub Release.