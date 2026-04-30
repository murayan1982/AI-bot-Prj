## Release notes and checklist policy

### Policy

`main` is not treated as a full historical archive for release notes or release checklists.

Historical release information is preserved by:

- Git tags
- GitHub Releases

The `main` branch should keep only the documentation needed for the current public version.

### Release notes

Use a stable filename for the current release notes:

```text
docs/RELEASE_NOTES.md
```

Rules:

- `docs/RELEASE_NOTES.md` represents the current release only.
- Do not keep old version-specific release notes on `main` unless there is a specific reason.
- When preparing a new release, update `docs/RELEASE_NOTES.md` for that version.
- When publishing the release, copy the release notes content to the GitHub Release page.
- Past release notes are preserved by the corresponding Git tag and GitHub Release.

Avoid keeping multiple version-specific release note files on `main`.

Prefer a single stable file:

```text
docs/RELEASE_NOTES.md
```

### Release checklist

Release checklist files are internal working files.

Rules:

- `release_checklist_*.md` files may be used during release preparation.
- They may be deleted after the release is completed or when the next version starts.
- Public docs must not link to release checklist files.
- Release notes must not depend on release checklist files.
- Distribution zip files should not include release checklist files.

### README links

README should link only to stable public documentation files.

Recommended link:

```markdown
- [Release Notes](docs/RELEASE_NOTES.md)
```

Avoid version-specific links from README:

```markdown
- [Release Notes](docs/RELEASE_NOTES.md)
```

### Documentation rule

Any document that remains on `main` or is included in the public zip must not reference files that are expected to be deleted during the next development cycle.