# Release Evidence Automation Specification

## Purpose

Automate release and publication evidence so the repository can prove whether
GitHub Releases, PyPI, conda-forge, GitHub Pages, and future registries are
published, current, and version-consistent.

## Evidence Schema

### JSON Report Schema

```json
{
  "report_version": "1.0",
  "generated_at": "2026-05-12T12:00:00Z",
  "source": {
    "version": "0.5.0",
    "git_tag": "v0.5.0",
    "commit": "abc1234",
    "repository": "github.com/owner/microcosting_healthservices"
  },
  "registries": [
    {
      "name": "pypi",
      "status": "published|unpublished|future-only|published-with-gaps|recipe-only|private",
      "version": "0.5.0",
      "url": "https://pypi.org/project/nwau-py/",
      "checked_at": "2026-05-12T12:00:00Z"
    },
    {
      "name": "conda-forge",
      "status": "recipe-only|future-only|unpublished|published",
      "version": null,
      "url": null,
      "checked_at": "2026-05-12T12:00:00Z",
      "notes": "Not yet submitted"
    },
    {
      "name": "github_release",
      "status": "published|unpublished",
      "version": "0.5.0",
      "url": "https://github.com/owner/microcosting_healthservices/releases/tag/v0.5.0",
      "checked_at": "2026-05-12T12:00:00Z"
    },
    {
      "name": "github_pages",
      "status": "published|unpublished|future-only",
      "url": "https://owner.github.io/microcosting_healthservices/",
      "checked_at": "2026-05-12T12:00:00Z"
    },
    {
      "name": "crates_io",
      "status": "future-only",
      "version": null,
      "url": null,
      "checked_at": "2026-05-12T12:00:00Z",
      "notes": "Rust core not yet stable"
    },
    {
      "name": "internal_registry",
      "status": "private",
      "version": "0.5.0",
      "url": "https://internal.example.invalid/nwau/",
      "checked_at": "2026-05-12T12:00:00Z"
    }
  ],
  "workflows": [
    {
      "name": "release",
      "status": "passing|failing|unknown",
      "latest_run": "2026-05-11T10:00:00Z"
    },
    {
      "name": "publish",
      "status": "passing|failing|unknown",
      "latest_run": "2026-05-11T10:00:00Z"
    },
    {
      "name": "docs",
      "status": "passing|failing|unknown",
      "latest_run": "2026-05-12T08:00:00Z"
    },
    {
      "name": "ci",
      "status": "passing|failing|unknown",
      "latest_run": "2026-05-12T09:00:00Z"
    },
    {
      "name": "conda_recipe",
      "status": "future-only|passing|unknown",
      "latest_run": null
    }
  ],
  "consistency_checks": {
    "version_tag_match": true,
    "readme_badges_current": true,
    "homepage_links_valid": true,
    "warnings": []
  }
}
```

### Markdown Report Schema

The Markdown report should render the JSON report as:

```
# Release Evidence Report

Generated: 2026-05-12T12:00:00Z

## Source
- Version: 0.5.0
- Tag: v0.5.0
- Commit: abc1234

## Registry Status
| Registry | Status | Version | URL |
|----------|--------|---------|-----|
| PyPI | published | 0.5.0 | https://... |
| conda-forge | future-only | — | — |
| GitHub Release | published | 0.5.0 | https://... |
| GitHub Pages | published | — | https://... |
| crates.io | future-only | — | — |

## Workflow Status
| Workflow | Status | Latest Run |
|----------|--------|------------|
| release | passing | 2026-05-11 |
| publish | passing | 2026-05-11 |
| docs | passing | 2026-05-12 |
| ci | passing | 2026-05-12 |
| conda recipe | future-only | — |

## Consistency Checks
- ✅ Version/tag match
- ✅ README badges current
- ✅ Homepage links valid

## Warnings
(none)
```

## Evidence States

| State | Meaning |
|---|---|
| `published` | Registry has the claimed version, and it matches source |
| `unpublished` | Registry exists but no matching version is published |
| `recipe-only` | Registry source recipe exists, but a released package/version is not yet published |
| `future-only` | Registry is planned but not yet targeted |
| `private` | Registry publishes through a private channel that is not public evidence |
| `published-with-gaps` | Registry has a version but it is stale or mismatched |

## Implementation Notes

- The report can be generated as a standalone Python script or integrated into
  an existing CLI command.
- Registry checks should use public APIs (PyPI JSON API, GitHub Releases API,
  GitHub Pages HTTP status) and fall back to local metadata when offline.
- Consistency checks compare package version, git tag, GitHub Release tag, and
  PyPI version.
- README badge URLs are checked for HTTP 200 status.
- Homepage links in `pyproject.toml`, `Cargo.toml`, `README.md`, and docs
  config are validated.
- Future-only registries are recorded but not checked.

## Evidence Surfaces

- Python module or CLI command that generates JSON and Markdown reports.
- Tests with mocked registry responses.
- Release checklist references the report.
- Publication claims in docs reference the report output.

## References

- `conductor/tracks/release_supply_chain_governance_20260504/`
- `.github/workflows/release.yml`
- `.github/workflows/publish.yml`
- `pyproject.toml`
